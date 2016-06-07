from flask import Flask, url_for, request, render_template, redirect
from app import app
from explosion import math as exmath
from explosion.asteroid import math as astermath

# Asteroid Pages
#asteroid main
@app.route('/asteroid', methods = ['GET'])
def asteroid_page():
    return render_template('asteroid.html')

# Asteroid Functions
@app.route('/asteroid_main_function', methods = ['POST'])
def asteroid_function_form():
    exmath.hello()
    astermath.hello()
    return redirect(url_for('asteroid_page'))

@app.route('/asteroid_input_params_function', methods = ['POST'])
def asteroid_input_params_form():
    diameter_m = request.form['diameter_m']
    angle_deg = request.form['angle_deg']
    velocity_kms = request.form['velocity_kms']
    density_kgm3 = request.form['density_kgm3']
    target_density_kgm3 = request.form['target_density_kgm3']

    print('asteroid_input_params_form ' + diameter_m)
    # return redirect(url_for('asteroid_page'))
    return render_template('asteroid_results.html', t_diameter_m=diameter_m, t_angle_deg=angle_deg, t_velocity_kms=velocity_kms, t_density_kgm3=density_kgm3, t_target_density_kgm3=target_density_kgm3)