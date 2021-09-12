""" Simple app for producing board of MBTA commuter routes """
import requests
# from jsonapi_client import Session, Filter, ResourceTuple

from flask import Flask, render_template

app = Flask(__name__)
BASE_ENDPOINT = "https://api-v3.mbta.com/"
SCHEDULES_ARGS = "predictions?filter[stop]=place-north&sort=-departure_time&filter[route_type]=0,1,2"
ALERTS_ARGS = "alerts?filter[stop]=place-north&page[limit]=5"

def get_departures():
    response = requests.get(BASE_ENDPOINT + SCHEDULES_ARGS)

    departures = []
    for prediction in response.json()["data"]:
        departure_time = prediction['attributes']['departure_time']
        if departure_time:
            departure_time = departure_time[11:16]
            departures.append({
                "Line": prediction['relationships']['route']['data']['id'],
                "DepartureTime": departure_time
            })

    return departures[::-1]

def get_alerts():
    response = requests.get(BASE_ENDPOINT + ALERTS_ARGS)

    alerts = []
    for alert in response.json()["data"]:
        alerts.append({
            "Message": alert['attributes']['header']
        })

    return alerts

@app.route('/')
def index():
    departures = get_departures()
    alerts = get_alerts()
    return render_template('index.html', departures=departures, alerts=alerts)
