import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
# from database import get_cur
import csv

def get_conn():
    conn = psycopg2.connect(dbname="postgres", user="zack", password="password", host="database-1.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com")
    conn.autocommit = False
    return conn

conn = get_conn()
cur = conn.cursor("my_cursor")

cur.execute("SELECT * FROM vehicles ORDER BY vehicle_id, vehicle_timestamp")
vehicles = cur.fetchmany(5000)

# print(len(vehicles))

for vehicle in vehicles:
    # print(vehicle)
    if vehicle[5] == '0.0':
        cur2 = conn.cursor()
        cur2.execute("INSERT INTO stopped_vehicles(speed, route_name) VALUES ('{speed}', '{route_name}')".format(speed=vehicle[5], route_name =  vehicle[2]))
        cur2.execute("commit")

# # with open('stops.csv', "w") as file:
# #     writer = csv.writer(file, delimiter=',')
# #     for stop in stops:
# #         print(stop)
# #         writer.writerow(stop)

# with open('stops.csv', "r") as file:
#     reader = csv.reader(file, delimiter=',')
#     for row in reader:
#         print(row)
#         break
# print("donzo!")