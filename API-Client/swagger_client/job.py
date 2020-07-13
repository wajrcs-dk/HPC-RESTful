import requests
import json
import os
import subprocess
import sys
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

    def update_job_status(self, job, access_token, logger):
        logger.log('Updating status', job)
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        job['created'] = now
        job['updated'] = now
        r = self.update_job(job['jobId'], access_token, job)
        print (r)
        logger.log('Updated status', job)

    def mark_job_error(self, job, access_token, logger):
        job['status'] = 'cronjob_failed'
        print (job)
        print (access_token)
        self.update_job_status(job, access_token, logger)

    def run(self, cmd, print_result):
        '''stream = os.popen(cmd)
        cmd_output = stream.read()
        exit_code = 0
        '''
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return [out.decode("utf-8"), err.decode("utf-8"), process.returncode]

    def execute_cmd(self, job, cmd, access_token, logger):
        cmd_str = ''
        valid = False
        valid_reason = ''

        if cmd['subJobType'] == 'hpc_status':
            cmd_str = 'scontrol show jobid ' + cmd['parameters']
            valid = True

        if cmd['subJobType'] == 'hpc':
            valid_reason = 'Hpc job: Invalid script'
            filename, file_extension = os.path.splitext(cmd['parameters'])
            if os.path.isfile(cmd['parameters']) and file_extension == '.sh':
                cmd_str = 'sbatch ' + cmd['parameters']
                valid = True

        if cmd['subJobType'] == 'compile':
            valid_reason = 'Compile job: Invalid file'
            if os.path.isfile(cmd['parameters']):
                cmd_str = 'sbatch --wrap="make -f ' + cmd['parameters'] + '"'
                valid = True

        elif cmd['subJobType'] == 'archive':
            valid_reason = 'Archive job: Invalid path'
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isdir(os.path.dirname(parameters[0])) and os.path.isdir(parameters[1]):
                    cmd_str = 'zip -r ' + parameters[0] + ' ' + parameters[1]
                    valid = True
                if os.path.isdir(os.path.dirname(parameters[0])) and os.path.isfile(parameters[1]):
                    cmd_str = 'zip -r ' + parameters[0] + ' ' + parameters[1]
                    valid = True

        elif cmd['subJobType'] == 'unarchive':
            valid_reason = 'Unarchive job: Invalid path'
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isfile(parameters[0]) and os.path.isdir(parameters[1]):
                    cmd_str = 'unzip ' + parameters[0] + ' -d ' + parameters[1]
                    valid = True
        
        elif cmd['subJobType'] == 'copy':
            valid_reason = 'Copy job: Invalid path'
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isfile(parameters[0]) or os.path.isdir(parameters[0]):
                    if os.path.isfile(parameters[1]) or os.path.isdir(parameters[1]):
                        cmd_str = 'cp ' + parameters[0] + ' ' + parameters[1]
                        valid = True

        if valid == True:
            logger.log('Running cmd "' + cmd_str + '"', job)
            result = self.run(cmd_str, False)
            cmd_output = result[0]
            cmd_error = result[1]
            cmd_code = result[2]

            logger.log('Output cmd: "' + cmd_output.replace("\n", "|") + '"', job)

            if cmd_code != 0:
                logger.log('Error in cmd with code: "' + str(cmd_code) + '"', job)
                logger.log('Error in cmd: "' + cmd_error.replace("\n", "|") + '"', job)
                job['jobMetaData']['error'] = "Command: " + cmd_str + " ErrorCode: " + str(cmd_code) + " Output: " + cmd_output.replace("\n", "|") + " Error: " + cmd_error.replace("\n", "|")
                print (access_token)
                self.mark_job_error(job, access_token, logger)
                return False
            else:
                if cmd['subJobType'] == 'hpc':
                    logger.log('Updating hpc jobId', job)
                    job['hpcJobId'] = int(cmd_output.replace("Submitted batch job", "").strip())
                    now = time.strftime('%Y-%m-%d %H:%M:%S')
                    job['created'] = now
                    job['updated'] = now
                    self.update_job(job['jobId'], access_token, job)
                    logger.log('Updated hpcJobId to '+str(job['hpcJobId']), job)
                
                cmd_output = cmd_output.replace("\n", '|')
                logger.log('Output cmd "' + cmd_output + '"', job)
                logger.log('Completed cmd "' + cmd_str + '"', job)

                return cmd_output
        else:
            logger.log('Error in cmd: "' + valid_reason + '"', job)
            job['jobMetaData']['error'] = valid_reason
            self.mark_job_error(job, access_token, logger)
            return False

    def execute_pre_post_jobs(self, job, pre, access_token, logger):
        ind = 1
        commands = []
        
        if pre == True:
            for cmd in job['commands']:
                if cmd['subJobType'] != 'hpc':
                    commands.append(cmd)
                else:
                    break
        else:
            after = False
            for cmd in job['commands']:
                if after == True:
                    commands.append(cmd)
                if cmd['subJobType'] == 'hpc':
                    after = True

        for cmd in commands:
            logger.log('Running ' + str(ind) + ' of ' + str(len(commands)), job)
            ind = ind + 1
            if self.execute_cmd(job, cmd, access_token, logger) == False:
                return False

    def process_job(self, job, access_token, logger):
        cmd_obj = {}
        
        for cmd in job['commands']:
            if cmd['subJobType'] == 'hpc':
                cmd_obj = cmd
                break

        if 'subJobType' in cmd_obj:
            logger.log('Running hpc command', job)
            cmd_output = self.execute_cmd(job, cmd_obj, access_token, logger)
        
            if cmd_output != False:
                logger.log('Completed hpc command', job)

            return cmd_output
        else:
            return True

    def check_hpc_job_status(self, job, access_token, logger):
        ret = 0
        
        cmd_obj = {}
        cmd_obj['subJobType'] = 'hpc_status'
        cmd_obj['parameters'] = str(job['hpcJobId'])
        result = self.execute_cmd(job, cmd_obj, access_token, logger)

        if result != False:
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
                        logger.log('Found job state via HPC: ' + str(attr), job)
                        attr = attr.split("=")

                        if len(attr)==2:
                            if attr[1] == 'COMPLETED':
                                ret = 2
                            elif attr[1] == 'PENDING':
                                ret = 1
                            elif attr[1] == 'RUNNING':
                                ret = 1
                            elif attr[1] == 'FAILED':
                                ret = 3
                            elif attr[1] == 'CANCELLED':
                                ret = 4
                            else:
                                ret = 5
                            break
            logger.log('Returning job state: ' + str(ret), job)
        return ret

    def execute_job(self, job, access_token, logger):
        completed = False

        if (job['status'] == 'new'):
            job['status'] = 'cronjob_in_progress'
            self.update_job_status(job, access_token, logger)
        
        if (job['status'] == 'cronjob_in_progress'):
            logger.log('Running pre jobs', job)
            ret = self.execute_pre_post_jobs(job, True, access_token, logger)
            if ret != False:
                logger.log('Completed pre jobs', job)
                
                ret = self.process_job(job, access_token, logger)
                
                if ret == True:
                    job['status'] = 'completed'
                    self.update_job_status(job, access_token, logger)
                elif ret != False:
                    job['status'] = 'hpc_queued'
                    self.update_job_status(job, access_token, logger)
        
        if (job['status'] == 'hpc_queued'):
            ret = self.check_hpc_job_status(job, access_token, logger)
            if ret == 1:
                job['status'] = 'hpc_in_progress'
                self.update_job_status(job, access_token, logger)
            if ret == 2:
                job['status'] = 'hpc_in_progress'
                self.update_job_status(job, access_token, logger)
            if ret == 3:
                job['status'] = 'hpc_failed'
                self.update_job_status(job, access_token, logger)
            if ret == 4:
                job['status'] = 'hpc_aborted'
                self.update_job_status(job, access_token, logger)
        
        if (job['status'] == 'hpc_in_progress'):
            ret = self.check_hpc_job_status(job, access_token, logger)
            if ret == 2:
                job['status'] = 'completed'
                self.update_job_status(job, access_token, logger)

                logger.log('Running post jobs', job)
                ret = self.execute_pre_post_jobs(job, False, access_token, logger)
                
                if ret != False:
                    logger.log('Completed post jobs', job)
                    completed = True
                    logger.log('Completed finally', job)
            if ret == 3:
                job['status'] = 'hpc_failed'
                self.update_job_status(job, access_token, logger)
            if ret == 4:
                job['status'] = 'hpc_aborted'
                self.update_job_status(job, access_token, logger)

        return completed