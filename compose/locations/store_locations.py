import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from database import Vehicles, engine
from sqlalchemy.orm import sessionmaker
from time import sleep, time
from datetime import datetime
import logging

def loop():
    print("abt to try")
    try:
        truth = True
        while (truth):
            # print("in endless truth loop")
            test_vehicles = []
            base_url = "https://api.actransit.org/transit/gtfsrt/vehicles/?token=369BB8F6542E51FF57BC06577AFE829C"

            Session = sessionmaker()
            Session.configure(bind=engine)
            session = Session()
            
            
            # test_vehicle = Vehicle(id=101)
            # print("in insertion try block")

            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get(base_url)
            feed.ParseFromString(response.content) 

            for entity in feed.entity:
                # test_vehicle = Vehicles(id=101)
                # session.add(test_vehicle)
                # session.commit() 

                   

                print("ENTITY...... ", entity)
                id=entity.id
                trip_id=entity.vehicle.trip.trip_id,
                start_time=entity.vehicle.trip.start_time,
                start_date=entity.vehicle.trip.start_date,
                schedule_relationship=entity.vehicle.trip.schedule_relationship
                route_id=entity.vehicle.trip.route_id,
                stop_id=entity.vehicle.stop_id
                lon=entity.vehicle.position.longitude,
                lat=entity.vehicle.position.latitude,
                bearing=entity.vehicle.position.bearing,
                current_stop_sequence = entity.vehicle.current_stop_sequence
                current_status = entity.vehicle.current_status
                occupancy_status = entity.vehicle.occupancy_status
                try:
                    speed=entity.vehicle.position.speed,
                except:
                    speed=None
                timestamp=entity.vehicle.timestamp,
                vehicle_id=entity.vehicle.vehicle.id
                print("entity.... ", entity)

                ts = time()
                string_ts = datetime.fromtimestamp(ts)
                string_feed_ts = datetime.fromtimestamp(timestamp[0])
                delta = string_ts - string_feed_ts
                if delta.days > 0:
                    print("bad data", delta)
                    continue
            
                print("about to make vehicle object")
                print("lon.... ", lon)
                print("lat.... ", lat)
                print("current stop sequence... ", current_stop_sequence)
                print("current status... ", current_status)
                print("schedule relationship... ", schedule_relationship)
                print("occupancy status... ", occupancy_status)

                vehicle = Vehicles(
                    id=id,
                    trip_id=trip_id[0],
                    route_name=route_id[0],
                    stop_id = stop_id,
                    # loc = "ST_GeomFromText('POINT(-71.060316 48.432044)', 4326)",
                    # loc = 'POINT({lon} {lat})'.format(lon=lon[0], lat=lat[0]),
                    lat = lat[0],
                    lon= lon[0],
                    bearing=bearing[0],
                    speed=speed[0],
                    vehicle_timestamp=datetime.fromtimestamp(timestamp[0]),
                    vehicle_id=vehicle_id,
                    current_stop_sequence = current_stop_sequence,
                    current_status = current_status,
                    occupancy_status = occupancy_status,
                )
           
                try:

                    #### TEST VEHICLE #####
                    # test_vehicle = Vehicle(id=100)
                    print("in insertion try block")
                    session.add(vehicle)
                    session.commit()
                except Exception as ex:
                    logging.warning("Insertion error")
                    logging.warning(ex)
            sleep(30)
    except Exception as e:
        print("fail")
        print(e)
        sleep(60)
        loop()



if __name__ == '__main__':

    print("Haiii")
    loop()

    # test_vehicle = Vehicles(id=101)
    # print("in insertion try block")
    # session.add(test_vehicle)
    # session.commit() 
    # sleep(3)


# logging.warning("ping?")

# print("ziiiing")