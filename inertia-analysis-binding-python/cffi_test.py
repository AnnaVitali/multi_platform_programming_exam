from native import library_cffi

SQUARE_SIDE_SUCTION_CUP = 145

ffi = library_cffi.ffi
lib = library_cffi.lib

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

vertices_polygon = [
    (665, 394),
    (20, 262),
    (20, 135),
    (665, 4),
    (689, 17),
    (689, 380),
    (665, 394)
]

point_array_polygon = ffi.new("Point[]", [{"x": x, "y": y} for x, y in vertices_polygon])
area_polygon = lib.get_polygon_area(point_array_polygon, len(vertices_polygon))

print("============== Area ===============")
print(f"The area of the wood piece is: {area_polygon}")

cups_center = [(210, 200), (588, 200)]
polygons = []

for i, (center_x, center_y) in enumerate(cups_center, start=1):
    vertices_square_cup = square_cup_verticies(center_x, center_y)
    point_array_cup = ffi.new("Point[]", [{"x": x, "y": y} for x, y in vertices_square_cup])
    
    area_square_cup = lib.get_polygon_area(point_array_cup, len(vertices_square_cup))
    absolute_moments = lib.get_absolute_moments_of_inertia(point_array_cup, len(vertices_square_cup))

    cup = ffi.new("Polygon", {
        "area": area_square_cup,
        "barycenter": {"x": center_x, "y": center_y},
        "absolute_moments_of_inertia": absolute_moments,
        "angle": 0.0
    })
    
    polygons.append(cup[0])
    
    baricentric_moments = lib.get_baricentric_moments_of_inertia(cup)
    
    print(f"============== Area for Cup {i} ===============")
    print(f"The area of the square cup {i} is: {area_square_cup}")
    print(f"=== Absolute Moment of Inertia for Cup {i} ====")
    print(f"Absolute moment of inertia for cup {i}:")
    print(f"jx: {absolute_moments.i:.5e} \njy: {absolute_moments.j:.5e} \njxy: {absolute_moments.ij:.5e}")
    print(f"Baricentric moment of inertia for cup {i}:")
    print(f"jx: {baricentric_moments.i:.5e} \njy: {baricentric_moments.j:.5e} \njxy: {baricentric_moments.ij:.5e}")
    
polygons_array = ffi.new("Polygon[]", polygons)
overall_center_of_gravity = lib.get_overall_center_of_gravity(polygons_array, len(polygons))

print("========== Test Overall Center of Gravity ===========")
print(f"Overall center of gravity: x = {overall_center_of_gravity.x}, y = {overall_center_of_gravity.y}")

combined_absolute_moments = lib.get_combined_absolute_moment_of_inertia(polygons_array, len(polygons))

print(f"=== Test Absolute Moments of inertia entire piece ===")
print(f"jx: {combined_absolute_moments.i:.5e} \njy: {combined_absolute_moments.j:.5e} \njxy: {combined_absolute_moments.ij:.5e}")

combined_baricentric_moments = lib.get_combined_baricentric_moments_of_inertia(polygons_array, len(polygons), ffi.new("Point*", {"x": overall_center_of_gravity.x, "y": overall_center_of_gravity.y}))

print(f"== Test Baricentric Moments of inertia entire piece ==")
print(f"jx: {combined_baricentric_moments.i:.5e} \njy: {combined_baricentric_moments.j:.5e} \njxy: {combined_baricentric_moments.ij:.5e}")


