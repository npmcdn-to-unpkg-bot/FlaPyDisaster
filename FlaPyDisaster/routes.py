from flask import Flask, url_for, request, render_template, redirect
from app import app
from hurricane_routes import *

# server root
@app.route('/')
@app.route('/home')
def main_page():
    return render_template('HomePage.html')
