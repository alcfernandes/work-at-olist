#!/usr/bin/env bash
# Call: 70 ##########################################

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2016-02-29T12:00:00Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 70
}'

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2016-02-29T14:00:00Z",
    "call_id": 70
}'

# Call: 71 ##########################################

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2017-12-11T15:07:13Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 71
}'

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2017-12-11T15:14:56Z",
    "call_id": 71
}'

# Call: 72 ##########################################

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2017-12-12T22:47:56Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 72
}'

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2017-12-12T22:50:56Z",
    "call_id": 72
}'

# Call: 73 ##########################################

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2017-12-12T21:57:13Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 73
}'

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2017-12-12T22:10:56Z",
    "call_id": 73
}'

# Call: 74 ##########################################

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2017-12-12T04:57:13Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 74
}'

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2017-12-12T06:10:56Z",
    "call_id": 74
}'

# Call: 75 ##########################################

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2017-12-13T21:57:13Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 75
}'

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2017-12-14T22:10:56Z",
    "call_id": 75
}'

# Call: 76 ##########################################

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2017-12-12T15:07:58Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 76
}'

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2017-12-12T15:12:56Z",
    "call_id": 76
}'

# Call: 77 ##########################################

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2018-02-28T21:57:13Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 77
}'

curl -X POST \
  http://127.0.0.1:8000/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2018-03-01T22:10:56Z",
    "call_id": 77
}'