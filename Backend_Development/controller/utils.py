from app import app
from model.assignment_model import AssignmentModel
from flask import request
from flask import make_response
import jwt
from configs.config import server_config
import requests

def decode_auth_token(s):
    try:
        payload = jwt.decode(s, server_config['SECRET_KEY'],algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def isValidToken(s, entry_num, role):
    print("yoy ", type(s), s)
    st=decode_auth_token(str(s))
    print(st, entry_num+"#"+role)
    return st == entry_num+"#"+role

def create(cpu_snap:str, mem_snap:str, kp:str, resume:bool, tap_dev:str, user:str, password:str, id:int):
    # start vm
    json_req = {
        "cpu_snapshot_path" : cpu_snap,
        "memory_snapshot_path" : mem_snap,
        "kernel_path" : kp,
        "resume" : resume,
        "tap_device":tap_dev,
        "config":{
                "username":user,
                "password":password,
                "id":id,
        }
    }
    r = requests.post("http://10.237.23.38:8012/create", json=json_req)
    return r.json()

def snapshot(cpu_snap:str, mem_snap:str, rpc_port:int, resume:bool, tap_dev:str):
    # start vm
    json_req = {
        "cpu_snapshot_path" : cpu_snap,
        "memory_snapshot_path" : mem_snap,
        "rpc_port" : rpc_port,
        "resume" : resume,
        "tap_device":tap_dev
    }
    r = requests.post("http://10.237.23.38:8012/snapshot", json=json_req)
    return (r.text)
