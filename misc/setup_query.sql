UPDATE vehicles SET loc = ST_SetSRID(ST_MakePoint(lon :: FLOAT, lat :: FLOAT),4326)


DROP TABLE IF EXISTS predictions;

CREATE TABLE public.predictions
(
  id SERIAL PRIMARY KEY
  stop_id integer,
  trip_id integer,
  vehicle_id integer,
  route_name character varying,
  predicted_delay character varying,
  predicted_departure timestamp without time zone,
  prediction_datetime timestamp without time zone
);

DROP TABLE IF EXISTS vehicles; 
CREATE TABLE vehicles
(
  pk SERIAL PRIMARY KEY,
  id INT NOT NULL,	
  trip_id VARCHAR,
  route_name character varying,
  schedule_relationship VARCHAR,
  stop_id VARCHAR,
  loc geometry(Point,4326),
  lat VARCHAR,
  lon VARCHAR,
  bearing character varying,
  speed character varying,
  vehicle_timestamp timestamp without time zone,
  vehicle_id VARCHAR,
  current_stop_sequence INT,
  current_status VARCHAR,
  occupancy_status VARCHAR 	
	
);





DROP TABLE IF EXISTS stoppedvehicles;
CREATE TABLE public.stoppedvehicles
(
  id int NOT NULL,
  trip_id VARCHAR,
  route_name character varying,
  stop_id integer,
  loc geometry(Point,4326),
  bearing character varying,
  speed character varying,
  vehicle_timestamp timestamp without time zone,
  vehicle_id VARCHAR
);
