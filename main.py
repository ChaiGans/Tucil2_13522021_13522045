class Position:
  def __init__(self, x, y):
    self.x = x
    self.y = y

point_list = []
def dnc_curve(initial_position : Position, end_position : Position, control_coordinate : Position, n_iteration : int):
  global point_list
  if (n_iteration == 0):
    point_list.append(initial_position)
    point_list.append(end_position)
  else :
    middle_point_1 = Position((initial_position.x + control_coordinate.x)/2 , (initial_position.y + control_coordinate.y)/2)
    middle_point_2 = Position((end_position.x + control_coordinate.x)/2 , (end_position.y + control_coordinate.y)/2)
    dnc_curve(initial_position, control_coordinate, middle_point_1, n_iteration-1)
    dnc_curve(control_coordinate, end_position, middle_point_2, n_iteration-1)

dnc_curve(Position(2,0), Position(6,6), Position(3,3) , 3)
point_list = sorted(list(set(point_list)), key=lambda p: p.x)
for point in point_list:
  print(point.x, point.y)
