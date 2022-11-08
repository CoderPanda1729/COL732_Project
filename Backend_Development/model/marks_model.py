import mysql.connector
import json
from flask import make_response
from configs.config import dbconfig


class marksModel:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE IF NOT EXISTS grades(
                course_id VARCHAR(40),
                assignment_id VARCHAR(40),
                entry_no CHAR(40) NOT NULL,
                submission_time INT NOT NULL,
                auto_marks float,
                plag_points int,
                marks FLOAT,
                remarks LONGTEXT,
                primary key (course_id, assignment_id, entry_no)
            )'''
            self.cursor.execute(sql)
            print("Connection Established ")

        except Exception as e:
            print(e)
            print("Some Connection Error")

    def submit(self, course_id, assign_id, entry_no, submission_time):
        query = f'''INSERT into grades(course_id, assignment_id, entry_no, submission_time) 
                     values('{course_id}', '{assign_id}', '{entry_no}', {submission_time}) '''
        self.cursor.execute(query)
        return make_response({"message": "Data added succesfully."}, 201)

    def setMarks(self, course_id, assign_id, entry_no, marks, remarks):
        query = f'''select * form grades where entry_no = '{entry_no}' and
                course_id = '{course_id}' and assignment_id = '{assign_id}' '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            query = f'''Update grades set marks = {marks}, remarks = {remarks} where entry_no = '{entry_no}' 
                    and course_id = '{course_id}' and assignment_id = '{assign_id}' '''
            self.cursor.execute(query)
            return make_response({"message": "Marks added"}, 201)
        else:
            return make_response({"message": "No entry found!"}, 404)

    def getMarks(self, course_id, assign_id, entry_no):
        query = f'''select * form grades where entry_no = '{entry_no}' and
                course_id = '{course_id}' and assignment_id = '{assign_id}' '''
        self.cursor.execute(query)
        marks = self.cursor.fetchone()
        if marks:
            return make_response({"message" : "success", "data": marks}, 201)
        else:
            return make_response({"message":"Submission not found"},404)

    def getAllMarks(self, course_id, assign_id):
        query = f'''select * form grades where course_id = '{course_id}' and assignment_id = '{assign_id}' '''
        self.cursor.execute(query)
        marks = self.cursor.fetchall
        if marks:
            return make_response({"message" : "success", "data": marks}, 201)
        else:
            return make_response({"message":"No Submission found"},404)

    def runAutoGrader(self, course_id, assign_id, entry_no, auto_marks, plag_pts):
        query = f'''select * form grades where entry_no = '{entry_no}' and
                course_id = '{course_id}' and assignment_id = '{assign_id}' '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            query = f'''Update grades set auto_marks = {marks}, plag_points = {plag_pts} where entry_no = '{entry_no}' 
                    and course_id = '{course_id}' and assignment_id = '{assign_id}' '''
            self.cursor.execute(query)
            return make_response({"message": "Marks added"}, 201)
        else:
            return make_response({"message": "No entry found!"}, 404)

