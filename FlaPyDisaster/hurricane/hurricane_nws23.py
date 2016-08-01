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

def radial_decay(Rmax, r):
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

def MaximumGradientWind_AtRadius(Pw, Cp, r, lat_deg):
    K = K_WindGradient(lat_deg)
    f = CoriolisFrequency(lat_deg)
    return K * ((Pw - Cp) ** 0.5) - (r * f)/2

def K_WindGradient(lat_deg):
    """
    This is for the PMH
    This is what I thought, but apparently not: (1.0/(Rho0_kPa * math.e)) ** (0.5)
    lat 24, K 68.1; lat 45, K 65
    SPH: (65-68.1)/(45-24) = -0.147619048
    PMH: (66.2 - 70.1)/(45 - 24) = -0.185714286
    """

    return 70.1 + -0.185714286 * (lat_deg - 24.0)

def AsymmetryFactor(Fspeed_mps, r, ):
    """
    To factors: 1 kt, 0.514791 mps, 1.853248 kph, 1.151556 mph
    WindAngle_deg: Angle between the track direction and surface wind direction
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

def ObMaxWind_10m10min_AtRadius(Cp, r, lat_deg, Fspeed_mps, GWRF = 0.95):
    Vs = MaximumGradientWind_AtRadius(Cp, r, lat_deg)
    A = AsymmetryFactor(Fspeed_mps, 0.0)
    return (GWRF * Vs) + A