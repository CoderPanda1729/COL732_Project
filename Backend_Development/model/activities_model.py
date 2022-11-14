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
                static_dist int,
                grading_time int,
                cheat_label int,
                marks int,
                time int,
                primary key (entry_no,assignment_id)
                '''

            self.cursor.execute(sql)
            print("Connection Established ")
        except:
            print("Connection Error")
        
    def record_activity(self, entry_no, assign_id,course_id, operation):
        try:
            t = round(time.time(),0) 
            query = f"insert into student_activity(entry_no, assignment_id, operation, time) values('{entry_no}', '{course_id+'_'+assign_id}', '{operation}', {t})"
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
    
    def getAllMarks(self, course_id, asmt_id):
        query = f'''
            select entry_no, max(marks), cheat_label
            from student_activity
            where assignment_id = {course_id+'_'+asmt_id}
            group by entry_no;
        '''
        res = self.cursor.fetchall()
        return make_response(res)






    

