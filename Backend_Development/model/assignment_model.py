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
                asmt_name varchar(200),
                start_time INT NOT NULL,
                end_time INT NOT NULL,
                iso varchar(200),
                pdf_link varchar(200),
                primary key (course_id,asmt_id)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")

        except Exception as e:
            print(e)
            print("Some Connection Error")

    def assignment_get(self,course_id,asmt_id):
        self.cursor.execute('SELECT * FROM assignment WHERE course_id = %s AND asmt_id = %s', (course_id, asmt_id))
        assignment=self.cursor.fetchone()
        # return everything in assignment if it exists
        if assignment:
            return make_response(assignment,201)
        else:
            return make_response({"message":"Assignment not found"},404)

    def assignment_update(self, data):
        # update all columns
        course_id = data['course_id']
        pdf_link = data['pdf_link']
        asmt_name = data['asmt_name']
        asmt_id = data['asmt_id']
        iso = data['iso']
        start_time = int(data['start_time'])
        end_time = int(data['end_time'])
        self.cursor.execute(f"UPDATE assignment SET asmt_name='{asmt_name}',start_time={start_time}, end_time={end_time},iso='{iso}', pdf_link='{pdf_link}' WHERE course_id=%s AND asmt_id=%s", (course_id, asmt_id))
        return make_response({"message":"Assignment updated"},201)
    
    def assignment_create(self, data):
        course_id = data['course_id']
        pdf_link = data['pdf_link']
        asmt_id = data['asmt_id']
        asmt_name = data['asmt_name']
        iso = data['iso']
        start_time = int(data['start_time'])
        end_time = int(data['end_time'])
        self.cursor.execute(f"INSERT INTO assignment(course_id, asmt_id,asmt_name, start_time, end_time,iso, pdf_link) VALUES('{course_id}', '{asmt_id}', '{asmt_name}','{start_time}', '{end_time}','{iso}','{pdf_link}')")
        return make_response({"message":"Assignment created"},201)
    
    def getAllAss(self,course_id):
        self.cursor.execute(f"select asmt_id,asmt_name,start_time,end_time,iso,pdf_link from assignment where course_id='{course_id}';")
        asmts = self.cursor.fetchall()
        return asmts