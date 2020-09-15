import time
import json
import os
import shutil
import sys
from swagger_client import job
from swagger_client import auth
from swagger_client import logger


# Usage:
#
# python3 cronjob.py <host> <port> <API> <Temp Location> <Time to recheck> <run counter>

# Local Docker Cluster:
# python3 cronjob.py 172.17.0.1 8081 Master-Thesis/HPC-RESTful/1.0.0/ /data/jobs/ 5 10

# Localhost:
# python3 cronjob.py localhost 8081 Master-Thesis/HPC-RESTful/1.0.0/ /data/jobs/ 5 10

# GWDG Virtualhost:
# python3 cronjob.py 141.5.101.84 8081 Master-Thesis/HPC-RESTful/1.0.0/ /usr/users/walamgi/data/jobs/ 5 10

# Checking if script is executed with necessary arguents.
if len(sys.argv) != 7:
    print ('Program requires these cli parameters: <progran> <host> <port> <endpoint> <temp_path> <time_to_sleep> <run counter>')
else:
    runner = True
    time_to_sleep = int(sys.argv[5])
    run_counter = int(sys.argv[6])
    run_index = 0
    
    # In case of docker host use 172.17.0.1
    URL = 'http://' + sys.argv[1] + ':' + sys.argv[2] + '/' + sys.argv[3];
    BASE_PATH = sys.argv[4]
    pageLength = 1

    # While this script is running.
    while runner:
        run_index = run_index + 1

        print('Getting token.')
        authObj = auth.Auth()
        access_token = authObj.get()

        loggerObj = logger.Logger(URL, access_token)
        loggerObj.log_open()

        pageNumber = 1
        totalPages = 1
        # Creating job object.
        jobObj = job.Job(URL, access_token)

        # While there are new pages than process them.
        while pageNumber <= totalPages:
            loggerObj.log('Getting jobs for page: "'+str(pageNumber) + '" Total pages: "' + str(totalPages) + '"')
            
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
                loggerObj.log('Processing jobs with page ' + str(pageNumber))
                
                # If there are incomplete jobs.
                if len(jobs['jobs']) > 0:
                    
                    # Processing each job.
                    for job_db in jobs['jobs']:
                        print(job_db)
                        loggerObj.log('Processing job', job_db)
                        download_file = True
                        
                        # If the temporary location is not created than try to create it.
                        if not os.path.exists(BASE_PATH + str(job_db['jobId']) + '/'):
                            os.makedirs(BASE_PATH + str(job_db['jobId']) + '/')
                            jobMetaData = job_db['jobMetaData']
                            # Download
                            if 'hasFile' in jobMetaData and jobMetaData['hasFile']==True:
                                download_file = False
                                if 'file 'in jobMetaData:
                                    loggerObj.log('Downloading job file', job_db)
                                    file = BASE_PATH + str(job_db['jobId']) + '/' + jobMetaData['file']
                                    if jobObj.getFile(job_db['jobId'], file, 'input_file'):
                                        download_file = True
                                        loggerObj.log('Downloaded job file', job_db)
                                    else:
                                        loggerObj.log('Error in downloading job file', job_db)
                                else:
                                    loggerObj.log('No job file', job_db)

                        if download_file == True:
                            # Process job here.
                            completed = jobObj.execute_job(job_db, loggerObj)

                        # If job is completed or failed than remove temporary location. 
                        if job_db['status'] == 'hpc_aborted' or job_db['status'] == 'cronjob_failed' or job_db['status'] == 'hpc_failed' or job_db['status'] == 'completed':
                            if os.path.exists(BASE_PATH + str(job_db['jobId']) + '/'):
                                shutil.rmtree(BASE_PATH + str(job_db['jobId']) + '/')
                else:
                    loggerObj.log('No job found')
                loggerObj.log('Processed jobs with page ' + str(pageNumber))
                totalPages = jobs['totalPages']
            else:
                loggerObj.log('Failed getting jobs with page ' + str(pageNumber) + ', error: '+json.dumps(jobs))
            
            pageNumber = pageNumber + 1
        
        loggerObj.log_close()
        
        # Wait (in secs) to fetch again incompelete jobs.
        time.sleep(time_to_sleep)

        # Stop script
        if run_index==run_counter:
            runner = False