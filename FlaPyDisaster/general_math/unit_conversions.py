#############
# Constants #
#############
# Distance
feet_per_meter = 3.28084

# Velocity
mps_per_mph = 0.44704

# Energy
joules_per_megatontnt = 0.000000000000000239

#####################
# Converion "Enums" #
#####################
class DistanceUnits():
    """Enum like class containing the supported distance units"""
    feet = 'ft'
    meter = 'm'
    kilometer = 'km'

    def get_units_list():
        return [DistanceUnits.feet, DistanceUnits.meter, DistanceUnits.kilometer]
    
    def get_pretty_units():
        return ['feet', 'meter', 'kilometer']

class VelocityUnits():
    """Enum like class containing the supported velocity units"""
    kmps = 'km/s'
    mps = 'm/s'
    mph = 'mph'

class EnergyUnits():
    """Enum like class containing the supported energy units"""
    joules = 'J'
    Megaton_TNT = 'Mt-TNT'
    Kiloton_TNT = 'Kt-TNT'

def hello():
    ret_string = "This is the unit conversion package! This will contain some help text."
    print(ret_string)

def distance_conversion(value_in, unit_in, unit_out):
    """Convert value from one supported distance unit to another"""
    value_out = None

    if unit_in == DistanceUnits.feet:
        if unit_out == DistanceUnits.feet:
            value_out = value_in
        elif unit_out == DistanceUnits.meter:
            value_out = value_in / feet_per_meter
        elif unit_out == DistanceUnits.kilometer:
            value_out = value_in / feet_per_meter / 1000
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    elif unit_in == DistanceUnits.meter:
        if unit_out == DistanceUnits.feet:
            value_out = value_in * feet_per_meter
        elif unit_out == DistanceUnits.meter:
            value_out = value_in
        elif unit_out == DistanceUnits.kilometer:
            value_out = value_in / 1000
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    elif unit_in == DistanceUnits.kilometer:
        if unit_out == DistanceUnits.feet:
            value_out = value_in * 1000 * feet_per_meter
        elif unit_out == DistanceUnits.meter:
            value_out = value_in * 1000
        elif unit_out == DistanceUnits.kilometer:
            value_out = value_in
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    else:
        raise ValueError("Input Unit Not Supported: " + unit_in)
        return None

    return value_out

def velocity_conversion(value_in, unit_in, unit_out):
    """Convert value from one supported velocity unit to another"""
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

def energy_conversion(value_in, unit_in, unit_out):
    """Convert value from one supported energy unit to another"""
    value_out = None
    if unit_in == EnergyUnits.joules:
        if unit_out == EnergyUnits.joules:
            value_out = value_in
        elif unit_out == EnergyUnits.Megaton_TNT:
            value_out = value_in * joules_per_megatontnt
        elif unit_out == EnergyUnits.Kiloton_TNT:
            value_out = value_in * joules_per_megatontnt * 1000
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    elif unit_in == EnergyUnits.Megaton_TNT:
        if unit_out == EnergyUnits.joules:
            value_out = value_in / joules_per_megatontnt
        elif unit_out == EnergyUnits.Megaton_TNT:
            value_out = value_in
        elif unit_out == EnergyUnits.Kiloton_TNT:
            value_out = value_in * 1000
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    elif unit_in == EnergyUnits.Kiloton_TNT:
        if unit_out == EnergyUnits.joules:
            value_out = value_in / 1000 / joules_per_megatontnt
        elif unit_out == EnergyUnits.Megaton_TNT:
            value_out = value_in / 1000
        elif unit_out == EnergyUnits.Kiloton_TNT:
            value_out = value_in
        else:
            raise ValueError("Output Unit Not Supported: " + unit_out)
            return None
    else:
        raise ValueError("Input Unit Not Supported: " + unit_in)
        return None

    return value_out