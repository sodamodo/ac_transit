import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker   
from sqlalchemy import create_engine
import psycopg2



def get_conn():    
    conn = psycopg2.connect(dbname="postgres", user="zack", password="password", host="database-1.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com")
    conn.autocommit = False
    return conn


conn = get_conn()
# cur = conn.cursor("my_cursor")
cur = conn.cursor()


engine = create_engine('postgresql://zack:password@database-1.c3ohfvdvxlpf.us-east-2.rds.amazonaws.com/postgres', echo=True)
 
Base = declarative_base()
 

class Stop(Base):
    __tablename__ = 'stops'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry('POINT'))
    stp_identi = Column(String(254), nullable=True)
    stp_511_id = Column(Float, nullable=True)
    stp_descri = Column(String(254), nullable=True)
    route = Column(String(254), nullable=True)

class Route(Base):
    __tablename__ = 'routes'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry('LINESTRING'))
    pub_rte = Column(String(8), nullable=True)

# Stop.route = relationship(Route, back_populates="stop")
# Route.stop = relationship(Stop, back_populates="route")

# class RouteStop(Base):
#     __tablename__ = 'routestops'
#     route_id = relationship("Customer", back_populates="stop")
#     # route_id = Column(String(8), nullable=False) 
#     stop_id =  Column(String(8), nullable=False)

Session = sessionmaker(bind=engine)
session = Session()    


for stop in session.query(Stop):
    route_split = stop.route.split()
    for route in route_split:
        # print(route)
        cur.execute("INSERT INTO routestops VALUES('{route_id}', '{stop_id}')".format(route_id=route, stop_id=stop.stp_identi))
        cur.execute("commit")