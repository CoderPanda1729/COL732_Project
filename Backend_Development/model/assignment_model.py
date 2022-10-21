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
                course_id INT,
                assignment_id INT,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                template_vmid INT NOT NULL,
                pdf MEDIUMBLOB,
                primary key (course_id,assignment_id)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")

        except Exception as e:
            print(e)
            print("Some Connection Error")

    def assignment_get(self,data,course_id,assignment_id):
        self.cursor.execute('SELECT * FROM assignment WHERE course_id = %s AND assignment_id = %s', (course_id, assignment_id))
        assignment=self.cursor.fetchone()
        # return everything in assignment if it exists
        if assignment:
            return make_response({"message":"Assignment found","json":json.dumps(assignment,default=str)},201)
        else:
            return make_response({"message":"Assignment not found"},404)

    def assignment_upload_pdf(self, data, course_id, assignment_id):
        self.cursor.execute('SELECT * FROM assignment WHERE course_id = %s AND assignment_id = %s', (course_id, assignment_id))
        assignment=self.cursor.fetchone()
        # check if assignment exists
        if assignment:
            self.cursor.execute('UPDATE assignment SET pdf = %s WHERE course_id = %s AND assignment_id = %s', (data,course_id,assignment_id))
            return make_response({"message":"PDF updated succsessfully"},201)
        else:
            return make_response({"message":"Assignment not found"},404)

    def assignment_update(self, data, course_id, assignment_id):
        self.cursor.execute('SELECT * FROM assignment WHERE course_id = %s AND assignment_id = %s', (course_id, assignment_id))
        assignment=self.cursor.fetchone()
        # check if assignment exists
        if assignment:
            # update all columns
            for column in ['start_time','end_time','template_vmid','pdf']:
                if column in data:
                    self.cursor.execute(f"UPDATE assignment SET {column}=%s WHERE course_id=%s AND assignment_id=%s", (data[column], course_id, assignment_id))
            return make_response({"message":"Assignment update"},201)
        else:
            # if the json has complete data, create a new assignment
            # TODO: handle pdf
            if 'start_time' in data and 'end_time' in data  and 'template_vmid' in data:
                self.cursor.execute(f"INSERT INTO assignment(course_id, assignment_id, start_time, end_time, template_vmid) VALUES('{course_id}', '{assignment_id}', '{data['start_time']}', '{data['end_time']}', '{data['template_vmid']}')")
                return make_response({"message":"Assignment created"},201)
            else:
                return make_response({"message":"Assignment not found"},404)
    