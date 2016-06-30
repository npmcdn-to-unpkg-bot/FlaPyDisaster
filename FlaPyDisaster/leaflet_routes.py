from flask import Flask, url_for, request, render_template, redirect,jsonify
from app import app
import geojson

@app.route('/leaflet')
def leaflet_redirect():
    return render_template('leaflet_test.html')

@app.route('/leaflet_test_latlng', methods = ['POST'])
def leaflet_test_latlng():
    print("leaflet test in Flask.")
    lat = request.json['lat']
    lng = request.json['lng']
    print("lat: " + lat)
    print("lng: " + lng)
    return "Success"

@app.route('/leaflet_test_js')
def leaflet_test_js():
    return render_template('/js/leaflet_test.js')

@app.route('/leaflet_geojson_test')
def leaflet_geojson_test():
    # 42.4, -71.15   42.4, -71.12        42.4, -71.05
    point_1 = geojson.Point((-71.15, 42.4));
    point_2 = geojson.Point((-71.12, 42.4));
    point_3 = geojson.Point((-71.05, 42.4));

    multi_pt = geojson.MultiPoint(point_1, point_2, point_3)

    line_str = geojson.LineString([(-71.15, 42.4), (-71.12, 42.4), (-71.05, 42.4)])

    line_feature = geojson.Feature(geometry = line_str, properties = {"value":5})

    return jsonify(result = line_feature, max = 10, min = 2)