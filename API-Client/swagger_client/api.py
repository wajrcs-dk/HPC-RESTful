import requests

class Api:

    def get(url, params):
        # sending get request and saving the response as response object 
        r = requests.get(url = url, params = params)

        # extracting data in json format 
        return r.json()

    def post(url, data):
        # sending get request and saving the response as response object 
        r = requests.post(url = url, data = data)

        # extracting data in json format 
        return r.json()

    def put(url, data):
        # sending get request and saving the response as response object 
        r = requests.put(url = url, data = data)

        # extracting data in json format 
        return r.json()

    def delete(url):
        # sending get request and saving the response as response object 
        r = requests.delete(url = url)

        # extracting data in json format 
        return r.json()