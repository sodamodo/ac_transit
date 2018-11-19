

Convert routes on stop table into JSON list.



##### API CODES

predictions - 78A6470DBD59DB9CDFBF9427A4443A2E

1 - 9A9392AEE88125369B928F281DBD341B
2 - 59D69D98A213F47907DCC4666C429F97
3 - 4D8D94A3FF690D5DF8A99632D14DF06C
4 - 1E2B2B65A3BB9B09E6581DB918E59552
5 - 7C8EB1A0359B4FCB17645149332000EA
6 - E73043FEBE5FE52ECE7E35E4AD29C1F0
7 - C1C124A2128F34A92DE7BA44E1723ADC
8 - 1FBF820DDA7B36BC245B4662C8652142
9 - 6EDE923273A789628CC571F8381228C1
10 - FEA38127BA898B57C50E44BA8CC4ED5B
11 - BB23E1BB9E6A1FFA9FC90DBF1667CA0E
12 - CEF6C4904CAB78D632C2ED96AD835A4D
13 - 846CEAE09EF0ED844DA114929C3B06F0
14 - DECCCBDEAABEC6E7F5462628664D43BC
15 - A11EB2F3B50E1BAC9781B64E3AB703DF
16 - 234E960C8F3367C64DF67A8CCB3538A7
17 - 337EAEE9402F615021C2F41CE6808EA1
18 - FD87E46473298FCB4245BA8F0A1D5136
19 - 4F15092F9CB725502FB1506DD630B805
20 - 0031A200345291CBACC08DDAEC4D6A00

###### Processing 
Opens a local CSV of all stops. Pulls every vehicle point. Is passed
a route and looks through the JSON routes in each stop and pulls out the stops for that passed route. Knowing the stops that the vehicle (which comes with its route) is using, if the vehicle is slow enough and close enough to a stop it uploads record with vehicle info as well as the stop its stopped at. 


#####Querying

SELECT predictions.stop_id, predictions.trip_id, predictions.vehicle_id, route_name, predicted_delay, prediction_datetime,
	predicted_departure, time
	FROM predictions LEFT JOIN stoppedvehicles ON
	predictions.vehicle_id = stoppedvehicles.vehicle_id AND predictions.trip_id = stoppedvehicles.trip_id WHERE time IS NOT NULL;
	
SELECT (predicted_departure - vehicle_timestamp) AS delta FROM predwstoppedvehicletime;

SELECT (vehicle_timestamp - vehicle_actual_arrival) FROM vehicles LEFT JOIN predwstoppedvehicletime 
	ON vehicles.vehicle_id = predwstoppedvehicletime.vehicle_id AND vehicles.trip_id = predwstoppedvehicletime.trip_id;

#####Create a view for each prediction which incudles the timestamp when the bus actually arrived

CREATE MATERIALIZED VIEW predwrrival AS (SELECT predictions.id AS prediction_id,  predictions.stop_id, predictions.trip_id, predictions.vehicle_id, route_name, predicted_delay, prediction_datetime,
	predicted_departure, time AS actual_arrival_time
	FROM predictions LEFT JOIN stoppedvehicles ON
	predictions.vehicle_id = stoppedvehicles.vehicle_id AND predictions.trip_id = stoppedvehicles.trip_id WHERE time IS NOT NULL
	);


#####master arrivals table without deltas. Keeping the no negative time till time delta
SELECT * FROM vehicles LEFT JOIN predwarrival 
ON vehicles.trip_id = predwarrival.trip_id AND vehicles.vehicle_id = predwarrival.vehicle_id
	WHERE (actual_arrival_time - vehicle_timestamp) > INTERVAL '0';
SELECT * FROM vehicles LEFT JOIN predwarrival ON vehicles.trip_id = predwarrival.trip_id AND vehicles.vehicle_id = predwarrival.vehicle_id;

#####Creates a master table that has all the vehicle points with their associated predictions

CREATE TABLE master AS (
SELECT predwarrival.stop_id, predwarrival.trip_id, predwarrival.route_name,
	predicted_delay, prediction_datetime, predicted_departure, predwarrival.vehicle_id,
	vehicles.id, loc, vehicle_timestamp, actual_arrival_time FROM vehicles LEFT JOIN predwarrival 
ON vehicles.trip_id = predwarrival.trip_id AND vehicles.vehicle_id = predwarrival.vehicle_id
	WHERE (actual_arrival_time - vehicle_timestamp) > INTERVAL '0');

#####Add predicted_tta column
```sql
ALTER TABLE master ADD COLUMN actual_tta INTERVAL;
```
#####Add predicted_tta column
ALTER TABLE master ADD COLUMN predicted_tta INTERVAL;

#####Set time in minutes till bus arrival

UPDATE master SET actual_tta = (actual_arrival_time - vehicle_timestamp);
#####Set time in minutes till predicted bus arrival
UPDATE master SET actual_tta = (predicted_departure - vehicle_timestamp);
#####Gets actual time until vehicle arrives at stop
SELECT (actual_arrival_time - vehicle_timestamp) AS actual_mta FROM vehicles LEFT JOIN predwarrival 
ON vehicles.trip_id = predwarrival.trip_id AND vehicles.vehicle_id = predwarrival.vehicle_id
	WHERE (actual_arrival_time - vehicle_timestamp) > INTERVAL '0';
SELECT * FROM vehicles LEFT JOIN predwarrival ON vehicles.trip_id = predwarrival.trip_id AND vehicles.vehicle_id = predwarrival.vehicle_id;



#### Master SQL Command 

```sql
REFRESH MATERIALIZED VIEW predwarrival;

DROP TABLE public.master;

CREATE TABLE master AS (
SELECT predwarrival.stop_id, predwarrival.trip_id, predwarrival.route_name,
	predicted_delay, prediction_datetime, predicted_departure, predwarrival.vehicle_id,
	vehicles.id, loc, vehicle_timestamp, actual_arrival_time FROM vehicles LEFT JOIN predwarrival 
ON vehicles.trip_id = predwarrival.trip_id AND vehicles.vehicle_id = predwarrival.vehicle_id
	WHERE (actual_arrival_time - vehicle_timestamp) > INTERVAL '0');

ALTER TABLE master ADD COLUMN actual_tta INTERVAL;
ALTER TABLE master ADD COLUMN predicted_tta INTERVAL;

UPDATE master SET actual_tta = (actual_arrival_time - vehicle_timestamp);

UPDATE master SET predicted_tta = (predicted_departure - vehicle_timestamp);
```

##### Tinkers
vehicle_timestamp from vehicles is in corrent timezone, however NOW() returns in GMT.

##### Issues 
* How to handle if there is DB connection exception
