DROP TABLE predictions;

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

DROP TABLE vehicles;

CREATE TABLE public.vehicles
(
  id uuid NOT NULL,
  trip_id integer,
  start_time time with time zone,
  start_date integer,
  route_name character varying,
  loc geometry(Point,4326),
  bearing character varying,
  speed character varying,
  vehicle_timestamp timestamp without time zone,
  vehicle_id integer,
  CONSTRAINT vehicles_pkey PRIMARY KEY (id)
);

DROP TABLE stoppedvehicles;

CREATE TABLE public.stoppedvehicles
(
  id uuid NOT NULL,
  trip_id integer,
  start_time time with time zone,
  start_date integer,
  route_name character varying,
  stop_id integer,
  loc geometry(Point,4326),
  bearing character varying,
  speed character varying,
  vehicle_timestamp timestamp without time zone,
  vehicle_id integer
)