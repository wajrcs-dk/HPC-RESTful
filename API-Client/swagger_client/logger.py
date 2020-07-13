import time

class Logger:

    f = None

    def log_open(self):
        self.f = open("swagger_logs/cronjob.log","a+")

    def log(self, str_msg, job=''):
        if job == '':
            msg = time.strftime('%Y-%m-%d %H:%M:%S') + ": "+ str_msg
        else:
            msg = time.strftime('%Y-%m-%d %H:%M:%S') + ": Job [" + str(job['jobId']) + "]["+ job['status'] +"] "+ str_msg
        
        print (msg)
        self.f.write(msg+"\n")

    def log_close(self):
        self.f.close()