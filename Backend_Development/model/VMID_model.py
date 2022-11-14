import mysql.connector
import json
import os
from flask import make_response
from configs.config import dbconfig, vmbconfig
from requests import request as http_request
import shutil
from .course_model import course_model
import requests
from random import randint
from controller.utils import create,snapshot
from .activities_model import activities_model 
# from app import app

class VmidModel:
    def __init__(self):
        '''
        this table is to keep track of running VMs
        '''
        try:

            self.conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cursor=self.conn.cursor(dictionary=True)

            sql='''CREATE TABLE IF NOT EXISTS running_vm(
                entry_no CHAR(40),
                course_id CHAR(40),
                assignment_id CHAR(80),
                rpc_port INT,
                vmid INT,
                password CHAR(40),
                primary key (entry_no,course_id,assignment_id)
            )'''

            self.cursor.execute(sql)
            print("Connection Established ")
            self.images_path = '../images/'
        except Exception as e:
            print(e)
            print("Some Connection Error")

    def generate_password(self):
        alphabet = [(65,90),(97,122),(48,57)]
        pass_len = randint(8,12)
        res = ''
        for i in range(pass_len):
            a = alphabet[randint(0,2)]
            res+=chr(randint(a[0],a[1]))
        return res
    
    def generate_vmid(self):
        '''
        returns the least number which is not in the vmid list
        '''
        self.cursor.execute('select vmid from running_vm;')
        vmids = self.cursor.fetchall()
        vmids_list = []
        for i in vmids:
            vmids_list.append(i['vmid'])
        for i in range(50):
            if(i not in vmids_list):
                return i
        return -1

    def get_vm(self, entry_no, course_id, assignment_id):
        # get record in table
        self.cursor.execute('SELECT * FROM running_vm WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, assignment_id,entry_no))
        vm=self.cursor.fetchone()
        if vm:
            return make_response({'message':'running','password':vm['password'],'vmid':vm['vmid']},201)
        else:
            return make_response({"message":"VM does not exist"},201) 

    def check_running(self,entry_no,course_id, asmt_id):
        self.cursor.execute('SELECT * FROM running_vm WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, asmt_id,entry_no))
        vm=self.cursor.fetchone()
        if vm:
            return True
        else:
            return False
    
    ##Prashant Mishra 
    # @app.route("/check/<string:entry_no>/<string:course_id>/<string:asmt_id>",methods=["POST"])
    def start_fresh(entry_no,course_id, asmt_id, iso="bzimage_final8"):
    # def start_fresh(self,entry_no,course_id, asmt_id, iso="bzimage_final8"):
        '''
        launch the VM fresh, will be used by the assingnment maker
        iso has to be used, currently hard coded because only that is supported
        '''
        # vmid = self.generate_vmid()
        # if(vmid == -1):
        #     return make_response({'message':'start failed'},201)
        # password = self.generate_password()
        # print('starting', entry_no, password, vmid)
        # resp = create('null','null', self.images_path+iso,False,"vmtap100",entry_no,password,vmid)
        activity_obj=activities_model()
        activity_obj.record_activity(entry_no,course_id,asmt_id,"start")
        # rpc_port = resp['port']
        #also send the entry_no,VMID and password to the ssh

        # print('create response', resp)
        # sql=f'''INSERT INTO running_vm(entry_no,course_id,assignment_id,rpc_port,vmid,password) 
        #         VALUES ('{entry_no}','{course_id}','{asmt_id}',{rpc_port},{vmid},'{password}')'''
        # self.cursor.execute(sql)
        return make_response({'message':'started','password':"password",'vmid':11})
        # return make_response({'message':'started','password':password,'vmid':vmid})
    
    def save_template(self, entry_no,course_id,asmt_id):
        '''
        get the running vm entry and signal the snapshot team to take the snapshot and store it in /course/asmt/cpu_template, mem_template
        '''
        self.cursor.execute('SELECT * FROM running_vm WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, asmt_id,entry_no))
        vm=self.cursor.fetchone()
        if(vm):
            res = snapshot(f"{course_id}_{asmt_id}_cpu_template",
            f"{course_id}_{asmt_id}_mem_template",
            vm['rpc_port'],
            False,
            'vmtap100'
            )

            print('SNAPSHOT ',res)
            if(res=='''"Snapshot taken successfully"'''):
                self.cursor.execute(f"DELETE FROM running_vm WHERE entry_no='{entry_no}' and course_id='{course_id}' and assignment_id='{asmt_id}'")
                print('SNAPSHOT SUCCESSFUL')
                return {'message':'saved'}
            else:
                return {'message':'save failed'}
        else:
            return {'message':'no vm'}
    


    def start_template(self, entry_no, course_id, asmt_id, iso):
        '''
        this is for the student when he starts the assignment
        '''
        self.cursor.execute('SELECT * FROM running_vm WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, asmt_id,entry_no))
        vm=self.cursor.fetchone()        
        if not vm:
            # start vm
            resp = create(f"{course_id}_{asmt_id}_cpu_template",
            f"{course_id}_{asmt_id}_mem_template",
            self.images_path+iso,
            True, "vmtap100",entry_no,password,vmid)
            if('port' in resp):
                rpc_port = int(resp['port'])
                password = self.generate_password()
                vmid = self.generate_vmid()
                sql = f'''
                INSERT INTO running_vm(entry_no,course_id,assignment_id,rpc_port,vmid,password) 
                VALUES ('{entry_no}','{course_id}','{asmt_id}',{rpc_port},{vmid},'{password}');
                '''
                self.cursor.execute(sql)
                return make_response({"message":"started", "rpc_port":rpc_port, 'password':password, 'vmid':vmid}, 201)
            else:
                return make_response({'message':'start failed'},201)
        else:
            return make_response({"message":"started",'password':vm['password'],'vmid':vm['vmid']},201) 

    def resume_vm(self, entry_no, course_id, asmt_id, iso):
        self.cursor.execute('SELECT * FROM running_vm WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, asmt_id,entry_no))
        vm=self.cursor.fetchone()
        if not vm:#if not running then launch a VM            
            # resume vm
            vmid=self.generate_vmid()
            password=self.generate_password()
            resp = create(f"{course_id}_{asmt_id}_{entry_no}_cpu",f"{course_id}_{asmt_id}_{entry_no}_mem",
            self.images_path+iso,True,"vmtap100",entry_no,password,vmid)     

            activity_obj=activities_model()
            activity_obj.record_activity(entry_no,course_id,asmt_id,"resume")

            if('port' in resp):
                rpc_port = int(resp['port'])
                # update table
                sql = f'''
                INSERT INTO running_vm(entry_no, course_id,assignment_id,rpc_port,vmid,password) 
                VALUES ('{entry_no}','{course_id}','{asmt_id}',{rpc_port},{vmid},'{password}')
                '''
                self.cursor.execute(sql)
                return make_response({"message":"resumed", 'password':password, 'vmid':vmid},201)
            else:
                return make_response({'message':'resume failed'},201)
        else:
            return make_response({"message":"resumed", 'password':vm['password'], 'vmid':vm['vmid']},201) 
                    
    def pause_vm(self, entry_no, course_id, asmt_id):
        self.cursor.execute('SELECT * FROM running_vm WHERE course_id = %s AND assignment_id = %s AND entry_no = %s', (course_id, asmt_id,entry_no))
        vm=self.cursor.fetchone()
        # return everything in assignment if it exists
        if vm:
            # pause vm
            resp = snapshot(f"{course_id}_{asmt_id}_{entry_no}_cpu", f"{course_id}_{asmt_id}_{entry_no}_mem",
            vm['rpc_port'],False,'vmtap100')

            activity_obj=activities_model()
            activity_obj.record_activity(entry_no,course_id,asmt_id,"pause")
            print('PAUSE VM ', resp)
            if(resp == '''"Snapshot taken successfully"'''):
                # update table
                self.cursor.execute(f"DELETE FROM running_vm WHERE course_id=%s AND assignment_id=%s AND entry_no=%s", (course_id, asmt_id, entry_no))
                return make_response({"message":'paused'},201)
            else:
                return make_response({'message':'pause failed'},201)
        else:
            # VM record NOT FOUND
            return make_response({"message":"No Record Found "},201)
    
    
                    
    
                    
                    