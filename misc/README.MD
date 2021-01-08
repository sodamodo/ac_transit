
This project constantly collects data from the AC Transit API and stores it in
a PostGIS database. This is done using a python script deployed on a Kubernetes cluster. The script records both the positions of the bus fleet every 30 seconds
as well as takes samples of the predictions issued by the NextBus system.

I am currently working on a way to compare predicted and actual arrival times
in order to eventually improve the accuracy of the predictions.
