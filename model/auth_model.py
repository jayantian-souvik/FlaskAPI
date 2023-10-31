import json
import re
import jwt
from functools import wraps

import mysql.connector
from flask import make_response, request
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig

class auth_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['hostname'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit=True
            self.cur = self.con.cursor(dictionary=True)
            print("Conection Successfully")
        except:
            print("Something Went Wrong.")


    def token_auth(self, endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                print(endpoint)
                authorization = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwtdecoded = jwt.decode(token, "souvik", algorithms=["HS256"])
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR": "TOKEN_EXPIRED"}, 401)

                    jwtdecoded = jwt.decode(token, "souvik", algorithms=["HS256"])

                    role_id = jwtdecoded['payload']['roleID']
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint = '{endpoint}' ")
                    result = self.cur.fetchall()
                    if(len(result)) > 0:
                        # print(json.loads(result[0]['roles']))
                        # print(type(json.loads(result[0]['roles'])))
                        allowed_roles = json.loads(result[0]['roles'])
                        if role_id in allowed_roles:
                            return func(*args)
                        else:
                            return make_response({"ERROR": "INVALID_ROLE"}, 404)
                    else:
                        return make_response({"ERROR": "UNKNOW_ENDPOINT"}, 404)

                else:
                    return make_response({"ERROR": "INVALID_TOKEN"}, 401)

            return inner2
        return inner1