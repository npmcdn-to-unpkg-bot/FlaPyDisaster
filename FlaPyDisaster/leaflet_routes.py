import flask as fl
from app import app
from globes import *


@app.route('/leaflet')
def leaflet_redirect():
    return flapy_app.leaflet_redirect()


@app.route('/leaflet/test_latlng', methods=['POST'])
def leaflet_test_latlng():
    lat = fl.request.json['lat']
    lng = fl.request.json['lng']
    return flapy_app.leaflet_test_latlng(lat, lng)


@app.route('/leaflet/test_js')
def leaflet_test_js():
    return flapy_app.leaflet_test_js()


@app.route('/leaflet/geojson_test')
def leaflet_geojson_test():
    return flapy_app.leaflet_geojson_test()


@app.route('/leaflet/geojson_points_test')
def leaflet_geojson_points_test():
    return flapy_app.leaflet_geojson_points_test()
