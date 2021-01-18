from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from geoalchemy2 import Geometry
import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="busdb", user="bususer", password="thebuspass", host="busdb.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com")
    conn.autocommit = True
    cur = conn.cursor()
    return cur

Base = declarative_base()


class Vehicles(Base):
    __tablename__ = 'vehicles'
    pk = Column(Integer, primary_key=True)
    id = Column(Integer)
    trip_id = Column(Integer)
    route_name = Column(String)
    schedule_relationship = Column(String)
    stop_id = Column(String)
    loc = Column(Geometry(geometry_type='POINT'))
    lat = Column(String)
    lon = Column(String)
    bearing = Column(String)
    speed = Column(String)
    vehicle_timestamp = Column(String)
    vehicle_id = Column(String)
    current_stop_sequence = Column(Integer)
    current_status = Column(String)
    occupancy_status = Column(String)


engine = create_engine('postgresql://bususer:thebuspass@busdb.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com/busdb')

    # loc = Column(Geometry(geometry_type='POINT', srid=4326))