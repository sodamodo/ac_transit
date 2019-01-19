#!/bin/sh
echo "I am worker"
/usr/bin/rq worker -u redis://redis:6379
