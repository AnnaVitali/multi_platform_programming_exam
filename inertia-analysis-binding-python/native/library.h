#ifndef MOMENTS_OF_INERTIA_H
#define MOMENTS_OF_INERTIA_H

typedef struct {
    double x;
    double y;
} Point;

typedef struct {
    double i;
    double j;
    double ij;
} InertiaMoments;


typedef struct {
    double area;
    Point barycenter;
    InertiaMoments absolute_moments_of_inertia;
    double angle;
} Polygon;

double get_polygon_area(Point* vertices, int num_vertices);
InertiaMoments get_absolute_moments_of_inertia(Point* vertices, int num_vertices);
InertiaMoments get_baricentric_moments_of_inertia(Polygon* polygon);
Point get_overall_center_of_gravity(Polygon* polygons, int num_polygons);
InertiaMoments get_combined_absolute_moment_of_inertia(Polygon* polygons, int num_polygons);
InertiaMoments get_combined_baricentric_moments_of_inertia(Polygon* polygons, int num_polygons, Point* center_of_gravity);

#endif // MOMENTS_OF_INERTIA_H