import requests
import json
from app import login
from flask_login import UserMixin
from flask import session
from app import config as cfg

class Customer():
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    user_id = ''
    first_name = ''

    def auth(self, access_code):
        """
        Authenticates a user against an AWS Lambda function
        """
        payload = '{"access_code": "%s"}' % (access_code)
        # payload = json.dumps(payload)
        url = "%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['auth'])
        # print(url)
        r = requests.post(url, headers=self.headers, data=payload)
        req = r.json()
        if req['message'] == 'Success':
            self.id = req['id']
            return True
        else:
            return False

    def load(self, id):
        url = "https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/%s" % id
        r = requests.get(url).json()
        self.user_id = r['id']
        self.first_name = r['name']['first']
        return self

    def set_password(self, password):
        pass

    def check_password(self, password):
        pass

@login.user_loader
def load_user(id):
    #user = User()
    #u = user.load(id)
    #session['user_first_name'] = u.first_name
    #session['user_id'] = u.user_id
    #return u
    pass
