from flask import Flask, url_for, request, render_template, redirect
from app import app
from explosion import explosion_math
from explosion.asteroid import asteroid_math
import math

# Asteroid Pages
#asteroid main
@app.route('/asteroid', methods = ['GET'])
def asteroid_page():
    return render_template('asteroid.html')

# Asteroid Functions
@app.route('/asteroid_main_function', methods = ['POST'])
def asteroid_function_form():
    explosion_math.hello()
    asteroid_math.hello()
    return redirect(url_for('asteroid_page'))

@app.route('/asteroid_input_params_function', methods = ['POST'])
def asteroid_input_params_form():
    diameter_m = request.form['diameter_m']
    angle_deg = request.form['angle_deg']
    angle_rad = math.radians(float(angle_deg))
    velocity_kms = request.form['velocity_kms']
    density_kgm3 = request.form['density_kgm3']
    target_density_kgm3 = request.form['target_density_kgm3']

    breakup_alt = asteroid_math.BreakupAltitude(float(density_kgm3), float(diameter_m), float(velocity_kms) * 1000, angle_rad)
    airburst_alt = asteroid_math.AirburstAltitude(breakup_alt, float(diameter_m), float(density_kgm3), float(angle_rad))

    print('airburst altitude: ' + str(airburst_alt))
    # return redirect(url_for('asteroid_page'))
    return render_template('asteroid_results.html', t_diameter_m=diameter_m, t_angle_deg=angle_deg, t_velocity_kms=velocity_kms, t_density_kgm3=density_kgm3, t_target_density_kgm3=target_density_kgm3, t_breakup_alt_m=str(breakup_alt), t_airburst_alt_m=str(airburst_alt))