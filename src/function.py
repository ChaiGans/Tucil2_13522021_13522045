class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

def find_midpoint(point_a, point_b):
    return Point(
        (point_a.x + point_b.x) / 2,
        (point_a.y + point_b.y) / 2
    )

def dnc_curve(control_start, control_middle, control_end, depth, max_depth, points_list):
    if depth < max_depth:
        middle_point_1 = find_midpoint(control_start, control_middle)
        middle_point_2 = find_midpoint(control_middle, control_end)
        middle_point = find_midpoint(middle_point_1, middle_point_2)
        depth += 1

        # left
        dnc_curve(control_start, middle_point_1, middle_point, depth, max_depth, points_list)

        points_list.append(middle_point)

        # right
        dnc_curve(middle_point, middle_point_2, control_end, depth, max_depth, points_list)

def dnc_n_curve(control_points, depth, max_depth, points_list, point_list_of_every_iteration):
    if depth < max_depth:
        middle_point_useful_left = [control_points[0]]
        middle_point_useful_right = [control_points[-1]]
        middle_of_middle_point = [find_midpoint(control_points[i], control_points[i + 1]) for i in range(len(control_points) - 1)]
        
        # Append the first and last midpoints to the left and right lists, respectively
        middle_point_useful_left.append(middle_of_middle_point[0])
        middle_point_useful_right.insert(0, middle_of_middle_point[-1])
        
        # Calculate the successive midpoints until only one or two points remain
        while len(middle_of_middle_point) > 2:
            middle_of_middle_point = [find_midpoint(middle_of_middle_point[i], middle_of_middle_point[i + 1]) for i in range(len(middle_of_middle_point) - 1)]
            middle_point_useful_left.append(middle_of_middle_point[0])
            middle_point_useful_right.insert(0, middle_of_middle_point[-1])
        
        # Handle the case when two points remain
        if len(middle_of_middle_point) == 2:
            new_middle_point = find_midpoint(middle_of_middle_point[0], middle_of_middle_point[1])
            middle_point_useful_left.append(new_middle_point)
            middle_point_useful_right.insert(0, new_middle_point)

        # Save iteration result
        point_list_of_every_iteration.append(middle_point_useful_left + [new_middle_point] + middle_point_useful_right)

        # Recursive calls for the left and right halves
        dnc_n_curve(middle_point_useful_left, depth + 1, max_depth, points_list, point_list_of_every_iteration)
        points_list.append(new_middle_point)
        dnc_n_curve(middle_point_useful_right, depth + 1, max_depth, points_list, point_list_of_every_iteration)    
    
def generate_bezier_dnc(start_point, control_points, end_point, iterations):
    bezier_curve_points = [start_point]
    dnc_curve(start_point, control_points, end_point, 0, iterations, bezier_curve_points)
    bezier_curve_points += [end_point]
    return bezier_curve_points

def generate_bezier_dnc_n_curve(start_point, control_points, end_point, iterations):
    bezier_curve_points = []
    point_each_iteration = []
    dnc_n_curve([start_point] + control_points + [end_point], 0, iterations, bezier_curve_points, point_each_iteration)
    point_each_iteration.append([start_point] + bezier_curve_points + [end_point])
    # print(point_each_iteration)
    # for x in point_each_iteration:
    #     x.append(end_point)
    #     x.insert(0, start_point)
    print(point_each_iteration)
    return [start_point] + bezier_curve_points + [end_point], point_each_iteration

def generate_bezier_bruteforce(start_point, control_point, end_point, iterations):
    num_points = 2 ** iterations
    
    points = [start_point]
    for i in range(1, num_points):
        t = i / num_points
        x = (1 - t)**2 * start_point.x + 2 * (1 - t) * t * control_point.x + t**2 * end_point.x
        y = (1 - t)**2 * start_point.y + 2 * (1 - t) * t * control_point.y + t**2 * end_point.y
        points.append(Point(x, y))
    points.append(end_point)
    
    return points

# print(generate_bezier_dnc_n_curve(Point(5,1), [Point(2,2), Point(3,3)], Point(6,6), 4))
# print(generate_bezier_bruteforce(Point(5,1), Point(2,2), Point(6,6), 4))