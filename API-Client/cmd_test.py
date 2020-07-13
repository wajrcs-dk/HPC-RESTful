import os
import subprocess

cmd = 'zip -r /data/zip.zip /data/test/'

process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()

print (str(out.decode("utf-8")))

print ("Err Code")

print (process.returncode)

print ("Err Msg")

print (err.decode("utf-8"))