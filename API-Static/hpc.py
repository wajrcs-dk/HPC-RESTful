import requests
import yaml
import json
import time
import sys

# Checking if script is executed with necessary arguents.
if len(sys.argv) != 2:
    print ('Program requires these cli parameters: <host> <port>')
else:
    HOST = sys.argv[0]
    PORT = sys.argv[1]
    BASE_URL = 'http://'+HOST+':'+PORT+'/Master-Thesis/HPC-RESTful/1.0.0'
    yaml_file = 'hpc.yml'
    attempt = 0
    time_to_sleep = 5

    with open(yaml_file) as file:
        hpc_job = yaml.load(file, Loader=yaml.FullLoader)
        get_url = BASE_URL + '/job/{jobId}?accessToken=' + hpc_job['accessToken']
        post_url = BASE_URL + '/job?accessToken=' + hpc_job['accessToken']
        # Don't need to post accessToken
        del hpc_job['accessToken']

        # Posting request
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(post_url, data=json.dumps(hpc_job), headers=headers)
        result = r.json()
        print(result)

        if 'jobId' in result:
            print ('Job Id '+str(result['jobId']))
            get_url = get_url.replace('{jobId}', str(result['jobId']))
            
            while True:
                attempt = attempt + 1
                time.sleep(time_to_sleep)
                r = requests.get(get_url, headers=headers)
                job_db = r.json()
                if 'jobId' in job_db:
                    print ("Job [" + str(job_db['jobId']) + "][" + job_db['status'] + "] Try " + str(attempt))
                    if job_db['status'] == 'completed':
                        break
                    if job_db['status'] == 'hpc_aborted' or job_db['status'] == 'hpc_failed' or job_db['status'] == 'cronjob_failed':
                        print ('Job log: ' + job_db['log'])
                        raise Exception('Job status: ' + job_db['status'])
                else:
                    raise Exception('GET/ Error from REST API Server: ' + json.dumps(job_db))
        else:
            raise Exception('POST/ Error from REST API Server: ' + json.dumps(result))