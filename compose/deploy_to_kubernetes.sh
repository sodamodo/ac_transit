!/usr/bin/env bash
gcloud auth login
gcloud config set project ac-transit-224721
gcloud config set compute/zone us-central1-a

gcloud container clusters get-credentials standard-cluster-1

kubectl apply -f ./deployment.yaml
