from general import general_objects as geno
import csv

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
    def __init__(self, name, track_filetrack_file_uri, bbox, block_per_deg_x = 10, block_per_deg_y = 10):
        """
        :param geno.BoundingBox bbox: input bounding box
        """
        
        self.track_file_uri = track_file_uri
        self.bbox = bbox
        self.track_points = []
        self.grid = geno.LatLonGrid(bbox.top_lat_y, bbox.bot_lat_y, bbox.left_lon_x, bbox.right_lon_x, block_per_deg_x, block_per_deg_y)
    
    def load(self):
        with open(self.track_file_uri, 'r') as tsv:
            tsv_reader = csv.reader(tsv, delimiter = '\t')
            for row in tsv_reader:
                # process row into track
                pass
        pass

    def get_2d_grid(self):
        pass
    
    def get_1d_grid(self):
        pass

    def get_grid_to_geojson_collection(self):
        pass

    def get_track_to_geojson_collection(self):
        pass

    def get_storm_to_geojson_collection(self):
        pass

    def save(self, save_file_uri, save_type = 'image', incl_track = True, incl_readme = True):
        pass

    def calculate_windfield(self, model = 'nws23', resolution_PxPerDeg = 10):
        pass

    def get_inf(self):
        pass


