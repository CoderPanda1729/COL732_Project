import mysql.connector
import json
from flask import make_response
from configs.config import dbconfig,server_config
import jwt
import datetime
import app


class user_model():
    def __init__(self):

        try:

            self.conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE user_login(
                entry_no CHAR(40) NOT NULL,
                role CHAR(40),
                password CHAR(100)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")

        except:
            print("Some Connection Error")

    def user_signup_model(self,data):

        if 'entry_no' in data and 'password' in data and 'role' in data and 'name' in data:

            self.cursor.execute('SELECT * FROM user_login WHERE entry_no = %s  AND role=%s ', (data['entry_no'],data['role'],))
            account=self.cursor.fetchone()
            if not account:
                self.cursor.execute(f"INSERT INTO user_login(entry_no, role, password) VALUES('{data['entry_no']}', '{data['role']}', '{data['password']}')")
                return make_response({"message":"SignUp_SUCCESSFULLY"},201)
            else:
                return make_response({"message":"ACCOUNT_ALREADY_EXIT"},404)

        else:
            return make_response({"message":"WRONG_INPUT_FORMAT"},404)

    def encode_auth_token(self, s):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': s
            }
            return jwt.encode(
                payload,
                server_config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def user_login_model(self,data):
        print(data)
        if 'entry_no' in data and 'password' in data and 'role' in data:
            print(data)
            entry_num=data['entry_no']
            password=data['password']
            role=data['role']
            self.cursor.execute('SELECT * FROM user_login WHERE entry_no = %s AND password = %s AND role=%s ', (entry_num, password,role,))
            account=self.cursor.fetchone()
            print(account)
            print(self.encode_auth_token(entry_num+"#"+role).decode())
            if account:
                return make_response({"message":"LOGIN_SUCCESSFULLY","token":self.encode_auth_token(entry_num+"#"+role).decode()},201)

            else:
                return make_response({"message":"NO_SUCH_ACCOUNT_EXIT"},404)
        else:
            return make_response({"message":"WRONG_INPUT_FORMAT"},404)
    
    def user_forgot_password_model(self , data):

        if 'entry_no' in data and 'role' in data and 'password' in data:

            self.cursor.execute(f"UPDATE user_login SET password = '{data['password']}'  WHERE entry_no = %s AND role=%s ", (data['entry_no'], data['role'],))

            if self.cursor.rowcount>0:
                return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
            else:
                return make_response({"message":"WRONG_INFO"},400) 
        else:
            return make_response({"message":"WRONG_INPUT_FORMAT"},404)
    
    def user_change_password(self, data):
        if ('entry_no' in data and 'role' in data and 'prev_password' in data and 'new_password' in data):
            self.cursor.execute('SELECT * FROM user_login WHERE entry_no = %s AND password = %s AND role=%s ', (data['entry_no'], data['prev_password'],data['role']))
            account = self.cursor.fetchone()
            if(not account):
                return make_response({'message:Password incorrect'},401)
            self.cursor.execute(f'')
            self.cursor.execute(f"UPDATE user_login SET password='{data['new_password']}' WHERE entry_no=%s AND role=%s", (data['entry_no'], data['role']))
            return make_response({'message':'Change password successful'},201)
        else:
            return make_response({"message":"WRONG_INPUT_FORMAT"},400)