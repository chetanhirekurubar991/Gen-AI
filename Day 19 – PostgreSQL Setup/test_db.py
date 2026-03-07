import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
connection = os.getenv("DB_URL")
try:
    conn=psycopg2.connect(connection)
    print("Connected to database")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM USERS;")
    users=cursor.fetchall()
    for user in users:
        print(user)
    cursor.close()
    conn.close()
    print("Connection Closed")
except Exception as e:
    print(f"Error : {e}")


