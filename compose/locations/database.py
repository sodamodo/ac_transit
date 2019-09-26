from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2

def get_cur():
    conn = psycopg2.connect(dbname="bus", user="postgres", password="password", host="107.178.209.119")
    conn.autocommit = True
    cur = conn.cursor()
    return cur

# Base = declarative_base()


# class Routes(Base):
#     __tablename__ = 'routes'
#     route_id = Column(String(10))

# engine = create_engine('postgresql://postgres:transit@35.188.80.87/postgres')
