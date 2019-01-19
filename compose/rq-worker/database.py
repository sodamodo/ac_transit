import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="bp", user="postgres", password="transit", host="35.224.158.32")
    conn.autocommit = True
    cur = conn.cursor()
    return cur
