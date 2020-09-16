import requests
import yaml
import json
import time
import sys
import os

# Checking if script is executed with necessary arguents.
if len(sys.argv) < 3:
    print ('Program requires these cli parameters: <host> <port> <filename>')
else:
    HOST = sys.argv[1]
    PORT = sys.argv[2]
    BASE_URL = 'http://'+HOST+':'+PORT+'/Master-Thesis/HPC-RESTful/1.0.0'
    yaml_file = 'hpc.yml'
    attempt = 0
    time_to_sleep = 5

    with open(yaml_file) as file:
        hpc_job = yaml.load(file, Loader=yaml.FullLoader)

        get_url = BASE_URL + '/job/{jobId}?accessToken=' + hpc_job['accessToken']
        post_url = BASE_URL + '/job?accessToken=' + hpc_job['accessToken']
        post_file_url = BASE_URL + '/file/uploadFile?filename='+hpc_job['jobMetaData']['file']+'&accessToken=' + hpc_job['accessToken']
        get_file_url = BASE_URL + '/file/{jobId}/getFile?fileType=output_file&accessToken=' + hpc_job['accessToken']

        # Don't need to post accessToken
        del hpc_job['accessToken']

        if hpc_job['jobMetaData']['hasFile'] == True:
            print ('Uploading file.')
            # Posting request
            files = {'fileName': open(sys.argv[3],'rb')}
            r = requests.post(post_file_url, files=files)
            result = r.json()
            print(result)
            hpc_job['jobMetaData']['input_file'] = result['uploaded_file']
            print ('Uploading file completed.')

        # Posting request
        headers = {'Content-type': 'application/json', 'accept': 'text/plain'}
        r = requests.post(post_url, data=json.dumps(hpc_job), headers=headers)
        result = r.json()
        print(result)

        if 'jobId' in result:
            print ('Job Id '+str(result['jobId']))
            get_url = get_url.replace('{jobId}', str(result['jobId']))
            get_file_url = get_file_url.replace('{jobId}', str(result['jobId']))
            
            while True:
                attempt = attempt + 1
                time.sleep(time_to_sleep)
                r = requests.get(get_url, headers=headers)
                job_db = r.json()
                if 'jobId' in job_db:
                    print ("Job [" + str(job_db['jobId']) + "][" + job_db['status'] + "] Try " + str(attempt))
                    if job_db['status'] == 'completed':
                        if job_db['jobMetaData']['output'] != '':
                            head, tail = os.path.split(job_db['jobMetaData']['output'])
                            r = requests.get(get_file_url, allow_redirects=True)
                            open(tail, 'wb').write(r.content)
                        break
                    if job_db['status'] == 'hpc_aborted' or job_db['status'] == 'hpc_failed' or job_db['status'] == 'cronjob_failed':
                        print ('Job log: ' + job_db['log'])
                        raise Exception('Job status: ' + job_db['status'])
                else:
                    raise Exception('GET/ Error from REST API Server: ' + json.dumps(job_db))
        else:
            raise Exception('POST/ Error from REST API Server: ' + json.dumps(result))