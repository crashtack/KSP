"""
    An autopilot landing script that preforms a 'Suicide Burn'
    to land vessel

    Things to add:
    [ ] How much delta_v is expended?

"""
import krpc, math, time, sys

conn = krpc.connect(name='Launch Science Station to Orbit')
vessel = conn.space_center.active_vessel
canvas = conn.ui.stock_canvas
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

def suicide_burn_calc(vessel,saf,g,thrust,vs):
    safety      = saf          # 1 corresponds to no safety margin, 1.1 had 10% safety margin
    shipmass    = vessel.mass
    va = ((thrust/shipmass) + g)
    a = (vs**2)/(2*va)
    return safety * a

def suicide_burn_height(vessel,saf,g,thrust,vs):
    shipmass = vessel.mass
    a = (thrust/shipmass) - g
    t = vs / a
    h = (0.5*(vs**2))/a
    return h

def surface_velocity(vt):
    Vab = ((vt[0]**2)+(vt[1]**2))**.5
    Vs  = ((vt[2]**2)+(Vab**2))**.5
    return Vs

def print_status(h, throttle, burn_height, burn_time, vs):
    message = ("Height: %.2f SBH: %.1f Throttle: %.2f Burn Time: %.2f Vertical Velocity: %.2f  " % (h,burn_height,throttle,burn_time,vs))
    sys.stdout.write("\r" + message)
    sys.stdout.flush()

def update_display(h, throttle, burn_height, burn_time, vs, vv, thrust):
    global display_Thurst
    global display_Height
    global display_SBH
    global display_vs
    global display_vv
    global display_burntime
    global display_throttle
    display_Thurst.content      = ('Thrust   :  %.2f kN' % (thrust/1000))
    display_Height.content      = ('Height   :  %.2f m' % h)
    display_SBH.content         = ('SBH      :  %.2f m' % burn_height)
    display_vs.content          = ('Velocity :  %.2f m/s' % vs)
    display_vv.content          = ('V Velocity: %.2f m/s' % vv)
    display_burntime.content    = ('Burn Time:  %.2f' % burn_time)
    display_throttle.content    = ('Throttle :  %.2f' % throttle)

""" Setup the UI panel """
screen_size = canvas.rect_transform.size        # get the size of the game window
panel = canvas.add_panel()                      # add a panel to contain UI elements
rect = panel.rect_transform
rect.size = (200, 400)
rect.position = (110-(screen_size[0]/2),0)

display_Thurst = panel.add_text('Thurst: 0 kN')
display_Thurst.rect_transform.position = (0,100)
display_Thurst.color = (1,1,1)
display_Thurst.size = 18

display_Height = panel.add_text('Height: 0 m')
display_Height.rect_transform.position = (0,-40)
display_Height.color = (1,1,1)
display_Height.size = 18

display_SBH = panel.add_text('Suicide Burn alt: 0 m')
display_SBH.rect_transform.position = (0,-60)
display_SBH.color = (1,1,1)
display_SBH.size = 18

display_vs = panel.add_text('Velocity: 0 m/s')
display_vs.rect_transform.position = (0,-80)
display_vs.color = (1,1,1)
display_vs.size = 18

display_vv = panel.add_text('V Velocity: 0 m/s')
display_vv.rect_transform.position = (0,-100)
display_vv.color = (1,1,1)
display_vv.size = 18

display_burntime = panel.add_text('Burn Time: 0 s')
display_burntime.rect_transform.position = (0,-120)
display_burntime.color = (1,1,1)
display_burntime.size = 18

display_throttle = panel.add_text('Throttle: 0')
display_throttle.rect_transform.position = (0,-140)
display_throttle.color = (1,1,1)
display_throttle.size = 18


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
print('Orbital Body: ', vessel.orbit.body.name)
print('Gravity = ', g)

time.sleep(1)
vessel.control.sas = True

""" Set Parameters for Landing """
safety = 1.0
vLand = -8      # landing speed m/s
runmode = 1     # ??
thrust = vessel.max_thrust
print('Max Thrust = ', thrust)
counter = 0     # for checking if landed

""" Find ship parameters """
shipmass    = vessel.mass
print('Mass = ', shipmass)
h = vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
velocity_tupple = vessel.velocity(vessel.orbit.body.reference_frame)
vs = surface_velocity(velocity_tupple)      # surface Velocity
vv = -velocity_tupple[2]                    #vertical velocity
vDiff = vLand - vs
SBH = suicide_burn_height(vessel,safety,g,thrust,vs)
print('SBH = ', SBH)
a = (thrust/shipmass) - g
t = vs / a
dV = t * thrust / 1000
print('Delta V: ', dV)

""" Loop until landed """
while runmode:
    h = vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
    velocity_tupple = vessel.velocity(vessel.orbit.body.reference_frame)
    vs = -surface_velocity(velocity_tupple)      # surface Velocity
    vv = -velocity_tupple[2]
    vDiff = vLand - vs

    """ Calculates values for landing """
    SBH = suicide_burn_height(vessel,safety,g,thrust,vs)     # Calculates the suicide burn Height
    time_to_burn = ((SBH - h)/vs)
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
        if h < (SBH - vs):
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
        #if h/-vs < 2:
            #print('h/-vs')
            # gear on
            # brakes off
        if vs > -6:
            print()
            print('vs is now less then -6 ms, switching to final approach')
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

        if vs > -0.1 and h < 100:
            counter += 1
            time.sleep(.1)
        if counter > 20:
            runmode = 0     # if landed for 2 seconde then exit

    print_status(h, vessel.control.throttle, SBH, time_to_burn, vs)
    update_display(h, vessel.control.throttle, SBH, time_to_burn, vs, vv, thrust)
    time.sleep(0.05)

""" Landing notification and program exit """
if runmode == 0:
    vessel.control.throttle = 0
    vessel.control.rcs = False
    vessel.control.sas = False
    print()
    print("Landing Complete")
