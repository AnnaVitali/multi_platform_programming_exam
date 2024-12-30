import ctypes
import matplotlib as plt

lib = ctypes.CDLL("./native/library.so")

class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]
    
lib.get_polygon_area.argtypes = [ctypes.POINTER(Point), ctypes.c_int]

def square_suction_cup(center_x, center_y):
    square_side = 145
    half_side = square_side / 2

    square_coords = [
        (center_x - half_side, center_y - half_side),
        (center_x - half_side, center_y + half_side),
        (center_x + half_side, center_y + half_side),
        (center_x + half_side, center_y - half_side),
        (center_x - half_side, center_y - half_side)  # Close the square
    ]
    square_x, square_y = zip(*square_coords)

    return square_x, square_y

# Define the sides of the polygon and its vertices
sides = [((665, 394), (20, 262)), ((20, 262), (20, 135)), ((20, 135), (665, 4)), ((665, 4), (689, 17)),
            ((689, 17), (689, 380)), ((689, 380), (665, 394))]
points = [(665, 394), (20, 262), (20, 135), (665, 4), (689, 17), (689, 380), (665, 394)]

# Plot the polygon
x, y = zip(*points)  # Extract x and y coordinates
plt.figure(figsize=(8, 6))
plt.plot(x, y, '-o', label="Polygon")  # Draw the polygon and mark vertices
plt.scatter(*zip(*points), color='red', zorder=5, label="Vertices")  # Highlight vertices

# Add labels for vertices
for idx, (px, py) in enumerate(points[:-1]):  # Exclude the last repeated vertex
    plt.text(px + 5, py + 5, f"P{idx + 1}", color="blue", fontsize=10)

center_x1, center_y1 = (210, 200)
center_x2, center_y2 = (588, 200)

square_x1, square_y1 = square_suction_cup(center_x1, center_y1)
square_x2, square_y2 = square_suction_cup(center_x2, center_y2)

area_square_cup = lib.compute_polygon_area(list(zip(square_x1, square_y1)))

print(f"The area of the square cup is {area_square_cup}")