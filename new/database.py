import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="34.70.43.210")
    conn.autocommit = True
    cur = conn.cursor()
    return cur