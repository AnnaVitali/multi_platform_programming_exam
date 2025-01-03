import ctypes

SQUARE_SIDE_SUCTION_CUP = 145

# Define the Point structure
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]
    
class InertiaMoments(ctypes.Structure):
    _fields_ = [("i", ctypes.c_double), ("j", ctypes.c_double), ("ij", ctypes.c_double)]
    
class Polygon(ctypes.Structure):
    _fields_ = [("area", ctypes.c_double), ("barycenter", Point), ("absolute_moments_of_inertia", InertiaMoments), ("angle", ctypes.c_double)]
      
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

lib.get_absolute_moments_of_inertia.argtypes = [ctypes.POINTER(Point), ctypes.c_int]
lib.get_absolute_moments_of_inertia.restype = InertiaMoments

lib.get_baricentric_moments_of_inertia.argtypes = [ctypes.POINTER(Polygon)]
lib.get_baricentric_moments_of_inertia.restype = InertiaMoments

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

point_array_polygon = (Point * len(vertices_polygon))(*[Point(x, y) for x, y in vertices_polygon])
area_polygon = lib.get_polygon_area(point_array_polygon, len(vertices_polygon))

print("============== Area ===============")
print(f"The area of the wood piece is: {area_polygon}")


cups_center = [(210, 200), (588, 200)]

for i, (center_x, center_y) in enumerate(cups_center, start=1):
    vertices_square_cup = square_cup_verticies(center_x, center_y)
    point_array_cup = (Point * len(vertices_square_cup))(*[Point(x, y) for x, y in vertices_square_cup])
    
    area_square_cup = lib.get_polygon_area(point_array_cup, len(vertices_square_cup))
    absolute_moments = lib.get_absolute_moments_of_inertia(point_array_cup, len(vertices_square_cup))

    cup = Polygon(area_square_cup, Point(center_x, center_y), absolute_moments, angle=0.0)
    
    baricentric_moments = lib.get_baricentric_moments_of_inertia()
    
   
    print(f"============== Area for Cup {i} ===============")
    print(f"The area of the square cup {i} is: {area_square_cup}")
    print(f"=== Absolute Moment of Inertia for Cup {i} ====")
    print(f"Absolute moment of inertia for cup {i}:")
    print(f"jx: {absolute_moments.i} /n jy: {absolute_moments.j} /n jxy: {absolute_moments.ij}")
    print(f"Baricentric moment of inertia for cup {i}:")
    print(f"jx: {baricentric_moments.i} /n jy: {baricentric_moments.j} /n jxy: {baricentric_moments.ij}")








