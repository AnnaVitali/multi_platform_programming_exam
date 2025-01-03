from native import library_cffi

ffi = library_cffi.ffi
lib = library_cffi.lib

vertices_polygon = [
    (665, 394),
    (20, 262),
    (20, 135),
    (665, 4),
    (689, 17),
    (689, 380),
    (665, 394)
]

point_array_polygon = [ffi.new("Point *", {"x": x, "y": y}) for x, y in vertices_polygon]
point_array_polygon = ffi.new("Point[]", point_array_polygon)
area_polygon = lib.get_polygon_area(point_array_polygon, len(vertices_polygon))

print("============== Area ===============")
print(f"The area of the wood piece is: {area_polygon}")
