from database import get_cur
from models import Prediction

import logging


def process_prediction(prediction_data):
    logging.warning("===========PROCESS PRED METHOD CALLED=============")
    cur = get_cur()
    predictions = []
    if prediction_data == None:
        logging.warning("===========PREDICTION DATA IS NONE=============")
        pass
    else:
        if type(prediction_data == list):
            try:
                for prediction in prediction_data:
                    # print("type of prediction list...", type(prediction))
                    logging.warning("===========ADDING TO PREDICTION LIST THE FOLLOWING=============")
                    logging.warning(prediction)
                    predictions.append(Prediction(prediction))
            except:
                pass
    logging.warning("===========TIME TO MAKE SOME SQLLLLS=============")
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
        logging.warning("=========SEEE SQL STRING===========")
        logging.warning(sql_string)
        cur.execute(sql_string)
