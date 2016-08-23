from general import general_objects as geno

###########################################
# struct like classes for hurricane event #
###########################################
class track_point():
    def __init__(self, season_year, storm_num, storm_name, timestamp, lat, lon, MaxWind, Cp, Rmax, Fspeed, bearing, seq, GWAF):
        pass

class output_point():
    def __init__(self, windspeed_nws23, friction):
        pass

#########################
# hurricane event class #
#########################
class hurricane_event():
    def __init__(self, name, track_filetrack_file_uri, bbox):
        self.track_file_uri = track_file_uri
        self.bbox = bbox
        self.track_points = []
        self.grid = [[]]
        pass
    
    def load():
        pass

    def get_2d_grid():
        pass
    
    def get_1d_grid():
        pass

    def get_grid_to_geojson_collection():
        pass

    def get_track_to_geojson_collection():
        pass

    def get_storm_to_geojson_collection():
        pass

    def save(save_file_uri, save_type = 'image', incl_track = True, incl_readme = True):
        pass

    def calculate_windfield(model = 'nws23', resolution_PxPerDeg = 10):
        pass

    def get_inf():
        pass


