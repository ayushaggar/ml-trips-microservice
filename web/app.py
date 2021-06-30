from flask import Flask
from src.database import mongo
from src.controllers import TripController
import os

# initialisation of flask and mongo
db_uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
    '@' + os.environ['MONGODB_HOSTNAME'] + \
    ':27017/' + os.environ['MONGODB_DATABASE']
app = Flask(__name__)
app.config["MONGO_URI"] = db_uri
mongo.init_app(app)

# trips routes
app.add_url_rule(
    "/total_trips",
    methods=["GET"],
    view_func=TripController.total_trips)
app.add_url_rule(
    "/average_fare_heatmap",
    methods=["GET"],
    view_func=TripController.average_fare_heatmap)
app.add_url_rule(
    "/average_speed_24hrs",
    methods=["GET"],
    view_func=TripController.average_speed_24hrs)

# status route to check health of api
app.add_url_rule(
    "/status",
    methods=["GET"],
    view_func=TripController.status)

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True)
