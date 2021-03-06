﻿from flask import Flask, url_for, request, render_template, redirect
from app import app
import PIL
from hurricane import hurricane_utils as hu
# from hurricane import hurricane_math


# hurricane main
@app.route('/hurricane', methods = ['GET'])
def hurricane_page():
    return render_template('html/hurricane.html')
    
@app.route('/hurricane/main_file', methods = ['POST'])
def hurricane_file_form():
    filename = request.form['file_uri']
    catalog = hu.HurdatCatalog(filename)
    storm_data_table = catalog.storm_catalog[0].to_model_dataframe().to_html()
    #storm_data_table = catalog.storm_catalog[0].to_hurdat_dataframe().to_html()
    print(filename)
    return render_template("html/hurricane_table_test.html", name="Catalog Data Frame", data=storm_data_table)
    #return redirect(url_for('hurricane_page'))

@app.route('/hurricane/main_function', methods = ['POST'])
def hurricane_function_form():
    return redirect(url_for('hurricane_page'))

@app.route('/hurricane/table_test', methods = ['GET'])
def table_test():
    catalog = hu.HurdatCatalog(r'Documentation\Hurricane\HURDAT\hurdat2-1851-2015-070616_with_header.txt')
    
    # data_table = catalog.storm_data.head().to_html()
    storm_data_table = catalog.storm_catalog[0].to_model_dataframe().to_html()
    return render_template("html/hurricane_table_test.html", name="Catalog Data Frame", data=storm_data_table)