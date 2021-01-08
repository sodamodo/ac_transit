from database import engine, Predictions as sql_Predictions
from sqlalchemy.orm import sessionmaker
import requests
import random
from time import sleep
import csv
from models import Stop, Prediction
from ast import literal_eval
from time import sleep
# from redis import Redis
# from rq import Queue
from submit_prediction_data import process_prediction
import logging
import random
import json
from datetime import datetime

# from huey import RedisHuey
# huey = RedisHuey('predictor', host='redis')

class Predictor:
    def __init__(self):
        self.token_list = [
        '9A9392AEE88125369B928F281DBD341B',
        '59D69D98A213F47907DCC4666C429F97',
        '4D8D94A3FF690D5DF8A99632D14DF06C',
        '1E2B2B65A3BB9B09E6581DB918E59552',
        '7C8EB1A0359B4FCB17645149332000EA',
        'E73043FEBE5FE52ECE7E35E4AD29C1F0',
        'C1C124A2128F34A92DE7BA44E1723ADC',
        '1FBF820DDA7B36BC245B4662C8652142',
        '6EDE923273A789628CC571F8381228C1',
        'FEA38127BA898B57C50E44BA8CC4ED5B',
        'BB23E1BB9E6A1FFA9FC90DBF1667CA0E',
        'CEF6C4904CAB78D632C2ED96AD835A4D',
        '846CEAE09EF0ED844DA114929C3B06F0',
        'DECCCBDEAABEC6E7F5462628664D43BC',
        'A11EB2F3B50E1BAC9781B64E3AB703DF',
        '234E960C8F3367C64DF67A8CCB3538A7',
        '337EAEE9402F615021C2F41CE6808EA1',
        'FD87E46473298FCB4245BA8F0A1D5136',
        '4F15092F9CB725502FB1506DD630B805',
        '0031A200345291CBACC08DDAEC4D6A00'

        ]
        self.stop_index = 0
        self.token_index = 0
        self.url = "https://api.actransit.org/transit/stops/{}/predictions/?token=" + self.token_list[self.token_index]


    # @huey.task()
    def process_prediction(self, prediction_data):

        session = Session()

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
                logging.warning("=====BAD TIMING DATA=====")
                continue

        
        logging.warning("===Made it to has predictions====")
        logging.warning("===I has this many predictions====")
        logging.warning(len(predictions))
        sql_predictions = []

        for prediction in predictions:
            sql_predictions.append(
                sql_Predictions(
                    stop_id=prediction.stop_id,
                    trip_id=prediction.trip_id,
                    vehicle_id=prediction.vehicle_id,
                    route_name=prediction.route_name,
                    predicted_delay=prediction.route_name,
                    predicted_departure=prediction.predicted_departure,
                    prediction_datetime=prediction.prediction_datetime

                )
            )
        
        session.add_all(sql_predictions)
        session.commit()
        
    def get_prediction_data(self, stop_id):
        r = requests.get(self.url.format(stop_id))
        prediction_list = []
        predictions = r.content

        if r.status_code == '404' or r.content == b'':
            return None
        else:

            predictions = predictions.decode("utf-8")
            predictions = json.loads(predictions)
            for prediction in predictions:
                if type(prediction) != dict:
                    continue
                else:
                    prediction_list.append(list(prediction.values()))

            return prediction_list



    def read_stops_from_csv(self):
        stops = []
        stops_file = open("stops.csv", "r")
        stops_table = csv.reader(stops_file, delimiter=',')
        for stops_row in stops_table:
            stop = Stop(stops_row)
            stops.append(stop)
        return stops 

    def cycle_token_and_stop_index(self):
        token = None
        if (self.stop_index % 250 == 0):
            if self.token_index > 19:
                self.token_index = 0

            token = self.token_list[self.token_index]
            self.token_index += 1
            
        if (self.stop_index == 5291):
            self.stop_index = 0

        return token


if __name__ == '__main__':

    


    logging.warning("sleeeeping")
    sleep(5)
    predictor = Predictor()
    
    Session = sessionmaker()
    Session.configure(bind=engine)


    while (True):
        try:
            # logging.warning("Made it to try block of loops WUMPPPPX")
            predictions = []

            stops = predictor.read_stops_from_csv()



            stop_list = stops
            stop = random.choice(stop_list)

            
            prediction_data = predictor.get_prediction_data(stop_id=stop.stop_id)
            # prediction_data = predictor.get_prediction_data(stop_id=55811)

            # logging.warning("process to be enqueued")
            
            # logging.warning("======PROCESS PREDICTION======")
            # logging.warning("======PRE DATA LENGTH======")
            # logging.warning(len(prediction_data))

            # logging.warning("======DATA TO BE PROCESSED======")
            # logging.warning(prediction_data)

            if len(prediction_data) > 0:
                predictor.process_prediction(prediction_data[:10])


            # q.enqueue(process_prediction, prediction_data)
            # logging.warning("============LENGTH OF QUEUE====")

            # logging.warning("=====RIGHT BEFORE STOP INDEX......now show it!======")
            # logging.warning(predictor.stop_index)
            predictor.stop_index += 1
            
            token = predictor.cycle_token_and_stop_index()
            
        except Exception as e:
            sleep(1)
            logging.warning("I threw an exception in the loop!")
            logging.warning(str(e))

