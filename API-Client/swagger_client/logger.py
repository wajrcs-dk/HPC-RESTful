import time

def log_open():
	return open("swagger_logs/cronjob.log","a+")

def log(f, str):
	msg = time.strftime('%Y-%m-%d %H:%M:%S') + ": "+ str
	print (msg)
	f.write(msg+"\n")

def log_close(f):
	f.close()