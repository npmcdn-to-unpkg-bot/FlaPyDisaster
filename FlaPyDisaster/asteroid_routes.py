import flask as fl
from app import app
from globes import *


# Asteroid Pages
# asteroid main
@app.route('/asteroid', methods=['GET'])
def asteroid_page():
    return flapy_app.asteroid_page()


# Asteroid Functions
@app.route('/asteroid/main_function', methods=['POST'])
def asteroid_function_form():
    return flapy_app.asteroid_function_form()


@app.route('/asteroid/input_params_function', methods=['POST'])
def asteroid_input_params_form():
    diameter_in = fl.request.form['diameter']
    diameter_unit = fl.request.form['diameter_unit']

    angle_in = fl.request.form['angle']
    angle_unit = fl.request.form['angle_unit']

    velocity_in = fl.request.form['velocity']
    velocity_unit = fl.request.form['velocity_unit']

    density_kgpm3 = float(fl.request.form['density_kgm3'])
    target_density_kgpm3 = float(fl.request.form['target_density_kgm3'])

    radius_obs_in = fl.request.form['radius_obs']
    radius_obs_unit = fl.request.form['radius_obs_unit']

    return flapy_app.asteroid_input_params_form(diameter_in, diameter_unit, angle_in, angle_unit, velocity_in, velocity_unit, density_kgpm3, target_density_kgpm3, radius_obs_in,radius_obs_unit)


@app.route('/asteroid/map_event')
def asteroid_map_event():
    return flapy_app.asteroid_map_event()


@app.route('/asteroid/map_event_geojsoncollection', methods=['GET'])
def asteroid_map_event_geojsoncollection():
    return flapy_app.asteroid_map_event_geojsoncollection()
