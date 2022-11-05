import mysql.connector
from configs.config import dbconfig
from datetime import datetime
import time
from flask import make_response

class activities_model():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=dbconfig['host'], port = dbconfig["port"], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)
            sql='''CREATE TABLE if not exists student_activity(
                entry_no varchar(40) NOT null,
                assignment_id CHAR(100),
                operation varchar(40),
                time int,
                primary key (entry_no,assignment_id)
                '''

            self.cursor.execute(sql)
            print("Connection Established ")
        except:
            print("Connection Error")
        
    def record_activity(self, entry_no, assign_id, operation):
        try:
            t = round(time.time(),0) 
            query = f"insert into student_activity(entry_no, assignment_id, operation, time) values('{entry_no}', '{assign_id}', '{operation}', {t})"
            self.cursor.execute(query)
            return make_response({"message":"Succesfully updated"},201)
        except:
            return make_response({"message":"Error"},404)

    def get_records(self, entry_no, assign_id):
        try:
            query = f'''select operation, time from student_activity 
            where entry_no = '{entry_no}' and assignment_id = '{assign_id}'; '''
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            l = []
            for x in results:
                l.append((x[0], x[1]))
            # return l
            return make_response({"message":"Succesfully updated","record":l},201)
        except:
            return make_response({"message":"Error"},404)
            






    

