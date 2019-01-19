!/usr/bin/env bash

# Use this to get kubectl to work for deployments
# gcloud container clusters get-credentials standard-cluster-1 --zone us-central1-a --project ac-transit-229019

gcloud auth login
gcloud config set project ac-transit-229019
gcloud config set compute/zone us-central1-a

docker build --tag gcr.io/ac-transit-229019/locations:v2 locations/.
docker tag gcr.io/ac-transit-229019/locations:v2 gcr.io/ac-transit-229019/locations:v2
gcloud docker -- push gcr.io/ac-transit-229019/locations:v2

docker build --tag gcr.io/ac-transit-229019/predictions:v10 predictions/.
docker tag gcr.io/ac-transit-229019/predictions:v10 gcr.io/ac-transit-229019/predictions:v10
gcloud docker -- push gcr.io/ac-transit-229019/predictions:v10

docker build --tag gcr.io/ac-transit-229019/rq-server:v1 rq-server/.
docker tag gcr.io/ac-transit-229019/rq-server:v1 gcr.io/ac-transit-229019/rq-server:v1
gcloud docker -- push gcr.io/ac-transit-229019/rq-server:v1

docker build --tag gcr.io/ac-transit-229019/rq-worker:v3 rq-worker/.
docker tag gcr.io/ac-transit-229019/rq-worker:v3 gcr.io/ac-transit-229019/rq-worker:v3
gcloud docker -- push gcr.io/ac-transit-229019/rq-worker:v3
