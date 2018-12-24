DROP TABLE IF EXISTS combinedpredictions;

CREATE TABLE combinedpredictions AS (
	SELECT predictions.stop_id
	,predictions.trip_id
	,predictions.vehicle_id
	,predictions.route_name
	,prediction_datetime
	,predicted_departure
	,vehicle_timestamp AS actual_arrival_time FROM predictions LEFT JOIN stoppedvehicles
	ON predictions.vehicle_id = stoppedvehicles.vehicle_id
		AND predictions.trip_id = stoppedvehicles.trip_id WHERE vehicle_timestamp IS NOT NULL
	);

DROP TABLE IF EXISTS master;

CREATE TABLE master AS (
	SELECT combinedpredictions.stop_id
	,combinedpredictions.trip_id
	,combinedpredictions.route_name
	,prediction_datetime
	,predicted_departure
	,combinedpredictions.vehicle_id
	,vehicles.id
	,loc
	,vehicle_timestamp
	,actual_arrival_time FROM vehicles LEFT JOIN combinedpredictions
	ON vehicles.trip_id = combinedpredictions.trip_id
		AND vehicles.vehicle_id = combinedpredictions.vehicle_id WHERE (actual_arrival_time - vehicle_timestamp) > INTERVAL '0'
	);

ALTER TABLE master ADD COLUMN actual_tta INTERVAL;

ALTER TABLE master ADD COLUMN predicted_tta INTERVAL;

UPDATE master
SET actual_tta = (actual_arrival_time - vehicle_timestamp);

UPDATE master
SET predicted_tta = (predicted_departure - vehicle_timestamp)

SELECT AVG(predicted_tta - actual_tta) AS delta
	,EXTRACT(hour FROM vehicle_timestamp) AS hour
FROM master
GROUP BY hour;