""" Simple app for producing board of MBTA commuter routes """
import requests
# from jsonapi_client import Session, Filter, ResourceTuple

from flask import Flask, render_template

app = Flask(__name__)
BASE_ENDPOINT = "https://api-v3.mbta.com/"
SCHEDULES_ARGS = "schedules?include=route,trip,stop&filter[stop]=place-north"

def get_routes():
    response = requests.get(BASE_ENDPOINT + SCHEDULES_ARGS)
    return response.json()["data"][:10]

@app.route('/')
def index():
    routes = get_routes()
    for route in routes:
        print(route)
    return render_template('index.html', routes=routes)
