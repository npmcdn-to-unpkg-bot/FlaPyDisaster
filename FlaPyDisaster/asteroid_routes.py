from flask import Flask, url_for, request, render_template, redirect
from app import app
from explosion import explosion_math
from explosion.asteroid import asteroid_math
from explosion.asteroid import asteroid_event
import math
from general import unit_conversions, general_geometry

# Asteroid Pages
#asteroid main
@app.route('/asteroid', methods = ['GET'])
def asteroid_page():
    return render_template('asteroid.html', distance_units = unit_conversions.DistanceUnits.get_pretty_units())

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
    

    ## calculate energy (Megaton TNT), breakup altitude (m), and airburst altitude (m)
    
    #breakup_alt_m = asteroid_math.BreakupAltitude(float(density_kgm3), diameter_m, velocity_mps, angle_rad)
    #airburst_alt_m = asteroid_math.AirburstAltitude(breakup_alt_m, diameter_m, float(density_kgm3), float(angle_rad))
    #energy_MtTnt = unit_conversions.energy_conversion(asteroid_math.KeneticEnergy(float(density_kgm3), diameter_m, velocity_mps), unit_conversions.EnergyUnits.joules, unit_conversions.EnergyUnits.Megaton_TNT)
    #ret_period_yr = asteroid_math.ReturnPeriodEarth(energy_MtTnt)

    #breakup_velocity_mps = asteroid_math.VelocityAtAltitude_PreBreakup(breakup_alt_m, velocity_mps, diameter_m, float(density_kgm3), angle_rad)
    #airburst_velocity_mps = asteroid_math.PostBreakupVelocity(breakup_alt_m, breakup_velocity_mps, diameter_m, float(density_kgm3), angle_rad, (airburst_alt_m > 0))
    #airburst_energy_MtTnt = unit_conversions.energy_conversion(asteroid_math.KeneticEnergy(float(density_kgm3), diameter_m, airburst_velocity_mps), unit_conversions.EnergyUnits.joules, unit_conversions.EnergyUnits.Megaton_TNT)

    #overpressure_obs_bar = explosion_math.NewmarkOverpressure(airburst_energy_MtTnt, radius_obs_m)

    event = asteroid_event.AsteroidEvent(diameter_m, angle_rad, velocity_mps, density_kgpm3, target_density_kgpm3, None) 

    print('airburst altitude: ' + str(event.airburst_alt_m))
    # return redirect(url_for('asteroid_page'))
    return render_template('asteroid_results.html'
                           , t_diameter_m = (diameter_in + " " + diameter_unit)
                           , t_angle_deg = (angle_in + " " + angle_unit)
                           , t_velocity_kms = (velocity_in + " " + velocity_unit)
                           , t_density_kgm3 = (density_kgm3 + " kg/m^3")
                           , t_target_density_kgm3 = (target_density_kgm3 + " kg/m^3")
                           # start calculated parameters
                           , t_breakup_alt_m = (str(event.breakup_alt_m) + " m")
                           , t_airburst_alt_m = (str(event.airburst_alt_m) + " m") 
                           , t_energy_MtTnt = (str(event.initial_energy_j) + " " + unit_conversions.EnergyUnits.joules)
                           , t_retperiod_yr = (str(event.ret_period_yr) + " yr")
                           , t_airburst_velocity_mps = (str(event.airburst_velocity_mps) + " " + unit_conversions.VelocityUnits.mps)
                           , t_airburst_energy_MtTnt = (str(event.airburst_energy_j) + " " + unit_conversions.EnergyUnits.joules)
                           , t_radius_obs = (radius_obs_in + radius_obs_unit)
                           , t_overpressure_obs_bar = (str(event.get_overpressure(radius_obs_in)) + " bar") )