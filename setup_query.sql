DROP TABLE IF EXISTS predictions;

CREATE TABLE public.predictions
(
  stop_id integer,
  trip_id integer,
  vehicle_id integer,
  route_name character varying,
  predicted_delay character varying,
  predicted_departure timestamp without time zone,
  prediction_datetime timestamp without time zone
);
DROP TABLE IF EXISTS vehicles;
CREATE TABLE public.vehicles
(
  id int NOT NULL,
  trip_id VARCHAR,
  route_name character varying,
  loc geometry(Point,4326),
  bearing character varying,
  speed character varying,
  vehicle_timestamp timestamp without time zone,
  vehicle_id VARCHAR
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
