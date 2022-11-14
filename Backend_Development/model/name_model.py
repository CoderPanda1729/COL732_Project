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
        print(entry_no)
        sql_query = f"select name from Name where entry_no='{entry_no}';"
        self.cursor.execute(sql_query)
        name = self.cursor.fetchone()
        if(name):
            return name['name']
        else:
            return 'not signed'
    
    def add_name(self, entry_no, name):
        try:
            sql_query = f"insert into Name(entry_no, name) values('{entry_no}','{name}');"
            self.cursor.execute(sql_query)
            return make_response({'message':'Name add'},201)
        except:
            return make_response({'message':'Entry number not found'}, 404)

    def delete_name(self, entry_no):
        try:
            sql_query = f'delete from Name where entry_no={entry_no}'
            self.cursor.execute(sql_query)
            return make_response({'message':'Name deleted'},201)
        except:
            return make_response({'message':'Entry number not found'}, 404)