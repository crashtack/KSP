import krpc, math, time, sys

def suicide_burn_calc(vessel,saf,g,thrust,vs):
    safety      = saf          # 1 corresponds to no safety margin, 1.1 had 10% safety margin
    mass    = vessel.mass
    va = ((thrust/mass) + g)
    a = (vs**2)/(2*va)
    return safety * a

def suicide_burn_height(vessel,saf,g,thrust,vs):
    mass = vessel.mass
    a = (thrust/mass) + g
    t = vs / a
    h = (0.5*(vs**2))/a
    return h * saf

def surface_velocity(vt):
    Vab = ((vt[0]**2)+(vt[1]**2))**.5
    Vs  = ((vt[2]**2)+(Vab**2))**.5
    return Vs

def print_status(h, throttle, burn_height, burn_time, vs):
    message = ("Height: %.2f SBH: %.1f Throttle: %.2f Burn Time: %.2f Vertical Velocity: %.2f  " % (h,burn_height,throttle,burn_time,vs))
    sys.stdout.write("\r" + message)
    sys.stdout.flush()

def update_display(h, throttle, burn_height, burn_time, vs, vv, thrust, mass, Ai, Ac):
    # global display_Thurst
    # global display_Height
    # global display_SBH
    # global display_vs
    # global display_vv
    # global display_burntime
    # global display_throttle
    # global display_Mass
    # global display_currentAccel
    # global display_initialAccel
    # global current_acceleration
    # global initial_acceleration
    display_Thurst.content      = ('Thrust   :  %.2f kN' % (thrust/1000))
    display_Height.content      = ('Height   :  %.2f m' % h)
    display_SBH.content         = ('SBH      :  %.2f m' % burn_height)
    display_vs.content          = ('Velocity :  %.2f m/s' % vs)
    display_vv.content          = ('V Velocity: %.2f m/s' % vv)
    display_burntime.content    = ('Burn Time:  %.2f' % burn_time)
    display_throttle.content    = ('Throttle :  %.2f' % throttle)
    display_Mass.content        = ('Mass : %.2f k' % mass)
    display_initialAccel.content= ('Initial Accel: %.2f' % Ai)
    display_currentAccel.content= ('Current Accel: %.2f' % Ac)

def setup_ui(vessel, canvas):
    global display_Thurst
    global display_Height
    global display_SBH
    global display_vs
    global display_vv
    global display_burntime
    global display_throttle
    global display_Mass
    global display_currentAccel
    global display_initialAccel
    """ Setup the UI panel """
    screen_size = canvas.rect_transform.size        # get the size of the game window
    panel = canvas.add_panel()                      # add a panel to contain UI elements
    rect = panel.rect_transform
    rect.size = (400, 400)
    rect.position = (110-(screen_size[0]/2),0)
    fontsize = 14

    display_startMass   = panel.add_text('Starting Mass: %.2f k' % vessel.mass)
    display_startMass.rect_transform.position = (-10,80)
    display_startMass.color = (1,1,1)
    display_startMass.size = fontsize

    display_Mass        = panel.add_text('Mass         : 0 k')
    display_Mass.rect_transform.position = (-10,60)
    display_Mass.color = (1,1,1)
    display_Mass.size = fontsize

    display_Thurst = panel.add_text('Thurst: 0 kN')
    display_Thurst.rect_transform.position = (0,100)
    display_Thurst.color = (1,1,1)
    display_Thurst.size = fontsize

    display_Height = panel.add_text('Height: 0 m')
    display_Height.rect_transform.position = (0,-40)
    display_Height.color = (1,1,1)
    display_Height.size = fontsize

    display_SBH = panel.add_text('Suicide Burn alt: 0 m')
    display_SBH.rect_transform.position = (0,-60)
    display_SBH.color = (1,1,1)
    display_SBH.size = fontsize

    display_vs = panel.add_text('Velocity: 0 m/s')
    display_vs.rect_transform.position = (0,-80)
    display_vs.color = (1,1,1)
    display_vs.size = fontsize

    display_vv = panel.add_text('V Velocity: 0 m/s')
    display_vv.rect_transform.position = (0,-100)
    display_vv.color = (1,1,1)
    display_vv.size = fontsize

    display_burntime = panel.add_text('Burn Time: 0 s')
    display_burntime.rect_transform.position = (0,-120)
    display_burntime.color = (1,1,1)
    display_burntime.size = fontsize

    display_throttle = panel.add_text('Throttle: 0')
    display_throttle.rect_transform.position = (0,-140)
    display_throttle.color = (1,1,1)
    display_throttle.size = fontsize

    display_initialAccel = panel.add_text('Initial Accel: 0')
    display_initialAccel.rect_transform.position = (0,-160)
    display_initialAccel.color = (1,1,1)
    display_initialAccel.size = fontsize

    display_currentAccel = panel.add_text('Current Accel: 0')
    display_currentAccel.rect_transform.position = (0,-180)
    display_currentAccel.color = (1,1,1)
    display_currentAccel.size = fontsize
