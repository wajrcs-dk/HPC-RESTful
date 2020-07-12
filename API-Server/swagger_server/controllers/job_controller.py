import connexion
import six
import json
import time

from swagger_server.models.job import Job  # noqa: E501
from swagger_server.models.job_metadata import JobMetadata  # noqa: E501
from swagger_server.models.pagination_response import PaginationResponse  # noqa: E501
from swagger_server import util

'''
a. Job successfully completed: new > cronjob_in_progress > hpc_queued > hpc_in_progress > completed.
b. Job failed at HPC: new > cronjob_in_progress > hpc_queued > hpc_in_progress > hpc_failed.
c. Job aborted by user before its execution: new > cronjob_in_progress > hpc_queued > hpc_aborted.
d. Job failed to queue in HPC: new > cronjob_in_progress > cronjob_failed.
'''


def add_job(body, access_token):  # noqa: E501
    """Schedules a new job to the HPC system

     # noqa: E501

    :param name: Name of the job
    :type name: str
    :param commands: commands of the job
    :type commands: str
    :param job_meta_data: Metadata of the job
    :type job_meta_data: dict | bytes
    :param job_type: Type of the job
    :type job_type: str
    :param access_token: Access token
    :type access_token: str

    :rtype: Job
    """

    if access_token != 'N9TT-9G0A-B7FQ-RANC':
        error_code = 401
        error_message = {
            "detail": "You are not authorized to use this API.",
            "status": error_code,
            "title": "Unauthorized",
            "type": "about:blank"
        }
        return error_message, error_code
    
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    jobMetaData = []
    commands = []
    userId = 1

    if not('jobMetaData' in body and 'name' in body and 'commands' in body):
        error_code = 405
        error_message = {
            "detail": 'Invalid input, please provide jobMetaData, name and commands',
            "status": error_code,
            "title": "Invalid input",
            "type": "about:blank"
        }
        return error_message, error_code

    if not('error' in body['jobMetaData'] and 'output' in body['jobMetaData']):
        error_code = 405
        error_message = {
            "detail": 'Invalid input, please provide error and output in jobMetaData',
            "status": error_code,
            "title": "Invalid input",
            "type": "about:blank"
        }
        return error_message, error_code

    if not(isinstance(body['commands'], list)):
        error_code = 405
        error_message = {
            "detail": 'Invalid input, please provide commands as list',
            "status": error_code,
            "title": "Invalid input",
            "type": "about:blank"
        }
        return error_message, error_code

    hpc_cout = 0
    for cmd in body['commands']:
        if not('subJobType' in cmd and 'parameters' in cmd):
            error_code = 405
            error_message = {
                "detail": 'Invalid input, please provide subJobType and parameters in commands',
                "status": error_code,
                "title": "Invalid input",
                "type": "about:blank"
            }
            return error_message, error_code
        if cmd['subJobType'] == 'hpc':
                hpc_cout = hpc_cout + 1
        if hpc_cout > 1:
            error_code = 405
            error_message = {
                "detail": 'Invalid input, please provide only one subJobType=hpc in commands',
                "status": error_code,
                "title": "Invalid input",
                "type": "about:blank"
            }
            return error_message, error_code

    try:
        jobMetaData = json.dumps(body['jobMetaData'])
        commands = json.dumps(body['commands'])
    except Exception as e: # work on python 3.x
        error_code = 405
        error_message = {
            "detail": 'Invalid JSON: '+str(e),
            "status": error_code,
            "title": "Invalid input",
            "type": "about:blank"
        }
        return error_message, error_code

    bodyPost = {
        "hpcJobId": 0,
        "operation": 'queue',
        "userId": userId,
        "name": body['name'],
        "commands": commands,
        "jobMetaData": jobMetaData,
        "created": now,
        "updated": now,
        "result": '',
        "log": '',
        "status": 'new'
    }

    job_id = 0
    row = []

    try:
        job_id = Job.insert_job(bodyPost)
    except Exception as e: # work on python 3.x
        error_code = 500
        error_message = {
            "detail": 'Error in inserting job into database: '+str(e),
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code

    try:
        row = Job.get_job(job_id)
    except Exception as e: # work on python 3.x
        error_code = 500
        error_message = {
            "detail": 'Error in getting job from database: '+str(e),
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code

    row = row[0]
    jobMetaData = json.loads(row[6])
    commands = json.loads(row[5])
    
    ind = 0
    for cmd in commands:
        commands[ind]['parameters'] = cmd['parameters'].replace('{jobId}', str(job_id))
        ind = ind + 1

    jobMetaData['output'] = jobMetaData['output'].replace('{jobId}', str(job_id))
    
    # commands
    my_result = {
        "jobId": row[0],
        "hpcJobId": row[1],
        "operation": row[2],
        "userId": row[3],
        "name": row[4],
        "commands": json.dumps(commands),
        "jobMetaData": json.dumps(jobMetaData),
        "created": row[7],
        "updated": row[8],
        "result": row[9],
        "log": row[10],
        "status": row[11]
    }
    Job.update_job(job_id, my_result)
    
    my_result['jobMetaData'] = jobMetaData
    my_result['commands'] = commands

    if connexion.request.is_json:
        return my_result
    else:
        return my_result


def delete_job(job_id, access_token):  # noqa: E501
    """Deletes an existing job

     # noqa: E501

    :param job_id: Job id to delete
    :type job_id: int
    :param access_token: Access token
    :type access_token: str

    :rtype: None
    """

    if access_token != 'N9TT-9G0A-B7FQ-RANC':
        error_code = 401
        error_message = {
          "detail": "You are not authorized to use this API.",
          "status": error_code,
          "title": "Unauthorized",
          "type": "about:blank"
        }
        return error_message, error_code

    row = []

    try:
        row = Job.get_job(job_id)
    except Exception as e: # work on python 3.x
        error_code = 500
        error_message = {
            "detail": 'Error in getting job from database: '+str(e),
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code

    if len(row) == 1:
        status = row[0][12]
        if Job.delete_job_status(status):
            try:
                Job.delete_job(job_id)
            except Exception as e: # work on python 3.x
                error_code = 500
                error_message = {
                    "detail": 'Error in deleting job into database: '+str(e),
                    "status": error_code,
                    "title": "Internal Server Error",
                    "type": "about:blank"
                }
                return error_message, error_code
        else:
            error_code = 409
            error_message = {
              "detail": "Job with jobId " + str(job_id) + " cannot be deleted with this status.",
              "status": error_code,
              "title": "Job cannot deleted",
              "type": "about:blank"
            }
            return error_message, error_code
    else:
        error_code = 404
        error_message = {
          "detail": "Job with jobId " + str(job_id) + " not found.",
          "status": error_code,
          "title": "Not found",
          "type": "about:blank"
        }
        return error_message, error_code
    
    return {'sucess':True}


def find_jobs_by_status(page_length, page_number, access_token, status=None):  # noqa: E501
    """Finds jobs, optionally by status

    Multiple status values can be provided with comma separated strings # noqa: E501

    :param page_length: Number of records to return
    :type page_length: int
    :param page_number: Start index for paging
    :type page_number: int
    :param access_token: Access token
    :type access_token: str
    :param status: Status values that need to be considered for filter
    :type status: List[str]

    :rtype: object
    """

    if access_token != 'N9TT-9G0A-B7FQ-RANC':
        error_code = 401
        error_message = {
          "detail": "You are not authorized to use this API.",
          "status": error_code,
          "title": "Unauthorized",
          "type": "about:blank"
        }
        return error_message, error_code

    my_result_total = []
    my_result = []
    try:
        my_result_total = Job.get_jobs_cout(status)
        my_result = Job.get_jobs(status, page_number, page_length)
    except Exception as e: # work on python 3.x
        error_code = 500
        error_message = {
            "detail": 'Error in getting jobs from database: '+str(e),
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code

    index = 0
    for row in my_result:
        row = {
            "jobId": row[0],
            "hpcJobId": row[1],
            "operation": row[2],
            "userId": row[3],
            "name": row[4],
            "commands": json.loads(row[5]),
            "jobMetaData": json.loads(row[6]),
            "created": row[7],
            "updated": row[8],
            "result": row[9],
            "log": row[10],
            "status": row[11]
        }
        my_result[index] = row
        index = index + 1

    pagination = PaginationResponse(my_result_total[0][0], page_number, page_length, my_result)

    if connexion.request.is_json:
        return pagination
    else:
        return pagination


def get_job_by_id(job_id, access_token):  # noqa: E501
    """Finds job by ID

    Returns a single job # noqa: E501

    :param job_id: ID of job to return
    :type job_id: int
    :param access_token: Access token
    :type access_token: str

    :rtype: Job
    """

    if access_token != 'N9TT-9G0A-B7FQ-RANC':
        error_code = 401
        error_message = {
          "detail": "You are not authorized to use this API.",
          "status": error_code,
          "title": "Unauthorized",
          "type": "about:blank"
        }
        return error_message, error_code

    row = []
    try:
        row = Job.get_job(job_id)
    except Exception as e: # work on python 3.x
        error_code = 500
        error_message = {
            "detail": 'Error in getting job from database: '+str(e),
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code

    if len(row) == 1:
        row = row[0]
        my_result = {
            "jobId": row[0],
            "hpcJobId": row[1],
            "operation": row[2],
            "userId": row[3],
            "name": row[4],
            "commands": json.loads(row[5]),
            "jobMetaData": json.loads(row[6]),
            "created": row[7],
            "updated": row[8],
            "result": row[9],
            "log": row[10],
            "status": row[11]
        }

        if connexion.request.is_json:
            return my_result
        else:
            return my_result
    else:
        error_code = 404
        error_message = {
          "detail": "Job with jobId " + str(job_id) + " not found.",
          "status": error_code,
          "title": "Not found",
          "type": "about:blank"
        }
        return error_message, error_code


def update_job(body, job_id, access_token):  # noqa: E501
    """Updates an existing job

     # noqa: E501

    :param body: Job object that needs to be added
    :type body: dict | bytes
    :param job_id: ID of job to return
    :type job_id: int
    :param access_token: Access token
    :type access_token: str

    :rtype: Job
    """
    
    if access_token != 'N9TT-9G0A-B7FQ-RANC':
        error_code = 401
        error_message = {
          "detail": "You are not authorized to use this API.",
          "status": error_code,
          "title": "Unauthorized",
          "type": "about:blank"
        }
        return error_message, error_code

    '''
    if connexion.request.is_json:
        body = Job.from_dict(connexion.request.get_json())  # noqa: E501
    '''

    try:
        row = Job.get_job(job_id)
    except Exception as e: # work on python 3.x
        error_code = 500
        error_message = {
            "detail": 'Error in getting job from database: '+str(e),
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code

    if len(row) == 1:

        if not('error' in body['jobMetaData'] and 'output' in body['jobMetaData']):
            error_code = 405
            error_message = {
                "detail": 'Invalid input',
                "status": error_code,
                "title": "Invalid input",
                "type": "about:blank"
            }
            return error_message, error_code

        if not(isinstance(body['commands'], list)):
            error_code = 405
            error_message = {
                "detail": 'Invalid input, please provide commands as list',
                "status": error_code,
                "title": "Invalid input",
                "type": "about:blank"
            }
            return error_message, error_code

        hpc_cout = 0
        for cmd in body['commands']:
            if not('subJobType' in cmd and 'parameters' in cmd):
                error_code = 405
                error_message = {
                    "detail": 'Invalid input, please provide subJobType and parameters in commands',
                    "status": error_code,
                    "title": "Invalid input",
                    "type": "about:blank"
                }
                return error_message, error_code
            if cmd['subJobType'] == 'hpc':
                    hpc_cout = hpc_cout + 1
            if hpc_cout > 1:
                error_code = 405
                error_message = {
                    "detail": 'Invalid input, please provide only one subJobType=hpc in commands',
                    "status": error_code,
                    "title": "Invalid input",
                    "type": "about:blank"
                }
                return error_message, error_code


        body['jobMetaData'] = json.dumps(body['jobMetaData'])
        body['commands'] = json.dumps(body['commands'])

        if Job.update_job_status(row[0][12], body['status']):
            try:
                Job.update_job(job_id, body)
            except Exception as e: # work on python 3.x
                error_code = 500
                error_message = {
                    "detail": 'Error in updating job into database: '+str(e),
                    "status": error_code,
                    "title": "Internal Server Error",
                    "type": "about:blank"
                }
                return error_message, error_code
            
            body['jobId'] = job_id
            body['jobMetaData'] = json.loads(body['jobMetaData'])
            body['commands'] = json.loads(body['commands'])
            return body
        else:
            error_code = 409
            error_message = {
              "detail": "Job with jobId " + str(job_id) + " cannot be updated with this status.",
              "status": error_code,
              "title": "Job cannot updated",
              "type": "about:blank"
            }
            return error_message, error_code
    else:
        error_code = 404
        error_message = {
          "detail": "Job with jobId " + str(job_id) + " not found.",
          "status": error_code,
          "title": "Not found",
          "type": "about:blank"
        }
        return error_message, error_code


def update_job_by_operation(job_id, operation, access_token):  # noqa: E501
    """Updates operation of an existing job

     # noqa: E501

    :param job_id: name that need to be updated
    :type job_id: int
    :param operation: Job Operation
    :type operation: str
    :param access_token: Access token
    :type access_token: str

    :rtype: Job
    """

    if access_token != 'N9TT-9G0A-B7FQ-RANC':
        error_code = 401
        error_message = {
          "detail": "You are not authorized to use this API.",
          "status": error_code,
          "title": "Unauthorized",
          "type": "about:blank"
        }
        return error_message, error_code

    try:
        row = Job.get_job(job_id)
    except Exception as e: # work on python 3.x
        error_code = 500
        error_message = {
            "detail": 'Error in getting job from database: '+str(e),
            "status": error_code,
            "title": "Internal Server Error",
            "type": "about:blank"
        }
        return error_message, error_code

    if len(row) == 1:

        try:
            Job.update_job_operation(job_id, operation)
        except Exception as e: # work on python 3.x
            error_code = 500
            error_message = {
                "detail": 'Error in updating job into database: '+str(e),
                "status": error_code,
                "title": "Internal Server Error",
                "type": "about:blank"
            }
            return error_message, error_code

        row = row[0]
        my_result = {
            "jobId": row[0],
            "hpcJobId": row[1],
            "operation": operation,
            "userId": row[3],
            "name": row[4],
            "commands": json.loads(row[5]),
            "jobMetaData": json.loads(row[6]),
            "created": row[7],
            "updated": row[8],
            "result": row[9],
            "log": row[10],
            "status": row[11]
        }

        if connexion.request.is_json:
            return my_result
        else:
            return my_result
    else:
        error_code = 404
        error_message = {
          "detail": "Job with jobId " + str(job_id) + " not found.",
          "status": error_code,
          "title": "Not found",
          "type": "about:blank"
        }
        return error_message, error_code
