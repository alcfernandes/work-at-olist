# Work at Olist

# Description

A solution to the [problem](https://github.com/olist/work-at-olist/blob/master/README.md) proposed by [Olist](https://olist.com/).

This application implements an HTTP REST API that receives records of telephone calls and calculates monthly bills 
for a given subscriber.

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
