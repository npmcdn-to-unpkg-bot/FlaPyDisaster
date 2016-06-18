import math

def hello():
    ret_string = "This is the explosion math package!  Some help info is below."
    print(ret_string)

def GeneralBombEquation(mass_kg, radius_m):
    """
    General Sadovsky bomb overpressure equation, surface explosion at standard atmospheric condidtions.
    :param mass_kg: Mass in kg TNT
    :param radius_m: Distance from explosion in meters
    :returns: Overpressure in atmospheres
    :Reference: BlastEffectCalculation.pdf, Equation 2
    """
    if (dRadiusM == 0 or mass_Kg == 0):
        return -1
    return ( (0.95 * (math.pow(mass_kg, .33333) / radius_m))
            + (3.9 * math.pow( (mass_kg * mass_kg), .33333 ) / (radius_m * radius_m))
            + (13.0 * mass_kg / (radius_m ** 3.0)) )

def NewmarkOverpressure(energy_MtTnt, radius_m):
    """
    Newmark-Hansen Overpressure formula.  Intended for surface blasts, but adapted to air-bursts.
    :param energy_MtTnt: Energy in Megatons TNT
    :param radius_m: Actual distance from blast in m (hypotenuse distance for airburst events).
    :returns: overpressure in bar
    :Reference: NuclearBlastOverpressure.pdf, Equation 3
    """

    energy_tnt = energy_MtTnt * 1000000
    return ( 6784 * (energy_tnt / (radius_m ** 3)) ) + ( 93 * (math.sqrt(energy_tnt / (radius_m ** 3))) )

def RadiusFromOverpressure(overpressure_bar, energy_tnt, radiusUpperBound_km = 1000, errorThreshold = 0.0001, maxInterations = 100):
    """
    Find the radius of a given overpressure for a given event energy.  Lower limit of 0 
    Uses a bisection search to solve the Newmark-Hansen Ovepressure Formula
    :param overpressure_bar: Overpressure in Bars
    :param energy_tnt: Energy in Megatons TNT
    :param radiusUpperBound_km: Upper bound for radius in kilometers. Default value of 1000 km
    :param errorThreshold: Error threshold (percentage) to stop bisection search at. Default value of 0.0001
    :param maxInterations: Maximum number of bisection search iterations to run. Default value of 100
    :returns: Radius in km and calculation error in a tuple, in that order
    """

    XUpper = radiusUpperBound_km * 1000
    XLower = 0.1
    XMid = 0

    YMid = 0
    XOld = 1
    iter = 0
    Error = 100

    while True:
        XMid = (XUpper + XLower / 2)
        Ymid = NewmarkOverpressure(energy_tnt, XMid)

        if XMid != 0:
            Error = math.abs((XMid - XOld) / XMid) * 100

        if YMid < overpressure_bar:
            Xupper = XMid

        elif YMid  > overpressure_bar:
            XLower = XMid
        else:
            return (XMid/1000, Error)

        iter = iter + 1

        if Error <= errorThreshold or iter > maxInterations:
            return (XMid/1000, Error)
