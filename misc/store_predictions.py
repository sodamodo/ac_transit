from database import get_cur
import requests
import random
from time import sleep
import csv
from models import Stop, Prediction
from ast import literal_eval
from time import sleep
from redis import Redis
from rq import Queue
import threading
from submit_prediction_data import process_prediction



def increment_token():
    if token_index > 19:
        token_index = 0
    token = token_list[token_index]
    token_index += 1


def get_prediction_data(stop_id):
    r = requests.get(base_url.format(stop_id))
    prediction_list = []
    predictions = r.content

    if r.status_code == '404' or r.content == b'':
        return None
    else:

        predictions = predictions.decode("utf-8")
        predictions = literal_eval(predictions)
        for prediction in predictions:
            if type(prediction) != dict:
                continue
            else:
                prediction_list.append(list(prediction.values()))
        return prediction_list


#This is confusing with get_stops_on_route, need to rename to be less confusing
def get_stops_for_route(cur, stops, route):
    stops_on_route = []
    for stop in stops:
        for stop_route in stop.json_routes:
            if stop_route == route:
                stops_on_route.append(stop)
    return stops_on_route



def loop():
    stop_index = 0
    while (truth):
        try:
            predictions = []
            stop_list = stops
            for stop in stop_list:
                prediction_data = get_prediction_data(stop.stop_id)
                q.enqueue(process_prediction, prediction_data)
                # process_prediction(prediction_data)
                t = threading.Thread(target=process_prediction, args=(prediction_data,))
                t.start()
                stop_index += 1
                if (stop_index % 250 == 0):
                    if token_index > 19:
                        token_index = 0
                    token = token_list[token_index]
                    token_index += 1
                if (stop_index == 5291):
                    stop_index = 0
                # print(stop.stop_id)
            print("cycled!")
        except:
            # sleep(.5)
            loop()

if __name__ == '__main__':

    # q = Queue(connection=Redis(host="redis-17312.c99.us-east-1-4.ec2.cloud.redislabs.com", port=17312, password="transit"))
    # q.empty()
    token_list = [
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

    token = '9A9392AEE88125369B928F281DBD341B'
    token_index = 0
    base_url = "https://api.actransit.org/transit/stops/{}/predictions/?token=" + token
    cur = get_cur()

    truth = True
    stops = []
    stops_file = open("stops.csv", "r")
    stops_table = csv.reader(stops_file, delimiter=',')
    for stops_row in stops_table:
        stop = Stop(stops_row)
        stops.append(stop)

    print("out of the loop")

    loop()
