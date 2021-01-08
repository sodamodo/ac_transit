import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from database import get_cur
from time import sleep, time
from datetime import datetime


base_url = "https://api.actransit.org/transit/gtfsrt/vehicles/?token=369BB8F6542E51FF57BC06577AFE829C"


feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get(base_url)
feed.ParseFromString(response.content)


for entity in feed.entity:
    print(entity)
    # print("ID... ", entity.id)

    # id=entity.vehicle.id
    print("ID... ", entity.vehicle)

    trip_id=entity.vehicle.trip_id
    print("tripid.. ", trip_id)

    schedule_relationship = entity.vehicle.schedule_relationship
    print("schedule relationship,... ", schedule_relationship)

    route_id = entity.vehicle.route_id
    print("schedule relationship,... ", route_id)

    break
