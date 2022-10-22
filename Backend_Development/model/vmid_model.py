from doctest import REPORT_CDIFF
import mysql.connector
import json
from flask import make_response
from configs.config import dbconfig


class VmidModel:
    def __init__(self):

        try:

            self.conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE IF NOT EXISTS vmid(
                entry_no CHAR(40),
                course_id INT,
                assignment_id INT,
                vmid INT NOT NULL,
                plag_report MEDIUMBLOB,
                primary key (entry_no,course_id,assignment_id)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")

        except Exception as e:
            print(e)
            print("Some Connection Error")

    def vm_get(self,data,entry_no,course_id,assignment_id):
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, assignment_id,entry_no))
        vm=self.cursor.fetchone()
        # return everything in assignment if it exists
        if vm:
            # returing error as VM already assigned
            return make_response({"message":"VM Already Assigned"},404)
        else:
            new_vmid=2
            ## TODO funtion call to create new VM and update new_vmid
            self.cursor.execute(f"INSERT INTO vmid(entry_no,course_id, assignment_id,vmid) VALUES('{entry_no}','{course_id}', '{assignment_id}', '{new_vmid}')")
            return make_response({"message":"New VM assigend "},201) 
   
    def resume_vm(self,data,entry_no,course_id,assignment_id):
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, assignment_id,entry_no))
        vm=self.cursor.fetchone()
        # return everything in assignment if it exists
        if vm:
            temp_vmid=vm['vmid']
            # TODO Add function call to backend to resume vm with temp_vmid
            # TODO SENDING ACKNOWLEDGEMENT (is make_response sufficient)
            return make_response({"message":"VM Resumed"},201)
        else:
            # VM record NOT FOUND
            return make_response({"message":"No Record Found "},404) 
                    
    def pause_vm(self,data,entry_no,course_id,assignment_id):
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, assignment_id,entry_no))
        vm=self.cursor.fetchone()
        # return everything in assignment if it exists
        if vm:
            temp_vmid=vm['vmid']
            # TODO Add function call to backend to pause vm with temp_vmid
            # TODO SENDING ACKNOWLEDGEMENT (is make_response sufficient)
            return make_response({"message":"VM Paused"},201)
        else:
            # VM record NOT FOUND
            return make_response({"message":"No Record Found "},404) 
    
    
    def get_plag_report(self,data,entry_no,course_id,assignment_id):
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, assignment_id,entry_no))
        vm=self.cursor.fetchone()
        # return everything in assignment if it exists
        if vm:
            if vm['plag_report'] is None:
                return make_response({"message":"No plag report found"},404)
            else:
                report=vm['plag_report']
                # TODO Currently just dumping the report 
                return make_response({"message":"Plag report","json":json.dumps(report,default=str)},201)
        else:
            # VM record NOT FOUND
            return make_response({"message":"No Record Found "},404) 
                    
                    
                    