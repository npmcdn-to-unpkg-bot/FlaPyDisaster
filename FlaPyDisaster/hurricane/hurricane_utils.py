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