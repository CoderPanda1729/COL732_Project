import os
import mysql.connector

dbconfig = {
    "host":"localhost",
    "port":"3306",
    "username":"gautam",
    "password":"password",
    "database":"App"
}

def scp(username, password, hostname, source, target):
    os.system(f"sshpass -p '{password}' scp -o StrictHostKeyChecking=no {username}@{hostname}:{source} {target}")

def download(course, assignment):
    try:
        connection = mysql.connector.connect(
            host = dbconfig["host"],
            port = dbconfig["port"],
            user = dbconfig["username"],
            password = dbconfig["password"],
            database = dbconfig["database"]
        )
        cursor = connection.cursor(dictionary=True)
    except:
        print("connection error")
        exit()

    sql_query = f"select entry_no, vmid, password from running_vm where course_id = '{course}' and assignment_id = {assignment};"
    cursor.execute(sql_query)
    students = cursor.fetchall()
    for student in students:
        username = student['entry_no']
        hostname = f"192.168.{200+student['vmid']}.2"
        password = student['password']
        if course not in os.listdir("/home/col732_gautam/submissions"):
            os.system(f"mkdir /home/col732_gautam/submissions/{course}")
        if username not in os.listdir(f"/home/col732_gautam/submissions/{course}"):
            os.system(f"mkdir /home/col732_gautam/submissions/{course}/{username}")
        try:
            source = "sub/solution.py"
            target = f"/home/col732_gautam/submissions/{course}/{username}/{assignment}.py"
            scp(username, password, hostname, source, target)
        except:
            continue

download("COL732", "73204")
