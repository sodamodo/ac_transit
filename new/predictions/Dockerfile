FROM ubuntu

RUN mkdir -p /app
RUN apt-get update && apt-get -y install cron python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . /app
WORKDIR /app
# RUN ["chmod", "+x", "entrypoint.sh"]
RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]


# Add crontab file in the cron directory
# ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/hello-cron

# Apply cron job
# RUN crontab /etc/cron.d/hello-cron

# Create the log file to be able to run tail
# RUN touch /var/log/cron.log

# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log



