"""
    An autopilot landing script that preforms a 'Suicide Burn'
    to land vessel

    Things to add:
    [ ] How much delta_v is expended?

"""
import krpc, math, time, sys

conn = krpc.connect(name='Launch Science Station to Orbit')
vessel = conn.space_center.active_vessel
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

def suicide_burn_calc(vessel,saf,g,thrust,vv):
    safety      = saf          # 1 corresponds to no safety margin, 1.1 had 10% safety margin
    shipmass    = vessel.mass
    va = ((thrust/shipmass) + g)
    a = (vv**2)/(2*va)
    return safety * a

def print_status(h, throttle, burn_height, burn_time, vv):
    message = ("Height: %.2f SNH: %.1f Throttle: %.2f Burn Time: %.2f Vertical Velocity: %.2f" % (h,burn_height,throttle,burn_time,vv))
    sys.stdout.write("\r" + message)
    sys.stdout.flush()

""" Ship Setup """
#throttle = vessel.control.throttle
vessel.control.throttle = 0
time.sleep(1)

vessel.control.rcs = False
time.sleep(1)
ap = vessel.auto_pilot
ap.reference_frame = vessel.orbital_reference_frame
ap.engage()
ap.disengage()
g = vessel.orbit.body.surface_gravity

time.sleep(1)
vessel.control.sas = True

""" Set Parameters for Landing """
safety = .90
vLand = -8      # landing speed m/s
runmode = 1     # ??
thrust = vessel.max_thrust
counter = 0     # for checking if landed

""" Find ship parameters """
h = vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
velocity_tupple = vessel.velocity(vessel.orbit.body.reference_frame)
vv = -velocity_tupple[2]
vDiff = vLand - vv

""" Calculates values for landing """


""" Loop until landed """
while runmode:
    h = vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
    velocity_tupple = vessel.velocity(vessel.orbit.body.reference_frame)
    vv = -velocity_tupple[2]
    vDiff = vLand - vv

    """ Calculates values for landing """
    SBH = suicide_burn_calc(vessel,safety,g,thrust,vv)     # Calculates the suicide burn Height
    time_to_burn = ((SBH - h)/vv)
    zeroAccelTrust = ((vessel.mass * g)/thrust)


    """ Initial setup for high altitude """
    if runmode == 1:
        vessel.control.throttle = 0
        if h < 50000:
            print()
            print(' Passing thru 50000m, setting autopilot to retrograde')
            #ap.reference_frame = vessel.surface_velocity_reference_frame
            #brakes on
            #vessel.control.sas = True
            vessel.control.sas_mode = vessel.control.sas_mode.retrograde
            print('SAS Mode is now set to radial: ', ap.sas_mode)
            #ap.target_direction = (0,-1,0)
            runmode = 2

    """ Suicide burn start """
    if runmode == 2:
        if h < (SBH - vv):
        #if h < SBH:
            vessel.control.throttle = 1
            vessel.control.rcs = False
            print()
            print('Starting Suicide Brun!')
            vessel.control.gear = True
            runmode = 3

    if runmode == 3:
        #else:
            #vessel.control.throttle = 0
        #if h/-vv < 2:
            #print('h/-vv')
            # gear on
            # brakes off
        if vv > -6:
            print()
            print('vv is now less then -6 ms, switching to final approach')
            print('SAS Mode: ', ap.sas_mode)
            #ap.disengage()
            #vessel.control.sas = True
            vessel.control.rcs = True
            vessel.control.sas_mode = vessel.control.sas_mode.radial
            print('SAS Mode is now set to radial: ', ap.sas_mode)
            # ap.target_direction = (1,0,0)
            runmode = 4

    """ Suicide burn final approach """
    if runmode == 4:
        if vDiff > 0:
            vessel.control.throttle = zeroAccelTrust + 0.01
        elif vDiff < 0:
            vessel.control.throttle = zeroAccelTrust - 0.01

        if vv > -0.1 and h < 100:
            counter += 1
            time.sleep(.1)
        if counter > 20:
            runmode = 0     # if landed for 2 seconde then exit

    print_status(h, vessel.control.throttle, SBH, time_to_burn, vv)
    time.sleep(0.05)

""" Landing notification and program exit """
if runmode == 0:
    vessel.control.throttle = 0
    vessel.control.rcs = False
    vessel.control.sas = False
    print()
    print("Landing Complete")
