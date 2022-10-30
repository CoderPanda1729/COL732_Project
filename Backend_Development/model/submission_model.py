import mysql.connector
import json
from flask import make_response
from configs.config import dbconfig


class SubmissionModel:
    def __init__(self):

        try:

            self.conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE IF NOT EXISTS submission(
                course_id VARCHAR,
                assignment_id VARCHAR,
                entry_no CHAR(40) NOT NULL,
                status VARCHAR NOT NULL,
                submission_time INT NOT NULL,
                marks FLOAT NOT NULL,
                plag_path VARCHAR NOT NULL,
                primary key (course_id, assignment_id, entry_no)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")

        except Exception as e:
            print(e)
            print("Some Connection Error")

    def submission_get(self,data, entry_no, course_id, assignment_id):
        self.cursor.execute('SELECT * FROM submission WHERE entry_no = %s AND course_id = %s AND assignment_id = %s', (entry_no, course_id, assignment_id))
        submission=self.cursor.fetchone()

        if submission:
            return make_response({"message":"Submission found","json":json.dumps(submission,default=str)},201)
        else:
            return make_response({"message":"Submission not found"},404)
    
    def submission_get_all(self, data, course_id, assignment_id):
        self.cursor.execute('SELECT * FROM submission WHERE course_id = %s AND assignment_id = %s', (course_id, assignment_id))
        submissions=self.cursor.fetchall()

        if submissions:
            self.cursor.execute('SELECT entry_no FROM course WHERE course_id = %s AND role = %s', (course_id, 'student'))
            enrolledStudents = self.cursor.fetchall()
            
            studentsInSubmissions = {}
            for s in submissions:
                studentsInSubmissions[s['entry_no']] = 1
            missingEntries = []
            for entry in enrolledStudents:
                if entry not in studentsInSubmissions:
                    missingEntries.append(entry)
            
            sendSubmissions = {}
            sendSubmissions['submissions'] = submissions
            sendSubmissions['missing'] = missingEntries
            return make_response({"message":"Submissions found","json":json.dumps(sendSubmissions,default=str)},201)
        else:
            return make_response({"message":"No submission found"},404)        

    def submission_upload(self, data, entry_no, course_id,assignment_id, status, submission_time, marks, plag_path):
        try:
            self.cursor.execute('INSERT INTO submission VALUES (%s, %s, %s, %s, %s, %s, %s)', (entry_no, course_id,assignment_id, status, submission_time, marks, plag_path))
            return make_response({"message":"Submission uploaded succsessfully"},201)
        except:
            return make_response({"message":"Failed to upload submission"},404)

    def submission_update(self, data, entry_no, course_id, assignment_id):
        self.cursor.execute('SELECT * FROM submission WHERE entry_no = %s AND course_id = %s AND assignment_id = %s', (entry_no, course_id, assignment_id))
        submission=self.cursor.fetchone()
        # check if submission exists
        if submission:
            # update all columns
            for column in ['status','submission_time','marks','plag_path']:
                if column in data:
                    self.cursor.execute("UPDATE submission SET {column}=%s WHERE entry_no=%s AND course_id=%s AND assignment_id=%s", (data[column], entry_no, course_id, assignment_id))
            return make_response({"message":"Submission updated"},201)
        else:
            if 'status' in data and 'submission_time' in data  and 'marks' in data and 'plag_path' in data:
                self.cursor.execute('INSERT INTO submission VALUES (%s, %s, %s, %s, %s, %s, %s)', (entry_no, course_id,assignment_id, data['status'], data['submission_time'], data['marks'], data['plag_path']))
                return make_response({"message":"Submission not found, created new submission"},201)
            else:
                return make_response({"message":"Submission not found"},404)            
    