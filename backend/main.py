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

def dnc_curve(control_points, depth, max_depth, points_list):
    if depth < max_depth:
        new_control_points = [control_points[0]]
        for i in range(len(control_points) - 1):
            mid_point = find_midpoint(control_points[i], control_points[i + 1])
            new_control_points.append(mid_point)
        new_control_points.append(control_points[-1])

        mid_index = len(new_control_points) // 2

        left_points = []
        right_points = []

        for i in range(len(new_control_points)):
            if i <= mid_index:
                left_points.append(new_control_points[i])
            if i >= mid_index:
                right_points.append(new_control_points[i])

        dnc_curve(left_points, depth + 1, max_depth, points_list)
        points_list.append(new_control_points[len(new_control_points) // 2])
        dnc_curve(right_points, depth + 1, max_depth, points_list)

def generate_bezier_curve(start_point, control_points, end_point, iterations):
    bezier_curve_points = [start_point]
    all_control_points = [start_point] + control_points + [end_point]
    dnc_curve(all_control_points, 0, iterations, bezier_curve_points)
    bezier_curve_points.append(end_point)
    return bezier_curve_points

print(generate_bezier_curve(Point(0,1), [Point(2,2)], Point(3,1), 2))

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

# def main():
#     print("Enter your start, control, and end points for the Bézier curve:")

#     # Input for start point
#     start_input = input("Enter start point as 'x,y': ").strip()
#     start_x, start_y = map(float, start_input.split(','))
#     start_point = Point(start_x, start_y)

#     # Input for control point
#     control_input = input("Enter control point as 'x,y': ").strip()
#     control_x, control_y = map(float, control_input.split(','))
#     control_point = Point(control_x, control_y)

#     # Input for end point
#     end_input = input("Enter end point as 'x,y': ").strip()
#     end_x, end_y = map(float, end_input.split(','))
#     end_point = Point(end_x, end_y)

#     # Input for number of iterations
#     iterations_input = input("Enter the number of iterations for curve refinement: ").strip()
#     iterations = int(iterations_input)

#     # Generate and print the Bézier curve points
#     bezier_points = generate_bezier_curve(start_point, control_point, end_point, iterations)
#     print("\nThe points on the Bézier curve are:")
#     for point in bezier_points:
#         print(point)


# main()

