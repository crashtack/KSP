import krpc, time, math, sys
from my_kRPC_Functions import vessel_info, get_engines, decouple_if_empty

turn_start_altitude = 250
turn_end_altitude = 45000
target_altitude = 120000
main_engine_throttle = 0.0

conn = krpc.connect(name='Launch Science Station to Orbit')
vessel = conn.space_center.active_vessel

# Set up streams for telemetry
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
eccentricity = conn.add_stream(getattr, vessel.orbit, 'eccentricity')

stage_1_resources = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
stage_3_resources = vessel.resources_in_decouple_stage(stage=3, cumulative=False)
stage_4_resources = vessel.resources_in_decouple_stage(stage=4, cumulative=False)
stage_5_resources = vessel.resources_in_decouple_stage(stage=5, cumulative=False)
stage_6_resources = vessel.resources_in_decouple_stage(stage=6, cumulative=False)
srb_fuel = conn.add_stream(stage_5_resources.amount, 'SolidFuel')
launcher_fuel = conn.add_stream(stage_6_resources.amount, 'LiquidFuel')
second_stage_fuel = conn.add_stream(stage_2_resources.amount, 'LiquidFuel')

# Pre-launch setup
vessel.control.sas = False
vessel.control.rcs = False
vessel.control.throttle = main_engine_throttle

print("SRB Fuel: %.2f" % srb_fuel())
print("Main Engine Fuel: %.2f" % launcher_fuel())
print("Upper Stage Fuel: %.2f" % second_stage_fuel())

vessel, stage = vessel_info(conn)
engines = get_engines(vessel)
while True:
    #vessel = conn.space_center.active_vessel
    #current_stage = my_kRPC_Functions.current_stage(vessel)
    time.sleep(1)
    print('waiting')
    #engines = my_kRPC_Functions.get_engines(vessel)
    vessel, stage, engines = decouple_if_empty(vessel, stage, engines, conn)
