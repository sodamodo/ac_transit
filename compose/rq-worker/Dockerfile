# FROM ubuntu

# # RUN apt-get install python3
# # RUN apt-get install redis
# RUN apt-get update && apt-get -y install cron python3-pip redis

# RUN pip3 install --upgrade pip setuptools rq


# ADD ./rq-worker-entrypoint.sh /usr/bin/rq-worker-entrypoint.sh
# ADD ./submit_prediction_data.py ./submit_prediction_data.py
# ADD ./database.py ./database.py

# RUN chmod +x /usr/bin/rq-worker-entrypoint.sh
# ENTRYPOINT ["/usr/bin/rq-worker-entrypoint.sh"]


FROM alpine:3.4

RUN apk --no-cache add python3
RUN apk --no-cache add redis
RUN python3 -m ensurepip && pip3 install --upgrade pip setuptools rq

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install psycopg2-binary

ADD ./submit_prediction_data.py ./submit_prediction_data.py
ADD ./database.py ./database.py
ADD ./models.py ./models.py


ADD ./rq-worker-entrypoint.sh /usr/bin/rq-worker-entrypoint.sh
RUN chmod +x /usr/bin/rq-worker-entrypoint.sh
ENTRYPOINT ["/usr/bin/rq-worker-entrypoint.sh"]