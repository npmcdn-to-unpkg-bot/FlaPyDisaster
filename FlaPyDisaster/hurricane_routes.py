import flask as fl
from app import app
# import global variables
from globes import *


# global variables
catalog = None


# hurricane main
@app.route('/hurricane', methods=['GET'])
def hurricane_page():
    return flapy_app.hurricane_page()


@app.route('/hurricane/main_file', methods=['POST'])
def hurricane_file_form():
    return flapy_app.hurricane_file_form(fl.request.files['hurdat_file'])


@app.route('/hurricane/hurdat_track_geojson', methods=['GET'])
def hurricane_geojson_test():
    return flapy_app.hurricane_geojson_test()


@app.route('/hurricane/main_function', methods=['POST'])
def hurricane_function_form():
    return flapy_app.hurricane_function_form()


@app.route('/hurricane/table_test', methods=['GET'])
def table_test():
    return flapy_app.table_test()


@app.route('/hurricane/hurricane_table_js')
def hurricane_tables_js():
    return flapy_app.hurricane_tables_js()


@app.route('/hurricane/change_table')
def change_table():
    return flapy_app.change_table(fl.request.args.get('name', '', type=str))

@app.route('/hurricane/geojson_event_map')
def map_hurricane_event():
    return flapy_app.map_hurricane_event()
