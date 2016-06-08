#############
# Constants #
#############
# Distance
feet_per_meter = 3.28084

# Velocity
mps_per_mph = 0.44704

#####################
# Converion "Enums" #
#####################
class DistanceUnits():
    ft = 'feet'
    m = 'meter'
    km = 'kilometer'

class VelocityUnits():
    kmps = 'km/s'
    mps = 'm/s'
    mph = 'mph'

def distance_conversion(value_in, unit_in, unit_out):
    value_out = None

    if unit_in == DistanceUnits.ft:
        if unit_out == DistanceUnits.ft:
            value_out = value_in
        elif unit_out == DistanceUnits.m:
            value_out = value_in / feet_per_meter
        elif unit_out == DistanceUnits.km:
            value_out = value_in / feet_per_meter / 1000
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    elif unit_in == DistanceUnits.m:
        if unit_out == DistanceUnits.ft:
            value_out = value_in * feet_per_meter
        elif unit_out == DistanceUnits.m:
            value_out = value_in
        elif unit_out == DistanceUnits.km:
            value_out = value_in / 1000
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    elif unit_in == DistanceUnits.km:
        if unit_out == DistanceUnits.ft:
            value_out = value_in * 1000 * feet_per_meter
        elif unit_out == DistanceUnits.m:
            value_out = value_in * 1000
        elif unit_out == DistanceUnits.km:
            value_out = value_in
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    else:
        raise ValueError("Input Unit Not Supported: " + unit_in)
        return None

    return value_out

def velocity_conversion(value_in, unit_in, unit_out):
    value_out = None

    if unit_in == VelocityUnits.mph:
        if unit_out == VelocityUnits.mph:
            value_out = value_in
        elif unit_out == VelocityUnits.mps:
            value_out = value_in / mps_per_mph
        elif unit_out == VelocityUnits.kmps:
            value_out = value_in / mps_per_mph / 1000
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    elif unit_in == VelocityUnits.mps:
        if unit_out == VelocityUnits.mph:
            value_out = value_in * mps_per_mph
        elif unit_out == VelocityUnits.mps:
            value_out = value_in
        elif unit_out == VelocityUnits.kmps:
            value_out = value_in / 1000
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    elif unit_in == VelocityUnits.kmps:
        if unit_out == VelocityUnits.mph:
            value_out = value_in * 1000 * mps_per_mph
        elif unit_out == VelocityUnits.mps:
            value_out = value_in * 1000
        elif unit_out == VelocityUnits.kmps:
            value_out = value_in
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    else:
        raise ValueError("Input Unit Not Supported: " + unit_in)
        return None

    return value_out