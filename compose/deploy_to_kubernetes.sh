!/usr/bin/env bash
gcloud auth login
gcloud config set project luckydogagilityg
gcloud config set compute/zone us-central1-a

gcloud container clusters get-credentials standard-cluster-2



kubectl apply -f ./redis-deployment.yaml
kubectl apply -f ./redis-service.yaml
#
# kubectl apply -f ./rq-server-deployment.yaml
# kubectl apply -f ./rq-server-service.yaml
#
# kubectl apply -f ./rq-worker-deployment.yaml
# kubectl apply -f ./rq-worker-service.yaml
#
#
#
# kubectl apply -f ./deployment.yaml
