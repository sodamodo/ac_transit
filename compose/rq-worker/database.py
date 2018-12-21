import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="transit", host="35.230.49.21")
    conn.autocommit = True
    cur = conn.cursor()
    return cur
