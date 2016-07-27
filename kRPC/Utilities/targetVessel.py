import krpc, math
conn = krpc.connect()

vessel = conn.space_center.active_vessel
target = conn.space_center.target_vessel
if target is None:
    print ('No target vessel')
    exit(1)

def dot(u,v):
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

frame = vessel.reference_frame
n0 = vessel.flight(frame).normal
n1 = target.flight(frame).normal
print (math.acos(dot(n0,n1)) * (180.0 / math.pi))
