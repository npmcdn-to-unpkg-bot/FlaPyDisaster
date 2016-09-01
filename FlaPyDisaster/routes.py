import flask as fl
from app import app
# needed for Flask to run
from hurricane_routes import *
from asteroid_routes import *
from leaflet_routes import *
from general import unit_conversions


# server root
@app.route('/')
@app.route('/home')
def main_page():
    return fl.render_template('html/HomePage.html')


###############
# Test routes #
###############


# JQuery function route
@app.route('/test/distance_unit_conversion')
def unit_conversion_route():
    number = fl.request.args.get('number', 0, type=float)
    unit_in = fl.request.args.get('unit_in', '', type=str)
    unit_out = fl.request.args.get('unit_out', '', type=str)
    new_num = unit_conversions.distance_conversion(number, unit_in, unit_out)
    return fl.jsonify(result=new_num)


# asteroid result page route
@app.route('/test/asteroid_result')
def asteroid_result_test():
    return fl.render_template('html/asteroid_results.html'
                              , t_diameter_m="10 m"
                              , t_angle_deg="90 deg"
                              , t_velocity_kms="10 mps"
                              , t_density_kgm3="1000 kg/m^3"
                              , t_target_density_kgm3="2000 kg/m^3"
                              # start calculated parameters
                              , t_breakup_alt_m="100 m"
                              , t_airburst_alt_m="150 m"
                              , t_energy_MtTnt="100 Mt-TNT"
                              , t_retperiod_yr="10 yr"
                              , t_airburst_velocity_mps="50 m/s"
                              , t_airburst_energy_MtTnt="200 Mt-TNT"
                              , t_radius_obs="300 m"
                              , t_overpressure_obs_bar="100 bar")
