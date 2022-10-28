import mysql.connector
from configs.config import dbconfig

class course_model():

    def __init__(self):

        try:
            self.connection = mysql.connector.connect(
                host = dbconfig["host"],
                port = dbconfig["port"],
                user = dbconfig["username"],
                password = dbconfig["password"],
                database = dbconfig["database"]
            )
            self.cursor = self.connection.cursor(dictionary=True)

            sql_query = '''
                create table if not exists course(
                    entry_no varchar(40) not null,
                    role varchar(40) not null,
                    course_id varchar(40) not null,
                    primary key(entry_no, role, course_id)
                );
            '''

            self.cursor.execute(sql_query)
            self.connection.commit()
            print("connection established")

        except:
            print("connection error")

    def get_course_model(self, entry_no, role):
        try:
            sql_query = f"select course_id from course where entry_no='{entry_no}' and role='{role}';"
            self.cursor.execute(sql_query)
        except:
            print("database error")
        courses = self.cursor.fetchall()
        return courses

    def set_course_model(self, entry_no, role, course_id):
        try:
            sql_query = f"insert into course(entry_no, role, course_id) values('{entry_no}','{role}','{course_id}');"
            self.cursor.execute(sql_query)
            self.connection.commit()
        except:
            print("course already added")

    def removeMember(self, entry_no, role, course_id):
        try:
            sql_query = f"delete from course where entry_no='{entry_no}' and role='{role}' and course_id='{course_id}';"
            self.cursor.execute(sql_query)
            self.connection.commit()
        except:
            print('DELETE UNSUCCESSFUL')
    
    def getAllMembers(self,course_id):
        try:
            sql_query = f"select entry_no,role from course where course_id='{course_id}';"
            self.cursor.execute(sql_query)
        except:
            print("database error")
        courses = self.cursor.fetchall()
        return courses
            