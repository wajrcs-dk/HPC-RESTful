import time
from swagger_client import job

class Logger:

    f = None

    def log_open(self):
        self.f = open("swagger_logs/cronjob.log","a+")

    def log(self, str_msg, job_db=''):

        if job_db == '':
            msg = time.strftime('%Y-%m-%d %H:%M:%S') + ": "+ str_msg
        else:
            msg = time.strftime('%Y-%m-%d %H:%M:%S') + ": Job [" + str(job_db['jobId']) + "]["+ job_db['status'] +"] "+ str_msg

            URL = 'http://restapi:8080/Master-Thesis/HPC-RESTful/1.0.0/';
            access_token = 'N9TT-9G0A-B7FQ-RANC'
            jobObj = job.Job(URL, access_token)
            jobObj.update_job_logs(job_db, msg)
        
        print (msg)

        self.f.write(msg+"\n")

    def log_close(self):
        self.f.close()