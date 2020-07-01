import requests
import json
import os
import time
from swagger_client.api import Api

class Job:

    # Constructor method with instance variables name and age
    def __init__(self, URL):
        self.URL = URL

    def find_jobs_by_status(self, params):
        return Api.get(self.URL + 'job/findJobsByStatus', params)

    def update_job(self, job_id, access_token, data):
        return Api.put(self.URL + 'job/' + str(job_id) + '?accessToken='+ access_token, data)

    def execute_cmd(self, job, cmd, logger, f):
        logger.log(f, 'Job ' + str(job['jobId']) + ' running cmd "' + cmd + '"')
        stream = os.popen(cmd)
        output = stream.read()
        logger.log(f, 'Job ' + str(job['jobId']) + ' output cmd "' + output + '"')
        logger.log(f, 'Job ' + str(job['jobId']) + ' completed cmd "' + cmd + '"')
        return output

    def execute_pre_post_requisites(self, job, pre_post_requisites, logger, f):
        for cmd in pre_post_requisites:
            self.execute_cmd(job, cmd, logger, f)

    def execute_job(self, job, access_token, logger, f):
        if (job['status'] == 'new'):
            logger.log(f, 'Job ' + str(job['jobId']) + ' updating status to cronjob_in_progress')
            job['status'] = 'cronjob_in_progress'
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            job['created'] = now
            job['updated'] = now
            self.update_job(job['jobId'], access_token, job)
            logger.log(f, 'Job ' + str(job['jobId']) + ' updated status to cronjob_in_progress')
        
        if (job['status'] == 'cronjob_in_progress'):
            logger.log(f, 'Job ' + str(job['jobId']) + ' running prerequisites')
            prerequisites = job['jobMetaData']['prerequisites']
            self.execute_pre_post_requisites(job, prerequisites, logger, f)
            logger.log(f, 'Job ' + str(job['jobId']) + ' completed prerequisites')
            
            logger.log(f, 'Job ' + str(job['jobId']) + ' running command')
            self.execute_cmd(job, job['command'], logger, f)
            logger.log(f, 'Job ' + str(job['jobId']) + ' completed command')

            logger.log(f, 'Job ' + str(job['jobId']) + ' updating status to hpc_queued')
            job['status'] = 'hpc_queued'
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            job['created'] = now
            job['updated'] = now
            self.update_job(job['jobId'], access_token, job)
            logger.log(f, 'Job ' + str(job['jobId']) + ' updated status to hpc_queued')
        
        if (job['status'] == 'hpc_queued'):
            logger.log(f, 'Job ' + str(job['jobId']) + ' updating status to hpc_in_progress')
            job['status'] = 'hpc_in_progress'
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            job['created'] = now
            job['updated'] = now
            self.update_job(job['jobId'], access_token, job)
            logger.log(f, 'Job ' + str(job['jobId']) + ' updated status to hpc_in_progress')
        
        if (job['status'] == 'hpc_in_progress'):
            logger.log(f, 'Job ' + str(job['jobId']) + ' running postrequisites')
            postrequisites = job['jobMetaData']['postrequisites']
            self.execute_pre_post_requisites(job, postrequisites, logger, f)
            logger.log(f, 'Job ' + str(job['jobId']) + ' completed postrequisites')

            logger.log(f, 'Job ' + str(job['jobId']) + ' updating status to completed')
            job['status'] = 'completed'
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            job['created'] = now
            job['updated'] = now
            self.update_job(job['jobId'], access_token, job)
            logger.log(f, 'Job ' + str(job['jobId']) + ' updated status to completed')