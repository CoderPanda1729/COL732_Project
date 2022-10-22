import mysql.connector
import json
from flask import make_response
from configs.config import dbconfig

class NameModel:
    def __init__(self):
        try:

            self.conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE IF NOT EXISTS Name(
                entry_no CHAR(40) NOT NULL,
                name CHAR(255) NOT NULL,
                primary key (entry_no)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")

        except Exception as e:
            print(e)
            print("Some Connection Error")

    def name_get(self, entry_no):
        self.cursor.execute('SELECT name FROM Name WHERE entry_no = %s', entry_no)
        name = self.cursor.fetchone()
        if name:
            return make_response({"message":"Entry Number found","json":json.dumps(name,default=str)},201)
        else:
            return make_response({"message":"Entry Number not found"},404)