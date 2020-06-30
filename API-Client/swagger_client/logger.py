
def log_open():
	return open("swagger_logs/cronjob.log","w+")

def log(f, str):
	print (str)
	f.write(str+"\n")

def log_close(f):
	f.close()