import mysql.connector
from configs.config import dbconfig
from datetime import datetime

class login_timing_model():
    def __init__(self):

        try:

            self.conn = mysql.connector.connect(host=dbconfig['host'], port = dbconfig["port"], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE if not exists login_timing(
                session_id int not null,
                entry_no varchar(40) NOT null,
                course_id varchar(40),
                assignment_id CHAR(100),
                start_time datetime,
                end_time datetime,
                primary key(session_id))
                '''

            self.cursor.execute(sql)
            print("Connection Established ")

        except:
            print("Connection Error")
        
        self.id = 0

    def start_vm(self, entry_no, course_id, assignment_id):
        try:
            start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            query = f"insert into login_timing(session_id, entry_no, course_id, assignment_id, start_time) values({self.id}, '{entry_no}', '{course_id}', '{assignment_id}' ,'{start_time}')"
            self.cursor.execute(query)
            self.id+=1

            return self.id-1 
        
        except:
            print("Error!")

    def stop_vm(self, session_id, entry_no, course_id, assignment_id):
        try:
            end_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            query = f'''update login_timing set end_time = '{end_time}'
            where session_id = {session_id} and entry_no = '{entry_no}' and course_id = '{course_id}' and assignment_id = '{assignment_id}' '''
            self.cursor.execute(query)

        except:
            print("Error!")


