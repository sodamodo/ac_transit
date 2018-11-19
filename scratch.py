import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from database import get_cur
import csv

cur = get_cur()

cur.execute("SELECT * FROM stops")
stops = cur.fetchall()


# with open('stops.csv', "w") as file:
#     writer = csv.writer(file, delimiter=',')
#     for stop in stops:
#         print(stop)
#         writer.writerow(stop)

with open('stops.csv', "r") as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        print(row)
        break
print("donzo!")