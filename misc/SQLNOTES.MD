72R test stop -- 50888

72 testtop -- 3079	

SELECT * FROM predictions WHERE stop_id = 50888;

SELECT stoppedvehicles.id, stoppedvehicles.trip_id, stoppedvehicles.stop_id, stoppedvehicles.vehicle_id, stoppedvehicles.time FROM sanpablorapidstops INNER JOIN stoppedvehicles ON (sanpablorapidstops.stop_id:: VARCHAR = stoppedvehicles.stop_id);


#### vehiclewithprediction