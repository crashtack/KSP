import krpc, math, time, sys

conn = krpc.connect(name='Launch Science Station to Orbit')
vessel = conn.space_center.active_vessel

while True:
    print('Gear State: ', vessel.control.gear)
    time.sleep(1)
    print('Lowering Gear')
    vessel.control.gear = True
    time.sleep(10)
    print('Gear State: ', vessel.control.gear)
    time.sleep(1)
    print('Raising Gear')
    vessel.control.gear = False
