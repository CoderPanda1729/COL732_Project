import mysql.connector
from configs.config import dbconfig
import sys

conn = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
conn.autocommit = True
cursor = conn.cursor(dictionary=True)

tableNames = sys.argv[1:]

for table in tableNames:
    cursor.execute("DELETE FROM %s", table)