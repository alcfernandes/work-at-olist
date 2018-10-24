# Work at Olist

# Description

A solution to the [problem](https://github.com/olist/work-at-olist/blob/master/README.md) proposed by [Olist](https://olist.com/).

This application implements an HTTP REST API that receives records of telephone calls and calculates monthly bills 
for a given subscriber.

Working environment: [Api Root](https://olist-calls-pro.herokuapp.com/api/). [Api Admin](https://olist-calls-pro.herokuapp.com/admin/). (*login: olist, password: olist2018*)


## Installing and testing instructions
1. Clone the repository;  
2. Create a virtual environment;
3. Activate the virtual environment;
4. Install the dependencies;
5. Configure the instance with .env;
6. Run data migration;
7. Run the tests;
8. Create super user;
9. Load default pricing rules;
9. Run Django Server.

```console
git clone https://github.com/alcfernandes/work-at-olist.git work-at-olist
cd work-at-olist/
python -m venv .venv
source .venv/bin/activate
pip install -r requerements-dev.txt
cp contrib/env-sample .env
python manage.py migrate
python manage.py test
python manage.py createsuperuser
python manage.py loaddata contrib/pricingrule.json
python manage.py runserver
```

## Work Environment (Brief Description)

|   |    |
|---|---|
|  Computer |   MacBook Air - 1.7GHz Intel Core i7 - 8GB memory |
|  Operating System | macOS High Sierra (10.13.6)  |
|  IDE | PyCharm 2018.2.4 (Professional Edition)   |
|  Python | 3.7.0  |
|  Main Libraries| Django 2.1.2 /  Django Rest Framework 3.8.2 |


## API Documentation

### Call Detail Record

#### List Call Detail records

```console
(GET) https://olist-calls-pro.herokuapp.com/api/call-detail/
```
cURL:

````console
curl -X GET \
  https://olist-calls-pro.herokuapp.com/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
````
Result:

````console
(200 OK)
[
    {
        "url": "https://olist-calls-pro.herokuapp.com/api/call-detail/1/",
        "id": 1,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "99988526423",
        "destination": "9933468278",
        "call_id": 70
    },
    {
        "url": "https://olist-calls-pro.herokuapp.com/api/call-detail/2/",
        "id": 2,
        "type": "end",
        "timestamp": "2016-02-29T14:00:00Z",
        "source": null,
        "destination": null,
        "call_id": 70
    }
]
````


#### Create Start Call Detail Record
```console
(POST) https://olist-calls-pro.herokuapp.com/api/call-detail/
```
cURL:
````console
curl -X POST \
  https://olist-calls-pro.herokuapp.com/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2016-02-29T12:00:00Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 70    
}'
````
Result:

````console
(201 Created)
{
    "url": "https://olist-calls-prod.herokuapp.com/api/call-detail/17/",
    "id": 17,
    "type": "start",
    "timestamp": "2016-02-29T12:00:00Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 70
}

````

#### Create End Call Detail Record
```console
(POST) https://olist-calls-pro.herokuapp.com/api/call-detail/
```
cURL:
````console
curl -X POST \
  https://olist-calls-pro.herokuapp.com/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "end",
    "timestamp": "2016-02-29T14:00:00Z",
    "call_id": 70    
}'
````
Result:

````console
(201 Created)
{
    "url": "https://olist-calls-pro.herokuapp.com/api/call-detail/18/",
    "id": 18,
    "type": "end",
    "timestamp": "2016-02-29T14:00:00Z",
    "source": null,
    "destination": null,
    "call_id": 70
}

````

#### List Call Detail records

```console
(GET) https://olist-calls-pro.herokuapp.com/api/call-detail/
```
cURL:

````console
curl -X GET \
  https://olist-calls-pro.herokuapp.com/api/call-detail/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
````
Result:

````console
(200 OK)
[
    {
        "url": "https://olist-calls-pro.herokuapp.com/api/call-detail/1/",
        "id": 1,
        "type": "start",
        "timestamp": "2016-02-29T12:00:00Z",
        "source": "99988526423",
        "destination": "9933468278",
        "call_id": 70
    },
    {
        "url": "https://olist-calls-pro.herokuapp.com/api/call-detail/2/",
        "id": 2,
        "type": "end",
        "timestamp": "2016-02-29T14:00:00Z",
        "source": null,
        "destination": null,
        "call_id": 70
    }
]

````

#### Retrieve a  Call Detail records

```console
(GET) https://olist-calls-pro.herokuapp.com/api/call-detail/1/
```
cURL:

````console
curl -X GET \
  https://olist-calls-pro.herokuapp.com/api/call-detail/1/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
````
Result:

````console
(200 OK)
{
    "url": "https://olist-calls-pro.herokuapp.com/api/call-detail/1/",
    "id": 1,
    "type": "start",
    "timestamp": "2016-02-29T12:00:00Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 70
}
````

#### Update a Call Detail Record

```console
(PUT) https://olist-calls-pro.herokuapp.com/api/call-detail/1/
```
cURL:

````console
curl -X PUT \
  https://olist-calls-pro.herokuapp.com/api/call-detail/1/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "type": "start",
    "timestamp": "2016-02-29T10:00:00Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 70    
}'
````
Result:

````console
(200 OK)
{
    "url": "https://olist-calls-pro.herokuapp.com/api/call-detail/1/",
    "id": 1,
    "type": "start",
    "timestamp": "2016-02-29T10:00:00Z",
    "source": "99988526423",
    "destination": "9933468278",
    "call_id": 70
}

````

#### Delete a Call Detail Record
```console
(DEL) https://olist-calls-pro.herokuapp.com/api/call-detail/1/
```
cURL:

````console
curl -X DELETE \
  https://olist-calls-pro.herokuapp.com/api/call-detail/1/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
````
Result:

````console
(204 No Content)
````

### Call

#### List Call records

```console
(GET) https://olist-calls-pro.herokuapp.com/api/call/
```
cURL:

````console
curl -X GET \
  https://olist-calls-pro.herokuapp.com/api/call/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
````
Result:

````console
(200 OK)
[
    {
        "url": "https://olist-calls-pro.herokuapp.com/api/call/70/",
        "id": 70,
        "detail_start": "https://olist-calls-pro.herokuapp.com/api/call-detail/1/",
        "detail_end": "https://olist-calls-pro.herokuapp.com/api/call-detail/2/",
        "duration": "2h0m0s",
        "price": "11.16"
    }
]
````

#### Retrieve a Call record

```console
(GET) https://olist-calls-pro.herokuapp.com/api/call/70/
```
cURL:

````console
curl -X GET \
  https://olist-calls-pro.herokuapp.com/api/call/70/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
````
Result:

````console
(200 OK)
{
    "url": "https://olist-calls-pro.herokuapp.com/api/call/70/",
    "id": 70,
    "detail_start": "https://olist-calls-pro.herokuapp.com/api/call-detail/1/",
    "detail_end": "https://olist-calls-pro.herokuapp.com/api/call-detail/2/",
    "duration": "2h0m0s",
    "price": "11.16"
}
````

### Bill

#### Get a Subscriber Bill

```console
(GET) https://olist-calls-pro.herokuapp.com/api/bill/?subscriber=99988526423&period=02/2016
```
cURL:

````console
curl -X GET \
  'https://olist-calls-pro.herokuapp.com/api/bill/?subscriber=99988526423&period=02/2016' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
````
Result:

````console
(200 OK)
[
    {
        "destination": "9933468278",
        "start_date": "2016-02-29",
        "start_time": "12:00:00",
        "duration": "2h0m0s",
        "price": "11.16"
    },
    {
        "destination": "9933468278",
        "start_date": "2016-02-29",
        "start_time": "12:00:00",
        "duration": "2h0m0s",
        "price": "11.16"
    }
]
````

### Pricing Rules

The price rule table can be changed by Django Admin.

```console
https://olist-calls-pro.herokuapp.com/admin/
```

|   |    |
|---|---|
|  Login |   olist |
|  Password | olist2018 |


