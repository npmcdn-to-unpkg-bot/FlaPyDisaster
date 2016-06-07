from flask import Flask, url_for, request, render_template, redirect
from app import app
from explosion import math as exmath
from explosion.asteroid import math as astermath

#asteroid main
@app.route('/asteroid', methods = ['GET'])
def asteroid_page():
    return render_template('asteroid.html')

@app.route('/asteroid_main_function', methods = ['POST'])
def asteroid_function_form():
    exmath.hello()
    astermath.hello()
    return redirect(url_for('asteroid_page'))