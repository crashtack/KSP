import krpc
import time

conn = krpc.connect()
vessel = conn.space_center.active_vessel
control = vessel.control
flight = vessel.flight(vessel.orbit.body.reference_frame)

target = 15 # target altitude above the surface, in meters
mu = vessel.orbit.body.gravitational_parameter
g = vessel.orbit.body.surface_gravity

print('mu= %.2f g= %.2f' % (mu,g))

target = int(input('Enter Target Altitude: '))
print('Target altitude set to %i meters' % target)
input('Ready?')
while True:

    alt_error = target - flight.surface_altitude

    # compute the desired acceleration:
    #   g   to counteract gravity
    #   -v  to push the vertical speed towards 0
    #   e   to push the altitude error towards 0
    a = g - flight.vertical_speed + alt_error

    # Compute throttle setting using newton's law F=ma
    F = vessel.mass * a
    control.throttle = F / vessel.available_thrust

    time.sleep(0.01)
