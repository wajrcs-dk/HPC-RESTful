import requests

class Api:

    def getFile(url, file):
        try:
            r = requests.get(url, allow_redirects=True)
            open(file, 'wb').write(r.content)
            return True
        except Exception as e: # work on python 3.x
            error_message = {
                "detail": 'HTTP request exception: '+str(e),
                "status": 500,
                "title": "HTTP request exception",
                "type": "about:blank"
            }
            print(error_message['detail'])
            return error_message

    def uploadFile(url, file):
        try:
            files = {'fileName': open(file,'rb')}
            r = requests.post(url, files=files)
            return r.json()
        except Exception as e: # work on python 3.x
            error_message = {
                "detail": 'HTTP request exception: '+str(e),
                "status": 500,
                "title": "HTTP request exception",
                "type": "about:blank"
            }
            print(error_message['detail'])
            return error_message

    def get(url, params):
        try:
            # sending get request and saving the response as response object 
            r = requests.get(url = url, params = params)

            # extracting data in json format 
            return r.json()
        except Exception as e: # work on python 3.x
            error_message = {
                "detail": 'HTTP request exception: '+str(e),
                "status": 500,
                "title": "HTTP request exception",
                "type": "about:blank"
            }
            print(error_message['detail'])
            return error_message

    def post(url, data):
        try:
            # sending get request and saving the response as response object 
            r = requests.post(url = url, data = data)

            # extracting data in json format 
            return r.json()
        except Exception as e: # work on python 3.x
            error_message = {
                "detail": 'HTTP request exception: '+str(e),
                "status": 500,
                "title": "HTTP request exception",
                "type": "about:blank"
            }
            print(error_message['detail'])
            return error_message

    def put(url, data):
        try:
            # sending get request and saving the response as response object
            r = requests.put(url = url, json = data)
            # extracting data in json format 
            return r.json()
        except Exception as e: # work on python 3.x
            error_message = {
                "detail": 'HTTP request exception: '+str(e),
                "status": 500,
                "title": "HTTP request exception",
                "type": "about:blank"
            }
            print(error_message['detail'])
            return error_message

    def delete(url):
        try:
            # sending get request and saving the response as response object 
            r = requests.delete(url = url)

            # extracting data in json format 
            return r.json()
        except Exception as e: # work on python 3.x
            error_message = {
                "detail": 'HTTP request exception: '+str(e),
                "status": 500,
                "title": "HTTP request exception",
                "type": "about:blank"
            }
            print(error_message['detail'])
            return error_message