from database import get_cur
from models import Prediction
from datetime import datetime
import pytz
import logging



def convert_to_utc(time_string):
    local = pytz.timezone ("America/Los_Angeles")
    naive = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt
def process_prediction(prediction_data):

    logging.warning("=======ARE YOU EVEN WORKING??=====")
    cur = get_cur()
    predictions = []
    if prediction_data == None:
        pass
    else:
        if type(prediction_data == list):
            try:
                for prediction in prediction_data:
                    # # print("type of prediction list...", type(prediction))
                    predictions.append(Prediction(prediction))
            except:
                pass



    for prediction in predictions:
        predicted_departure_dt = datetime.strptime(prediction.predicted_departure, "%Y-%m-%dT%H:%M:%S")
        prediction_datetime_dt = datetime.strptime(prediction.prediction_datetime, "%Y-%m-%dT%H:%M:%S")
        delta = predicted_departure_dt - prediction_datetime_dt
        if (delta.seconds > 600):
            continue



        sql_string=  """
        INSERT INTO predictions VALUES ('{stop_id}', '{trip_id}', '{vehicle_id}', '{route_name}', '{predicted_delay}',
                                        '{predicted_departure}', '{prediction_datetime}');
        """.format(
            stop_id=prediction.stop_id,
            trip_id=prediction.trip_id,
            vehicle_id=prediction.vehicle_id,
            route_name=prediction.route_name,
            predicted_delay=prediction.predicted_delay,
            predicted_departure=prediction.predicted_departure,
            prediction_datetime=prediction.prediction_datetime
        )
        cur.execute(sql_string)


