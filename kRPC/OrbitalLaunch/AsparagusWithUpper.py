import krpc, time, math, sys
from my_kRPC_Functions import vessel_info, get_engines, decouple_if_empty, current_stage

turn_start_altitude = 250
turn_end_altitude = 45000
target_altitude = 80000

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
#srb_fuel = conn.add_stream(stage_4_resources.amount, 'SolidFuel')
launcher_fuel = conn.add_stream(stage_2_resources.amount, 'LiquidFuel')
#second_stage_fuel = conn.add_stream(stage_1_resources.amount, 'LiquidFuel')

# Pre-launch setup
vessel.control.sas = False
vessel.control.rcs = False
vessel.control.throttle = 1

def print_status(stage):
    message = ("altitude: %.2f apoapsis: %.2f stage: %i" % (altitude(), apoapsis(),stage))
    sys.stdout.write("\r" + message)
    sys.stdout.flush()

# get vessel info
time.sleep(1)
vessel = vessel_info(conn)
time.sleep(1)
engines = get_engines(vessel)
stage = current_stage(engines)
for part in engines:
    print("Found Engines: ", part.name , "Stage: ", part.stage)

# Countdown...
print('3...'); time.sleep(1)
print('2...'); time.sleep(1)
print('1...'); time.sleep(1)
print('Launch!')

# Activate the first stage
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel = vessel_info(conn)

# Main ascent loop
srbs_separated = False
turn_angle = 0
while True:
    time.sleep(.1)
    print_status(stage)
    #print("altitude: %.2f" % altitude())
    # Gravity turn
    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
        frac = (altitude() - turn_start_altitude) / (turn_end_altitude - turn_start_altitude)
        new_turn_angle = frac * 90
        if abs(new_turn_angle - turn_angle) > 0.5:
            turn_angle = new_turn_angle
            vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, 90)

    # Separate SRBs when finished
    # if not srbs_separated:
    #     #print("srb fuel: %f" % srb_fuel())
    #     if srb_fuel() < .1:
    #         time.sleep(.5)
    #         vessel.control.activate_next_stage()
    #         srbs_separated = True
    #         print('SRBs separated')

    vessel, stage, engines = decouple_if_empty(vessel, stage, engines, conn)

    # Decrease throttle when approaching target apoapsis
    if apoapsis() > target_altitude*0.98:
        print('Approaching target apoapsis')
        break

vessel.control.throttle = 0
print('Remaining launcher_fuel: %.2f' % launcher_fuel())
# Wait until out of atmosphere
print('Coasting out of atmosphere')
vessel.control.activate_next_stage()
time.sleep(.1)
vessel.control.activate_next_stage()
while altitude() < 70500:
    print_status(stage)
    time.sleep(.1)
    pass
vessel.control.throttle = 1
# Disable engines when target apoapsis is reached
while apoapsis() < target_altitude:
    print_status(stage)
    time.sleep(.1)
    pass
print('Target apoapsis reached')
vessel.control.throttle = 0


# Plan circularization burn (using vis-viva equation)
print('Planning circularization burn')
mu = vessel.orbit.body.gravitational_parameter
r = vessel.orbit.apoapsis
a1 = vessel.orbit.semi_major_axis
a2 = r
v1 = math.sqrt(mu*((2./r)-(1./a1)))
v2 = math.sqrt(mu*((2./r)-(1./a2)))
delta_v = v2 - v1
node = vessel.control.add_node(ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

# Calculate burn time (using rocket equation)
F = vessel.available_thrust
Isp = vessel.specific_impulse * 9.82
m0 = vessel.mass
m1 = m0 / math.exp(delta_v/Isp)
flow_rate = F / Isp
burn_time = (m0 - m1) / flow_rate

# Orientate ship
print('Orientating ship for circularization burn')
vessel.auto_pilot.reference_frame = node.reference_frame
vessel.auto_pilot.target_direction = (0,1,0)
vessel.auto_pilot.wait()

# Wait until burn
print('Waiting until circularization burn')
burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
lead_time = 5
conn.space_center.warp_to(burn_ut - lead_time)

# Execute burn
print('Ready to execute burn')
time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
while time_to_apoapsis() - (burn_time/2.) > 0:
    print_status(stage)
    time.sleep(.1)
    pass
print('Executing burn')
vessel.control.throttle = 1
time.sleep(burn_time - 0.1)
print('Fine tuning')
vessel.control.throttle = 0.25
remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)
while remaining_burn()[1] > 0:
    print_status(stage)
    time.sleep(.1)
    pass
vessel.control.throttle = 0
node.remove()

print('Launch complete')
