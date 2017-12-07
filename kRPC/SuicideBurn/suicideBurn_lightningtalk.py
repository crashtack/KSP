"""
    An autopilot landing script that preforms a 'Suicide Burn'
    to land vessel

    Things to add:
    [ ] How much delta_v is expended?

"""
import krpc, math, time, sys
from suicideBurnFunctions import suicide_burn_calc, suicide_burn_height, \
print_status, update_display, setup_ui, surface_velocity

conn = krpc.connect(name='Launch Science Station to Orbit')
vessel = conn.space_center.active_vessel
canvas = conn.ui.stock_canvas
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

""" Setting up the UI """
setup_ui(vessel, canvas)

""" Ship Setup """
# throttle = vessel.control.throttle
vessel.control.throttle = 0
time.sleep(1)

vessel.control.rcs = True
time.sleep(1)
ap = vessel.auto_pilot
ap.reference_frame = vessel.orbital_reference_frame
ap.engage()
ap.disengage()
g = vessel.orbit.body.surface_gravity
print('Orbital Body: ', vessel.orbit.body.name)
print('Gravity = ', g)

time.sleep(1)
vessel.control.sas = True

""" Set Parameters for Landing """
safety = 1.0       # 1.1 for larger lander on Kerbal, 2 for small lander,
vLand = -8.0        # landing speed m/s
runmode = 1         # set the initial runmode

counter = 0         # for checking if landed

""" Find ship parameters """
global mass
mass = vessel.mass
print('Mass = ', mass)
thrust = vessel.max_thrust
initial_acceleration = thrust / mass
print('Theoredical Maxx Acceleration: ', initial_acceleration)
vacuum_acceleration = vessel.max_vacuum_thrust / mass
print('Theoredical Max Vac Acceleration: ', vacuum_acceleration)

current_acceleration = vessel.thrust / mass
print('Max Thrust = ', thrust)

h = vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
velocity_tupple = vessel.velocity(vessel.orbit.body.reference_frame)
vs = surface_velocity(velocity_tupple)      # surface Velocity
vv = -velocity_tupple[2]                    # vertical velocity
vDiff = vLand - vs
zeroAccelTrust = ((mass * g) / thrust)

SBH = suicide_burn_height(vessel, safety, g, thrust, vs)
print('SBH = ', SBH)
a = (thrust / mass) - g
t = vs / a
dV = t * thrust / 1000
print('Delta V: ', dV)
print()

""" Loop until landed """
while runmode:
    mass = vessel.mass
    h = vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
    # velocity_tupple = vessel.velocity(vessel.orbit.body.reference_frame)
    velocity_tupple = vessel.flight(vessel.orbit.body.reference_frame).velocity
    vs = -surface_velocity(velocity_tupple)      # surface Velocity
    vv = vessel.flight(vessel.orbit.body.reference_frame).vertical_speed
    vDiff = vLand - vv

    """ Calculates values for landing """
    # Calculates the suicide burn Height
    SBH = suicide_burn_height(vessel, safety, g, thrust, vs)
    time_to_burn = ((SBH - h) / vs)

    """ Initial setup for high altitude """
    if runmode == 1:
        vessel.control.throttle = 0
        if h > SBH * 2:
            conn.space_center.physics_warp_factor = 2
        if h < 50000:
            print()
            print(' Passing thru 50000m, setting autopilot to retrograde')
            vessel.control.sas_mode = vessel.control.sas_mode.retrograde
            print('SAS Mode is now set to radial: ', ap.sas_mode)
            runmode = 7

    if runmode == 7:
        if h < 4000:
            conn.space_center.physics_warp_factor = 0
            print('Dropping like a rock!')
            runmode = 6

    """ performing a short pre-burn at SBH + 20\%
        to determine initial acceleration"""
    if runmode == 5:
        if h < SBH * 2:
            conn.space_center.physics_warp_factor = 0
        if h < (SBH + (SBH * 1)):
            print()
            print("performing Pre-Burn")
            vessel.control.throttle = 1
            time.sleep(.5)
            initial_acceleration = vessel.thrust / mass
            zeroAccelTrust = ((mass * g) / vessel.thrust)
            print("initial acceleration: ", initial_acceleration)
            vessel.control.throttle = 0
            runmode = 2

    """determine new initial acceleration"""
    if runmode == 6:
        if h < SBH * 2:
            conn.space_center.physics_warp_factor = 0
        if h < (SBH + (SBH * .1)):
            print()
            print("Calculating Acceleration")
            initial_acceleration = vessel.max_thrust / mass
            zeroAccelTrust = ((mass * g) / vessel.max_thrust)
            print("Avalable acceleration: ", initial_acceleration)
            runmode = 2

    """ Suicide burn start """
    if runmode == 2:
        # if h < (SBH - vs):
        if h < SBH * 2:
            conn.space_center.physics_warp_factor = 0
        if h < SBH:
            vessel.control.throttle = 1
            vessel.control.rcs = False
            print()
            print('Starting Suicide Brun!')
            vessel.control.gear = True
            # initial_acceleration = thrust/mass
            # print("initial acceleration: ", initial_acceleration)
            time.sleep(1)
            runmode = 3

    """ During Suicide Burn """
    if runmode == 3:
        print()
        current_acceleration = vessel.thrust / mass
        print("current accel: %.2f" % current_acceleration)

        if h < SBH + 110:

            if current_acceleration > initial_acceleration:
                vessel.control.throttle = vessel.control.throttle - .2
            elif current_acceleration < initial_acceleration:
                vessel.control.throttle = vessel.control.throttle + .05

            if vs > -6:
                print()
                print('vs is now less then -6 ms, switching to final approach')
                print('SAS Mode: ', ap.sas_mode)
                # ap.disengage()
                # vessel.control.sas = True
                vessel.control.rcs = True
                vessel.control.sas_mode = vessel.control.sas_mode.radial
                print('SAS Mode is now set to radial: ', ap.sas_mode)
                print('Switching to Runmode 4')
                print('zeroAccelTrust = ', zeroAccelTrust)
                vessel.control.throttle = zeroAccelTrust
                time.sleep(.1)
                # ap.target_direction = (1,0,0)
                runmode = 4
        else:
            if vessel.control.throttle > 0:
                print("SBH is greater then 50m from current Height,\
                      chopping throttle")
                vessel.control.throttle = 0
            else:
                print("waiting for vessel to drop a bit")
                if vs > -6:
                    print()
                    print('vs is now less then -6 ms,\
                           switching to final approach')
                    print('SAS Mode: ', ap.sas_mode)
                    # ap.disengage()
                    # vessel.control.sas = True
                    vessel.control.rcs = True
                    vessel.control.sas_mode = vessel.control.sas_mode.radial
                    print('SAS Mode is now set to radial: ', ap.sas_mode)
                    print('Switching to Runmode 4')
                    print('zeroAccelTrust = ', zeroAccelTrust)
                    vessel.control.throttle = zeroAccelTrust
                    time.sleep(.1)
                    # ap.target_direction = (1,0,0)
                    runmode = 4

    """ Suicide burn final approach """
    if runmode == 4:
        print()
        # print('vDiff: ', vDiff)
        if h > 30:
            if vv < -8:
                # print('vv = ', vv)
                vessel.control.throttle = vessel.control.throttle + 0.05
            else:
                # print('VV ok to land, vv = ', vv)
                vessel.control.throttle = vessel.control.throttle - 0.07
        else:
            if vv < -3:
                # print('vv = ', vv)
                vessel.control.throttle = vessel.control.throttle + 0.02
            else:
                # print('VV ok to land, vv = ', vv)
                vessel.control.throttle = vessel.control.throttle - 0.05

        if vv > -2.0 and h < 15:
            counter += 1
            time.sleep(.1)
            if counter > 20:
                runmode = 0     # if landed for 2 seconde then exit

    print_status(h, vessel.control.throttle, SBH, time_to_burn, vs)
    update_display(h, vessel.control.throttle, SBH, time_to_burn,
                   vs, vv, thrust, mass, initial_acceleration,
                   current_acceleration)
    time.sleep(0.025)

""" Landing notification and program exit """
if runmode == 0:
    vessel.control.throttle = 0
    vessel.control.rcs = False
    vessel.control.sas = False
    print()
    print("Landing Complete")
    input("Hit Enter to Quit")
