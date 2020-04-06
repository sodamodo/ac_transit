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
    if prediction_data is not None:
        if type(prediction_data) == list:
            try:
                for prediction in prediction_data:
                    # # print("type of prediction list...", type(prediction))
                    predictions.append(Prediction(prediction))
            except Exeption as e:
                print(str(e))


    # bulk_template = "INSERT INTO predictions (stop_id, trip_id, vehicle_id, route_name, predicted_delay, predicted_departure, prediction_datetime ) VALUES"
    # print("OG bs len", len(bulk_template))

    # print("HOW MANYT PREDS???", len(predictions))
    for prediction in predictions:
        predicted_departure_dt = datetime.strptime(prediction.predicted_departure, "%Y-%m-%dT%H:%M:%S")
        prediction_datetime_dt = datetime.strptime(prediction.prediction_datetime, "%Y-%m-%dT%H:%M:%S")
        delta = predicted_departure_dt - prediction_datetime_dt
        # print("here is the time delta....  ", delta)
        if (delta.seconds > 600):
            # print("Delta too much..... ", delta.seconds > 600)
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
        # print(sql_string)
        cur.execute(sql_string)
        # # print("prediction inserted??")



    # row_string = "('{stop_id}', '{trip_id}', '{vehicle_id}', '{route_name}', '{predicted_delay}', '{predicted_departure}', '{prediction_datetime}'),".format(
    #                                                                                                                                                         stop_id=prediction.stop_id,
    #                                                                                                                                                         trip_id=prediction.trip_id,
    #                                                                                                                                                         vehicle_id=prediction.vehicle_id,
    #                                                                                                                                                         route_name=prediction.route_name,
    #                                                                                                                                                         predicted_delay=prediction.predicted_delay,
    #                                                                                                                                                         predicted_departure=prediction.predicted_departure,
    #                                                                                                                                                         prediction_datetime=prediction.prediction_datetime
    #                                                                                                                                                         )
    #
    #
    #
    #     # # print("bulk string..... ", bulk_template)
    #     # # print("row string..... ", row_string)
    #     # # print("SUPER COMBO,,,", bulk_template + row_string)
    #     bulk_template += row_string
    #     # print("combined???? ", bulk_template)
    # # print("did add?????", bulk_template)
    #
    # if len(bulk_template) > 140:
    #     # print("bulk string i. f not None...", bulk_template)
    #     # bulk_template = bulk_template[:-1]
    #     bulk_template = bulk_template.replace("),", ");")
    #     # print("bulk string after comma remova.... ",  bulk_template)
    #     # bulk_template = bulk_template + ';'
    #     # print("BULK STRING AFTER SHAVE AND ADD....  ", bulk_template)
    #
    #     cur.execute(bulk_template)
