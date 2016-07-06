from flask import Flask, url_for, request, render_template, redirect,jsonify
from app import app
import geojson
import mapping.leaflet_map as lm

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
    points = []
    points.append((-71.15, 42.4))
    points.append((-71.12, 42.4));
    points.append((-71.05, 42.4));

    line_str = geojson.LineString(points)

    line_feature = geojson.Feature(geometry = line_str, properties = {"value":5})

    return jsonify(result = line_feature, max = 10, min = 2)

@app.route('/leaflet_geojson_points_test')
def leaflet_geojson_points_test():
    # 42.4, -71.15   42.4, -71.12        42.4, -71.05
    points = []
    points.append((-71.15, 42.4))
    points.append((-71.12, 42.4));
    points.append((-71.05, 42.4));

    multi_pt = geojson.MultiPoint(points)

    pt_feature = geojson.Feature(geometry = multi_pt, properties = {"value":1})

    pt_feature_dict = lm.create_feature(points, lm.geojson_geometry.multipoint, 1)

    return jsonify(result = pt_feature, max = 10, min = 2)