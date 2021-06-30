from flask import request, jsonify
from src.database import mongo
from datetime import datetime, timedelta
import logging
import s2cell
import pandas as pd
from bson import json_util
import json

# calculation of s2id


def gets2id(lat, long):
    try:
        s2id = s2cell.lat_lon_to_cell_id(lat, long, 16)
    except Exception as e:
        s2id = -1
    return s2id

# calculation of speed


def getSpeed(trip_miles, trip_seconds):
    try:
        speed = (trip_miles * 1.60934) / (trip_seconds / 3600)
    except Exception as e:
        speed = -1
    return speed

# Trip Controller class with different route functions


class TripController:

    @staticmethod
    def status():
        response = jsonify({
            'message': 'ok healthy'})  # health check
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @staticmethod
    def total_trips():
        try:
            # using lt and not lte as here both date should be inclusive
            # for example 2020-02-01 00:00:00 to 2020-02-02 23:59:59 for
            # start=2020-02-01&end=2020-02-02
            myquery = {"trip_start_timestamp": {
                "$gte": datetime.strptime(request.args.get("start"), '%Y-%m-%d'),
                "$lt": datetime.strptime(request.args.get("end"), '%Y-%m-%d') + timedelta(days=1)
            }}
            # mongodb query result saved in dataframe
            df = pd.DataFrame(list(mongo.db.trips.find(myquery)))

            # convert date to string
            df['date'] = (df['trip_start_timestamp'].dt.date).astype(str)

            # group by date and count trips
            df = df.groupby(['date']).size().reset_index(name='total_trips')

            # transforming into required response formats
            d = {}
            d["data"] = df.to_dict('records')
            result = json.loads(
                json_util.dumps(
                    d, json_options=json_util.RELAXED_JSON_OPTIONS))
            response = jsonify(result)
        except Exception as e:
            logging.warning(e)  # logging error
            result = json.loads(json_util.dumps({
                'message': 'unsuccessful'}, json_options=json_util.RELAXED_JSON_OPTIONS))
            response = jsonify(result)

        # putting header response
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @staticmethod
    def average_fare_heatmap():
        try:
            # using lt and not lte as here date should be inclusive
            # for example 2020-02-01 00:00:00 to 2020-02-01 23:59:59 for
            # date=2020-02-01
            myquery = {"trip_start_timestamp": {
                "$gte": datetime.strptime(request.args.get("date"), '%Y-%m-%d'),
                "$lt": datetime.strptime(request.args.get("date"), '%Y-%m-%d') + timedelta(days=1)
            }}

            # mongodb query result saved in dataframe
            df = pd.DataFrame(list(mongo.db.trips.find(myquery)))

            # calculating s2id
            df['s2id'] = df.apply(
                lambda r: gets2id(
                    r['pickup_latitude'],
                    r['pickup_longitude']),
                axis=1)

            # removing trips for which not able to find s2id it will be when
            # lat and long is None
            df = df.loc[df['s2id'] != -1]

            # group by s2id and mean fare
            df = df.groupby(['s2id'])['fare'].mean().reset_index()
            df['fare'] = df['fare'].round(2)

            # transforming into required response formats
            d = {}
            d["data"] = df.to_dict('records')
            result = json.loads(
                json_util.dumps(
                    d, json_options=json_util.RELAXED_JSON_OPTIONS))
            response = jsonify(result)
        except Exception as e:
            logging.warning(e)  # logging error
            result = json.loads(json_util.dumps({
                'message': 'unsuccessful'}, json_options=json_util.RELAXED_JSON_OPTIONS))
            response = jsonify(result)

        # putting header response
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @staticmethod
    def average_speed_24hrs():
        try:
            # using gt and not gte as here data should be 24hrs back
            # for example 2020-02-01 00:00:01 to 2020-02-02 00:00:00 for
            # date=2020-02-02
            myquery = {"trip_end_timestamp": {
                "$gt": datetime.strptime(request.args.get("date"), '%Y-%m-%d') - timedelta(days=1),
                "$lte": datetime.strptime(request.args.get("date"), '%Y-%m-%d')
            }}

            # mongodb query result saved in dataframe
            df = pd.DataFrame(list(mongo.db.trips.find(myquery)))

            # calculating speed
            df['speed'] = df.apply(
                lambda r: getSpeed(
                    r['trip_miles'],
                    r['trip_seconds']),
                axis=1)

            # removing trips for which not able to find speed it will be when
            # miles or seconds are None
            df = df.loc[df['speed'] != -1]
            d = {}
            # mean speed by 2 decimal
            d["data"] = [{"average_speed": round(df['speed'].mean(), 2)}]
            response = jsonify(d)
        except Exception as e:
            logging.warning(e)  # logging error
            result = json.loads(json_util.dumps({
                'message': 'unsuccessful'}, json_options=json_util.RELAXED_JSON_OPTIONS))
            response = jsonify(result)

        # putting header response
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
