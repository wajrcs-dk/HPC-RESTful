import requests
from swagger_client.api import Api

class Job:

	# Constructor method with instance variables name and age
    def __init__(self, URL):
        self.URL = URL

    def find_jobs_by_status(self, params):
        return Api.get(self.URL + 'job/findJobsByStatus', params)

    def update_job(self, job_id, access_token, data):
        return Api.put(self.URL + 'job/' + str(job_id) + '?accessToken='+ access_token, data)

    