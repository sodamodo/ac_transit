import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="bus", user="postgres", password="password", host="107.178.209.119")
    conn.autocommit = True
    cur = conn.cursor()
    return cur
