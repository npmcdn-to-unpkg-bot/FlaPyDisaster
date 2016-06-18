import explosion.asteroid.asteroid_math as astr_math
import explosion.explosion_math as expl_math
from general.general_objects import BoundingBox, LatLonGrid
from general import unit_conversions, general_geometry

class AsteroidEvent:
    def __init__(self, diameter_m, angle_rad, init_velocity_mps, density_kgpm3, target_density_kgpm3, grid):
        # input params
        self.diameter_m = diameter_m
        self.angle_rad = angle_rad
        self.init_velocity_mps = init_velocity_mps
        self.density_kgpm3 = density_kgpm3
        self.target_density_kgpm3 = target_density_kgpm3
        self.grid = grid

        # derived params
        self.breakup_alt_m = astr_math.BreakupAltitude(self.density_kgpm3, self.diameter_m, self.init_velocity_mps, self.angle_rad)
        self.airburst_alt_m = astr_math.AirburstAltitude(self.breakup_alt_m, self.diameter_m, self.density_kgpm3, self.angle_rad)
        self.is_airburst = self.airburst_alt_m > 0
        self.initial_energy_j = astr_math.KeneticEnergy(self.density_kgpm3, self.diameter_m, self.init_velocity_mps)
        self.ret_period_yr = astr_math.ReturnPeriodEarth(unit_conversions.energy_conversion(self.initial_energy_j, unit_conversions.EnergyUnits.joules, unit_conversions.EnergyUnits.Megaton_TNT))
        self.breakup_velocity_mps = astr_math.VelocityAtAltitude_PreBreakup(self.breakup_alt_m, self.init_velocity_mps, self.diameter_m, self.density_kgpm3, self.angle_rad)
        self.airburst_velocity_mps = astr_math.PostBreakupVelocity(self.breakup_alt_m, self.breakup_velocity_mps, self.diameter_m, self.density_kgpm3, self.angle_rad, self.is_airburst)
        self.airburst_energy_j = astr_math.KeneticEnergy(self.density_kgpm3, self.diameter_m, self.airburst_velocity_mps)
        return

    def get_overpressure(self, radius_gz_m):
        airburst_mttnt = unit_conversions.energy_conversion(self.airburst_energy_j, unit_conversions.EnergyUnits.joules, unit_conversions.EnergyUnits.Megaton_TNT)
        hyp_distance_m = general_geometry.FindHypotenuseRightTriangle(radius_gz_m, self.airburst_alt_m)
        return expl_math.NewmarkOverpressure(airburst_mttnt, hyp_distance_m)