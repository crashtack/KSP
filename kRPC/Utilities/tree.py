import krpc, math, time, sys

conn = krpc.connect(name='Launch Science Station to Orbit')
vessel = conn.space_center.active_vessel

def print_part_tree(vessel):
    root = vessel.parts.root
    stack = [(root, 0)]
    while len(stack) > 0:
        part,depth = stack.pop()
        print(' '*depth, part.title)
        for child in part.children:
            stack.append((child, depth+1))

print_part_tree(vessel)
