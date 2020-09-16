import connexion
import flask
import six
import os
import time
import json

from swagger_server.models.job import Job  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def get_file(job_id, file_type, access_token):  # noqa: E501
    """downloads a file

     # noqa: E501

    :param job_id: name that need to be updated
    :type job_id: int
    :param file_type: Input or output file
    :type file_type: str
    :param access_token: Access token
    :type access_token: str

    :rtype: str
    """
    
    user = User()
    user_info = user.validate_user(access_token)
    userId = user_info[1]
    
    if not(userId.isdigit()):
        error_code = 405
        error_message = {
            "detail": 'Invalid input, please provide valid userId.',
            "status": error_code,
            "title": "Invalid input",
            "type": "about:blank"
        }
        return error_message, error_code

    if not(str(job_id).isdigit()):
        error_code = 405
        error_message = {
            "detail": 'Invalid input, please provide valid job_id.',
            "status": error_code,
            "title": "Invalid input",
            "type": "about:blank"
        }
        return error_message, error_code
    """
    row = [[0,1,2,3,4,5,{'filename':'s.md'}]]
    """
    row = []
    job = Job()
    cox = job.connect()
    if cox != '':
        error_code = 500
        error_message = {
            "detail": cox,
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code

    try:
        row = job.get_job(job_id, userId)
    except Exception as e: # work on python 3.x
        error_code = 500
        error_message = {
            "detail": 'Error in getting job from database: '+str(e),
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code
    
    job.close()

    if len(row) == 1:
        row = row[0]
        jobMetaData = json.loads(row[6])
        filename = jobMetaData[file_type]

        filepath = os.getcwd()+'/swagger_server/uploads/'

        resp = flask.send_from_directory(filepath, filename,
            as_attachment=True, 
            mimetype='application/octet-stream',
            attachment_filename=filename
        )
        return resp
    else:
        error_code = 404
        error_message = {
          "detail": "job with jobId " + str(job_id) + " not found.",
          "status": error_code,
          "title": "Not found",
          "type": "about:blank"
        }
        return error_message, error_code


def upload_file(filename, access_token, file_name=None):  # noqa: E501
    """uploads a file

     # noqa: E501

    :param filename: Name of the file
    :type filename: str
    :param access_token: Access token
    :type access_token: str
    :param file_name: 
    :type file_name: strstr

    :rtype: None
    """
    
    filename = str(time.time()) + '-' + filename
    filepath = os.getcwd()+'/swagger_server/uploads/'
    uploaded_file = connexion.request.files['fileName']
    uploaded_file.save(filepath+filename)

    return {'sucess':True, 'uploaded_file':filename}
