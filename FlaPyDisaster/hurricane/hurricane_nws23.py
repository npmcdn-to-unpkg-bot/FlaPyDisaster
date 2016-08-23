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
Pw_SPH_inhg = 29.77
Pw_PMH_inhg = 30.12
Rho0_kPa = 101.325 # Mean Sea Level Pressure
KmToNmi = 0.539957
MpsToKts = 1.94384
KpaToInhg = 0.2953
DegToRadians

def radial_decay(r_nmi, Rmax_nmi):
    """
    Calculates the radial decay factor for a given radius.
    Rmax_nmi < r_nmi: NWS 23 pdf page 53, page 27, Figure 2.12, emperical fit
    Rmax_nmi > r_nmi: NWS 23 pdf page 54, page 28, Figure 2.13, emperical fit (logistic regression)
    :param r_nmi: Point radius from center of storm in nautical miles
    :param Rmax_nmi: Radius of maximum winds in nautical miles
    """

    ret = 0
    if r_nmi >  Rmax_nmi:
        # NWS 23 pdf page 53
        slope = (-0.051 * math.log(Rmax_nmi)) - 0.1757
        intercept = (0.4244 * math.log(Rmax_nmi)) + 0.7586
        ret = (slope * math.log(r_nmi)) + intercept
    else:
        # NWS 23 pdf page 54
        ret = 1.01231578 / (1 + (-8.612066494 * math.exp(r_nmi - 0.678031222)))

    # keep radial decay between 0 and 1
    ret = max(min(ret, 1), 0)
    return ret

def CoriolisFrequency(lat_deg):
    w = 2.0 * math.pi / 24.0
    return 2.0 * w * math.sin(w)

def GradientWind_AtRadius(Pw_inhg, Cp_inhg, r_nmi, lat_deg):
    """
    NWS 23 pdf page 49, page 23, equation 2.2
    Need to confirm units
    :param Pw: Peripheral Pressure, pressure at edge of storm, should be near MSLP, In. Hg
    :param Cp: Central Pressure in In. Hg
    :param r_nmi: Radius from center of storm in nautical miles.  Use Radius of max winds (Rmax) to get maximum gradient wind
    :param lat_deg: Latitude of hurricane eye
    """

    K = K_WindGradient(lat_deg)
    f = CoriolisFrequency(lat_deg)
    return K * ((Pw_inhg - Cp_inhg) ** 0.5) - (r_nmi * f) / 2

def K_WindGradient(lat_deg):
    """
    NWS 23 pdf page 50, page 24, figure 2.10, emperical relationship (linear regression)
    This is for the PMH, We can also improve this relationship
    This is what I thought, but apparently not: (1.0/(Rho0_kPa * math.e)) ** (0.5)
    lat 24, K 68.1; lat 45, K 65
    SPH: (65-68.1)/(45-24) = -0.147619048
    PMH: (66.2 - 70.1)/(45 - 24) = -0.185714286
    :returns: K factor for kts, In. Hg
    """

    return 70.1 + -0.185714286 * (lat_deg - 24.0)

def AsymmetryFactor(Fspeed_kts, r_nmi, Rmax_nmi, anglecenter_deg):
    """
    NWS 23 pdf page 51, page 25, equation 2.5
    NWS 23 pdf page 281, page 257
    Factor for a moving hurricane, accounts for effect of forward speed on hurricane winds
    To conversion factors: 1 kt, 0.514791 mps, 1.853248 kph, 1.151556 mph
    :param Fspeed_kts: Forward speed of the storm
    :param r_nmi: Radius from the center of the storm in nautical miles
    :param Rmax_nmi: Radius of maximum winds in nautical miles
    :return: Asymmertry factor
    """
    To = 1
    beta = InflowAngle(Rmax_nmi, r_nmi) # need to figure out direction
    return 1.5 * (Fspeed_mph ** 0.63) * (To ** 0.37) * math.cos(math.radians(beta))

def InflowAngle(Rmax_nmi, r_nmi):
    """
    Emperical inflow angle calculation of PMH
    NWS 23 pdf page 55
    NOAA_NWS23_Inflow_Calc.xlsx
    :param Rmax_nmi: Radius of maximum winds in Nautical Miles
    :param r_nmi: Point radius from hurricane center in Nautical Miles
    :return: Inflow angle in degrees
    """
    Phi = None
    RmaxThree = 3 * Rmax_nmi
    if (r_nmi < RmaxThree):
        a = 11.438 * (Rmax_nmi ** -1.416)
        b = (1.1453) * Rmax_nmi + 1.4536
        PhiMax = 9.7043566358 * math.log(RmaxRmax_nmi) - 2.7295806727
        Phi = PhiMax / (1 + math.exp(-1 * a * (r_nmi - b)))
    else:
        x1 = (0.0000896902 * Rmax_nmi * Rmax_nmi) - (0.0036924418 * Rmax_nmi) + 0.0072307906
        x2 = (0.000002966 * Rmax_nmi * Rmax_nmi) - (0.000090532 * Rmax_nmi) - 0.0010373287
        x3 = (-0.0000000592 * Rmax_nmi * Rmax_nmi) + (0.0000019826 * Rmax_nmi) - 0.0000020198
        c = (9.7043566341 * math.log(Rmax_nmi)) - 2.7295806689
        Phi = (x3 * ((r_nmi - RmaxThree)**3)) + (x2 * ((r_nmi - RmaxThree)**2)) + (x1 * (r_nmi - RmaxThree)) + c
    return Phi

def calc_windspeed(Cp_kPa, r_km, lat_deg, Fspeed_mps, Rmax_km, anglecenter_deg, Pw_kPa = Pw_PMH_kPa, Vmax_mps = None, GWAF = 0.9):
    """
    :param Cp_kPa: Central Pressure in kPa
    :param r_mk: Point radius from center of storm in kilometers
    :param lat_deg: Latitude of hurricane eye
    :param Fspeed_mps: Forward speed of the storm in m/s
    :param Pw_kPa: Peripheral Pressure, pressure at edge of storm, should be near MSLP
    :param Rmax_km: Radius of maximum winds in km
    :param anglecenter_deg: Bearing from the eye to the current point in deg
    :param Vmax_mps: Input max windspeed to skip the calculation for it.  Useful when Vmax is know for a storm. m/s
    :param GWAF: Gradient Wind Adjustment Factor, semi-emprical adjustment to the Gradient Wind. Range 0.75-1.05, Generally between 0.9 and 1. NWS 23 pdf page 50, page 24, 2.2.7.2.1
    :return: Windspeed at a given radius for the storm in mps
    """

    r_nmi = r_km * KmToNmi
    Rmax_nmi = Rmax_km * KmToNmi
    Fspeed_kts = Fspeed_mps * MpsToKts
    Cp_inhg = Cp_kPa * KpaToInhg
    Pw_inhg = Pw_kPa * KpaToInhg

    # Step 1: Calculate Maximum Gradient Windspeed if unknown, 10m-10min Average
    Vgx = 0
    if(Vmax == None):
        Vgx = GradientWind_AtRadius(Pw_inhg, Cp_inhg, Rmax_nmi, lat_deg)
    else:
        Vmax_kts = Vmax_mps * MpsToKts
        Vgx = Vmax_kts
    # Step 2: Calculate the Radial Decay
    RadialDecay = radial_decay(r_km, Rmax_km) # need to convert to nmi
    # Step 3: Calculate the Asymmetry Factor
    Asym = AsymmetryFactor(Fspeed_kts, r_nmi, anglecenter_deg)

    # apply all factors and return windspeed at point
    windspeed_kts = (Vgx * GWAF * RadialDecay) + Asym
    return windspeed_kts / MpsToKts