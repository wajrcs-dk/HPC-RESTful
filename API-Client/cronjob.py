import time
import json
from swagger_client import job
from swagger_client import logger

runner = True
time_to_sleep = 5
access_token = ''
URL = 'http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/';
pageLength = 1
totalPages = 1

while runner:
	pageNumber = 1
	jobObj = job.Job(URL)
	f = logger.log_open()

	while pageNumber <= totalPages:
		logger.log(f, 'Getting jobs for page '+str(pageNumber))
		params = {
			'accessToken': 'N9TT-9G0A-B7FQ-RANC',
			'pageLength': pageLength,
			'pageNumber': pageNumber,
			'status': 'new,cronjob_in_progress,hpc_queued,hpc_in_progress'
		}
		jobs = jobObj.find_jobs_by_status(params)

		if not('status' in jobs):
			logger.log(f, 'Found jobs with page ' + str(pageNumber))
		else:
			logger.log(f, 'Failed getting jobs with page ' + str(pageNumber) + ', error: '+json.dumps(jobs))
		
		pageNumber = pageNumber + 1
		totalPages = jobs['totalPages']
	
	f.close()
	
	time.sleep(time_to_sleep)