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

def generate_bezier_curve(start_point, control_point, end_point, iterations):
    bezier_curve_points = [start_point]

    print(bezier_curve_points)
    dnc_curve(start_point, control_point, end_point, 0, iterations, bezier_curve_points)

    bezier_curve_points.append(end_point)
    return bezier_curve_points

# # main
# start = Point(0, 0)
# control = Point(1, 1)
# end = Point(3, 0)
# iterations = 2

# # Generate Bezier curve points
# bezier_points = generate_bezier_curve(start, control, end, iterations)
# # print(bezier_points)
# for point in bezier_points:
#     print(f'({point.x}, {point.y})')

def main():
    print("Enter your start, control, and end points for the Bézier curve:")

    # Input for start point
    start_input = input("Enter start point as 'x,y': ").strip()
    start_x, start_y = map(float, start_input.split(','))
    start_point = Point(start_x, start_y)

    # Input for control point
    control_input = input("Enter control point as 'x,y': ").strip()
    control_x, control_y = map(float, control_input.split(','))
    control_point = Point(control_x, control_y)

    # Input for end point
    end_input = input("Enter end point as 'x,y': ").strip()
    end_x, end_y = map(float, end_input.split(','))
    end_point = Point(end_x, end_y)

    # Input for number of iterations
    iterations_input = input("Enter the number of iterations for curve refinement: ").strip()
    iterations = int(iterations_input)

    # Generate and print the Bézier curve points
    bezier_points = generate_bezier_curve(start_point, control_point, end_point, iterations)
    print("\nThe points on the Bézier curve are:")
    for point in bezier_points:
        print(point)


main()

