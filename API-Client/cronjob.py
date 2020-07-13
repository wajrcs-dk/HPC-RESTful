import time
import json
import os
import shutil
from swagger_client import job
from swagger_client import logger

runner = True
time_to_sleep = 5
access_token = 'N9TT-9G0A-B7FQ-RANC'
URL = 'http://restapi:8080/Master-Thesis/HPC-RESTful/1.0.0/';
BASE_PATH = '/data/jobs/'
pageLength = 1
logger = logger.Logger()

while runner:
    pageNumber = 1
    totalPages = 1
    jobObj = job.Job(URL)
    logger.log_open()

    while pageNumber <= totalPages:
        logger.log('Getting jobs for page: "'+str(pageNumber) + '" Total pages: "' + str(totalPages) + '"')
        params = {
            'accessToken': access_token,
            'pageLength': pageLength,
            'pageNumber': pageNumber,
            'status': 'new,hpc_queued,hpc_in_progress'
        }
        jobs = jobObj.find_jobs_by_status(params)

        if not('status' in jobs):
            logger.log('Processing jobs with page ' + str(pageNumber))
            if len(jobs['jobs']) > 0:
                for job_db in jobs['jobs']:
                    print(job_db)
                    logger.log('Processing job', job_db)
                    
                    if not os.path.exists(BASE_PATH + str(job_db['jobId']) + '/'):
                        os.makedirs(BASE_PATH + str(job_db['jobId']) + '/')

                    completed = jobObj.execute_job(job_db, access_token, logger)

                    if os.path.exists(BASE_PATH + str(job['jobId']) + '/'):
                        shutil.rmtree(BASE_PATH + str(job['jobId']) + '/')
            else:
                logger.log('No job found')
            logger.log('Processed jobs with page ' + str(pageNumber))
            totalPages = jobs['totalPages']
        else:
            logger.log('Failed getting jobs with page ' + str(pageNumber) + ', error: '+json.dumps(jobs))
        
        pageNumber = pageNumber + 1
    
    logger.log_close()
    time.sleep(time_to_sleep)