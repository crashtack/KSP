import krpc
import math

def norm(v):
    return math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])

conn = krpc.connect()
active_vessel = conn.space_center.active_vessel
vessels = conn.space_center.vessels
vessel_distances = [(v, norm(v.position(active_vessel.reference_frame))) for v in vessels]

for vessel,distance in vessel_distances:
    if distance < 22500: # 22.5km
        print vessel.name, '%.1f km' % (distance/1000)
