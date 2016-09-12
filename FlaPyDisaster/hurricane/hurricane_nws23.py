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
Rho0_kPa = 101.325  # Mean Sea Level Pressure
KmToNmi = 0.539957
MpsToKts = 1.94384
KpaToInhg = 0.2953
MbToInhg = 0.02953


def radial_decay(r_nmi, rmax_nmi):
    """
    Calculates the radial decay factor for a given radius.
    Rmax_nmi < r_nmi: NWS 23 pdf page 53, page 27, Figure 2.12, emperical fit
    Rmax_nmi > r_nmi: NWS 23 pdf page 54, page 28, Figure 2.13, emperical fit (logistic regression)
    :param r_nmi: Point radius from center of storm in nautical miles
    :param rmax_nmi: Radius of maximum winds in nautical miles
    """

    ret = 0
    if r_nmi > rmax_nmi:
        # NWS 23 pdf page 53
        slope = (-0.051 * math.log(rmax_nmi)) - 0.1757
        intercept = (0.4244 * math.log(rmax_nmi)) + 0.7586
        ret = (slope * math.log(r_nmi)) + intercept
    else:
        # NWS 23 pdf page 54
        ret = 1.01231578 / (1 + (-8.612066494 * math.exp(r_nmi - 0.678031222)))

    # keep radial decay between 0 and 1
    ret = max(min(ret, 1), 0)
    return ret


def coriolis_frequency(lat_deg):
    w = 2.0 * math.pi / 24.0
    return 2.0 * w * math.sin(lat_deg)


def gradient_wind_at_radius(pw_inhg, cp_inhg, r_nmi, lat_deg):
    """
    NWS 23 pdf page 49, page 23, equation 2.2
    Need to confirm units
    :param pw_inhg: Peripheral Pressure, pressure at edge of storm, should be near MSLP, In. Hg
    :param cp_inhg: Central Pressure in In. Hg
    :param r_nmi: Radius from center of storm in nautical miles.  Use Radius of max winds (Rmax) to get maximum gradient wind
    :param lat_deg: Latitude of hurricane eye
    """

    k = k_wind_gradient(lat_deg)
    f = coriolis_frequency(lat_deg)
    return k * ((pw_inhg - cp_inhg) ** 0.5) - (r_nmi * f) / 2


def k_wind_gradient(lat_deg):
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


def asymmetry_factor(fspeed_kts, r_nmi, rmax_nmi, angle_from_center, track_bearing):
    """
    NWS 23 pdf page 51, page 25, equation 2.5
    NWS 23 pdf page 263, page 269
    NWS 23 pdf page 281, page 257
    Factor for a moving hurricane, accounts for effect of forward speed on hurricane winds
    To conversion factors: 1 kt, 0.514791 mps, 1.853248 kph, 1.151556 mph
    :param fspeed_kts: Forward speed of the storm
    :param r_nmi: Radius from the center of the storm in nautical miles
    :param rmax_nmi: Radius of maximum winds in nautical miles
    :param angle_from_center: int
    :param track_bearing: int
    :return: Asymmetry factor
    """
    to = 1
    phi_r = inflow_angle(rmax_nmi, r_nmi)  # need to figure out direction
    phi_rmax = inflow_angle(rmax_nmi, rmax_nmi)  # need to figure out direction
    beta = (phi_r - phi_rmax) % 360
    bearing_shift = (90 - angle_from_center + track_bearing) % 360
    beta = (beta + bearing_shift) % 360
    asym = 1.5 * (fspeed_kts ** 0.63) * (to ** 0.37) * math.cos(math.radians(beta))

    return asym
    # return beta


def inflow_angle(rmax_nmi, r_nmi):
    """
    Emperical inflow angle calculation of PMH
    NWS 23 pdf page 55
    NOAA_NWS23_Inflow_Calc.xlsx
    :param rmax_nmi: Radius of maximum winds in Nautical Miles
    :param r_nmi: Point radius from hurricane center in Nautical Miles
    :return: Inflow angle in degrees
    """
    phi = None
    rmax_three = 3 * rmax_nmi
    if r_nmi < rmax_three:
        a = 11.438 * (rmax_nmi ** -1.416)
        b = (1.1453 * rmax_nmi) + 1.4536
        phi_max = 9.7043566358 * math.log(rmax_nmi) - 2.7295806727
        phi = phi_max / (1 + math.exp(-1 * a * (r_nmi - b)))
    else:
        x1 = (0.0000896902 * rmax_nmi * rmax_nmi) - (0.0036924418 * rmax_nmi) + 0.0072307906
        x2 = (0.000002966 * rmax_nmi * rmax_nmi) - (0.000090532 * rmax_nmi) - 0.0010373287
        x3 = (-0.0000000592 * rmax_nmi * rmax_nmi) + (0.0000019826 * rmax_nmi) - 0.0000020198
        c = (9.7043566341 * math.log(rmax_nmi)) - 2.7295806689
        phi = (x3 * ((r_nmi - rmax_three) ** 3)) + (x2 * ((r_nmi - rmax_three) ** 2)) + (x1 * (r_nmi - rmax_three)) + c
    return phi


def calc_windspeed(cp_mb, r_nmi, lat_deg, fspeed_kts, rmax_nmi, angle_to_center, track_heading, pw_kpa=Pw_PMH_kPa, vmax_kts=None, gwaf=0.9):
    """
    :param cp_mb: Central Pressure in kPa
    :param r_nmi: Point radius from center of storm in kilometers
    :param lat_deg: Latitude of hurricane eye
    :param fspeed_kts: Forward speed of the storm in m/s
    :param pw_kpa: Peripheral Pressure, pressure at edge of storm, should be near MSLP
    :param rmax_nmi: Radius of maximum winds in km
    :param angle_to_center: Simple angle from point to center of storm, in bearing notation (North = 0)
    :param track_heading: Heading of track from current point to next point, except for the last point, which usees the previous heading
    :param vmax_kts: Input max windspeed to skip the calculation for it.  Useful when Vmax is know for a storm. m/s
    :param gwaf: Gradient Wind Adjustment Factor, semi-emprical adjustment to the Gradient Wind. Range 0.75-1.05, Generally between 0.9 and 1. NWS 23 pdf page 50, page 24, 2.2.7.2.1
    :return: Windspeed at a given radius for the storm in mps
    """
    cp_inhg = cp_mb * KpaToInhg
    pw_inhg = pw_kpa * KpaToInhg

    # Step 1: Calculate Maximum Gradient Windspeed if unknown, 10m-10min Average
    vgx = 0
    if vmax_kts is None:
        vgx = gradient_wind_at_radius(pw_inhg, cp_inhg, rmax_nmi, lat_deg)
    else:
        vgx = vmax_kts
    # Step 2: Calculate the Radial Decay
    radial_decay_factor = radial_decay(r_nmi, rmax_nmi)  # need to convert to nmi
    # Step 3: Calculate the Asymmetry Factor
    asym = asymmetry_factor(fspeed_kts, r_nmi, rmax_nmi, angle_to_center, track_heading)

    # apply all factors and return windspeed at point
    windspeed_kts = (vgx * gwaf * radial_decay_factor) + asym
    return windspeed_kts
    # return asym + 100
