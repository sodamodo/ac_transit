from ast import literal_eval

class Vehicle:
    def __init__(self, vehicle_array):
        self.id = vehicle_array[0]
        self.trip_id = vehicle_array[1]
        self.start_time = vehicle_array[2]
        self.start_date = vehicle_array[3]
        self.route_id = vehicle_array[4]
        self.loc = vehicle_array[5]
        self.bearing = vehicle_array[6]
        self.speed = vehicle_array[7]
        self.vehicle_id = vehicle_array[8]
        self.timestamp =vehicle_array[9]


class Stop:
    def __init__(self, stop_array):
        self.id = stop_array[0]
        self.geom = stop_array[1]
        self.stp_identi = stop_array[2]
        self.stop_id = stop_array[3]
        self.stp_descri = stop_array[4]
        self.route = stop_array[5]
        self.json_routes = literal_eval(stop_array[6])

class Prediction:
    def __init__(self, prediction_array):
        self.stop_id = prediction_array[0]
        self.trip_id = prediction_array[1]
        self.vehicle_id = prediction_array[2]
        self.route_name = prediction_array[3]
        self.predicted_delay = prediction_array[4]
        self.predicted_departure = prediction_array[5]
        self.prediction_datetime = prediction_array[6]