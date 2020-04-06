import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from datetime import datetime
from time import sleep, time
from models import Stop, Vehicle
from shapely import wkb
from geopy.distance import vincenty


# from database import get_cur
import csv

#This gets all the vehicles and puts them into an array of objects.
##### I THINK THIS IS MOOT 
def populate_vehicles(cur):
    cur.execute("SELECT * FROM vehiclesubset LIMIT 1000;")
    vehicles = []
    vehicles_table = cur.fetchall()
    for vehicles_row in vehicles_table:
        vehicle = Vehicle(vehicles_row)
        vehicles.append(vehicle)
    return vehicles
###########################
def get_conn():    
    conn = psycopg2.connect(dbname="postgres", user="zack", password="password", host="database-1.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com")
    conn.autocommit = False
    return conn


def get_stops_on_route(cur, vehicle, stops):
    stops_on_route = []
    for stop in stops:
        for route in stop.json_routes:
            if vehicle.route_id == route:
                stops_on_route.append(stop)

    return stops_on_route

def get_distance_from_stop(cur, vehicle, stop):

    vehicle_point = wkb.loads(vehicle.loc, hex=True)
    stop_point = wkb.loads(stop.geom, hex=True)
    distance = vincenty((vehicle_point.y, vehicle_point.x), (stop_point.y, stop_point.x)).m
    return distance

def get_closest_stop_on_route(vehicle):
    stop_dist_dict = {vehicle: {}}
    distance_list = []
    stops_on_route = get_stops_on_route(cur, vehicle, stops)
    for stop in stops_on_route:
        # distance_list.append(get_distance_from_stop(cur, vehicle, stop))
        stop_dist_dict[vehicle][stop.stop_id] = get_distance_from_stop(cur, vehicle, stop)

    return stop_dist_dict

def multiple_insert(insert_string):
    cur.execute(insert_string)
    multiple_insert_template_stirng = "INSERT INTO stopped_vehicles (id, trip_id, start_time, start_date, route_name, loc, bearing, speed, vehicle_timestamp) VALUES"
    limiter = 0

multiple_insert_template_stirng = "INSERT INTO stopped_vehicles (id, trip_id, start_time, start_date, route_name, stop_id, loc, bearing, speed, vehicle_timestamp, vehicle_id) VALUES"

conn = get_conn()
cur = conn.cursor("my_cursor")

cur.execute("SELECT *, ST_X(loc), ST_Y(loc) FROM vehicles_dev ORDER BY vehicle_id, vehicle_timestamp")


stops = []
stops_file = open("stops.csv", "r")
stops_table = csv.reader(stops_file, delimiter=',')
for stops_row in stops_table:
    stop = Stop(stops_row)
    stops.append(stop)


while True:

    vehicles = cur.fetchmany(5000)

    has_looped = False
    
    for vehicle in vehicles:
        print(vehicle)
        has_looped = True
        vehicle = Vehicle(vehicle)
        
        sql_string = """
                    INSERT INTO stopped_vehicles VALUES('{id}', '{trip_id}',
                                                '{route_id}', ST_GeomFromText('POINT({lon} {lat})', 4326),
                                                '{bearing}', '{speed}', '{timestamp}', '{vehicle_id}');

                    """.format(
                        id=vehicle.id,
                        trip_id=vehicle.trip_id,
                        route_id=vehicle.route_id,
                        lon=vehicle.y,
                        lat=vehicle.y,
                        bearing=vehicle.bearing,
                        speed=vehicle.speed,
                        # timestamp=datetime.fromtimestamp(timestamp[0]),
                        timestamp=vehicle.timestamp,
                        vehicle_id=vehicle.vehicle_id
                    )
        



        
        if vehicle.speed == "0.0":
            stop_dist_dict = get_closest_stop_on_route(vehicle)
        
            if len(stop_dist_dict[vehicle].items()) == 0:
                continue
            closest_stop = min(stop_dist_dict[vehicle].items(), key=lambda kv: kv[1])
            # print("closest stop....", closest_stop)
            stop_id = closest_stop[0]
            if closest_stop[1] < 25:
        
                # print("vehicle timestmap?", vehicle.vehicle_id)
                # print("python datatype for timestamp field", type(vehicle.timestamp))
        


                sql_bulk_insert = """
                ('{id}', '{trip_id}', '{route_id}', {stop_id}, '{loc}', '{bearing}', '{speed}', '{timestamp}', '{vehicle_id}'),
                """.format(
                    id=vehicle.id,
                    trip_id=vehicle.trip_id,
                    # start_time=vehicle.start_time,
                    # start_date=vehicle.start_date,
                    route_id=vehicle.route_id,
                    stop_id=stop_id,
                    loc=vehicle.loc,
                    bearing=vehicle.bearing,
                    speed=vehicle.speed,
                    timestamp=vehicle.timestamp,
                    vehicle_id=vehicle.vehicle_id
                )

                # print(counter)
                # counter += 1
                multiple_insert_template_stirng += sql_bulk_insert

                cur = conn.cursor()
                cur.execute(sql_string)
                cur.execute("commit")

    if has_looped is False:
        break


    # sql_bulk_insert = """
    #  ('{id}', '{trip_id}', '{start_time}', '{start_date}',
    #                             '{route_id}', {stop_id}, '{loc}',
    #                             '{bearing}', '{speed}', '{timestamp}', '{vehicle_id}'),
    # """.format(
    #     id=vehicle.id,
    #     trip_id=vehicle.trip_id,
    #     start_time=vehicle.start_time,
    #     start_date=vehicle.start_date,
    #     route_id=vehicle.route_id,
    #     stop_id=stop_id,
    #     loc=vehicle.loc,
    #     bearing=vehicle.bearing,
    #     speed=vehicle.speed,
    #     timestamp=vehicle.timestamp,
    #     vehicle_id=vehicle.vehicle_id
    # )



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