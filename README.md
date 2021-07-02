# ml-trips-microservice

## Objective
1) Web Service with 3 endpoints that provides basic analytics over Chicago Taxi Trips.
2) Production ready code for infrastructure deployment - deployability, maintainability, documentation, testing and easily extension

# Use
1) Interesting problem in transport, logistics, and
economics.
2) Leverage machine learning to build data products for ride-hailing, logistics, food
delivery, and payments.

**Input** -
1) Dataset can be obtained from https://drive.google.com/file/d/1ExhbFVz5Qb57VvobiEUPB6q0onLVmJEF/view?usp=sharing [contact me here - ayushaggar@gmail.com for data access]
2) The dataset includes taxi trips in Chicago for the year 2020.
3) There are 3,888,425 rows in the dataset

## Output
1) MongoDB server for storing and retrieving data
2) Docker for hosting MongoDB, Flask and Nginx Server
3) Flask - API for endpoints

## End Points
1) Total number of trips per day in the date range, based on the pickup time of the trip.
http://0.0.0.0/total_trips?start=2020-02-01&end=2020-02-02

2) The average fare per pick up location S2 ID at level 16 for the given date, based on the pickup
time of the trip.
http://0.0.0.0/average_fare_heatmap?date=2020-02-02

3) Average speed of trips that ended in the past 24 hours from the provided date.
Speed (km/h) = trip_distance/trip_hour
trip_distance(in km) = trip_miles*1.60934
trip_hour(in h) = trip_seconds/3600
http://0.0.0.0/average_speed_24hrs?date=2020-02-03

**Constraints / Notes** ::
1) All dates should be in ISO 8601 YYYY-MM-DD format and date ranges are inclusive on
both ends. Timezone is local to the dataset.
2) Provides up to 2 decimal places if the value returned by the API is decimal.
3) Response headers, handling - error, missing data, bad data, or other edge cases.

**Handle Cases**
1) When fare is missing then we have to remove that trip for calculating average speed
2) When trip_seconds is missing then we have to remove that trip for calculating average speed
3) When lat or long is missing then we have to remove that trip as we do not know S2 ID
3) Handled error responses

**Note**: Python code is pep8 compliant

## Tools use 
> Python 3 - Language

> MongoDB - DB

> Nginx - Server

> Docker - Launch application with dependencies

> Main Libraries Used -
1) flask - For Routing and Controllers
2) gunicorn - For server gateway
3) s2cell - For Getting S2 ID
4) unittest2 - For Unit Test
5) pandas - For Transformation
6) PyMongo - For DB Access
7) coverage - For Unit Test coverage report
8) gdown - For Downloading data from google drive
9) pyarrow - For reading parquet data

## Installing and Running

> Folders Used -
```sh
$ cd ml-trips-microservice
``` 

For Building and Running Docker Server:
```sh
$ docker-compose up --build -d
``` 

Use http://0.0.0.0/status for checking health status of API

For ETL Process:
```sh
$ pip install -r requirements.txt
$ python etl.py
``` 

## Steps for Ingesting data in mongodb (ETL Process)-
1) Downloading of parquet data from Google Drive link using gdown
2) Reading of parquet data
3) Dividing data in chunks and inserted in monngodb in sequence manner
4) Indexing in db for fast reterival - Indexing done after ETL so as to do fast bulk writing first as insert take time after indexing

## Improvement can be done by following things
1) More unit and functional test
2) More error monitoring and different api response depending on it
3) More logging for easy debugging
4) Using cloud native db like big query
5) Ingestion of data through Kafka streams
6) Integration of redis for cache response

## Creating git bundle
git bundle create ml_trips_microservice.bundle HEAD main

git clone ml_trips_microservice.bundle ml_trips_microservice