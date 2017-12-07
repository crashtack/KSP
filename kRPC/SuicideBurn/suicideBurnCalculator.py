"""
    Calculates the Suicide Burn Height
"""
import krpc, time

def suicide_burn_calc(vessel,saf, g, thrust):
    safety      = saf          # 1 corresponds to no safety margin, 1.1 had 10% safety margin
    shipmass    = vessel.mass

    velocity = vessel.velocity(vessel.orbit.body.reference_frame)
    vd = -velocity[2]
    va = ((thrust/shipmass) + g)
    a = (vd**2)/(2*va)
    return safety * a


conn = krpc.connect()
vessel = conn.space_center.active_vessel
saf = 1
g = vessel.orbit.body.surface_gravity

while True:
    print(suicide_burn_calc(vessel,saf, g))
    time.sleep(1)
