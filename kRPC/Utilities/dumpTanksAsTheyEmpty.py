import krpc

conn = krpc.connect()
vessel = conn.space_center.active_vessel
tanks = {}

# gets list of remaining xenon tanks
def gettank():
    global tanks
    tanks = {}
    for part in vessel.parts.all:
        if 'XenonGas' in part.resources.names:
            tanks[part] = part.decouple_stage

# decouple all empty tanks
def removeemptytank():
    for decoupler in vessel.parts.decouplers:
        if decoupler.part.children[0].resources.amount('XenonGas') == 0:
            decoupler.decouple()
            gettank()
            enabletank()

# enable next tank
def enabletank():
    for tank in tanks:
        if tanks[tank] == max(tanks.values()):
            for resource in tank.resources.with_resource('XenonGas'):
                resource.enabled = True
            return

# main loop
while True:
    gettank()
    removeemptytank()
    enabletank()
