from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engi
import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="busdb", user="bususer", password="thebuspass", host="busdb.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com")
    conn.autocommit = True
    cur = conn.cursor()
    return cur

Base = declarative_base()


class Vechicles(Base):
    __tablename__ = 'predictions'
    pk = Column(Integer)
    id = Column(Integer)
    trip_id = Column(Integer)
    route_name = Column(String)
    stop_id = Column(Integer)
    loc = Column(String)
    bearing = Column(String)
    speed = Column(String)
    vechicle_timestamp = Column(String)
    vehicle_id = Column(String)


engine = create_engine('postgresql://bususer:thebuspass@busdb.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com/busdb')

