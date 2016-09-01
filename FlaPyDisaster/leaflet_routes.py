import flask as fl
from app import app
import geojson
import mapping.leaflet_map as lm


@app.route('/leaflet')
def leaflet_redirect():
    return fl.render_template('html/leaflet_test.html')


@app.route('/leaflet/test_latlng', methods=['POST'])
def leaflet_test_latlng():
    print("leaflet test in Flask.")
    lat = fl.request.json['lat']
    lng = fl.request.json['lng']
    print("lat: " + lat)
    print("lng: " + lng)
    return "Success"


@app.route('/leaflet/test_js')
def leaflet_test_js():
    return fl.render_template('/js/leaflet_test.js')


@app.route('/leaflet/geojson_test')
def leaflet_geojson_test():
    # 42.4, -71.15   42.4, -71.12        42.4, -71.05
    points = [(-71.15, 42.4), (-71.12, 42.4), (-71.05, 42.4)]

    line_str = geojson.LineString(points)

    line_feature = geojson.Feature(geometry=line_str, properties={"value": 5})

    return fl.jsonify(result=line_feature, max=10, min=2)


@app.route('/leaflet/geojson_points_test')
def leaflet_geojson_points_test():
    # 42.4, -71.15   42.4, -71.12        42.4, -71.05
    points = [(-71.15, 42.4), (-71.12, 42.4), (-71.05, 42.4)]

    # multi_pt = geojson.MultiPoint(points)

    # pt_feature = geojson.Feature(geometry = multi_pt, properties = {"value":1})

    pt_feature_dict = lm.create_feature(points, lm.GeojsonGeometry.multipoint, 1)

    return fl.jsonify(result=pt_feature_dict['geojson'], max=10, min=2)
