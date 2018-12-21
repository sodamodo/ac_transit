#!/bin/sh
echo "I am worker"
/usr/bin/rq worker -u redis://:transit@redis-17312.c99.us-east-1-4.ec2.cloud.redislabs.com:17312
