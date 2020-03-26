from flask import Flask, escape, request, jsonify, Response
import datetime
from db import mongo, get_cases
import dateutil.parser as dateparser

import os

app = Flask(__name__, instance_relative_config=True)
env = os.environ.get("FLASK_ENV", "production")
if env == "production":
    app.config.from_object("config.ProductionConfig")
elif env == "development":
    app.config.from_object("config.DevelopmentConfig")
elif env == "testing":
    app.config.from_object("config.TestingConfig")


app.config["APPLICATION_ROOT"] = "/"

mongo.init_app(app)

# TODO: instead of a timestamp passing a single UUID might be better here
@app.route("/v1/cases")
def cases():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    pid = request.args.get("pid", type=str)

    try:
        if lat is not None:
            lat: int = round(lat)
        if lon is not None:
            lon: int = round(lon)
    except ValueError:
        return Response(None, status=400)

    since = request.args.get("since", type=str)
    if since is not None:
        try:
            since = dateparser.isoparse(since)
        except ValueError:
            return Response(None, status=400)

    cases = get_cases(lat, lon=lon, since=since)
    return jsonify(cases)
