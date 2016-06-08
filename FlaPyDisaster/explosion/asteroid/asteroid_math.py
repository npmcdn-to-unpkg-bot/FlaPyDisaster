import math
#############
# Constants #
#############
# Joules per megaton tnt
JoulesPerMegatonTNT = 4184000000000000
# Surface atmospheric density, kg/m^3
RhoZero = 1
# Scale height, assumed to be 8000m on average
H = 8000
# Drag coefficient for pre-breakup phase
CD = 2
# "Pancake Factor", represents the ratio of diameter to debris dispersion after airburst
FP = 7
# Pi...
PI = 3.1415

def hello():
    ret_string = "This is the asteroid math package!  Some help info is below."
    print(ret_string)

def KeneticEnergy(impactorDensity_kgpm3, diameter_m, initialVelocity_mps):
    """
    Impact energy in Joules.
    :param impactorDensity_kgpm3: impactor density in kg/m^3
    :param diameter_m: impactor diameter in meters
    :param initialVelocity_mps: initial velocity in m/s
    :returns: Kenitic energy in Joules (kg-m^2/s^2)
    """

    return (PI / 12) * impactorDensity_kgpm3 * (diameter_m ** 3) * (initialVelocity_mps * initialVelocity_mps)

def JoulesToMegatonTNT(energy_j):
    """
    Convert Joules to Megatons TNT.
    :param energy_j: Energy in Joules(kg-m^2/s^2)
    :returns: Energy in Megatons TNT
    """

    return energy_j / JoulesPerMegatonTNT

def ReturnPeriodEarth(energy_j):
    """
    Return period of Asteroid/Comet of a given energy (Megatons TNT) in Years.
    :param energy_j: Energy in Megatons TNT
    :returns: Return period of given energy level in years
    """

    return 109 * (energy_j ** 0.78)

def BreakupAltitude(impactorDensity_kgpm3, diameter_m, velocity_kmps, angle_rad):
    """
    Altitude where air stagnation pressure surpasses Asteriod strength.  Precursor to Airburst.
    :param impactorDensity_kgpm3: Impactor Density in kg/m^3
    :param diameter: Impactor diameter in meters
    :param velocity: impactor velocity in km/s
    :param angle: impactor approach angle above tangent plane in radians. 90 deg, PI/2 is straight down
    :returns: breakup altitude in m.
    """

    Yi = YieldStrength(impactorDensity_kgpm3)
    If = max(IfTerm(impactorDensity_kgpm3, diameter_m, velocity_kmps, angle_rad), 0)
    
    Zstar = 0
    if If <= 1:
        Zstar = -H * ( math.log(Yi / (velocity_kmps * velocity_kmps)) + 1.308 - (0.314 * If) - (1.303 * math.sqrt(1 - If)) )

    return Zstar

def YieldStrength(impactorDensity_kgpm3):
    """
    Yield strength equation for breakup altitude calculation. Only valid for density range 1000 to 8000.
    :param impactorDensity_kgpm3: Impactor density in kg/m^3
    :returns: Yield Strength in Pascals.
    """

    return 10 ** ( 2.107 + (0.0624 * math.sqrt(impactorDensity_kgpm3)) )

def IfTerm(impactorDensity_kgpm3, diameter_m, velocity_mps, angle_rad):
    """
    If term for breakup altitude equation.
    :param impactorDensity_kgpm3: Impactor density in kg/m^3
    :param diameter_m: Impactor diameter in meters
    :param velocity_mps: Impactor velocity in km/s
    :param angle_rad: impactor approach angle above tangent plane in radians. 90 deg, PI/2 is straight down
    :returns: If term for breakup altitude equation
    """

    numerator = 4.07 * CD * H * YieldStrength(impactorDensity_kgpm3)
    denominator = impactorDensity_kgpm3 * diameter_m * (velocity_mps * velocity_mps) * math.sin(angle_rad)
    return numerator / denominator

def AirburstAltitude(breakupAltitude_m, diameter_m, impactorDensity_kgpm3, angle_rad):
    """
    Altitude of Airburst, occurs after Breakup.
    :param breakupAltitude_m: Breakup Altitude in meters
    :param diameter_m: Impactor diameter in meters
    :param impactorDensity_kgpm3: Impactor diameter in kg/m^3
    :param angle_rad: impactor approach angle above tangent plane in radians. 90 deg, PI/2 is straight down
    :returns: Airbust height in meters.  If zero, there is no airburst
    """

    AirDensityAtBreakup = RhoZero * math.exp(-1 * breakupAltitude_m / H)
    L = diameter_m * math.sin(angle_rad) * math.sqrt(impactorDensity_kgpm3 / (CD * AirDensityAtBreakup))
    SecondTerm = 2 * H * math.log( 1 + ((L / (2 * H)) * math.sqrt((FP * FP) - 1)))

    if breakupAltitude_m > SecondTerm:
        return breakupAltitude_m - SecondTerm
    else:
        return 0

def NewmarkOverpressure(energy_tnt, radius_km):
    """
    Newmark-Hansen Overpressure formula.  Intended for surface blasts, but adapted to air-bursts.
    :param energy_j: Energy in Megatons TNT
    :param radius_km: Actual distance from blast in km
    """

    energy_tnt = energy_tnt * 1000000
    radius_m = radius_km * 1000
    return (6784 * (energy_tnt / math.pow(radius_m, 3))) + (93 * (math.pow((energy_tnt / math.pow(radius_m, 3)), 0.5)))

def RadiusFromOverpressure(overpressure_bar, energy_tnt, radiusUpperBound_km = 1000, errorThreshold = 0.0001, maxInterations = 100):
    """
    Find the radius of a given overpressure for a given event energy.  Lower limit of 1 
    Uses a bisection search to solve the Newmark-Hansen Ovepressure Formula
    :param overpressure_bar: Overpressure in Bars
    :param energy_tnt: Energy in Megatons TNT
    :param radiusUpperBound_km: Upper bound for radius in kilometers. Default value of 1000 km
    :param errorThreshold: Error threshold (percentage) to stop bisection search at. Default value of 0.0001
    :param maxInterations: Maximum number of bisection search iterations to run. Default value of 100
    """

    XUpper = radiusUpperBound_km
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
            return XMid

        iter = iter + 1

        if Error <= errorThreshold or iter > maxInterations:
            return XMid

def FindHypotenuseRightTriangle(side1, side2):
    """
    Find the hypotenuse of a triangle.
    :returns: Hypotenuse or -1 if error
    """
    if (Side1 != 0 and Side2 != 0):
        return math.sqrt( (Side1 * Side1) + (Side2 * Side2) )
    else:
        return -1

def FindBottomRightTriangle(Height, Hypotenuse):
    """
    Find third non-hypotenuse side of a triangle.
    :returns: Side length or -1 if error
    """
    if (Height != 0 and Hypotenuse != 0 and Hypotenuse > Height):
        return math.sqrt( (Hypotenuse * Hypotenuse) - (Height * Height) )
    else:
        return -1

def GeneralBombEquation(mass_kg, radius_m):
    """
    General Sadovsky bomb overpressure equation, surface explosion at standard atmospheric condidtions.
    :param mass_kg: Mass in kg TNT
    :param radius_m: Distance from explosion in meters
    :returns: Overpressure in atmospheres
    """
    if (dRadiusM == 0 or mass_Kg == 0):
        return -1
    return ( (0.95 * (math.pow(mass_kg, .33333) / radius_m))
            + (3.9 * math.pow( (mass_kg * mass_kg), .33333 ) / (radius_m * radius_m))
            + (13.0 * mass_kg / math.pow(radius_m, 3.0)) )