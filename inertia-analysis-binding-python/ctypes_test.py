import ctypes

SQUARE_SIDE_SUCTION_CUP = 145

# Define the Point structure
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]
    
def square_cup_verticies(center_x, center_y):
    half_side = SQUARE_SIDE_SUCTION_CUP / 2

    square_vertices = [
        (center_x - half_side, center_y - half_side),
        (center_x - half_side, center_y + half_side),
        (center_x + half_side, center_y + half_side),
        (center_x + half_side, center_y - half_side),
        (center_x - half_side, center_y - half_side)  
    ]
    
    return square_vertices

lib = ctypes.CDLL("./native/liblibrary.so")

lib.get_polygon_area.argtypes = [ctypes.POINTER(Point), ctypes.c_int]
lib.get_polygon_area.restype = ctypes.c_double

# Define the vertices of the wood piece
vertices_polygon = [
    (665, 394),
    (20, 262),
    (20, 135),
    (665, 4),
    (689, 17),
    (689, 380),
    (665, 394)
]

# Define the vertices of the cups
center_x1, center_x2 = (210, 200)
verticies_square_cup = square_cup_verticies(center_x1, center_x2)

point_array_cup1 = (Point * len(verticies_square_cup))(*[Point(x, y) for x, y in verticies_square_cup])
point_array_polygon = (Point * len(vertices_polygon))(*[Point(x, y) for x, y in vertices_polygon])

area_square_cup = lib.get_polygon_area(point_array_cup1, len(verticies_square_cup))
area_polygon = lib.get_polygon_area(point_array_polygon, len(vertices_polygon))

# Print the area
print(f"The area of the square cup is: {area_square_cup}")
print(f"The area of the wood piece is: {area_polygon}")