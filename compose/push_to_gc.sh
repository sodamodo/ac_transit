!/usr/bin/env bash
gcloud auth login
gcloud config set project ac-transit-224721
gcloud config set compute/zone us-central1

# docker build --tag gcr.io/ac-transit-224721/locations:v1 locations/.
# docker tag gcr.io/ac-transit-224721/locations:v1 gcr.io/ac-transit-224721/locations:v1
# gcloud docker -- push gcr.io/ac-transit-224721/locations:v1

docker build --tag gcr.io/ac-transit-224721/predictions:v2 predictions/.
docker tag gcr.io/ac-transit-224721/predictions:v2 gcr.io/ac-transit-224721/predictions:v2
gcloud docker -- push gcr.io/ac-transit-224721/predictions:v2

# docker build --tag gcr.io/ac-transit-224721/rq-server:v1 rq-server/.
# docker tag gcr.io/ac-transit-224721/rq-server:v1 gcr.io/ac-transit-224721/rq-server:v1
# gcloud docker -- push gcr.io/ac-transit-224721/rq-server:v1

# docker build --tag gcr.io/ac-transit-224721/rq-worker:v1 rq-worker/.
# docker tag gcr.io/ac-transit-224721/rq-worker:v1 gcr.io/ac-transit-224721/rq-worker:v1
# gcloud docker -- push gcr.io/ac-transit-224721/rq-worker:v1