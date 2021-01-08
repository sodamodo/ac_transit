#!/bin/bash
gcloud auth activate-service-account zacharybnoah@gmail.com --key-file 'ac-transit-229019-f32b66bc7da6.json' --project=ac-transit-229019
gsutil mb  gs://testb
gsutil ls 

#  pg_dump -h 35.239.236.79 -U postgres -W --table="master"  postgres > master.sql
