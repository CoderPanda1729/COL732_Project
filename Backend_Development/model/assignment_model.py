import mysql.connector
import json
from flask import make_response
from configs.config import dbconfig


class AssignmentModel:
    def __init__(self):

        try:

            self.conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE IF NOT EXISTS assignment(
                course_id varchar(80),
                asmt_id varchar(80),
                start_time INT NOT NULL,
                end_time INT NOT NULL,
                template_vmid INT,
                pdf_link varchar(200),
                primary key (course_id,asmt_id)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")

        except Exception as e:
            print(e)
            print("Some Connection Error")

    def assignment_get(self,data,course_id,asmt_id):
        self.cursor.execute('SELECT * FROM assignment WHERE course_id = %s AND asmt_id = %s', (course_id, asmt_id))
        assignment=self.cursor.fetchone()
        # return everything in assignment if it exists
        if assignment:
            return make_response({"message":"Assignment found","json":json.dumps(assignment,default=str)},201)
        else:
            return make_response({"message":"Assignment not found"},404)

    def assignment_update(self, data, course_id, asmt_id):
        # update all columns
        course_id = data['course_id']
        asmt_id = data['asmt_id']
        for column in ['start_time','end_time','pdf_link']:
            if column in data:
                self.cursor.execute(f"UPDATE assignment SET {column}=%s WHERE course_id=%s AND asmt_id=%s", (data[column], course_id, asmt_id))
        return make_response({"message":"Assignment updated"},201)
    
    def assignment_create(self, data):
        course_id = data['course_id']
        pdf_link = data['pdf_link']
        asmt_id = data['asmt_id']
        start_time = int(data['start_time'])
        end_time = int(data['end_time'])
        self.cursor.execute(f"INSERT INTO assignment(course_id, asmt_id, start_time, end_time, pdf_link) VALUES('{course_id}', '{asmt_id}', '{start_time}', '{end_time}','{pdf_link}')")
        return make_response({"message":"Assignment created"},201)
    
    def getAllAss(self,course_id):
        self.cursor.execute(f"select asmt_id,start_time,end_time,template_vmid,pdf_link from assignment where course_id='{course_id}';")
        asmts = self.cursor.fetchall()
        return asmts