import requests
import json
import os
import subprocess
import sys
import time
from swagger_client.api import Api

class Job:

    # Constructor method with instance variables name and age
    def __init__(self, URL, access_token):
        self.URL = URL
        self.access_token = access_token

    def getFile(self, job_id, file, file_type):
        return Api.getFile(self.URL + 'file/' + str(job_id) + '/getFile?fileType='+file_type+'&accessToken=' + self.access_token, file)

    def uploadFile(self, filename, file):
        return Api.uploadFile(self.URL + 'file/uploadFile?filename='+filename+'&accessToken=' + self.access_token, file)

    # This function fetches incomplete jobs from RESTful API server.
    def find_jobs_by_status(self, params):
        return Api.get(self.URL + 'job/findJobsByStatus', params)

    # This function updates a job via RESTful API server.
    def update_job(self, job_id, data):
        return Api.put(self.URL + 'job/' + str(job_id) + '?accessToken=' + self.access_token, data)

    # This function apply operation on a job via RESTful API server.
    def operation_job(self, job_id, operation):
        return Api.put(self.URL + 'job/updateByOperation/' + str(job_id) + '?operation=' + operation + '&accessToken=' + self.access_token, {})

    # This function changes operation of the job.
    def operation_job_status(self, job, operation, logger):
        logger.log('Updating operation', job)
        r = self.operation_job(job['jobId'], operation)
        logger.log('Updated operation', job)

    # This function updates job log via RESTful API server.
    def update_job_logs(self, job, log):
        job['log'] = job['log'] + log + "\n"
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        job['created'] = job['created'].replace('T', ' ').replace('Z', '')
        job['updated'] = now
        r = self.update_job(job['jobId'], job)

    # This function updates job status via RESTful API server.
    def update_job_status(self, job, logger):
        logger.log('Updating status', job)
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        job['created'] = job['created'].replace('T', ' ').replace('Z', '')
        job['updated'] = now
        r = self.update_job(job['jobId'], job)
        logger.log('Updated status', job)

    # This function marks job status as failed via RESTful API server.
    def mark_job_error(self, job, subJobType, logger):
        if subJobType == 'hpc_status':
            job['status'] = 'hpc_failed'
        elif subJobType == 'hpc_abort':
            job['status'] = 'hpc_failed'
        else:
            job['status'] = 'cronjob_failed'
        self.update_job_status(job, logger)

    # This function runs a bash command and return results.
    def run(self, cmd, print_result):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return [out.decode("utf-8"), err.decode("utf-8"), process.returncode]

    # This function generates and then runs a command from the API data and return results.
    def execute_cmd(self, job, cmd, logger):
        cmd_str = ''
        valid = False
        valid_reason = ''

        # HPC scancel command.
        if cmd['subJobType'] == 'hpc_abort':
            cmd_str = 'scancel ' + cmd['parameters']
            valid = True

        # HPC scontrol command.
        if cmd['subJobType'] == 'hpc_status':
            cmd_str = 'scontrol show jobid ' + cmd['parameters']
            valid = True

        # HPC sbatch command.
        if cmd['subJobType'] == 'hpc':
            valid_reason = 'Hpc job: Invalid script'
            filename, file_extension = os.path.splitext(cmd['parameters'])
            if os.path.isfile(cmd['parameters']) and file_extension == '.sh':
                cmd_str = 'sbatch ' + cmd['parameters']
                valid = True

        # Compile command using sbatch.
        if cmd['subJobType'] == 'compile':
            valid_reason = 'Compile job: Invalid file'
            if os.path.isfile(cmd['parameters']):
                cmd_str = 'sbatch --wrap="make -C ' + os.path.dirname(cmd['parameters']) + '"'
                valid = True

        # Archive command using zip.
        elif cmd['subJobType'] == 'archive':
            valid_reason = 'Archive job: Invalid path'
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isdir(os.path.dirname(parameters[0])) and os.path.isdir(parameters[1]):
                    cmd_str = 'cd ' + parameters[1] + ' && zip -FSr ' + parameters[0] + ' ./'
                    valid = True
                if os.path.isdir(os.path.dirname(parameters[0])) and os.path.isfile(parameters[1]):
                    cmd_str = 'zip -FSr ' + parameters[0] + ' ' + parameters[1]
                    valid = True

        # Unarchive command using unzip.
        elif cmd['subJobType'] == 'unarchive':
            valid_reason = 'Unarchive job: Invalid path'
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isfile(parameters[0]) and os.path.isdir(parameters[1]):
                    cmd_str = 'unzip ' + parameters[0] + ' -d ' + parameters[1]
                    valid = True
        
        # Copy command using cp.
        elif cmd['subJobType'] == 'copy':
            valid_reason = 'Copy job: Invalid path'
            parameters = cmd['parameters'].split('|')
            if len(parameters) == 2:
                if os.path.isfile(parameters[0]) or os.path.isdir(parameters[0]):
                    if os.path.isfile(parameters[1]) or os.path.isdir(parameters[1]):
                        cmd_str = 'cp ' + parameters[0] + ' ' + parameters[1]
                        valid = True

        # If command parameters are valid then run the command.
        if valid == True:
            logger.log('Running cmd "' + cmd_str + '"', job)

            # Run the command and get results.
            result = self.run(cmd_str, False)
            cmd_output = result[0]
            cmd_error = result[1]
            cmd_code = result[2]

            logger.log('Output cmd: "' + cmd_output.replace("\n", "|") + '"', job)

            # If command terminated or completed successfully.
            if cmd_code != 0:
                logger.log('Error in cmd with code: "' + str(cmd_code) + '"', job)
                logger.log('Error in cmd: "' + cmd_error.replace("\n", "|") + '"', job)
                job['jobMetaData']['error'] = "Command: " + cmd_str + " ErrorCode: " + str(cmd_code) + " Output: " + cmd_output.replace("\n", "|") + " Error: " + cmd_error.replace("\n", "|")
                self.mark_job_error(job, cmd['subJobType'], logger)
                return False
            else:
                # If command is to be run on HPC then update hpc job id.
                if cmd['subJobType'] == 'hpc' or cmd['subJobType'] == 'compile':
                    logger.log('Updating hpc jobId', job)
                    job['hpcJobId'] = int(cmd_output.replace("Submitted batch job", "").strip())
                    now = time.strftime('%Y-%m-%d %H:%M:%S')
                    job['created'] = job['created'].replace('T', ' ').replace('Z', '')
                    job['updated'] = now
                    self.update_job(job['jobId'], job)
                    logger.log('Updated hpcJobId to '+str(job['hpcJobId']), job)
                
                cmd_output = cmd_output.replace("\n", '|')
                logger.log('Completed cmd "' + cmd_str + '"', job)

                return cmd_output
        else:
            logger.log('Error in cmd: "' + valid_reason + '"', job)
            job['jobMetaData']['error'] = valid_reason
            self.mark_job_error(job, cmd['subJobType'], logger)
            return False

    def execute_pre_post_jobs(self, job, pre, logger):
        ind = 1
        commands = []
        
        # Run bash commands until we find HPC job.
        if pre == True:
            for cmd in job['commands']:
                if cmd['subJobType'] != 'hpc' and cmd['subJobType'] != 'compile':
                    commands.append(cmd)
                else:
                    break
        else:
            after = False
            for cmd in job['commands']:
                if after == True:
                    commands.append(cmd)
                if cmd['subJobType'] == 'hpc' or cmd['subJobType'] == 'compile':
                    after = True

        for cmd in commands:
            logger.log('Running ' + str(ind) + ' of ' + str(len(commands)), job)
            ind = ind + 1
            if self.execute_cmd(job, cmd, logger) == False:
                return False

    def process_job(self, job, logger):
        cmd_obj = {}

        # Find HPC job.
        for cmd in job['commands']:
            if cmd['subJobType'] == 'hpc' or cmd['subJobType'] == 'compile':
                cmd_obj = cmd
                break

        # Run HPC specfic job
        if 'subJobType' in cmd_obj:
            logger.log('Running hpc command', job)
            cmd_output = self.execute_cmd(job, cmd_obj, logger)
        
            if cmd_output != False:
                logger.log('Completed hpc command', job)

            return cmd_output
        else:
            return True

    # This function is used to generate
    def hpc_abort_job(self, job, logger):
        ret = 0
        cmd_obj = {}
        cmd_obj['subJobType'] = 'hpc_abort'
        cmd_obj['parameters'] = str(job['hpcJobId'])
        result = self.execute_cmd(job, cmd_obj, logger)

        if result != False:
            ret = 1
            logger.log('Returning job cancle: ' + str(result), job)
        return ret

    # This function checks HPC job status using sControl
    def check_hpc_job_status(self, job, logger):
        ret = 0
        
        cmd_obj = {}
        cmd_obj['subJobType'] = 'hpc_status'
        cmd_obj['parameters'] = str(job['hpcJobId'])
        result = self.execute_cmd(job, cmd_obj, logger)

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

    # This function schedule bash or HPC jobs as well as updates status of the job.
    def execute_job(self, job, logger):
        completed = False

        if (job['status'] == 'new'):
            job['status'] = 'cronjob_in_progress'
            self.update_job_status(job, logger)
        
        if (job['status'] == 'cronjob_in_progress'):
            logger.log('Running pre jobs', job)
            ret = self.execute_pre_post_jobs(job, True, logger)
            if ret != False:
                logger.log('Completed pre jobs', job)
                ret = self.process_job(job, logger)
                if ret == True:
                    job['status'] = 'completed'
                    self.update_job_status(job, logger)
                elif ret != False:
                    job['status'] = 'hpc_queued'
                    self.update_job_status(job, logger)
        
        if (job['status'] == 'hpc_queued'):
            ret = self.check_hpc_job_status(job, logger)
            
            if job['operation'] == 'queue':
                if ret == 1:
                    job['status'] = 'hpc_in_progress'
                    self.update_job_status(job, logger)
                if ret == 2:
                    job['status'] = 'hpc_in_progress'
                    self.update_job_status(job, logger)
                if ret == 3:
                    job['status'] = 'hpc_failed'
                    self.update_job_status(job, logger)
                if ret == 4:
                    job['status'] = 'hpc_aborted'
                    self.update_job_status(job, logger)
            
            if job['operation'] == 'abort':
                if ret == 1:
                    if self.hpc_abort_job(job, logger)==1:
                        job['status'] = 'hpc_aborted'
                        self.update_job_status(job, logger)
                    else:
                        job['status'] = 'hpc_failed'
                        self.update_job_status(job, logger)
                else:
                    job['operation'] = 'queue';
                    self.operation_job_status(job, 'queue', logger)


        if (job['status'] == 'hpc_in_progress'):
            ret = self.check_hpc_job_status(job, logger)
            
            if job['operation'] == 'queue':
                if ret == 2:
                    logger.log('Running post jobs', job)
                    ret = self.execute_pre_post_jobs(job, False, logger)
                    
                    if ret != False:
                        logger.log('Completed post jobs', job)

                        # Upload results
                        jobMetaData = job['jobMetaData']
                        if 'output' in jobMetaData and jobMetaData['output'] != '':
                            logger.log('Uploading output file', job)
                            head, tail = os.path.split(jobMetaData['output'])
                            res = self.uploadFile(tail, jobMetaData['output'])
                            if 'uploaded_file' in res:
                                now = time.strftime('%Y-%m-%d %H:%M:%S')
                                job['updated'] = now
                                job['jobMetaData']['output_file'] = res['uploaded_file']
                                self.update_job(job['jobId'], job)
                                logger.log('Uploaded file and updated job', job)
                            else:
                                logger.log('Error in uploading output file', job)
                
                        job['status'] = 'completed'
                        self.update_job_status(job, logger)
                        completed = True
                        logger.log('Completed finally', job)

                if ret == 3:
                    job['status'] = 'hpc_failed'
                    self.update_job_status(job, logger)
                if ret == 4:
                    job['status'] = 'hpc_aborted'
                    self.update_job_status(job, logger)
            
            if job['operation'] == 'abort':
                if ret == 1:
                    if self.hpc_abort_job(job, logger)==1:
                        job['status'] = 'hpc_aborted'
                        self.update_job_status(job, logger)
                    else:
                        job['status'] = 'hpc_failed'
                        self.update_job_status(job, logger)
                else:
                    job['operation'] = 'queue';
                    self.operation_job_status(job, 'queue', logger)

        return completed