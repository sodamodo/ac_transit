gcloud auth login
gcloud config set project sustained-fx-221520
gcloud config set compute/zone us-central1-a
# sudo gcloud container clusters create collector-clust --num-nodes=3


# docker build --tag gcr.io/sustained-fx-221520/locations:v3 compose/locations/
# docker tag gcr.io/sustained-fx-221520/locations:v3 gcr.io/sustained-fx-221520/locations:latest
# gcloud docker -- push gcr.io/sustained-fx-221520/locations:v3

docker build --tag gcr.io/sustained-fx-221520/predictions:v8 compose/predictions/
docker tag gcr.io/sustained-fx-221520/predictions:v8 gcr.io/sustained-fx-221520/predictions:latest
gcloud docker -- push gcr.io/sustained-fx-221520/predictions:v8


# docker build --tag gcr.io/sustained-fx-221520/rq-worker:v3 compose/rq-worker/
# docker tag gcr.io/sustained-fx-221520/rq-worker:v3 gcr.io/sustained-fx-221520/rq-worker:latest
# gcloud docker -- push gcr.io/sustained-fx-221520/rq-worker:v3



# docker build --tag gcr.io/sustained-fx-221520/postgis:v1 git://github.com/kartoza/docker-postgis
# docker tag gcr.io/sustained-fx-221520/postgis:v1 gcr.io/ac-transit-46ac1/postgis:latest

# kubectl run locations --image=gcr.io/sustained-fx-221520/locations:latest
# kubectl run predictions --image=gcr.io/sustained-fx-221520/predictions:latest
# kubectl run predictions --image=gcr.io/sustained-fx-221520/rq-server:latest
# kubectl run predictions --image=gcr.io/sustained-fx-221520/rq-worker:latest


# kubectl create -f ./postgis_pv.yaml
# kubectl create -f ./postgis_pvc.yaml
