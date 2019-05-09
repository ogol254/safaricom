# safaricom


## Introduction

[![Build Status](https://travis-ci.org/ogol254/safaricom.svg?branch=master)](https://travis-ci.org/ogol254/safaricom)

[![codecov](https://codecov.io/gh/ogol254/safaricom/branch/master/graph/badge.svg)](https://codecov.io/gh/ogol254/safaricom)



### Features

1. Users can create an account and log in and log out.
2. Users can post a movie.
3. Users can get all movies.
4. Users can get a movie
5. Users can delete a movie
6. Users can edit a movie


### Installing

*Step 1*

Create directory
```$ mkdir stackoverflow```

```$ cd stackoverflow```

Create and activate virtual environment

```$ virtualenv env```


```$ source env/bin/activate```

Clone the repository [```here```](https://github.com/ogol254/safaricom) or 

``` git clone https://github.com/ogol254/safaricom ```

Install project dependencies 


```$ pip install -r requirements.txt```


*Step 2* 

#### Set up database and virtual environment & Database 

Go to postgres terminal and create the following databases

Main database 


``` # CREATE DATABASE database_name ; ```

Test database 


``` # CREATE DATABASE test_database_name ; ```

*Step 3*

#### Storing environment variables 

```
export FLASK_APP="run.py"
export APP_SETTINGS="development"
export DATABASE_URL="dbname='database_name' host='localhost' port='5432' user='postgres' password='root'"
export DATABASE_TEST_URL="dbname='test_database_name' host='localhost' port='5432' user='postgress' password='root'"
```

*Step 4*

#### Running the application

```$ python run.py```

*Step 5*

#### Testing

```$ nosetests app/tests```

### API-Endpoints

#### Users Endpoints : /api/v1/

Method | Endpoint | Functionality
--- | --- | ---
POST | /auth/signup | Create a user account
POST | /auth/login | Sign in a user
POST | /auth/logout | Sign out a user
POST | /auth/validate | validate user

#### Movies Endpoints : /api/v1/movies

Method | Endpoint | Functionality
--- | --- | ---
POST | / | Post a movies
GET | / | Post all movies
GET | /str:flag | Get all movies with similar flag
GET | /int:movie_id | Get a single movie
PUT | /int:movie_id | Edit a single movie
DELETE | /int:movie_id | Delete a single movie
GET | /int:movie_id/watch | watch a movie
POST | /int:movie_id/comment | Add a comment to a movie
PUT | /int:movie_id/comment/int:comment_id | Edit a comment to a movie
