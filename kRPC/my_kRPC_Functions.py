
def print_part_tree(vessel):
    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part,depth = stack.pop()
        print(' '*depth, part.title)
        for child in part.children:
            stack.append((child, depth+1))

def print_part_tree_attached(vessel):
    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part,depth = stack.pop()
        if part.axially_attached:
            attach_mode = 'axial'
        else: # radially_attached
            attach_mode = 'radial'
        print(' '*depth, part.title, '-', attach_mode)
        for child in part.children:
            stack.append((child, depth+1))

def print_part_tree_attached_fuel(vessel):
    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part,depth = stack.pop()
        part_stage = part.stage
        if part.axially_attached:
            attach_mode = 'axial'
        else: # radially_attached
            attach_mode = 'radial'
        print(' '*depth, part.title, '-', attach_mode, '- Stage: ', part_stage)
        for child in part.children:
            stack.append((child, depth+1))

def engines_fuel_status(vessel):
    root = vessel.parts.root
    stack = [(root, 0)]
    engines = []
    while len(stack) > 0:
        part,depth = stack.pop()
        part_stage = part.stage
        if part.engine:
            engine = part.engine
            engines.append(part)
            #print(part.title, '-',engine.propellant_names)
        # if part.engine.propellants.name:
        #     print(' '*depth, part.title, '-', attach_mode, '- Stage: ', part_stage, '-', part.engine.propellants.name)
        for child in part.children:
            stack.append((child, depth+1))
    for part in engines:
        print(part.title, '-',part.engine.propellant_names, ' Parent-Parent: ', part.parent.parent.name, part.engine.propellants[0].name, ' Available: ', part.engine.propellants[0].total_resource_available)
    return engines

def current_stage(vessel):
    root = vessel.parts.root
    stack = [(root, 0)]
    stage = 0
    while len(stack) > 0:
        part,depth = stack.pop()
        if part.stage > stage:
            stage = part.stage
        for child in part.children:
            stack.append((child, depth+1))
    print('Current Stage: %i' % stage)
    return stage

def get_engines(vessel):
    root = vessel.parts.root
    stack = [(root, 0)]
    engines = []
    while len(stack) > 0:
        part,depth = stack.pop()
        if part.engine:
            engine = part.engine
            engines.append(part)
            #print(part.title, '-',part.engine.propellant_names, ' Parent-Parent: ', part.parent.parent.name, part.engine.propellants[0].name, ' Available: ', part.engine.propellants[0].total_resource_available)
        for child in part.children:
            stack.append((child, depth+1))
    return engines

def decouple_if_empty(vessel, engines, stage):
    for part in engines:
        if part.engine.propellants[0].total_resource_available == 0 and part.stage == stage:
            print(part.title, '-',part.engine.propellant_names, ' Parent-Parent: ', part.parent.parent.name, part.engine.propellants[0].name, ' Available: ', part.engine.propellants[0].total_resource_available)
            print(part.parent.parent.name)
            print(part.parent.parent.decoupler)
            vessel = part.parent.parent.decoupler.decouple()
            print('new_vessel: ', vessel)
    #engines = get_engines(new_vessel)
    #decouple_if_empty(vessel,engines,current_stage(new_vessel))
