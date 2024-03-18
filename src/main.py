from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from function import *
from tkinter import Tk, Canvas, messagebox, Radiobutton, IntVar
import tkinter as tk
import time

def close_window(event=None):
    window.destroy()

animation_in_progress = False
def generate_button():
    global ani, execution_time_var, ax, canvas, bezier_line, control_line,animation_in_progress

    if animation_in_progress:
        messagebox.showerror("Error", "An animation is already in progress. Please wait until it finishes before starting a new one.")
        return

    try:
        num_points = int(number_of_points.get())
        if num_points < 3:
            messagebox.showerror("Error", "You must input minimum 3 points.")
            return
    except ValueError:
        messagebox.showerror("Error", "Number of points must be an integer.")
        return

    try:
        points_str = input_points.get().strip()
        if not all(s.strip().count(',') == 1 for s in points_str.split('),(')):
            raise ValueError("Invalid format for points. Format should be (x,y),(x,y),... with no spaces between numbers and commas")

        points_list = [Point(float(point_part.split(',')[0].strip(' ()')), float(point_part.split(',')[1].strip(' ()'))) for point_part in points_str.split('),(')]
        if len(points_list) != num_points:
            raise ValueError("The number of input points does not match the number specified.")

        start_point = points_list[0]
        control_points = points_list[1:-1]
        end_point = points_list[-1]
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid points input: {e}")
        return

    try:
        iterations = int(number_of_iterations.get())
    except ValueError:
        messagebox.showerror("Error", "Number of iterations must be an integer.")
        return

    animation_in_progress = True

    ax.clear()
    ax.set_title('Bezier Curve Generator\nIterations more than 4 may take times')
    ax.set_axis_on()

    all_x = [p.x for p in points_list]
    all_y = [p.y for p in points_list]
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    ax.set_xlim(x_min - 1, x_max + 1)
    ax.set_ylim(y_min - 1, y_max + 1)

    bezier_line, = ax.plot([], [], 'b-', label='Bezier Curve', lw=2, marker='o', markersize=5)
    
    lines = []
    def init():
        global control_line, bezier_line  
        lines.clear() 
        control_line, = ax.plot([], [], 'ro--', label='Control Points', lw=1)
        bezier_line, = ax.plot([], [], 'b-', label='Bezier Curve', lw=2, marker='o', markersize=5)
        lines.append(control_line)
        lines.append(bezier_line)
        return lines

    def animate_bruteforce(i):
        global control_line, bezier_line, animation_in_progress
        if i < len(x_points):
            x = x_points[:i + 1]
            y = y_points[:i + 1]
            bezier_line.set_data(x, y)
            control_line.set_data(x_control, y_control)

        if i == len(x_points) - 1 :
            animation_in_progress = False
            
        return bezier_line,control_line

    x_control = [p.x for p in [start_point] + control_points + [end_point]]
    y_control = [p.y for p in [start_point] + control_points + [end_point]]
    control_line, = ax.plot(x_control, y_control, 'ro--', label='Control Points', lw=1,markersize=5)

    exec_time = 0
    try:
        if method_var.get() == 1:
            if len(points_list) != 3:
                raise ValueError("Brute force method requires exactly 3 points.")
            
            start_bf = time.time()
            bezier_points = generate_bezier_bruteforce(start_point, control_points[0], end_point, iterations)
            end_bf = time.time()

            exec_time = (end_bf - start_bf) * 1000
            x_points = [point.x for point in bezier_points]
            y_points = [point.y for point in bezier_points]
            ani = FuncAnimation(fig, animate_bruteforce, init_func=init, frames=len(x_points), interval=100, blit=True, repeat=False) # change interval for faster animation
        else:
            control_line.set_data(x_control, y_control)
            bezier_line.set_data([], [])
            intermediate_lines = []
            def animate_dnc(i):
                global animation_in_progress
                nonlocal intermediate_lines

                for line in intermediate_lines:
                    line.remove()
                intermediate_lines = []

                if i < len(all_iterations_points):
                    current_points = all_iterations_points[i]

                    x = [p.x for p in current_points]
                    y = [p.y for p in current_points]
                    line, = ax.plot(x, y, 'b--', lw=1, marker='o', markersize=5)
                    intermediate_lines.append(line)

                if i == len(all_iterations_points) - 1 or i == len(all_iterations_points):
                    animation_in_progress = False
                    line.set_color('b')
                    line.set_linestyle('-')
                    line.set_linewidth(2)

                return intermediate_lines

            start_dnc = time.time()
            all_iterations_points = generate_bezier_dnc_n_curve(start_point, control_points, end_point, iterations)
            end_dnc = time.time()
            exec_time = (end_dnc - start_dnc)*1000
            
            ani = FuncAnimation(fig, animate_dnc, init_func=init, frames=len(all_iterations_points), interval=500, blit=True, repeat=False)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        animation_in_progress = False
        return

    execution_time_var.set(f"Execution time: {exec_time:.4f} ms")

    control_line.set_data(x_control, y_control)
    ax.legend(handles=[control_line, bezier_line], loc='best')
    window.ani = ani
    canvas.draw()

# Main application window
window = Tk()
window.geometry("1142x618")
window.configure(bg = "#130202")

canvas = Canvas(
    window,
    bg = "#130202",
    height = 618,
    width = 1142,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    400.0,
    24.0,
    anchor="nw",
    text="Bezier Curve Generator",
    fill="#1EFF6A",
    font=("Times New Roman", 40 * -1)
)

canvas.create_rectangle(
    570.0,
    94.0,
    571.0,
    573.0,
    fill="#1EFF6A",
    outline="")

method_var = tk.IntVar(value=2)  # Default to DNC

# Create radio buttons for method selection
brute_force_rb = Radiobutton(window, text="Brute Force", variable=method_var, value=1, bg="#000000", fg="#0c88e9",font=("Times New Roman", 20))
dnc_rb = Radiobutton(window, text="Divide and Conquer", variable=method_var, value=2, bg="#000000", fg="#0c88e9",font=("Times New Roman", 20))
brute_force_rb.place(x=90.0, y=90.0)
dnc_rb.place(x=290.0, y=90.0)

# Create 'Number of Points' label and entry
number_of_points_label = tk.Label(window, text="Number of Points :", bg="#130202", fg="#1EFF6A", font=("Times New Roman", 32 * -1))
number_of_points_label.place(x=98.0, y=131.0)
number_of_points = tk.Entry(window, bg="#1EFF6A",fg="#000000", insertbackground="#000000",font=("Times New Roman", 20))
number_of_points.place(x=98.0, y=177.0, width=377.0, height=52.0)

# Create 'Input Points (x,y)' label and entry
input_points_label = tk.Label(window, text="Input Points (x,y) :", bg="#130202", fg="#1EFF6A", font=("Times New Roman", 32 * -1))
input_points_label.place(x=98.0, y=240.0)
input_points = tk.Entry(window, bg="#1EFF6A",fg="#000000", insertbackground="#000000",font=("Times New Roman", 20))
input_points.place(x=98.0, y=289.0, width=377.0, height=52.0)

# Create 'Number of Iterations' label and entry
number_of_iterations_label = tk.Label(window, text="Number of Iterations :", bg="#130202", fg="#1EFF6A", font=("Times New Roman", 32 * -1))
number_of_iterations_label.place(x=98.0, y=354.0)
number_of_iterations = tk.Entry(window, bg="#1EFF6A",fg="#000000", insertbackground="#000000",font=("Times New Roman", 20))
number_of_iterations.place(x=98.0, y=403.0, width=377.0, height=52.0)

# Create 'Execution time' label and entry
execution_time_var = tk.StringVar(window)
execution_time_var.set("Execution time: ")
execution_times_label = tk.Label(window,  textvariable=execution_time_var, bg="#130202", fg="#1EFF6A", font=("Times New Roman", 32 * -1))
execution_times_label.place(x=575.0, y=90.0)

# Create a Matplotlib figure and axes
fig = Figure()
ax = fig.add_subplot(111)
ax.set_axis_off()  # Hide axis initially
placeholder_text = ax.text(0.5, 0.5, "Click 'Generate' to display the Bezier curve", ha='center', va='center', fontsize=12)

canvas = FigureCanvasTkAgg(fig, master=window)
mpl_canvas_widget = canvas.get_tk_widget()
mpl_canvas_widget.place(x=580, y=135, width=550, height=440)

button_border = tk.Frame(window, highlightbackground="#1EFF6A", highlightthickness=2, bd=0)
button_border.place(x=153.0, y=504.0, width=264.0, height=69.0)

generate_button = tk.Button(button_border, text="Generate", command=generate_button, bg="#1EFF6A", fg="#000000", font=("Times New Roman", 32))
generate_button.pack(expand=True, fill=tk.BOTH)

window.bind('<Escape>', close_window)
window.resizable(False, False)
window.mainloop()
