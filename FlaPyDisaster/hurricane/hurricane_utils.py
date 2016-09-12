import datetime
import pandas as pd
import mapping.leaflet_map as lm
import copy
import math
import general.general_objects as geno
import general.general_units as genu
import hurricane.hurricane_nws23 as hm
import joblib as job


def load_hurdat():
    pass


def calc_bearing_north_zero(lat_ref, lon_ref, lat_loc, lon_loc):
    lon_delta = lon_loc - lon_ref
    lat_delta = lat_loc - lat_ref
    angle_deg = 0

    angle_deg = math.degrees(math.atan2(lon_delta, lat_delta))
    return (angle_deg + 360) % 360


def calc_bearing_great_circle(lat_ref, lon_ref, lat_loc, lon_loc):
    y = math.sin(lon_loc - lon_ref) * math.cos(lat_loc)
    x = math.cos(lat_ref) * math.sin(lat_loc) - math.sin(lat_ref) * math.cos(lat_loc) * math.cos(lon_loc - lon_ref)
    brng = math.degrees(math.atan2(y, x))
    return (brng + 360) % 360


def great_circle_distance():
    pass


class HurdatCatalog:
    """
    Class representing a catalog of hurdat hurricanes
    """

    class HurdatStormSystem:
        """
        Class representing a Hurricane from a hurdat data source
        """
        hurdat_headers = ["StormID/Date", "Name/Hour", "Rows/SpecialRow", "System Status", "Lat", "Lon",
                          "Max Wind (kts)", "Min Pressure (mBar)", "R34 NE(Nauts; kts)", "R34 SE (Nauts; kts)",
                          "R34 SW (Nauts; kts)", "R34 NW (Nauts; kts)", "R50 NE (Nauts; kts)", "R50 SE (Nauts; kts)",
                          "R50 SW (Nauts; kts)", "R50 NW (Nauts; kts)", "R64 NE (Nauts; kts)", "R64 SE (Nauts; kts)",
                          "R64 SW (Nauts; kts)", "R64 NW (Nauts; kts)"]
        df_hurdat_headers = ["storm_id/date", "name/time", "records/record_identifier", "system_status", "lat", "lon",
                             "max_wind_kts", "min_pressure_mb", "r34_ne_nmi", "r34_se_nmi", "r34_sw_nmi", "r34_nw_nmi",
                             "r50_ne_nmi", "r500_se_nmi", "r50_sw_nmi", "r50_nw_nmi", "r64_ne_nmi", "r64_se_nmi",
                             "r64_sw_nmi", "r64_nw_nmi"]
        model_headers = ["catalog_number", "name", "basin", "timestamp", "lat_y", "lon_x", "max_wind_kts", "min_cp_mb",
                         "sequence", "is_landfall_point", "rmax_nmi", "fspeed_kts", "gwaf"]
        hurdat_wind_no_data = -99
        hurdat_no_data = -999

        class HurdatTrackPoint:
            """
            Class representing a single track point of a hurdat storm
            """

            def __init__(self, year, month, day, hour, minute, record_identifier, status, lat_y, hemisphere_ns, lon_x,
                         hemisphere_ew, max_wind_kts, min_pressure_mb, r34_ne_nmi, r34_se_nmi, r34_sw_nmi, r34_nw_nmi,
                         r50_ne_nmi, r50_se_nmi, r50_sw_nmi, r50_nw_nmi, r64_ne_nmi, r64_se_nmi, r64_sw_nmi, r64_nw_nmi,
                         sequence):
                """
                :param int year: year of timestamp
                :param int month: month of timestamp
                :param int day: day of timestamp
                :param int hour: hour of timestamp
                :param int minute: minute of timestamp
                :param string record_identifier: Special identifier for track point i.e. landfall point, max wind point, etc.
                :param string status: status identifier for track point, check documentation, not really used currently
                :param float lat_y: latitude in degrees of track point
                :param string hemisphere_ns: whether the latitude is in the northern or southern hemisphere
                :param float lon_x: longitude in degrees of track point
                :param string hemisphere_ew: whether the longitude is in the eastern or western hemisphere
                :param float max_wind_kts: Maximum wind of the track point in knots
                :param float min_pressure_mb: minimum central pressure of track point in milibars
                :r*_*_nmi: parameters for the wind at radius * in each quadrent of the storm
                """
                # Time
                self.year = year
                self.month = month
                self.day = day
                self.hour = hour
                self.minute = minute
                self.timestamp = datetime.datetime(year, month, day, hour, minute)

                # Identifiers
                self.record_identifier = record_identifier
                self.status = status

                # Position
                self.lat_y = lat_y
                self.hemisphere_ns = hemisphere_ns
                self.lon_x = lon_x
                self.hemisphere_ew = hemisphere_ew

                # Intensities
                self.max_wind_kts = max_wind_kts
                self.min_pressure_mb = min_pressure_mb

                # Radius of 34kt winds
                self.r34_ne_nmi = r34_ne_nmi
                self.r34_se_nmi = r34_se_nmi
                self.r34_sw_nmi = r34_sw_nmi
                self.r34_nw_nmi = r34_nw_nmi

                # Radius of 50kt winds
                self.r50_ne_nmi = r50_ne_nmi
                self.r50_se_nmi = r50_se_nmi
                self.r50_sw_nmi = r50_sw_nmi
                self.r50_nw_nmi = r50_nw_nmi

                # Radius of 64kt winds
                self.r64_ne_nmi = r64_ne_nmi
                self.r64_se_nmi = r64_se_nmi
                self.r64_sw_nmi = r64_sw_nmi
                self.r64_nw_nmi = r64_nw_nmi

                self.sequence = sequence
                self.heading_to_next_point = None

            def point_to_xyz(self):
                ret_val = []
                lat = self.lat_y if self.hemisphere_ns == 'N' else self.lat_y * -1
                lon = self.lon_x if self.hemisphere_ew == 'E' else self.lon_x * -1
                val = self.max_wind_kts
                return [lat, lon, val]

            def point_lat_lon(self):
                lat = self.lat_y if self.hemisphere_ns == 'N' else self.lat_y * -1
                lon = self.lon_x if self.hemisphere_ew == 'E' else self.lon_x * -1
                return [lat, lon]

            def for_geojson_point(self):
                lon = self.lon_x if self.hemisphere_ew == 'E' else self.lon_x * -1
                lat = self.lat_y if self.hemisphere_ns == 'N' else self.lat_y * -1
                val = self.max_wind_kts
                return [[lon, lat], val]

            def to_hurdat_list(self):
                """
                return the track point as a list in hurdat format
                """
                return [str(self.year) + str(self.month).zfill(2) + str(self.day).zfill(2)
                        , str(self.hour).zfill(2) + str(self.minute).zfill(2)
                        , self.record_identifier
                        , self.status
                        , str(self.lat_y) + self.hemisphere_ns
                        , str(self.lon_x) + self.hemisphere_ew
                        , self.max_wind_kts
                        , self.min_pressure_mb
                        , self.r34_ne_nmi
                        , self.r34_se_nmi
                        , self.r34_sw_nmi
                        , self.r34_nw_nmi
                        , self.r50_ne_nmi
                        , self.r50_se_nmi
                        , self.r50_sw_nmi
                        , self.r50_nw_nmi
                        , self.r64_ne_nmi
                        , self.r64_se_nmi
                        , self.r64_sw_nmi
                        , self.r64_nw_nmi]

            def to_model_list(self):
                """
                return the track point as a list in model format
                """
                return [self.timestamp.strftime("%Y-%m-%d-%H-%M")
                        , self.lat_y * -1 if self.hemisphere_ns == 'S' else self.lat_y
                        , self.lon_x * -1 if self.hemisphere_ew == 'E' else self.lon_x
                        , self.max_wind_kts
                        , self.min_pressure_mb
                        , self.sequence
                        , 1 if self.record_identifier == "L" else 0]

        def __init__(self, storm_data=None, fspeed_kts=10, rmax_nmi=15, gwaf=0.9):
            """
            Initializer function
            :param list of list storm_data: list of list representing the raw data rows of the storm import file
            :param int fspeed_kts: forward speed of the storm.  This will eventually be calculated at each track point
            :param int rmax_nmi: radius of maximum winds of the storm.  constant for the entiere storm
            :param float gwaf: Gradient Wind Adjustment Factor.  "fudge factor" for hurricane intensity calculation.  standard is 0.9
            """
            self.storm_data = storm_data
            self.fspeed_kts = fspeed_kts
            self.rmax_nmi = rmax_nmi
            self.gwaf = gwaf
            self.basin = None
            self.cyclone_number = None
            self.year = None
            self.name = None
            self.track_point_count = None
            self.track_points = []
            self.source_data = None
            self.lat_lon_grid = None
            self.result_array = None

            self.unique_name = ''

            if storm_data is not None:
                self.parse_storm_data(storm_data)

        def parse_storm_data(self, storm_data):
            """
            Parse a storm data set, formatted as list of lists.  The input data is not altered
            """
            # todo cache the list data
            self.source_data = copy.deepcopy(storm_data)
            # parse storm level parameters from first row of data table
            self.parse_header_row(storm_data[0])

            # drop first row from local copy of the dataframe
            # storm_data.drop(storm_data.index[[0]], inplace = True)
            storm_data.pop(0)
            seq = 0
            # parse data rows
            for row in storm_data[1:]:
                self.parse_data_row(row, seq)
                seq += 1

        def calc_trackpoint_heading(self):
            if len(self.track_points) == 1:
                self.track_points[0].heading_to_next_point = 0
            for i in range(len(self.track_points)):
                if i == len(self.track_points) - 1:
                    self.track_points[i].heading_to_next_point = self.track_points[i-1].heading_to_next_point
                    continue

                next_lat_lng = self.track_points[i+1].point_lat_lon()
                curr_lat_lng = self.track_points[i].point_lat_lon()
                heading = calc_bearing_north_zero(curr_lat_lng[0], curr_lat_lng[1], next_lat_lng[0], next_lat_lng[1])
                self.track_points[i].heading_to_next_point = heading

        def parse_header_row(self, header_row):
            """
            Parse the header row of the hurdat format
            """
            self.basin = header_row[0][:2]
            self.cyclone_number = int(header_row[0][2:4])
            self.year = int(header_row[0][4:])
            self.name = header_row[1]
            self.track_point_count = int(header_row[2])

            self.unique_name = str(self.year) + "_" + str(self.cyclone_number) + "_" + self.name + "_" + self.basin

        def parse_data_row(self, data_row, sequence):
            """
            Parse a track point data row of the hurdat format
            """
            # Time
            year = int(data_row[0][:4])
            month = int(data_row[0][4:6])
            day = int(data_row[0][6:])
            hour = int(data_row[1][:2])
            minute = int(data_row[1][2:])

            # Identifiers
            record_identifier = data_row[2]
            status = data_row[3]

            # Position
            lat_y = float(data_row[4][:-1])
            hemisphere_ns = data_row[4][-1]
            lon_x = float(data_row[5][:-1])
            hemisphere_ew = data_row[5][-1]

            # Intensities
            max_wind_kts = int(data_row[6])  # 1min-10m average
            if max_wind_kts == self.hurdat_wind_no_data:
                max_wind_kts = math.nan

            min_pressure_mb = int(data_row[7])
            if min_pressure_mb == self.hurdat_no_data:
                min_pressure_mb = math.nan

            # Radius of 34kt winds
            r34_ne_nmi = int(data_row[8])
            if r34_ne_nmi == self.hurdat_no_data:
                r34_ne_nmi = math.nan
            r34_se_nmi = int(data_row[9])
            if r34_se_nmi == self.hurdat_no_data:
                r34_se_nmi = math.nan
            r34_sw_nmi = int(data_row[10])
            if r34_sw_nmi == self.hurdat_no_data:
                r34_sw_nmi = math.nan
            r34_nw_nmi = int(data_row[11])
            if r34_nw_nmi == self.hurdat_no_data:
                r34_nw_nmi = math.nan

            # Radius of 50kt winds
            r50_ne_nmi = int(data_row[12])
            if r50_ne_nmi == self.hurdat_no_data:
                r50_ne_nmi = math.nan
            r50_se_nmi = int(data_row[13])
            if r50_se_nmi == self.hurdat_no_data:
                r50_se_nmi = math.nan
            r50_sw_nmi = int(data_row[14])
            if r50_sw_nmi == self.hurdat_no_data:
                r50_sw_nmi = math.nan
            r50_nw_nmi = int(data_row[15])
            if r50_nw_nmi == self.hurdat_no_data:
                r50_nw_nmi = math.nan

            # Radius of 64kt winds
            r64_ne_nmi = int(data_row[16])
            if r64_ne_nmi == self.hurdat_no_data:
                r64_ne_nmi = math.nan
            r64_se_nmi = int(data_row[17])
            if r64_se_nmi == self.hurdat_no_data:
                r64_se_nmi = math.nan
            r64_sw_nmi = int(data_row[18])
            if r64_sw_nmi == self.hurdat_no_data:
                r64_sw_nmi = math.nan
            r64_nw_nmi = int(data_row[19])
            if r64_nw_nmi == self.hurdat_no_data:
                r64_nw_nmi = math.nan
            # create and store track point
            self.track_points.append(
                self.HurdatTrackPoint(year, month, day, hour, minute, record_identifier, status, lat_y, hemisphere_ns,
                                      lon_x, hemisphere_ew, max_wind_kts, min_pressure_mb, r34_ne_nmi, r34_se_nmi,
                                      r34_sw_nmi, r34_nw_nmi, r50_ne_nmi, r50_se_nmi, r50_sw_nmi, r50_nw_nmi,
                                      r64_ne_nmi, r64_se_nmi, r64_sw_nmi, r64_nw_nmi, sequence))

        def header_to_list(self, pad=False):
            """
            Returns the header as a list.  Optionally pads the list to the correct length to put into a hurdat format csv file
            """
            ret = [self.basin + str(self.cyclone_number).zfill(2) + str(self.year)
                   , self.name
                   , str(self.track_point_count)]

            if pad:
                ret.extend(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

            return ret

        def to_hurdat_dataframe(self):
            """
            returns the source hurdat data as a dataframe.  Data is constructed from track points if needed.
            """
            # data = []
            # if(self.source_data == None):
            #    data.append(self.header_to_list(True))
            #    for point in self.track_points:
            #        data.append(point.to_hurdat_list())
            # else:
            #    data = self.source_data

            data = self.source_data
            return pd.DataFrame(data, columns=self.df_hurdat_headers)

        def to_model_dataframe(self):
            data = []
            data_front = [self.cyclone_number
                          , self.name
                          , self.basin]
            data_back = [self.rmax_nmi
                         , self.fspeed_kts
                         , self.gwaf]
            for point in self.track_points:
                temp_row = data_front + point.to_model_list() + data_back
                data.append(temp_row)
            return pd.DataFrame(data, columns=self.model_headers)

        def track_to_xyz_list(self):
            print(str(self.track_points[0].lon_x))
            pass

        def track_to_geojson(self):
            temp_list = list(map((lambda x: x.for_geojson_point()), self.track_points))
            geojson_collection = list(map((lambda x: lm.create_feature(x[0], lm.GeojsonGeometry.point, x[1])['geojson']), temp_list))
            return geojson_collection

        def calculate_grid(self, px_per_deg_x, px_per_deg_y, fspeed_kts, rmax_nmi, bbox=None, do_parallel=False):
            if bbox is None:
                lat_list = list(map(lambda x: x.point_lat_lon()[0], self.track_points))
                lon_list = list(map(lambda x: x.point_lat_lon()[1], self.track_points))
                # diff_lat = max(int(max(lat_list) - min(lat_list)), 1)
                # diff_lon = max(int(max(lon_list) - min(lon_list)), 1)
                diff_lat = 2
                diff_lon = 2
                bbox = geno.BoundingBox(max(lat_list) + diff_lat, min(lat_list) - diff_lat, max(lon_list) + diff_lon, min(lon_list) - diff_lon)
            self.lat_lon_grid = geno.LatLonGrid(bbox.top_lat_y, bbox.bot_lat_y, bbox.left_lon_x, bbox.right_lon_x, px_per_deg_x, px_per_deg_y)

            lat_lon_list = self.lat_lon_grid.get_lat_lon_list()

            results = []

            if not do_parallel:
                results = [self.lat_lon_calc_loop(self.track_points, point[0], point[1], fspeed_kts, rmax_nmi) for point in lat_lon_list]
            else:
                num_procs = max(job.cpu_count() - 1, 1)

                results = job.Parallel(n_jobs=num_procs)(job.delayed(self.lat_lon_calc_loop)(self.track_points, point[0], point[1], fspeed_kts, rmax_nmi) for point in lat_lon_list)
            self.result_array = results

        def lat_lon_calc_loop(self, tps, lat_y, lon_x, fspeed_kts, rmax_nmi):
            max_wind = 0
            for track_point in tps:
                eye_lat_lon = track_point.point_lat_lon()
                angle_to_center = calc_bearing_north_zero(eye_lat_lon[0], eye_lat_lon[1], lat_y, lon_x)
                distance = genu.haversine_degrees_to_meters(lat_y, lon_x, eye_lat_lon[0], eye_lat_lon[1]) / 1000 * 0.539957
                windspeed_temp = hm.calc_windspeed(track_point.min_pressure_mb, distance, eye_lat_lon[0], fspeed_kts, rmax_nmi, angle_to_center, track_point.heading_to_next_point, vmax_kts=track_point.max_wind_kts)
                max_wind = max(max_wind, windspeed_temp)
            return [lat_y, lon_x, max_wind]

        def grid_to_geojson(self):
            if self.result_array is None:
                return None
            # flat_grid = [item for sublist in self.result_array for item in sublist]
            for_geojson_list = list(map((lambda x: [[x[1], x[0]], x[2]]), self.result_array))
            geojson_collection = list(map((lambda x: lm.create_feature(x[0], lm.GeojsonGeometry.point, x[1])['geojson']), for_geojson_list))
            # print(geojson_collection)
            return geojson_collection

    def __init__(self, catalog_file_uri):
        self.catalog_file_uri = catalog_file_uri
        self.storm_catalog = []
        self.storm_data = None

        self.parse_catalog(catalog_file_uri)

    def parse_catalog(self, catalog_file_uri):
        self.storm_data = pd.DataFrame()
        self.storm_data = pd.read_csv(catalog_file_uri)
        self.storm_data = self.storm_data.applymap((lambda x: str.strip(x) if isinstance(x, str) else x))
        # dropping last column because hurdat has trailing commas -.-
        self.storm_data.drop(self.storm_data.columns[-1], 1, inplace=True)
        self.storm_data.fillna('', inplace=True)

        storm_list = self.storm_data.values.tolist()

        storm_temp = None
        catalog_iter = 0
        while catalog_iter < len(storm_list):
            curr_row = storm_list[catalog_iter]

            # if row is header row, 4th element will be empty
            if not curr_row[3]:
                storm_temp = self.HurdatStormSystem()
                storm_temp.parse_header_row(curr_row)
                catalog_iter += 1
                seq = 0
                storm_count = catalog_iter + storm_temp.track_point_count
                while catalog_iter < storm_count:
                    storm_temp.parse_data_row(storm_list[catalog_iter], seq)
                    seq += 1
                    catalog_iter += 1
            storm_temp.calc_trackpoint_heading()
            self.storm_catalog.append(storm_temp)

    def get_names(self):
        return list(map((lambda x: x.unique_name), self.storm_catalog))

    def get_storm_by_name(self, name):
        storm = list(filter((lambda x: x.unique_name == name), self.storm_catalog))
        return storm
