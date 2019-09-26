import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from database import get_cur
from time import sleep, time
from datetime import datetime

def loop():
    try:
        truth = True
        while (truth):
            cur = get_cur()
            base_url = "https://api.actransit.org/transit/gtfsrt/vehicles/?token=369BB8F6542E51FF57BC06577AFE829C"
            # d = datetime.date.today()
            # print("today",d)


            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get(base_url)
            feed.ParseFromString(response.content)
            print("HOW LONG IS THIS FEED... ", len(feed.entity))
            for entity in feed.entity:
                try:
                    # print("I AM ENTITyYYY.... ",entity)

                    id=entity.vehicle.id
                    print("ID... ", id)

                    
                    lon=entity.vehicle.position.longitude,
                    print("LON.... ", lon)
                    
                    lat=entity.vehicle.position.latitude,
                    print("LAT.... ", lat)
                    
                    try:
                        speed=entity.vehicle.position.speed,
                    except:
                        speed=None
                    timestamp=entity.vehicle.timestamp

                    print("TIMESTAMP... ", timestamp)
                    vehicle_id=entity.vehicle.vehicle.id

                    print("VEHICLE ID... ", vehicle_id)
                except:
                    print("PROBLEM WIth ACCEESSING JSON OBJECT")
                ts = time()
                # string_ts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                # string_feed_ts = datetime.fromtimestamp(timestamp[0]).strftime('%Y-%m-%d %H:%M:%S')
                string_ts = datetime.fromtimestamp(ts)
                string_feed_ts = datetime.fromtimestamp(timestamp[0])
                delta = string_ts - string_feed_ts
                if delta.days > 0:
                    print("bad data", delta)
                    continue

                print("MADE IT TO THE STRING")
                sql_string = """
                 INSERT INTO vehicles VALUES('{id}', '{trip_id}',
                                            '{route_id}', ST_GeomFromText('POINT({lon} {lat})', 4326),
                                            '{speed}', '{timestamp}', {vehicle_id});
                """.format(
                    id=id,
                    trip_id=trip_id[0],
                    route_id=route_id[0],
                    lon=lon[0],
                    lat=lat[0],
                    speed=speed[0],
                    timestamp=datetime.fromtimestamp(timestamp[0]),
                    vehicle_id=vehicle_id
                )
                print("HAIII")
                print(sql_string)

                PRINT("TRIP ID... ", trip_id[0])
                try:
                    cur.execute(sql_string)
                except:
                    print("CANNOT INSERT INTO DATABASE")
            sleep(30)
    except:
        print("CALLED GENERAL EXCEPTION")
        sleep(10)
        loop()


if __name__ == '__main__':
    loop()



                # print("python today timestamp", string_ts)
                # print("feed today timestamp", string_feed_ts)


                # print("Output timestamp....", datetime.fromtimestamp(timestamp[0]))
                # sql_string = """
                # INSERT INTO vehicles VALUES('{id}', '{trip_id}', '{start_time}', '{start_date}',
                #                             '{route_id}', ST_GeomFromText('POINT({lon} {lat})', 4326),
                #                             '{bearing}', '{speed}', '{timestamp}', {vehicle_id});

                # """.format(
                #     id=id,
                #     trip_id=trip_id[0],
                #     start_time=start_time[0],
                #     start_date=start_date[0],
                #     route_id=route_id[0],
                #     lon=lon[0],
                #     lat=lat[0],
                #     bearing=bearing[0],
                #     speed=speed[0],
                #     timestamp=datetime.fromtimestamp(timestamp[0]),
                #     vehicle_id=vehicle_id
                # )


                 # print("vehicle id.... ", vehicle_id)
                # print("timestamp feed time and timestamp...", type(timestamp), timestamp)