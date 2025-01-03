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

lib.get_overall_center_of_gravity.argtypes = [ctypes.POINTER(Polygon), ctypes.c_int]
lib.get_overall_center_of_gravity.restype = Point

lib.get_combined_absolute_moment_of_inertia.argtypes = [ctypes.POINTER(Polygon), ctypes.c_int]
lib.get_combined_absolute_moment_of_inertia.restype = InertiaMoments

lib.get_combined_baricentric_moments_of_inertia.argtypes = [ctypes.POINTER(Polygon), ctypes.c_int, ctypes.POINTER(Point)]
lib.get_combined_baricentric_moments_of_inertia.restype = InertiaMoments


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
polygons = []

for i, (center_x, center_y) in enumerate(cups_center, start=1):
    vertices_square_cup = square_cup_verticies(center_x, center_y)
    point_array_cup = (Point * len(vertices_square_cup))(*[Point(x, y) for x, y in vertices_square_cup])
    
    area_square_cup = lib.get_polygon_area(point_array_cup, len(vertices_square_cup))
    absolute_moments = lib.get_absolute_moments_of_inertia(point_array_cup, len(vertices_square_cup))

    cup = Polygon(area_square_cup, Point(center_x, center_y), absolute_moments, angle=0.0)
    polygons.append(cup)
    
    baricentric_moments = lib.get_baricentric_moments_of_inertia(cup)
    
   
    print(f"============== Area for Cup {i} ===============")
    print(f"The area of the square cup {i} is: {area_square_cup}")
    print(f"=== Absolute Moment of Inertia for Cup {i} ====")
    print(f"Absolute moment of inertia for cup {i}:")
    print(f"jx: {absolute_moments.i:.5e} \njy: {absolute_moments.j:.5e} \njxy: {absolute_moments.ij:.5e}")
    print(f"Baricentric moment of inertia for cup {i}:")
    print(f"jx: {baricentric_moments.i:.5e} \njy: {baricentric_moments.j:.5e} \njxy: {baricentric_moments.ij:.5e}")

polygons_array = (Polygon * len(polygons))(*polygons)
overall_center_of_gravity = lib.get_overall_center_of_gravity(polygons_array, len(polygons))

print("========== Test Overall Center of Gravity ===========")
print(f"Overall center of gravity: x = {overall_center_of_gravity.x}, y = {overall_center_of_gravity.y}")

combined_absolute_moments = lib.get_combined_absolute_moment_of_inertia(polygons_array, len(polygons))

print(f"=== Test Absolute Moments of inertia entire piece ===")
print(f"jx: {combined_absolute_moments.i:.5e} \njy: {combined_absolute_moments.j:.5e} \njxy: {combined_absolute_moments.ij:.5e}")

combined_baricentric_moments = lib.get_combined_baricentric_moments_of_inertia(polygons_array, len(polygons), ctypes.byref(overall_center_of_gravity))

print(f"== Test Baricentric Moments of inertia entire piece ==")
print(f"jx: {combined_baricentric_moments.i:.5e} \njy: {combined_baricentric_moments.j:.5e} \njxy: {combined_baricentric_moments.ij:.5e}")
