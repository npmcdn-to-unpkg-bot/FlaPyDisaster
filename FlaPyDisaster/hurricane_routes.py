import flask as fl
import werkzeug as wk
import general as gen
import os
from app import app
from hurricane import hurricane_utils as hu


# global variables
catalog = None


# hurricane main
@app.route('/hurricane', methods=['GET'])
def hurricane_page():
    return fl.render_template('html/hurricane.html')


@app.route('/hurricane/main_file', methods=['POST'])
def hurricane_file_form():
    # Move this upload logic to a general method
    hurdat_file = fl.request.files['hurdat_file']
    filename = wk.secure_filename(hurdat_file.filename)
    hurdat_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), )
    file_uri = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    global catalog
    catalog = hu.HurdatCatalog(file_uri)

    storm_data_table = catalog.storm_catalog[0].to_model_dataframe().to_html()
    # storm_data_table = catalog.storm_catalog[0].to_hurdat_dataframe().to_html()
    # print(catalog.storm_catalog[0].track_to_geojson())
    return fl.render_template("html/hurricane_table_test.html", name="Catalog Data Frame", data=storm_data_table)


@app.route('/hurricane/hurdat_track_geojson', methods=['GET'])
def hurricane_geojson_test():
    geo_collect = catalog.storm_catalog[0].track_to_geojson()
    color_ramp = gen.general_colors.ColorPalettes.hex_to_rgb(gen.general_colors.ColorPalettes.simple_escalating_5, 255)
    sorted_values = list(map((lambda x: x.properties['value']), geo_collect))
    sorted_values.sort()
    value_bins = gen.general_colors.ColorPalettes.even_value_breaks(sorted_values, len(color_ramp))

    return fl.jsonify(result=geo_collect, colors=color_ramp, bins=value_bins)


@app.route('/hurricane/main_function', methods=['POST'])
def hurricane_function_form():
    return fl.redirect(fl.url_for('hurricane_page'))


@app.route('/hurricane/table_test', methods=['GET'])
def table_test():
    catalog = hu.HurdatCatalog(r'Documentation\Hurricane\HURDAT\hurdat2-1851-2015-070616_with_header.txt')

    # data_table = catalog.storm_data.head().to_html()
    storm_data_table = catalog.storm_catalog[0].to_model_dataframe().to_html()
    return fl.render_template("html/hurricane_table_test.html", name="Catalog Data Frame", data=storm_data_table)
