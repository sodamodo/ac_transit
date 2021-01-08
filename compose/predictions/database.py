from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="busdb", user="bususer", password="thebuspass", host="busdb.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com")
    conn.autocommit = True
    cur = conn.cursor()
    return cur

Base = declarative_base()


class Predictions(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    stop_id = Column(Integer)
    trip_id = Column(Integer)
    vehicle_id = Column(Integer)
    route_name = Column(String)
    predicted_delay = Column(String)
    predicted_departure = Column(String)
    prediction_datetime = Column(String)

engine = create_engine('postgresql://bususer:thebuspass@busdb.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com/busdb')
