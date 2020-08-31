import time
import json
import os
import shutil
import sys
from swagger_client import job
from swagger_client import logger


# Usage:
#
# python3 cronjob.py <host> <port> <API> <Temp Location> <Time to recheck>

# Local Docker Cluster:
# python3 cronjob.py 172.17.0.1 8081 Master-Thesis/HPC-RESTful/1.0.0/ /data/jobs/ 5

# Localhost:
# python3 cronjob.py localhost 8081 Master-Thesis/HPC-RESTful/1.0.0/ /data/jobs/ 5

# GWDG Virtualhost:
# python3 cronjob.py 141.5.101.84 8081 Master-Thesis/HPC-RESTful/1.0.0/ /usr/users/walamgi/data/jobs/ 5

# Checking if script is executed with necessary arguents.
if len(sys.argv) != 6:
    print ('Program requires these cli parameters: <progran> <host> <port> <endpoint> <temp_path> <time_to_sleep>')
else:
    runner = True
    time_to_sleep = int(sys.argv[5])
    access_token = 'N9TT-9G0A-B7FQ-RANC'
    
    # In case of docker host use 172.17.0.1
    URL = 'http://' + sys.argv[1] + ':' + sys.argv[2] + '/' + sys.argv[3];
    BASE_PATH = sys.argv[4]
    pageLength = 1
    logger = logger.Logger(URL, access_token)

    # While this script is running.
    while runner:
        pageNumber = 1
        totalPages = 1
        # Creating job object.
        jobObj = job.Job(URL, access_token)
        logger.log_open()

        # While there are new pages than process them.
        while pageNumber <= totalPages:
            logger.log('Getting jobs for page: "'+str(pageNumber) + '" Total pages: "' + str(totalPages) + '"')
            
            # Finding new jobs.
            params = {
                'accessToken': access_token,
                'pageLength': pageLength,
                'pageNumber': pageNumber,
                'status': 'new,hpc_queued,hpc_in_progress'
            }
            jobs = jobObj.find_jobs_by_status(params)

            # If response from RESTful server is valid.
            if not('status' in jobs):
                logger.log('Processing jobs with page ' + str(pageNumber))
                
                # If there are incomplete jobs.
                if len(jobs['jobs']) > 0:
                    
                    # Processing each job.
                    for job_db in jobs['jobs']:
                        print(job_db)
                        logger.log('Processing job', job_db)
                        
                        # If the temporary location is not created than try to create it.
                        if not os.path.exists(BASE_PATH + str(job_db['jobId']) + '/'):
                            os.makedirs(BASE_PATH + str(job_db['jobId']) + '/')

                        # Process job here.
                        completed = jobObj.execute_job(job_db, logger)

                        # If job is completed or failed than remove temporary location. 
                        if job_db['status'] == 'hpc_aborted' or job_db['status'] == 'cronjob_failed' or job_db['status'] == 'hpc_failed' or job_db['status'] == 'completed':
                            if os.path.exists(BASE_PATH + str(job_db['jobId']) + '/'):
                                shutil.rmtree(BASE_PATH + str(job_db['jobId']) + '/')
                else:
                    logger.log('No job found')
                logger.log('Processed jobs with page ' + str(pageNumber))
                totalPages = jobs['totalPages']
            else:
                logger.log('Failed getting jobs with page ' + str(pageNumber) + ', error: '+json.dumps(jobs))
            
            pageNumber = pageNumber + 1
        
        logger.log_close()
        
        # Wait (in secs) to fetch again incompelete jobs.
        time.sleep(time_to_sleep)