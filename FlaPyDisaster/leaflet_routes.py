from flask import Flask, url_for, request, render_template, redirect
from app import app

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