from database import get_cur
from models import Prediction



def process_prediction(prediction_data):

    cur = get_cur()
    predictions = []
    if prediction_data == None:
        pass
    else:
        if type(prediction_data == list):
            try:
                for prediction in prediction_data:
                    # print("type of prediction list...", type(prediction))
                    predictions.append(Prediction(prediction))
            except:
                pass
    for prediction in predictions:
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
        print(sql_string)
        cur.execute(sql_string)
