import mysql.connector
import json
import os
from flask import make_response
from configs.config import dbconfig, vmbconfig
from requests import request as http_request
import shutil
import requests
from .course_model import course_model
class VmidModel:
    def __init__(self):
        # print("hi there")
        try:

            self.conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE IF NOT EXISTS vmid(
                entry_no CHAR(40),
                course_id INT,
                assignment_id INT,
                version INT,
                rpc_port INT DEFAULT 0,
                iso_path TEXT,
                status ENUM('RUNNING', 'STOPPED', 'PAUSED') DEFAULT 'STOPPED',
                plag_report MEDIUMBLOB,
                par_version INT DEFAULT 0,
                version_name varchar(200) DEFAULT 'Root',
                primary key (entry_no,course_id,assignment_id,version)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")

        except Exception as e:
            print(e)
            print("Some Connection Error")

    def get_vm(self, entry_no, course_id, assignment_id,version):
        # get record in table
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s AND verison=%s', (course_id, assignment_id,entry_no,version))
        vm=self.cursor.fetchone()
        if vm:
            return make_response(vm,201)
        else:
            return make_response({"message":"VM does not exist"},404) 


    def create_vm(self, entry_no, course_id, assignment_id,iso_path = ""):
        vm_iso_path = ''
        if course_model().is_ta(course_id, entry_no):
            # For TAs, need to create template ISO
            vm_iso_path = f'./{course_id}_{assignment_id}_template.iso'
            if len(iso_path) > 0:
                # original iso given, copy
                shutil.copy(iso_path, vm_iso_path)
            else:
                # original iso not given, can't create
                if not os.path.isfile(vm_iso_path):
                    return make_response({"message":f"Couldn't start VM, {vm_iso_path} does not exist"},500) 

        else:
            # For students, need to create VM
            vm_iso_path = f'./{course_id}_{assignment_id}_{entry_no}_1_vm.iso'
            template_iso_path = f'./{course_id}_{assignment_id}_template.iso'
            if not os.path.isfile(template_iso_path):
                return make_response({"message":"Couldn't start VM, template does not exist"},500) 
            shutil.copy(template_iso_path, vm_iso_path)
        
        # check if vm exists
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s AND version = 1', (course_id, assignment_id,entry_no))
        vm=self.cursor.fetchone()        
        if vm:
            # update, because entry already exists
            self.cursor.execute(f"UPDATE vmid SET rpc_port=%s, iso_path=%s, status='STOPPED' WHERE course_id=%s AND assignment_id=%s AND entry_no=%s AND version=1", (0, vm_iso_path, course_id, assignment_id, entry_no))
        else:
            # insert, because entry does not exist
            self.cursor.execute(f"INSERT INTO vmid(entry_no,course_id, assignment_id, rpc_port, iso_path, status,version) VALUES('{entry_no}','{course_id}', '{assignment_id}', '{0}', '{vm_iso_path}', 'STOPPED',1)")
        return make_response({"message":"VM created"},201) 

    def start_vm(self, entry_no, course_id, assignment_id,version):
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s AND version=%d', (course_id, assignment_id,entry_no,version))
        vm=self.cursor.fetchone()        
        if vm:
            if vm['status']!='STOPPED':
                return make_response({"message":"VM already started", "VM status":vm['status']},500) 
            # start vm
            json_req = {
                "cpu_snapshot_path" : "test_cpu",
                "memory_snapshot_path" : "test_memory",
                "kernel_path" : vm['iso_path'],
                "resume" : False,
            }
            r = requests.post(vmbconfig+"/create", json=json_req)
            if r.status_code >= 400:
                return make_response({"message":"Couldn't start VM", "json":r.json()},500) 
            rpc_port = int(r.text)

            # update table
            self.cursor.execute(f"UPDATE vmid SET rpc_port=%s, status='RUNNING' WHERE course_id=%s AND assignment_id=%s AND entry_no=%s AND version=%d", (rpc_port, course_id,assignment_id, entry_no,version))
            return make_response({"message":"VM Started", "rpc_port":rpc_port}, 200)
        else:
            return make_response({"message":"VM doesn't exist"},404) 

    def resume_vm(self, entry_no, course_id, assignment_id,version):
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s AND version=%d', (course_id, assignment_id,entry_no,version   ))
        vm=self.cursor.fetchone()
        # return everything in assignment if it exists
        if vm:            
            if vm['status']!='PAUSED':
                return make_response({"message":"VM not paused", "VM status":vm['status']},500) 

            # resume vm
            json_req = {
                "cpu_snapshot_path" : vm['iso_path'][:-4] + "_cpu",
                "memory_snapshot_path" : vm['iso_path'][:-4] + "_mem",
                "kernel_path" : vm['iso_path'],
                "resume" : True,
            }
            r = requests.post(vmbconfig+"/create", json=json_req)
            if r.status_code >= 400:
                return make_response({"message":"Couldn't start VM", "json":r.json()},500) 
            rpc_port = int(r.text)

            # update table
            self.cursor.execute(f"UPDATE vmid SET rpc_port=%s, status='RUNNING' WHERE course_id=%s AND assignment_id=%s AND entry_no=%s AND version=%d", (rpc_port, course_id,assignment_id , entry_no,version))
            return make_response({"message":"VM Resumed", "rpc_port":rpc_port},201)
        else:
            # VM record NOT FOUND
            return make_response({"message":"No Record Found "},404) 
                    
    def pause_vm(self, entry_no, course_id, assignment_id,version):
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s AND version=%d', (course_id, assignment_id,entry_no,version   ))
        
        vm=self.cursor.fetchone()
        # return everything in assignment if it exists
        if vm:
            # pause vm
            if vm['status']!='RUNNING':
                return make_response({"message":"VM not running", "VM status":vm['status']},500) 
            json_req = {
                "cpu_snapshot_path" : vm['iso_path'][:-4] + "_cpu",
                "memory_snapshot_path" : vm['iso_path'][:-4] + "_mem",
                "kernel_path" : vm['iso_path'],
                "rpc_port" : vm['rpc_port'],
                "resume" : False
            }
            r = requests.post(vmbconfig+"/snapshot", json=json_req)
            if r.status_code >= 400:
                return make_response({"message":"Couldn't start VM", "json":r.json()},500) 

            # update table
            self.cursor.execute(f"UPDATE vmid SET rpc_port=%s, status='PAUSED' WHERE course_id=%s AND assignment_id=%s AND entry_no=%s AND version=%d", (0, course_id,assignment_id , entry_no,version))
            
            return make_response({"message":r.text},201)
        else:
            # VM record NOT FOUND
            return make_response({"message":"No Record Found "},404)   
    
    def get_plag_report(self,data,entry_no,course_id,assignment_id,version):
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no = %s AND version=%d', (course_id, assignment_id,entry_no,version   ))
        
        vm=self.cursor.fetchone()
        # return everything in assignment if it exists
        if vm:
            if vm['plag_report'] is None:
                return make_response({"message":"No plag report found"},404)
            else:
                report=vm['plag_report']
                # TODO Currently just dumping the report 
                return make_response({"message":"Plag report","json":report},201)
        else:
            # VM record NOT FOUND
            return make_response({"message":"No Record Found "},404) 
                    
    def get_tree(self,entry_no,course_id,assignment_id):
        self.cursor.execute('SELECT version,par_version,version_name FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no=%s', (course_id, assignment_id,entry_no))
        versions=self.cursor.fetchall()
        # return everything in assignment if it exists
        if versions:
            return make_response({"message":"Tree found","list":versions},201)
        else:
            return make_response({"message":"No versions found"},404)

    def fork(self, entry_no, course_id, assignment_id,parent_version,new_version_name):
        # Check if parent version exist
        self.cursor.execute('SELECT * FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no=%s AND version=%d', (course_id, assignment_id,entry_no,parent_version))
        versions=self.cursor.fetchone()
        if versions:
            self.cursor.execute('SELECT max(version) FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no=%s', (course_id, assignment_id,entry_no))
            next_version=self.cursor.fetchone()[0]+1
            for i in [".iso","_cpu","_mem"]:
                previous_path = f'./{course_id}_{assignment_id}_{entry_no}_{parent_version}_vm{i}'
                new_path = f'./{course_id}_{assignment_id}_{entry_no}_{next_version}_vm{i}'
                if not os.path.isfile(previous_path):
                    continue
                shutil.copy(previous_path, new_path)
            self.cursor.execute(f"INSERT INTO vmid(entry_no,course_id, assignment_id,version,par_version,version_name,iso_path ) VALUES('{entry_no}','{course_id}', '{assignment_id}', '{next_version}', '{parent_version}', '{new_version_name}','{f'./{course_id}_{assignment_id}_{entry_no}_{next_version}_vm.iso'}')")
            
            return make_response({"message":f"Forked {next_version}",},201)


        else:
            return make_response({"message":"Version Not Found"},404)
    
    def delete_query(self,entry_no,course_id,assignment_id,version):
        self.cursor.execute('SELECT version FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no=%s AND par_version=%d', (course_id, assignment_id,entry_no,version))
        versions=self.cursor.fetchall()
        
        ## DELETE QUERY
        self.cursor.execute('DELETE FROM vmid WHERE course_id = %s AND assignment_id = %s AND entry_no=%s AND version=%d', (course_id, assignment_id,entry_no,version))
        
        for i in [".iso","_cpu","_mem"]:
            previous_path = f'./{course_id}_{assignment_id}_{entry_no}_{version}_vm{i}'
            if not os.path.isfile(previous_path):
                continue
            os.remove(previous_path)

        for child in versions:
            self.delete_query(entry_no,course_id,assignment_id,child['version'])
