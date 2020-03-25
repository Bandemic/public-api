from flask import Flask
from flask_pymongo import PyMongo  # type: ignore
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://172.31.16.148:27017/bluto"
mongo = PyMongo(app)


def get_cases(lat: float, lon: float, since: datetime):
    return mongo.db.cases.find({lat: lat, lon: lon, since: {"$gte": since}})
