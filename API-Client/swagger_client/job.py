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

    def update_job_status(self, job, access_token, logger, f):
        logger.log(f, 'Job ' + str(job['jobId']) + ' updating status to ' + job['status'])
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        job['created'] = now
        job['updated'] = now
        self.update_job(job['jobId'], access_token, job)
        logger.log(f, 'Job ' + str(job['jobId']) + ' updated status to ' + job['status'])

    def mark_job_error(self, job, access_token, logger, f):
        job['status'] = 'cronjob_failed'
        self.update_job_status(job, access_token, logger, f)

    def execute_cmd(self, job, cmd, access_token, logger, f):
        cmd_str = ''
        valid = False

        if cmd['subJobType'] == 'hpc_status':
            cmd_str = 'scontrol show jobid ' + cmd['parameters']
            valid = True

        if cmd['subJobType'] == 'hpc':
            filename, file_extension = os.path.splitext(cmd['parameters'])
            if os.path.isfile(cmd['parameters']) and file_extension == '.sh':
                cmd_str = 'sbatch ' + cmd['parameters']
                valid = True
            else:
                cmd_str = 'sbatch --wrap="' + cmd['parameters'] + '"'
                valid = True

        elif cmd['subJobType'] == 'archive':
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isdir(os.path.dirname(parameters[0])) and os.path.isdir(parameters[1]):
                    cmd_str = 'zip -r ' + parameters[0] + ' ' + parameters[1]
                    valid = True

        elif cmd['subJobType'] == 'unarchive':
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isfile(parameters[0]) and os.path.isdir(parameters[1]):
                    cmd_str = 'unzip ' + parameters[0] + ' -d ' + parameters[1]
                    valid = True
        
        elif cmd['subJobType'] == 'copy':
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isfile(parameters[0]) or os.path.isdir(parameters[0]):
                    if os.path.isfile(parameters[1]) or os.path.isdir(parameters[1]):
                        cmd_str = 'cp ' + parameters[0] + ' ' + parameters[1]
                        valid = True

        if valid == True:
            logger.log(f, 'Job ' + str(job['jobId']) + ' running cmd "' + cmd_str + '"')
            stream = os.popen(cmd_str)

            if cmd['subJobType'] == 'hpc':
                logger.log(f, 'Job ' + str(job['jobId']) + ' updating hpc jobId')
                job['hpcJobId'] = int(cmd_output.replace("Submitted batch job", "").strip())
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                job['created'] = now
                job['updated'] = now
                self.update_job(job['jobId'], access_token, job)
                logger.log(f, 'Job ' + str(job['jobId']) + ' updated hpcJobId to '+str(job['hpcJobId']))

            cmd_output = stream.read()
            cmd_output = cmd_output.replace("\n", '|')
            logger.log(f, 'Job ' + str(job['jobId']) + ' output cmd "' + cmd_output + '"')
            logger.log(f, 'Job ' + str(job['jobId']) + ' completed cmd "' + cmd_str + '"')

            return cmd_output
        else:
            self.mark_job_error(job, access_token, logger, f)
            return False

    def execute_pre_post_requisites(self, job, pre_post_requisites, access_token, logger, f):
        ind = 1
        for cmd in pre_post_requisites:
            logger.log(f, 'Job ' + str(job['jobId']) + ' running ' + str(ind) + ' of ' + str(len(pre_post_requisites)))
            ind = ind + 1
            if self.execute_cmd(job, cmd, access_token, logger, f) == False:
                return False

    def process_job(self, job, access_token, logger, f):
        cmd_obj = {}
        cmd_obj['subJobType'] = job['jobType']
        cmd_obj['parameters'] = job['command']
        logger.log(f, 'Job ' + str(job['jobId']) + ' running command')
        cmd_output = self.execute_cmd(job, cmd_obj, access_token, logger, f)
        
        if cmd_output != False:
            logger.log(f, 'Job ' + str(job['jobId']) + ' completed command')

        return cmd_output

    def check_hpc_job_status(self, job, logger, f):
        ret = 0
        
        cmd_obj = {}
        cmd_obj['subJobType'] = 'hpc_status'
        cmd_obj['parameters'] = str(job['hpcJobId'])
        result = self.execute_cmd(job, cmd_obj, '', logger, f)

        result = result.split("\n")
        for line in result:
            line = line.strip().split(" ")
            for attr in line:
                '''
                PENDING,RUNNING,SUSPENDED,COMPLETED,CANCELLED,FAILED,
                TIMEOUT,NODE_FAIL,PREEMPTED,BOOT_FAIL,DEADLINE,OUT_OF_MEMORY,
                COMPLETING,CONFIGURING,RESIZING,REVOKED,SPECIAL_EXIT
                '''
                if attr.find('JobState=') != -1:
                    logger.log(f, 'Job ' + str(job['jobId']) + ' found job state via HPC: ' + str(attr))
                    attr = attr.split("=")

                    if len(attr)==2:
                        if attr[1] == 'COMPLETED':
                            ret = 2
                        elif attr[1] == 'PENDING':
                            ret = 1
                        elif attr[1] == 'RUNNING':
                            ret = 1
                        else:
                            ret = 3
                        break
        logger.log(f, 'Job ' + str(job['jobId']) + ' returning job state: ' + str(ret))
        return ret

    def execute_job(self, job, access_token, logger, f):
        if (job['status'] == 'new'):
            job['status'] = 'cronjob_in_progress'
            self.update_job_status(job, access_token, logger, f)
        
        if (job['status'] == 'cronjob_in_progress'):
            logger.log(f, 'Job ' + str(job['jobId']) + ' running prerequisites')
            ret = self.execute_pre_post_requisites(job, job['jobMetaData']['prerequisites'], access_token, logger, f)
            if ret != False:
                logger.log(f, 'Job ' + str(job['jobId']) + ' completed prerequisites')
                
                ret = self.process_job(job, access_token, logger, f)
                if ret != False:
                    job['status'] = 'hpc_queued'
                    self.update_job_status(job, access_token, logger, f)
        
        if (job['status'] == 'hpc_queued'):
            ret = self.check_hpc_job_status(job, logger, f)
            if ret == 1:
                job['status'] = 'hpc_in_progress'
                self.update_job_status(job, access_token, logger, f)
            if ret == 2:
                job['status'] = 'hpc_in_progress'
                self.update_job_status(job, access_token, logger, f)
        
        if (job['status'] == 'hpc_in_progress'):
            if self.check_hpc_job_status(job, logger, f) == 2:
                job['status'] = 'completed'
                self.update_job_status(job, access_token, logger, f)

                logger.log(f, 'Job ' + str(job['jobId']) + ' running postrequisites')
                ret = self.execute_pre_post_requisites(job, job['jobMetaData']['postrequisites'], access_token, logger, f)
                
                if ret != False:
                    logger.log(f, 'Job ' + str(job['jobId']) + ' completed postrequisites')

                    logger.log(f, 'Job ' + str(job['jobId']) + ' completed finally')