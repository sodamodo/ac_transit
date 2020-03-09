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


            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get(base_url)
            feed.ParseFromString(response.content)
            for entity in feed.entity:
                id=entity.id
                print(id)
                trip_id=entity.vehicle.trip.trip_id,
                print(trip_id)
                start_time=entity.vehicle.trip.start_time,
                
                print(start_time)
                start_date=entity.vehicle.trip.start_date,
                
                print(start_date)
                route_id=entity.vehicle.trip.route_id,
                
                print(route_id)
                lon=entity.vehicle.position.longitude,
                
                print(lon)
                lat=entity.vehicle.position.latitude,
                
                print(lat)
                bearing=entity.vehicle.position.bearing,
                
                print(bearing)
                
                
                try: 
                    speed=entity.vehicle.position.speed,
                except:
                    speed=None
                
                print("speeeeed", speed)
                timestamp=entity.vehicle.timestamp,
                
                print("timestamp... ", timestamp)
                
                vehicle_id=entity.vehicle.vehicle.id
                
                print("vehicle id..... ", vehicle_id)
                print("vehicle id.... ", vehicle_id)
                print("timestamp feed time and timestamp...", type(timestamp), timestamp)
                ts = time()
                string_ts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                string_feed_ts = datetime.fromtimestamp(timestamp[0]).strftime('%Y-%m-%d %H:%M:%S')
                string_ts = datetime.fromtimestamp(ts)
                string_feed_ts = datetime.fromtimestamp(timestamp[0])
                delta = string_ts - string_feed_ts
                if delta.days > 0:
                    print("bad data", delta)
                    continue
                print("python today timestamp", string_ts)
                print("feed today timestamp", string_feed_ts)


                print("Output timestamp....", datetime.fromtimestamp(timestamp[0]))



                sql_string = """
                INSERT INTO vehicles VALUES('{id}', '{trip_id}', 
                                            '{route_id}', ST_GeomFromText('POINT({lon} {lat})', 4326),
                                            '{bearing}', '{speed}', '{timestamp}', {vehicle_id});

                """.format(
                    id=id,
                    trip_id=trip_id[0],
                    start_time=start_time[0],
                    start_date=start_date[0],
                    route_id=route_id[0],
                    lon=lon[0],
                    lat=lat[0],
                    bearing=bearing[0],
                    speed=speed[0],
                    timestamp=datetime.fromtimestamp(timestamp[0]),
                    vehicle_id=vehicle_id
                )
                print(sql_string)

                dummy_sql = """
                                INSERT INTO vehicles VALUES('1', '718799020', 
                                            '56', ST_GeomFromText('POINT(-122.079467773 37.6335449219)', 4326),
                                            '179.0', '6.70559978485', '2020-02-26 20:02:07', 5022);

                """

                cur.execute(sql_string)
            sleep(30)
    except:
        print("FAIL")
        
        sleep(60)
        loop()


if __name__ == '__main__':
    loop()
