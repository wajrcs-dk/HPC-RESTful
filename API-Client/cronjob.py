import time
import json
from swagger_client import job
from swagger_client import logger

runner = True
time_to_sleep = 5
access_token = 'N9TT-9G0A-B7FQ-RANC'
URL = 'http://restapi:8080/Master-Thesis/HPC-RESTful/1.0.0/';
pageLength = 1
totalPages = 1

while runner:
    pageNumber = 1
    jobObj = job.Job(URL)
    f = logger.log_open()

    while pageNumber <= totalPages:
        logger.log(f, 'Getting jobs for page '+str(pageNumber))
        params = {
            'accessToken': access_token,
            'pageLength': pageLength,
            'pageNumber': pageNumber,
            'status': 'new,hpc_queued,hpc_in_progress'
        }
        jobs = jobObj.find_jobs_by_status(params)

        if not('status' in jobs):
            logger.log(f, 'Found jobs with page ' + str(pageNumber))
            for job_db in jobs['jobs']:
                logger.log(f, 'Processing job with id ' + str(job_db['jobId']))
                jobObj.execute_job(job_db, access_token, logger, f)
        else:
            logger.log(f, 'Failed getting jobs with page ' + str(pageNumber) + ', error: '+json.dumps(jobs))
        
        pageNumber = pageNumber + 1
        totalPages = jobs['totalPages']
    
    f.close()
    
    time.sleep(time_to_sleep)