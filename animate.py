import tkinter as tk
from time import sleep
from main import *

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
start_point = Point(5*80,1*80)
control_point = [Point(2*80,2*80), Point(3*80,3*80)]
end_point = Point(6*80,6*80)
iterations = 4  # More iterations for a smoother animation

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
    for control in control_point:
        draw_point(control, color="red")
    draw_point(end_point, color="red")
    
    # Draw lines connecting the control points
    for i in range (len(control_point)):
        if (i == 0):
            canvas.create_line(start_point.x, start_point.y, control_point[i].x, control_point[i].y, fill="red", dash=(4, 2))
        if (i == len(control_point)-1):
            canvas.create_line(control_point[i].x, control_point[i].y, end_point.x, end_point.y, fill="red", dash=(4, 2))
        if (0 < i < len(control_point)-1):
            canvas.create_line(control_point[i].x, control_point[i].y, control_point[i+1].x, control_point[i+1].y, fill="red", dash=(4, 2))
    
    # Add coordinate labels for control points
    # canvas.create_text(start_point.x + 10, start_point.y, text=f"({start_point.x}, {start_point.y})", anchor="w")
    # canvas.create_text(control_point.x + 10, control_point.y, text=f"({control_point.x}, {control_point.y})", anchor="w")
    # canvas.create_text(end_point.x + 10, end_point.y, text=f"({end_point.x}, {end_point.y})", anchor="w")
    
    # Generate Bezier curve points
    bezier_points = generate_bezier_dnc_n_curve(start_point, control_point, end_point, iterations)
    print(bezier_points)
    
    # Draw the curve point by point
    for i in range(len(bezier_points) - 1):
        draw_point(bezier_points[i], color="blue")
        canvas.create_line(bezier_points[i].x, bezier_points[i].y, bezier_points[i+1].x, bezier_points[i+1].y, fill="blue")
        root.update()
        sleep(0.3)

# Button to start the animation
animate_button = tk.Button(root, text="Animate Bezier Curve", command=animate_bezier_curve)
animate_button.pack(side=tk.BOTTOM)

# Start the Tkinter loop
root.mainloop()
