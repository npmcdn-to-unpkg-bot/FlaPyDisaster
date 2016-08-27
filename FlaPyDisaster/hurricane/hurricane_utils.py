import datetime
from collections import namedtuple
import pandas as pd
import csv 
import copy
def load_hurdat():
    pass


def CalcBearing_NorthZero(lat_ref, lon_ref, lat_loc, lon_loc):
    lon_delta = lon_loc - lon_ref
    lat_delta = lat_loc - lat_ref
    angle_deg = 0

    if(math.fabs(lon_delta < 0.0001)):
        angle_deg = 180 if lat_loc < lat_ref else 0
    else:
        if(math.fabs(lat_delta) < 0.0001):
            angle_deg = -90 if lon_loc < lon_ref else 90
        else:
            angle_deg = math.radians( math.atan(lon_delta / lat_delta) )
            
            if(angle_deg > 0):
                angle_deg = (angle_deg - 180) if (lat_loc < lat_ref) else angle_deg
            else:
                angle_deg = (angle_deg + 180) if (lat_loc < lat_ref) else angle_deg

    return angle_deg

def GreatCircleDistance():
    pass

class HurdatCatalog:
    """
    Class representing a catalog of hurdat hurricanes
    """
    class HurdatStormSystem:
        """
        Class representing a Hurricane from a hurdat data source
        """
        hurdat_headers = ["StormID/Date", "Name/Hour", "Rows/SpecialRow", "System Status", "Lat", "Lon", "Max Wind (kts)", "Min Pressure (mBar)", "R34 NE(Nauts; kts)", "R34 SE (Nauts; kts)", "R34 SW (Nauts; kts)", "R34 NW (Nauts; kts)", "R50 NE (Nauts; kts)", "R50 SE (Nauts; kts)", "R50 SW (Nauts; kts)", "R50 NW (Nauts; kts)", "R64 NE (Nauts; kts)", "R64 SE (Nauts; kts)", "R64 SW (Nauts; kts)", "R64 NW (Nauts; kts)"]
        df_hurdat_headers = ["storm_id/date", "name/time", "records/record_identifier", "system_status", "lat", "lon", "max_wind_kts", "min_pressure_mb", "r34_ne_nmi", "r34_se_nmi", "r34_sw_nmi", "r34_nw_nmi", "r50_ne_nmi", "r500_se_nmi", "r50_sw_nmi", "r50_nw_nmi", "r64_ne_nmi", "r64_se_nmi", "r64_sw_nmi", "r64_nw_nmi"]
        model_headers = ["catalog_number", "name", "basin", "year", "month", "day", "hour", "minute", "lat_y", "lon_x", "max_wind_kts", "min_cp_mb", "rmax_nmi", "fspeed_kts", "sequence", "gwaf"]
        #RecordIdentifier = namedtuple('RecordIdentifier', ['C', 'G', 'I', 'L', 'P', 'R', 'S', 'T', 'W'])

        #class RecordIdentifier:
        #    C = ('C', "Closest approach to a coast, not followed by a landfall")
        #    G = ('G', "Genesis")
        #    I = ('I', "An intensity peak in terms of both pressure and wind")
        #    L = ('L', "Landfall (center of system crossing a coastline)")
        #    P = ('P', "Minimum in central pressure")
        #    R = ('R', "Provides additional detail on the intensity of the cyclone when rapid changes are underway")
        #    S = ('S', "Change of status of the system")
        #    T = ('T', "Provides additional detail on the track (position) of the cyclone")
        #    W = ('W', "Maximum sustained wind speed")
        #    def __init__(self, identifier):
        #        self.identifier = identifier

        #    def ParseIdentifier(self, identifier):
        #        if(identifier == C[0]):
        #            return
            

        #class SystemStatus:
        #    TD = "Tropical cyclone of tropical depression intensity (< 34 knots)"
        #    TS = "Tropical cyclone of tropical storm intensity (34-63 knots)"
        #    HU = "Tropical cyclone of hurricane intensity (> 64 knots)"
        #    EX = "Extratropical cyclone (of any intensity)"
        #    SD = "Subtropical cyclone of subtropical depression intensity (< 34 knots)"
        #    SS = "Subtropical cyclone of subtropical storm intensity (> 34 knots)"
        #    LO = "A low that is neither a tropical cyclone, a subtropical cyclone, nor an extratropical cyclone (of any intensity)"
        #    WV = "Tropical Wave (of any intensity)"
        #    DB = "Disturbance (of any intensity)"

        class TrackPoint:
            """
            Class representing a single track point of a hurdat storm
            """
            def __init__(self, year, month, day, hour, minute, record_identifier, status, lat_y, hemisphere_ns, lon_x, hemisphere_ew, max_wind_kts, min_pressure_mb, r34_ne_nmi, r34_se_nmi, r34_sw_nmi, r34_nw_nmi, r50_ne_nmi, r50_se_nmi, r50_sw_nmi, r50_nw_nmi, r64_ne_nmi, r64_se_nmi, r64_sw_nmi, r64_nw_nmi, sequence ):
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
            
            def to_hurdat_list(self):
                """
                return the track point as a list in hurdat format
                """
                return [str(self.year) + str(self.month).zfill(2) + str(self.day).zfill(2)
                        ,str(self.hour).zfill(2) + str(self.minute).zfill(2)
                        ,self.record_identifier
                        ,self.status
                        ,str(self.lat_y) + self.hemisphere_ns
                        ,str(self.lon_x) + self.hemisphere_ew
                        ,self.max_wind_kts
                        ,self.min_pressure_mb
                        ,self.r34_ne_nmi
                        ,self.r34_se_nmi
                        ,self.r34_sw_nmi
                        ,self.r34_nw_nmi
                        ,self.r50_ne_nmi
                        ,self.r50_se_nmi
                        ,self.r50_sw_nmi
                        ,self.r50_nw_nmi
                        ,self.r64_ne_nmi
                        ,self.r64_se_nmi
                        ,self.r64_sw_nmi
                        ,self.r64_nw_nmi ]

            def to_model_list(self):
                """
                return the track point as a list in model format
                """
                return [self.year
                        ,self.month
                        ,self.day
                        ,self.hour
                        ,self.minute
                        ,self.lat_y * -1 if self.hemisphere_ns == 'S' else self.lat_y
                        ,self.lon_x * -1 if self.hemisphere_ew == 'E' else self.lon_x
                        ,self.max_wind_kts
                        ,self.min_pressure_mb
                        ,self.sequence ]

        def __init__(self, storm_data = None, fspeed_kts = 10, rmax_nmi = 15, gwaf = 0.9):
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

            if(storm_data != None):
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

            # parse data rows
            for row in storm_data[1:]:
               parse_data_row(row)

        def parse_header_row(self, header_row):
            """
            Parse the header row of the hurdat format
            """
            self.basin = header_row[0][:2]
            self.cyclone_number = int(header_row[0][2:4])
            self.year = int(header_row[0][4:])
            self.name = header_row[1]
            self.track_point_count = int(header_row[2])

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
            max_wind_kts = int(data_row[6])
            min_pressure_mb = int(data_row[7])

            # Radius of 34kt winds
            r34_ne_nmi = int(data_row[8])
            r34_se_nmi = int(data_row[9])
            r34_sw_nmi = int(data_row[10])
            r34_nw_nmi = int(data_row[11])

            # Radius of 50kt winds
            r50_ne_nmi = int(data_row[12])
            r50_se_nmi = int(data_row[13])
            r50_sw_nmi = int(data_row[14])
            r50_nw_nmi = int(data_row[15])

            # Radius of 64kt winds
            r64_ne_nmi = int(data_row[16])
            r64_se_nmi = int(data_row[17])
            r64_sw_nmi = int(data_row[18])
            r64_nw_nmi = int(data_row[19])
            # create and store track point
            self.track_points.append(self.TrackPoint(year, month, day, hour, minute, record_identifier, status, lat_y, hemisphere_ns, lon_x, hemisphere_ew, max_wind_kts, min_pressure_mb, r34_ne_nmi, r34_se_nmi, r34_sw_nmi, r34_nw_nmi, r50_ne_nmi, r50_se_nmi, r50_sw_nmi, r50_nw_nmi, r64_ne_nmi, r64_se_nmi, r64_sw_nmi, r64_nw_nmi, sequence))

        def header_to_list(self, pad=False):
            """
            Returns the header as a list.  Optionally pads the list to the correct length to put into a hurdat format csv file
            """
            ret =[self.basin + str(self.cyclone_number).zfill(2) + str(self.year)
                  ,self.name
                  ,str(self.track_point_count)]

            if pad:
                ret.append['','','','','','','','','','','','','','','','','']

            return ret

        def to_hurdat_dataframe(self):
            """
            returns the source hurdat data as a dataframe.  Data is constructed from track points if needed.
            """
            data = []
            #if(self.source_data == None):
            #    data.append(self.header_to_list(True))
            #    for point in self.track_points:
            #        data.append(point.to_hurdat_list())
            #else:
            #    data = self.source_data

            data = self.source_data
            return pd.DataFrame(data, columns=self.df_hurdat_headers)
   
        def to_model_dataframe(self):
            data = []
            data_front = [self.name
                          ,self.cyclone_number
                          ,self.basin]
            data_back = [self.rmax_nmi
                         ,self.fspeed_kts
                         ,self.gwaf]
            for point in self.track_points:
                temp_row = data_front + point.to_model_list() + data_back
                data.append(temp_row)
            return pd.DataFrame(data, columns=self.model_headers)

    def __init__(self, catalog_file_uri):
        self.catalog_file_uri = catalog_file_uri
        self.storm_catalog = []
        self.storm_data = None

        self.parse_catalog(catalog_file_uri)

    def parse_catalog(self, catalog_file_uri):
        self.storm_data = pd.DataFrame()
        self.storm_data = pd.read_csv(catalog_file_uri)
        self.storm_data = self.storm_data.applymap((lambda x:  str.strip(x) if isinstance(x, str) else x))
        self.storm_data.drop(self.storm_data.columns[-1], 1, inplace=True) # dropping last column because hurdat has trailing commas -.-
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
            
            self.storm_catalog.append(storm_temp)

