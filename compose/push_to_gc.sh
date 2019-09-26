!/usr/bin/env bash

# Use this to get kubectl to work for deployments
# gcloud container clusters get-credentials standard-cluster-1 --zone us-central1-a --project luckydogagilityg

gcloud auth login
gcloud config set project luckydogagilityg
gcloud config set compute/zone us-central1-a

# docker build --tag gcr.io/luckydogagilityg/locations:v2 locations/.
# docker tag gcr.io/luckydogagilityg/locations:v2 gcr.io/luckydogagilityg/locations:v2
# gcloud docker -- push gcr.io/luckydogagilityg/locations:v2

docker build --tag gcr.io/luckydogagilityg/predictions:v1 predictions/.
docker tag gcr.io/luckydogagilityg/predictions:v1 gcr.io/luckydogagilityg/predictions:v1
gcloud docker -- push gcr.io/luckydogagilityg/predictions:v1
#
docker build --tag gcr.io/luckydogagilityg/rq-server:v1 rq-server/.
docker tag gcr.io/luckydogagilityg/rq-server:v1 gcr.io/luckydogagilityg/rq-server:v1
gcloud docker -- push gcr.io/luckydogagilityg/rq-server:v1

docker build --tag gcr.io/luckydogagilityg/rq-worker:v1 rq-worker/.
docker tag gcr.io/luckydogagilityg/rq-worker:v1 gcr.io/luckydogagilityg/rq-worker:v3
gcloud docker -- push gcr.io/luckydogagilityg/rq-worker:v1
