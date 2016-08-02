import math
"""
SPH: Standard Project Hurricane
PMH: Probable Maximum Hurricane

Pressure profile equation

(p-Cp)/(Pw - Cp) = e ^ (-R/r)

Pw: Peripheral Pressure, pressure at edge of storm, should be a bit below MSLP
Cp: Central Pressure (P0 in paper)
Rmax: Radius of Maximum Winds (R in paper)
Fspeed: Forward speed of hurricane center (T in paper)
Dir: Track direction
Vgx: Maximum Gradient Winds
Rho0: Surace air density
r: distance (radius) from hurricane center
fcorr: Coriolis parameter, dependant on latitude
Vx: Observed maximum 10-m, 10-min winds over open water.  75% to 105% of Vgx.  Standard is 95%
    For moving hurricane: Vx = 0.95 * Vgx + (1.5 * T ^ 0.63 * To ^ 0.37 * cos(beta)
Vpt: 10m, 10min winds at a point (V in paper)
"""
Pw_SPH_kPa = 100.8
Pw_PMH_kPa = 102.0
Rho0_kPa = 101.325 # Mean Sea Level Pressure

def radial_decay(r, Rmax):
    """
    Calculates the radial decay factor for a given radius.
    Both parameters must be in the same units
    Rmax < r: NWS 23 pdf page 53, page 27, Figure 2.12, emperical fit
    Rmax > r: NWS 23 pdf page 54, page 28, Figure 2.13, emperical fit (logistic regression)
    :param r: Distance from the center of the storm
    :param Rmax: Radius of maximum winds
    """
    DistanceRatio = r / Rmax

    ret = 0
    if DistanceRatio > 1:
        # NWS 23 pdf page 53
        slope = (-0.051 * math.log(Rmax)) + -0.1757
        intercept = (0.4244 * math.log(Rmax)) + 0.7586
        ret = (slope * math.log(DistanceRatio)) + intercept
    else:
        # NWS 23 pdf page 54
        ret = 1.2203 / (1 + (160.21 * math.exp(-6.8702 * DistanceRatio)))

    # keep radial decay between 0 and 1
    ret = max(min(ret, 1), 0)
    return ret

def CoriolisFrequency(lat_deg):
    w = 2.0 * math.pi / 24.0
    return 2.0 * w * math.sin(w)

def GradientWind_AtRadius(Pw_kPa, Cp_kPa, r_km, lat_deg):
    """
    NWS 23 pdf page 49, page 23, equation 2.2
    Need to confirm units
    :param Pw: Peripheral Pressure, pressure at edge of storm, should be near MSLP
    :param Cp: Central Pressure
    :param r: Radius (distance) from center of storm.  Use Radius of max winds (Rmax) to get maximum gradient wind
    :param lat_deg: Latitude of hurricane eye
    """

    K = K_WindGradient(lat_deg)
    f = CoriolisFrequency(lat_deg)
    return K * ((Pw - Cp) ** 0.5) - (r * f) / 2

def K_WindGradient(lat_deg):
    """
    NWS 23 pdf page 50, page 24, figure 2.10, emperical relationship (linear regression)
    This is for the PMH, We can also improve this relationship
    This is what I thought, but apparently not: (1.0/(Rho0_kPa * math.e)) ** (0.5)
    lat 24, K 68.1; lat 45, K 65
    SPH: (65-68.1)/(45-24) = -0.147619048
    PMH: (66.2 - 70.1)/(45 - 24) = -0.185714286
    """

    return 70.1 + -0.185714286 * (lat_deg - 24.0)

def AsymmetryFactor(Fspeed_mps, r):
    """
    NWS 23 pdf page 51, page 25, equation 2.5
    Factor for a moving hurricane, accounts for effect of forward speed on hurricane winds
    :param Fspeed_mps: Forward speed of the storm
    :param r: distance from the center of the storm
    To conversion factors: 1 kt, 0.514791 mps, 1.853248 kph, 1.151556 mph
    WindAngle_deg: Angle between the track direction and surface wind direction
    :return: Asymmertry factor
    """
    To = 0.514791
    beta = InflowAngle()
    return 1.5 * (Fspeed_mps ** 0.63) * (To ** 0.37) * math.cos(beta)

def InflowAngle():
    """
    Need imperical inflow angle calculation
    NWS 23 pdf page 55
    """
    pass

def calc_windspeed(Pw_kPa, Cp_kPa, r_km, lat_deg, Fspeed_mps, Rmax_km, Vmax_mps = None, GWAF = 0.9):
    """
    :param Pw: Peripheral Pressure, pressure at edge of storm, should be near MSLP
    :param Cp: Central Pressure
    :param r: Radius (distance) from center of storm
    :param lat_deg: Latitude of hurricane eye
    :param Fspeed_mps
    :param Vmax: Input max windspeed to skip the calculation for it.  Useful when Vmax is know for a storm
    :param GWF: Gradient Wind Adjustment Factor, semi-emprical adjustment to the Gradient Wind. Range 0.75-1.05, Generally between 0.9 and 1. NWS 23 pdf page 50, page 24, 2.2.7.2.1
    :return: Windspeed at a given radius for the storm
    """

    # Step 1: Calculate Maximum Gradient Windspeed if unknown, 10m-10min Average
    if(Vmax == None):
        Vgx = GradientWind_AtRadius(Pw_kPa, Cp_kPa, Rmax_km, lat_deg)
    else:
        Vgx = Vmax
    # Step 2: Calculate the Radial Decay
    RadialDecay = radial_decay(r_km, Rmax_km)
    # Step 3: Calculate the Asymmetry Factor
    Asym = AsymmetryFactor(Fspeed_mps, r_km)

    # apply all factors and return windspeed at point
    return (Vgx * GWAF * RadialDecay) + Asym
