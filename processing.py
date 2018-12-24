import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from models import Stop, Vehicle
from database import get_cur
import re
import json
import csv
from collections import defaultdict
from geopy.distance import vincenty
from shapely import wkb

cur = get_cur()

stops = []
stops_file = open("stops.csv", "r")
stops_table = csv.reader(stops_file, delimiter=',')
for stops_row in stops_table:
    stop = Stop(stops_row)
    stops.append(stop)

#This gets all the vehicles and puts them into an array of objects.
def populate_vehicles(cur):
    cur.execute("SELECT * FROM vehicles;")
    vehicles = []
    vehicles_table = cur.fetchall()
    for vehicles_row in vehicles_table:
        vehicle = Vehicle(vehicles_row)
        vehicles.append(vehicle)
    return vehicles

#This is confusing with get_stops_for_route, need to rename to be less confusing 
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
    multiple_insert_template_stirng = "INSERT INTO stoppedvehicles (id, trip_id, start_time, start_date, route_name, loc, bearing, speed, vehicle_timestamp) VALUES"
    limiter = 0

def check_if_stopped(vehicle):
    pass

def submit_bulk_sql(sql_string):
    pass

# Calls san pablo hour
vehicles = populate_vehicles(cur)


multiple_insert_template_stirng = "INSERT INTO stoppedvehicles (id, trip_id, start_time, start_date, route_name, stop_id, loc, bearing, speed, vehicle_timestamp, vehicle_id) VALUES"


limiter = 0
counter = 0
for vehicle in vehicles:
    print("stop check called!")
    if vehicle.speed == "0.0":
        stop_dist_dict = get_closest_stop_on_route(vehicle)
        # closest_stop is stop_id and closest_stop[1] is distance
        # if stop_dist_dict.items() == {}:
        #     continue

        if len(stop_dist_dict[vehicle].items()) == 0:
            continue
        closest_stop = min(stop_dist_dict[vehicle].items(), key=lambda kv: kv[1])
        # print("closest stop....", closest_stop)
        stop_id = closest_stop[0]
        if closest_stop[1] < 25:

            print("vehicle timestmap?", vehicle.vehicle_id)
            print("python datatype for timestamp field", type(vehicle.timestamp))

            sql_bulk_insert = """
             ('{id}', '{trip_id}', '{start_time}', '{start_date}',
                                        '{route_id}', {stop_id}, '{loc}', 
                                        '{bearing}', '{speed}', '{timestamp}', '{vehicle_id}'),
            """.format(
                id=vehicle.id,
                trip_id=vehicle.trip_id,
                start_time=vehicle.start_time,
                start_date=vehicle.start_date,
                route_id=vehicle.route_id,
                stop_id=stop_id,
                loc=vehicle.loc,
                bearing=vehicle.bearing,
                speed=vehicle.speed,
                timestamp=vehicle.timestamp,
                vehicle_id=vehicle.vehicle_id
            )
            print(counter)
            counter += 1
            multiple_insert_template_stirng += sql_bulk_insert
    
    limiter += 1
    if limiter > 800:
        multiple_insert_template_stirng = multiple_insert_template_stirng[:-14] + ';'
        multiple_insert_template_stirng = multiple_insert_template_stirng.replace("None", "")
        print("the increasing big bulk import statement....")
        print(multiple_insert_template_stirng)
        cur.execute(multiple_insert_template_stirng)
        multiple_insert_template_stirng = "INSERT INTO stoppedvehicles (id, trip_id, start_time, start_date, route_name, stop_id, loc, bearing, speed, vehicle_timestamp, vehicle_id) VALUES"
        limiter = 0



    # if vehicle.speed == "0.0":
    #     stop_dist_dict = get_closest_stop_on_route(vehicle)
    #     # closest_stop is stop_id and closest_stop[1] is distance
    #     # if stop_dist_dict.items() == {}:
    #     #     continue

    #     if len(stop_dist_dict[vehicle].items()) == 0:
    #         continue
    #     closest_stop = min(stop_dist_dict[vehicle].items(), key=lambda kv: kv[1])
    #     # print("closest stop....", closest_stop)
    #     stop_id = closest_stop[0]
    #     if closest_stop[1] < 25:

    #         print("vehicle timestmap?", vehicle.vehicle_id)
    #         print("python datatype for timestamp field", type(vehicle.timestamp))

    #         sql_bulk_insert = """
    #          ('{id}', '{trip_id}', '{start_time}', '{start_date}',
    #                                     '{route_id}', {stop_id}, '{loc}', 
    #                                     '{bearing}', '{speed}', '{timestamp}', '{vehicle_id}'),

    #         """.format(
    #             id=vehicle.id,
    #             trip_id=vehicle.trip_id,
    #             start_time=vehicle.start_time,
    #             start_date=vehicle.start_date,
    #             route_id=vehicle.route_id,
    #             stop_id=stop_id,
    #             loc=vehicle.loc,
    #             bearing=vehicle.bearing,
    #             speed=vehicle.speed,
    #             timestamp=vehicle.timestamp,
    #             vehicle_id=vehicle.vehicle_id
    #         )
            
    #         multiple_insert_template_stirng = multiple_insert_template_stirng + sql_bulk_insert
    #         # sql_string = """
    #         # INSERT INTO stoppedvehicles VALUES('{id}', '{trip_id}', '{start_time}', '{start_date}',
    #         #                             '{route_id}', {stop_id}, '{loc}', 
    #         #                             '{bearing}', '{speed}', '{timestamp}', '{vehicle_id}')

    #         # """.format(
    #         #     id=vehicle.id,
    #         #     trip_id=vehicle.trip_id,
    #         #     start_time=vehicle.start_time,
    #         #     start_date=vehicle.start_date,
    #         #     route_id=vehicle.route_id,
    #         #     stop_id=stop_id,
    #         #     loc=vehicle.loc,
    #         #     bearing=vehicle.bearing,
    #         #     speed=vehicle.speed,
    #         #     timestamp=vehicle.timestamp,
    #         #     vehicle_id=vehicle.vehicle_id
    #         # )
    #         # print(sql_string)
            
    #         # cur.execute(sql_string)
    #         # print("unpack closest stop", closest_stop)
    #         # print("stop dict", stop_dist_dict)
    #         # print("closest stop", closest_stop)
            
    #     else:
    #         print("need moar data")
    #         continue
    #     if limiter > 10:
    #         break
    #     limiter += 1
# multiple_insert_template_stirng = multiple_insert_template_stirng[:-1] + ';'


# vehicle_map = {}
# for vehicle in vehicles:
#     distance_list = []
#     stops_on_route = get_stops_on_route(cur, vehicle, stops)
#     for stop in stops_on_route:
#         distance_list.append(get_distance_from_stop(cur, vehicle, stop))
#         vehicle_map[vehicle] = min(distance_list)
#         # print("distance stop<-->vehicle", dist)
        
#     sorted_by_value = sorted(vehicle_map.items(), key=lambda kv: kv[1])
#     print(sorted_by_value)







# print("these are the vehicles", vehicles)

# Uses first bus point is 72R bus array to get all the 72R
# stops out of the JSON list
# stops_on_spr = get_stops_on_route(cur, vehicles[0], stops)
# for stop in stops_on_spr:

#     sql_string = """

#         INSERT INTO sanpablorapidstops (SELECT * FROM stops WHERE stop_id={})
#     """.format(stop.stop_id)
#     cur.execute(sql_string)

