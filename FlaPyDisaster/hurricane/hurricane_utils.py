import datetime
from collections import namedtuple
import pandas as pd
import csv 
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
    class HurdatStormSystem:
        column_headers = ["StormID/Date", "Name/Hour", "Rows/SpecialRow", "System Status", "Lat", "Lon", "Max Wind (kts)", "Min Pressure (mBar)", "R34 NE(Nauts; kts)", "R34 SE (Nauts; kts)", "R34 SW (Nauts; kts)", "R34 NW (Nauts; kts)", "R50 NE (Nauts; kts)", "R50 SE (Nauts; kts)", "R50 SW (Nauts; kts)", "R50 NW (Nauts; kts)", "R64 NE (Nauts; kts)", "R64 SE (Nauts; kts)", "R64 SW (Nauts; kts)", "R64 NW (Nauts; kts)"]
        df_headers = ["date", "hour_min", "record_identifier", "system_status", "lat", "lon", "max_wind_kts", "min_pressure_mb", "r34_ne_nmi", "r34_se_nmi", "r34_sw_nmi", "r34_nw_nmi", "r50_ne_nmi", "r500_se_nmi", "r50_sw_nmi", "r50_nw_nmi", "r64_ne_nmi", "r64_se_nmi", "r64_sw_nmi", "r64_nw_nmi"]
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
            def __init__(self, year, month, day, hour, minute, record_identifier, status, lat_y, hemisphere_ns, lon_x, hemisphere_ew, max_wind_kts, min_pressure_mb, r34_ne_nmi, r34_se_nmi, r34_sw_nmi, r34_nw_nmi, r50_ne_nmi, r50_se_nmi, r50_sw_nmi, r50_nw_nmi, r64_ne_nmi, r64_se_nmi, r64_sw_nmi, r64_nw_nmi ):
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

        def __init__(self, storm_data = None):
            self.storm_data = storm_data
            self.basin = None
            self.cyclone_number = None
            self.year = None
            self.name = None
            self.track_point_count = None
            self.track_points = []

            if(storm_data != None):
                self.parse_data_table(storm_data)

        def parse_data_table(self, df):
            storm_data = pd.DataFrame() # for intellisense hints
            storm_data = df
            
            # parse storm level parameters from first row of data table
            self.parse_header_row(storm_data.iloc[[0]])

            # drop first row from local copy of the dataframe
            storm_data.drop(storm_data.index[[0]], inplace = True)

            # parse data rows
            for row in storm_data.iterrows():
               parse_data_row(row)

        def parse_header_row(self, header_row):
            self.basin = header_row.iloc[0, 0][:2]
            self.cyclone_number = int(header_row.iloc[0, 0][2:4])
            self.year = int(header_row.iloc[0, 0][4:])
            self.name = header_row.iloc[0, 1]
            self.track_point_count = int(header_row.iloc[0, 2])

        def parse_data_row(self, data_row):
             # Time
                year = int(data_row.iloc[0, 0][:4])
                month = int(data_row.iloc[0, 0][4:6])
                day = int(data_row.iloc[0, 0][6:])
                hour = int(data_row.iloc[0, 1][:2])
                minute = int(data_row.iloc[0, 1][2:])

                # Identifiers
                record_identifier = data_row.iloc[0, 2]
                status = data_row.iloc[0, 3]

                # Position
                lat_y = float(data_row.iloc[0, 4][:-1])
                hemisphere_ns = data_row.iloc[0, 4][-1]
                lon_x = float(data_row.iloc[0, 5][:-1])
                hemisphere_ew = data_row.iloc[0, 5][-1]

                # Intensities
                max_wind_kts = int(data_row.iloc[0, 6])
                min_pressure_mb = int(data_row.iloc[0, 7])

                # Radius of 34kt winds
                r34_ne_nmi = int(data_row.iloc[0, 8])
                r34_se_nmi = int(data_row.iloc[0, 9])
                r34_sw_nmi = int(data_row.iloc[0, 10])
                r34_nw_nmi = int(data_row.iloc[0, 11])

                # Radius of 50kt winds
                r50_ne_nmi = int(data_row.iloc[0, 12])
                r50_se_nmi = int(data_row.iloc[0, 13])
                r50_sw_nmi = int(data_row.iloc[0, 14])
                r50_nw_nmi = int(data_row.iloc[0, 15])

                # Radius of 64kt winds
                r64_ne_nmi = int(data_row.iloc[0, 16])
                r64_se_nmi = int(data_row.iloc[0, 17])
                r64_sw_nmi = int(data_row.iloc[0, 18])
                r64_nw_nmi = int(data_row.iloc[0, 19])
                # create and store track point
                self.track_points.append(self.TrackPoint(year, month, day, hour, minute, record_identifier, status, lat_y, hemisphere_ns, lon_x, hemisphere_ew, max_wind_kts, min_pressure_mb, r34_ne_nmi, r34_se_nmi, r34_sw_nmi, r34_nw_nmi, r50_ne_nmi, r50_se_nmi, r50_sw_nmi, r50_nw_nmi, r64_ne_nmi, r64_se_nmi, r64_sw_nmi, r64_nw_nmi))

    def __init__(self, catalog_file_uri):
        self.catalog_file_uri = catalog_file_uri
        self.storm_catalog = []
        self.storm_data = None

        self.parse_catalog(catalog_file_uri)

    def parse_catalog(self, catalog_file_uri):
        self.storm_data = pd.DataFrame()
        self.storm_data = pd.read_csv(catalog_file_uri)
        self.storm_data = self.storm_data.applymap((lambda x:  str.strip(x) if isinstance(x, str) else x))
        self.storm_data.drop(self.storm_data.columns[-1], 1, inplace=True)
        self.storm_data.fillna('', inplace=True)

        storm_temp = None
        catalog_iter = 0
        while catalog_iter < len(self.storm_data):

            curr_row = self.storm_data.iloc[[catalog_iter]]

            # if row is header row, 4th element will be empty
            if not curr_row.iloc[0, 3]:
                storm_temp = self.HurdatStormSystem()
                storm_temp.parse_header_row(curr_row)
                catalog_iter += 1

                storm_count = catalog_iter + storm_temp.track_point_count
                while catalog_iter < storm_count:
                    storm_temp.parse_data_row(self.storm_data.iloc[[catalog_iter]])
                    catalog_iter += 1
            
            self.storm_catalog.append(storm_temp)

