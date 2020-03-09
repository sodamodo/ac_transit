import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="postgres", user="zack", password="password", host="database-1.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com")
    conn.autocommit = True
    cur = conn.cursor()
    return cur
