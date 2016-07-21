from flask import Flask, url_for, request, render_template, redirect, jsonify
from app import app
from explosion import explosion_math
from explosion.asteroid import asteroid_math
from explosion.asteroid import asteroid_event
import math
from general import unit_conversions, general_geometry, general_objects, general_image, general_colors
import os

# Asteroid Pages
#asteroid main
@app.route('/asteroid', methods = ['GET'])
def asteroid_page():
    return render_template('asteroid.html'
                           , distance_units = unit_conversions.DistanceUnits.get_units_pair()
                           , velocity_units = unit_conversions.VelocityUnits.get_units_pair())

# Asteroid Functions
@app.route('/asteroid_main_function', methods = ['POST'])
def asteroid_function_form():
    explosion_math.hello()
    asteroid_math.hello()
    return redirect(url_for('asteroid_page'))

@app.route('/asteroid_input_params_function', methods = ['POST'])
def asteroid_input_params_form():
    diameter_in = request.form['diameter']
    diameter_unit = request.form['diameter_unit']

    angle_in = request.form['angle']
    angle_unit = request.form['angle_unit']

    velocity_in = request.form['velocity']
    velocity_unit = request.form['velocity_unit']

    density_kgpm3 = float(request.form['density_kgm3'])
    target_density_kgpm3 = float(request.form['target_density_kgm3'])

    radius_obs_in = request.form['radius_obs']
    radius_obs_unit = request.form['radius_obs_unit']

    # run any necessary unit conversions
    angle_rad = 0
    if angle_unit == 'deg':
        angle_rad = math.radians(float(angle_in))
    
    diameter_m = unit_conversions.distance_conversion(float(diameter_in), diameter_unit, unit_conversions.DistanceUnits.meter)
    velocity_mps = unit_conversions.velocity_conversion(float(velocity_in), velocity_unit, unit_conversions.VelocityUnits.mps)
    radius_obs_m = unit_conversions.distance_conversion(float(radius_obs_in), radius_obs_unit, unit_conversions.DistanceUnits.meter)
    
    # create asteroid event from input parameters
    latlon_grid = general_objects.LatLonGrid(30, 20, 10, 30, 2, 2)
    global event
    event = asteroid_event.AsteroidEvent(diameter_m, angle_rad, velocity_mps, density_kgpm3, target_density_kgpm3, latlon_grid, (25, 20))
    grid_res = event.get_effect_2d_grid(True, 5)
    # return redirect(url_for('asteroid_page'))
    
    if(os.path.isfile("test_out.txt")):
        os.remove("test_out.txt")
        with open("test_out.txt", "w") as write_file:
            for row in grid_res:
                out = ""
                for val in row:
                    curr_str = str(format(round(val[0], 5), 'f'))
                    out = out + curr_str + "\t"
                out.rstrip()
                write_file.write(out + "\n")

    return render_template('asteroid_results.html'
                           , t_diameter_m = (diameter_in + " " + diameter_unit)
                           , t_angle_deg = (angle_in + " " + angle_unit)
                           , t_velocity_kms = (velocity_in + " " + velocity_unit)
                           , t_density_kgpm3 = (str(density_kgpm3) + " kg/m^3")
                           , t_target_density_kgpm3 = (str(target_density_kgpm3) + " kg/m^3")
                           # start calculated parameters
                           , t_breakup_alt_m = (str(round(event.breakup_alt_m, 2)) + " m")
                           , t_airburst_alt_m = (str(round(event.airburst_alt_m, 2)) + " m") 
                           , t_energy_MtTnt = (str(round(unit_conversions.energy_conversion(event.initial_energy_j, unit_conversions.EnergyUnits.joules, unit_conversions.EnergyUnits.Megaton_TNT), 2)) + " " + unit_conversions.EnergyUnits.Megaton_TNT)
                           , t_retperiod_yr = (str(round(event.ret_period_yr, 2)) + " yr")
                           , t_airburst_velocity_mps = (str(round(event.airburst_velocity_mps, 2)) + " " + unit_conversions.VelocityUnits.mps)
                           , t_airburst_energy_MtTnt = (str(round(unit_conversions.energy_conversion(event.airburst_energy_j, unit_conversions.EnergyUnits.joules, unit_conversions.EnergyUnits.Megaton_TNT), 2)) + " " + unit_conversions.EnergyUnits.Megaton_TNT)
                           , t_radius_obs = (radius_obs_in + radius_obs_unit)
                           , t_overpressure_obs_bar = (str(round(event.get_newmark_overpressure(radius_obs_m), 2)) + " bar") )

@app.route('/asteroid_map_event')
def asteroid_map_event():
    geo = event.grid_to_geojson()
    geo_collect = event.grid_to_geojson_collection(.00001)
    return jsonify(result = geo, max = 10, min = 2)

@app.route('/asteroid_map_event_geojsoncollection')
def asteroid_map_event_geojsoncollection():

    color_ramp = general_colors.ColorPalettes.hex_to_rgb(general_colors.ColorPalettes.simple_escalating_5, 255)

    step_val = .00001
    maxmin = event.get_event_res_maxmin()
    geo_collect = event.grid_to_geojson_collection(step_val, maxmin[0] + step_val)
    sorted_values = list(map((lambda x: x.properties['value']), geo_collect))
    sorted_values.sort()
    value_bins = general_colors.ColorPalettes.even_value_breaks(sorted_values, len(color_ramp))
    # return jsonify(result = geo_collect, max = maxmin[0] + step_val, min = maxmin[1])#, val_list = values)
    return jsonify(result = geo_collect, colors = color_ramp, bins = value_bins)
