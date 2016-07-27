from flask import Flask, url_for, request, render_template, redirect
from app import app
# from hurricane import hurricane_math


# hurricane main
@app.route('/hurricane', methods = ['GET'])
def hurricane_page():
    return render_template('html/hurricane.html')
    
@app.route('/hurricane/main_file', methods = ['POST'])
def hurricane_file_form():
    filename = request.form['file_uri']
    print(filename)
    return redirect(url_for('hurricane_page'))

@app.route('/hurricane/main_function', methods = ['POST'])
def hurricane_function_form():
    # hurricane_math.HelloHurricane()
    return redirect(url_for('hurricane_page'))