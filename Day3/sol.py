import os
dirname = os.path.dirname(__file__)

input_file = open(dirname + "/input.txt", "r").read()

test = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

input_wires = input_file.split('\n')
wire1 = input_wires[0].split(",")
wire2 = input_wires[1].split(",")


def get_successive_positions(wire_path):
    positions = []
    initial_pos = (0, 0, 0)  # x coordinate, y coordinate, nb of steps so far
    positions.append(initial_pos)
    for i in range(len(wire_path)):
        direction, amount = wire_path[i][0], int(wire_path[i][1:])
        last_pos = positions[i]
        steps_so_far = last_pos[2] + abs(amount)
        if direction == 'U':
            positions.append((last_pos[0], last_pos[1] + amount, steps_so_far))
        elif direction == 'D':
            positions.append((last_pos[0], last_pos[1] - amount, steps_so_far))
        elif direction == 'R':
            positions.append((last_pos[0] + amount, last_pos[1], steps_so_far))
        else:
            positions.append((last_pos[0] - amount, last_pos[1], steps_so_far))
    return positions


pos1 = get_successive_positions(wire1)
pos2 = get_successive_positions(wire2)
intersections = []


def horiz_intersects_vert(horiz_start, horiz_end, vert_start, vert_end):
    vert_is_between_horiz = (min(horiz_start[0], horiz_end[0]) <= vert_start[0]
                             <= max(horiz_start[0], horiz_end[0]))
    horiz_is_between_vert = (min(vert_start[1], vert_end[1]) <= horiz_start[1]
                             <= max(vert_start[1], vert_end[1]))
    return horiz_is_between_vert and vert_is_between_horiz


def manhattan(point, reference=(0, 0)):
    return abs(point[0] - reference[0]) + abs(point[1] - reference[1])


for i in range(len(pos1) - 1):
    for j in range(len(pos2) - 1):
        does_intersect = 0
        if horiz_intersects_vert(pos1[i], pos1[i + 1], pos2[j], pos2[j + 1]):
            does_intersect = 1
        elif horiz_intersects_vert(pos2[j], pos2[j + 1], pos1[i], pos1[i + 1]):
            does_intersect = -1
        if does_intersect:
            if does_intersect == 1:
                x = pos2[j][0]
                y = pos1[i][1]
            else:
                x = pos1[i][0]
                y = pos2[j][1]
            intersection = (x, y)
            nb_steps = (pos1[i][2] + pos2[j][2] +
                        manhattan(intersection, pos1[i]) +
                        manhattan(intersection, pos2[j]))
            intersections.append((intersection, nb_steps))

# solution to 1st problem : closest intersection in Manhattan distance
distances = list(map(manhattan, [i[0] for i in intersections]))
distances.remove(0)
print(min(distances))

# solution to 2nd problem : closest intersection in nb of steps
steps = [i[1] for i in intersections]
steps.remove(0)
print(min(steps))