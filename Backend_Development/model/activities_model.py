import mysql.connector
from configs.config import dbconfig
from datetime import datetime
import time

class activities_model():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=dbconfig['host'], port = dbconfig["port"], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)
            sql='''CREATE TABLE if not exists student_activity(
                entry_no varchar(40) NOT null,
                course_id varchar(40) not null,
                assignment_id CHAR(100) not null,
                operation varchar(40),
                time int)
                '''

            self.cursor.execute(sql)
            print("Activity: Connection Established ")
        except:
            print("activity model: Connection Error")
        
    def record_activity(self, entry_no,course_id, assign_id, operation):
        try:
            t = round(time.time(),0) 
            query = f"insert into student_activity(entry_no,course_id, assignment_id, operation, time) values('{entry_no}','{course_id}', '{assign_id}', '{operation}', {t})"
            self.cursor.execute(query)
        except:
            print("Error!")

    def get_records(self, entry_no,course_id, assign_id):
        try:
            query = f'''select operation, time from student_activity 
            where entry_no = '{entry_no}' and assignment_id = '{assign_id}'  and course_id = '{course_id}'; '''
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            l = []
            for x in results:
                l.append(x[0], x[1])
            return l

        except:
            print("Error!")






    

