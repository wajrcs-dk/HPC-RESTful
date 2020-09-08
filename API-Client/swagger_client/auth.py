import os

class Auth:

    def get(self):
        access_token = ''
        filepath = os.getcwd()+'/auth.data'
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                access_token = line.strip()
                break
        return access_token