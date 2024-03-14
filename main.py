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

def dnc_n_curve(control_start, control_points, control_end, depth, max_depth, points_list):
    if (len(control_points) == 1):
        dnc_curve(control_start, control_points[0], control_end, depth, max_depth, points_list)
    else:
        mid_index = len(control_points)//2
        dnc_n_curve(control_start, control_points[:mid_index], control_end, depth, max_depth, points_list)
        dnc_n_curve(control_start, control_points[mid_index+1:], control_end, depth, max_depth, points_list)

def generate_bezier_dnc(start_point, control_points, end_point, iterations):
    bezier_curve_points = [start_point]
    dnc_curve(start_point, control_points, end_point, 0, iterations, bezier_curve_points)
    bezier_curve_points += [end_point]
    return bezier_curve_points

def generate_bezier_dnc_n_curve(start_point, control_points, end_point, iterations):
    bezier_curve_points = [start_point]
    dnc_n_curve(start_point, control_points, end_point, 0, iterations, bezier_curve_points)
    bezier_curve_points += [end_point]
    return bezier_curve_points

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

print(generate_bezier_dnc_n_curve(Point(5,1), [Point(2,2)], Point(6,6), 4))
print(generate_bezier_bruteforce(Point(5,1), Point(2,2), Point(6,6), 4))

# def main():
#     print("Enter start, control, and end points for the Bézier curve:")

#     start_input = input("Enter start point as 'x,y': ").strip()
#     start_x, start_y = map(float, start_input.split(','))
#     start_point = Point(start_x, start_y)

#     control_input = input("Enter control point as 'x,y': ").strip()
#     control_x, control_y = map(float, control_input.split(','))
#     control_point = Point(control_x, control_y)

#     end_input = input("Enter end point as 'x,y': ").strip()
#     end_x, end_y = map(float, end_input.split(','))
#     end_point = Point(end_x, end_y)

#     num_input = int(input("Enter the number of iterations: ").strip())
#     method = input("Choose the method ('dnc' for divide and conquer, 'bf' for brute force): ").strip().lower()

#     if method == 'dnc':
#         bezier_points = generate_bezier_dnc(start_point, control_point, end_point, num_input)
#     elif method == 'bf':
#         bezier_points = generate_bezier_bruteforce(start_point, control_point, end_point, num_input)
#     else:
#         print("Invalid method. Please enter 'dnc' or 'bf'.")
#         return

#     print("\nThe points on the Bézier curve are:")
#     for point in bezier_points:
#         print(point)

# # Run the CLI
# main()
