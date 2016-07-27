import krpc, time, math, sys

conn = krpc.connect(name='Show Velocities')
vessel = conn.space_center.active_vessel

altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

while True:
    velocity = vessel.velocity(vessel.orbit.body.reference_frame)
    vertical_velocity = -velocity[2]
    message = ('Altitude: %.2f Vertical Velocity: %.2f' % (altitude(),vertical_velocity))
    sys.stdout.write("\r" + message)
    sys.stdout.flush()
    #print(altitude())
    #print('Surface Velocity = %.1f' % vertical_velocity)
    time.sleep(.1)
