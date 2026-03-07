import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

conn_dt=os.getenv("DB_URL")
try:
    conn=psycopg2.connect(conn_dt)
    print("Connection Successfully")
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM USERS")
    users=cursor.fetchone()[0]
    print(f"Total is : {users}")
    cursor.close()
    conn.close()
    print("Connection Closed")
except Exception as e:
    print(f'Error : {e}')
