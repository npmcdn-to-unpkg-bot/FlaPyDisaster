import flask as fl
import general.general_utils as genu
import general.general_colors as genc
import general.general_units as gen_units
import general.general_objects as geno
from explosion import explosion_math
from explosion.asteroid import asteroid_math
from explosion.asteroid import asteroid_event
import os
from hurricane import hurricane_utils as hu
import math
import geojson
import mapping.leaflet_map as lm
import time
import numpy as np
import mapping.gdal_mapping as gdm


class FlaPyApp:
    def __init__(self):
        self.hurricane_catalog = None
        self.current_hurricane_name = None
        self.asteroid_catalog = None
        self.asteroid_event = None
        pass

    def hello(self):
        print("Hello")

    ########################
    # Hurricane Interfaces #
    ########################
    def hurricane_page(self):
        return fl.render_template('html/hurricane.html')

    def hurricane_file_form(self, hurdat_file):
        file_uri = genu.Web.get_web_file_uri(hurdat_file)

        self.hurricane_catalog = hu.HurdatCatalog(file_uri)

        storm_data_table = self.hurricane_catalog.storm_catalog[0].to_model_dataframe().to_html(classes='track_table')
        return fl.render_template("html/hurricane_table_test.html"
                                  , table_name="Catalog Data Frame"
                                  , data=storm_data_table
                                  , catalog_names=self.hurricane_catalog.get_names())

    def hurricane_geojson_test(self):
        geo_collect = self.hurricane_catalog.get_storm_by_name(self.current_hurricane_name)[0].track_to_geojson()
        color_ramp = genc.ColorPalettes.hex_to_rgb(genc.ColorPalettes.simple_escalating_5, 255)
        sorted_values = list(map((lambda x: x.properties['value']), geo_collect))
        sorted_values.sort()
        value_bins = genc.ColorPalettes.even_value_breaks(sorted_values, len(color_ramp))

        return fl.jsonify(result=geo_collect, colors=color_ramp, bins=value_bins)

    def hurricane_function_form(self):
        return fl.redirect(fl.url_for('hurricane_page'))

    def table_test(self):
        self.hurricane_catalog = hu.HurdatCatalog(r'Documentation\Hurricane\HURDAT\hurdat2-1851-2015-070616_with_header.txt')

        # data_table = storm_catalog.storm_data.head().to_html()
        storm_data_table = self.hurricane_catalog.storm_catalog[0].to_model_dataframe().to_html()
        return fl.render_template("html/hurricane_table_test.html", name="Catalog Data Frame", data=storm_data_table)

    def hurricane_tables_js(self):
        return fl.render_template('/js/hurricane_tables.js')

    def change_table(self, name):
        self.current_hurricane_name = name
        storm = self.hurricane_catalog.get_storm_by_name(name)[0]
        # ret_list = self.hurricane_catalog.get_storm_by_name(name)
        print("Start Event Calculation")
        start = time.time()
        storm.calculate_grid(10, 10, 15, 15, do_parallel=True)
        end = time.time()
        print("Calculation Time: " + str(end - start))
        print("num points: " + str(len(storm.result_array)))
        ret_data = storm.to_model_dataframe().to_html(classes='track_table')

        return fl.jsonify(table=ret_data)

    def map_hurricane_event(self):
        storm = self.hurricane_catalog.get_storm_by_name(self.current_hurricane_name)[0]
        geo_collect = storm.grid_to_geojson()
        sorted_values = list(map((lambda x: x.properties['value']), geo_collect))
        sorted_values.sort()
        color_ramp = genc.ColorPalettes.hex_to_rgb(genc.ColorPalettes.simple_escalating_5, 255)
        value_bins = genc.ColorPalettes.even_value_breaks(sorted_values, len(color_ramp))

        print("sending geojson events")
        return fl.jsonify(result=geo_collect, colors=color_ramp, bins=value_bins)

    def map_hurricane_event_canvas(self):
        storm = self.hurricane_catalog.get_storm_by_name(self.current_hurricane_name)[0]

        sorted_values = list(map((lambda x: x[2]), storm.result_array))
        sorted_values.sort()
        color_ramp = genc.ColorPalettes.hex_to_rgb(genc.ColorPalettes.simple_escalating_5, 255)
        value_bins = genc.ColorPalettes.even_value_breaks(sorted_values, len(color_ramp))

        print("sending canvas events")
        return fl.jsonify(colors=color_ramp, bins=value_bins, data=storm.result_array)

    def hurricane_save_event_to_raster(self):
        storm = self.hurricane_catalog.get_storm_by_name(self.current_hurricane_name)[0]

        start = time.time()
        two_d_gdm_list = np.flipud(np.array(list(map((lambda x: x[2]), storm.result_array))).reshape(storm.lat_lon_grid.get_block_height_y(), storm.lat_lon_grid.get_block_width_x()))
        file_uri = r'tmp/' + storm.unique_name + ".png"
        print("raster file uri: " + file_uri)
        gdm.list_to_raster(two_d_gdm_list, file_uri, True)
        end = time.time()
        print("Raster Save Time: " + str(end - start))

    def map_hurricane_event_d3(self):
        data = []
        return fl.jsonify(data=data)

    #######################
    # Asteroid Interfaces #
    #######################
    def asteroid_page(self):
        return fl.render_template('html/asteroid.html'
                                  , distance_units=gen_units.DistanceUnits.get_units_pair()
                                  , velocity_units=gen_units.VelocityUnits.get_units_pair())

    def asteroid_function_form(self):
        explosion_math.hello()
        asteroid_math.hello()
        return fl.redirect(fl.url_for('asteroid_page'))

    def asteroid_input_params_form(self, diameter_in, diameter_unit, angle_in, angle_unit, velocity_in, velocity_unit, density_kgpm3, target_density_kgpm3, radius_obs_in,radius_obs_unit):
        # run any necessary unit conversions
        angle_rad = 0
        if angle_unit == 'deg':
            angle_rad = math.radians(float(angle_in))

        diameter_m = gen_units.distance_conversion(float(diameter_in), diameter_unit, gen_units.DistanceUnits.meter)
        velocity_mps = gen_units.velocity_conversion(float(velocity_in), velocity_unit, gen_units.VelocityUnits.mps)
        radius_obs_m = gen_units.distance_conversion(float(radius_obs_in), radius_obs_unit, gen_units.DistanceUnits.meter)

        # create asteroid event from input parameters
        latlon_grid = geno.LatLonGrid(30, 20, 10, 30, 2, 2)

        self.asteroid_event = asteroid_event.AsteroidEvent(diameter_m, angle_rad, velocity_mps, density_kgpm3, target_density_kgpm3, latlon_grid, (25, 20))
        grid_res = self.asteroid_event.get_effect_2d_grid(True, 5)

        if os.path.isfile("test_out.txt"):
            os.remove("test_out.txt")
            with open("test_out.txt", "w") as write_file:
                for row in grid_res:
                    out = ""
                    for val in row:
                        curr_str = str(format(round(val[0], 5), 'f'))
                        out = out + curr_str + "\t"
                    out.rstrip()
                    write_file.write(out + "\n")

        return fl.render_template('html/asteroid_results.html'
                                  , t_diameter_m=(diameter_in + " " + diameter_unit)
                                  , t_angle_deg=(angle_in + " " + angle_unit)
                                  , t_velocity_kms=(velocity_in + " " + velocity_unit)
                                  , t_density_kgpm3=(str(density_kgpm3) + " kg/m^3")
                                  , t_target_density_kgpm3=(str(target_density_kgpm3) + " kg/m^3")
                                  # start calculated parameters
                                  , t_breakup_alt_m=(str(round(self.asteroid_event.breakup_alt_m, 2)) + " m")
                                  , t_airburst_alt_m=(str(round(self.asteroid_event.airburst_alt_m, 2)) + " m")
                                  , t_energy_MtTnt=(str(round(gen_units.energy_conversion(self.asteroid_event.initial_energy_j, gen_units.EnergyUnits.joules, gen_units.EnergyUnits.Megaton_TNT), 2)) + " " + gen_units.EnergyUnits.Megaton_TNT)
                                  , t_retperiod_yr=(str(round(self.asteroid_event.ret_period_yr, 2)) + " yr")
                                  , t_airburst_velocity_mps=(str(round(self.asteroid_event.airburst_velocity_mps, 2)) + " " + gen_units.VelocityUnits.mps)
                                  , t_airburst_energy_MtTnt=(str(round(gen_units.energy_conversion(self.asteroid_event.airburst_energy_j, gen_units.EnergyUnits.joules, gen_units.EnergyUnits.Megaton_TNT), 2)) + " " + gen_units.EnergyUnits.Megaton_TNT)
                                  , t_radius_obs=(radius_obs_in + radius_obs_unit)
                                  , t_overpressure_obs_bar=(str(round(self.asteroid_event.get_newmark_overpressure(radius_obs_m), 2)) + " bar"))

    def asteroid_map_event(self):
        geo = self.asteroid_event.grid_to_geojson()
        # geo_collect = event.grid_to_geojson_collection_stepped(.00001)
        return fl.jsonify(result=geo, max=10, min=2)

    def asteroid_map_event_geojsoncollection(self):
        color_ramp = genc.ColorPalettes.hex_to_rgb(genc.ColorPalettes.simple_escalating_5, 255)
        geo_collect = self.asteroid_event.grid_to_geojson_collection()
        sorted_values = list(map((lambda x: x.properties['value']), geo_collect))
        sorted_values.sort()
        value_bins = genc.ColorPalettes.even_value_breaks(sorted_values, len(color_ramp))
        return fl.jsonify(result=geo_collect, colors=color_ramp, bins=value_bins)

    ######################
    # Leaflet Interfaces #
    ######################
    def leaflet_redirect(self):
        return fl.render_template('html/leaflet_test.html')

    def leaflet_test_latlng(self, lat, lng):
        print("leaflet test in Flask.")
        print("lat: " + lat)
        print("lng: " + lng)
        return "Success"

    def leaflet_test_js(self):
        return fl.render_template('/js/leaflet_test.js')

    def leaflet_geojson_test(self):
        # 42.4, -71.15   42.4, -71.12        42.4, -71.05
        points = [(-71.15, 42.4), (-71.12, 42.4), (-71.05, 42.4)]

        line_str = geojson.LineString(points)

        line_feature = geojson.Feature(geometry=line_str, properties={"value": 5})

        return fl.jsonify(result=line_feature, max=10, min=2)

    def leaflet_geojson_points_test(self):
        # 42.4, -71.15   42.4, -71.12        42.4, -71.05
        points = [(-71.15, 42.4), (-71.12, 42.4), (-71.05, 42.4)]
        # multi_pt = geojson.MultiPoint(points)
        # pt_feature = geojson.Feature(geometry = multi_pt, properties = {"value":1})

        pt_feature_dict = lm.create_feature(points, lm.GeojsonGeometry.multipoint, 1)

        return fl.jsonify(result=pt_feature_dict['geojson'], max=10, min=2)

    pass
