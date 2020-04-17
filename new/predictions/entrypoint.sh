#!/bin/sh
python3 huey_consumer.py store_predictions.huey -k thread -w 4
