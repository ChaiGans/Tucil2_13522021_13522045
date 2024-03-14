import tkinter as tk
from time import sleep

# Assuming Point class and Bezier curve functions are already defined
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

def generate_bezier_dnc(start_point, control_points, end_point, iterations):
    bezier_curve_points = [start_point]
    all_control_points = [start_point] + [control_points] + [end_point]
    dnc_curve(all_control_points, 0, iterations, bezier_curve_points)
    bezier_curve_points.append(end_point)
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

# Initialize the Tkinter window
root = tk.Tk()
root.title("Bezier Curve Animation")

# Create a canvas widget
# Create a canvas widget
canvas_width = 600
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Define control points and number of iterations or points
start_point = Point(50, 350)
control_point = Point(300, 50)
end_point = Point(550, 350)
iterations = 2  # More iterations for a smoother animation

# Function to draw a point on the canvas
def draw_point(point, color="black"):
    radius = 3
    canvas.create_oval(point.x - radius, point.y - radius, point.x + radius, point.y + radius, fill=color, outline=color)

# Function to draw axis and grid lines
def draw_axis_and_grid():
    # Draw horizontal and vertical axis lines
    canvas.create_line(0, canvas_height // 2, canvas_width, canvas_height // 2, fill="gray", arrow=tk.BOTH)
    canvas.create_line(canvas_width // 2, 0, canvas_width // 2, canvas_height, fill="gray", arrow=tk.BOTH)
    
    # Draw grid lines
    for i in range(0, canvas_width, 50):
        canvas.create_line(i, 0, i, canvas_height, fill="lightgray")
    for i in range(0, canvas_height, 50):
        canvas.create_line(0, i, canvas_width, i, fill="lightgray")

    # Add labels for axes
    canvas.create_text(canvas_width // 2 + 10, 10, text="Y", anchor="w")
    canvas.create_text(canvas_width - 10, canvas_height // 2 - 10, text="X", anchor="w")



# Function to animate the Bezier curve drawing
def animate_bezier_curve():
    # Clear the canvas
    canvas.delete("all")
    
    # Draw axis and grid lines
    draw_axis_and_grid()

    # Draw the control points
    draw_point(start_point, color="red")
    draw_point(control_point, color="red")
    draw_point(end_point, color="red")
    
    # Draw lines connecting the control points
    canvas.create_line(start_point.x, start_point.y, control_point.x, control_point.y, fill="red", dash=(4, 2))
    canvas.create_line(control_point.x, control_point.y, end_point.x, end_point.y, fill="red", dash=(4, 2))
    
    # Add coordinate labels for control points
    canvas.create_text(start_point.x + 10, start_point.y, text=f"({start_point.x}, {start_point.y})", anchor="w")
    canvas.create_text(control_point.x + 10, control_point.y, text=f"({control_point.x}, {control_point.y})", anchor="w")
    canvas.create_text(end_point.x + 10, end_point.y, text=f"({end_point.x}, {end_point.y})", anchor="w")
    
    # Generate Bezier curve points
    bezier_points = generate_bezier_bruteforce(start_point, control_point, end_point, iterations)
    
    # Draw the curve point by point
    for i in range(len(bezier_points) - 1):
        draw_point(bezier_points[i], color="blue")
        canvas.create_line(bezier_points[i].x, bezier_points[i].y, bezier_points[i+1].x, bezier_points[i+1].y, fill="blue")
        # if(i%2==0):
        #     canvas.create_text(bezier_points[i].x + 30, bezier_points[i].y, text=f"({bezier_points[i].x}, {bezier_points[i].y})", anchor="w")
        # else:
        #     canvas.create_text(bezier_points[i].x - 60, bezier_points[i].y, text=f"({bezier_points[i].x}, {bezier_points[i].y})", anchor="w")

        root.update()
        sleep(0.3)

# Button to start the animation
animate_button = tk.Button(root, text="Animate Bezier Curve", command=animate_bezier_curve)
animate_button.pack(side=tk.BOTTOM)

# Start the Tkinter loop
root.mainloop()
