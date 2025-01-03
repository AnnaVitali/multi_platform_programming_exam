#include "library.h"
#include <math.h>
#include <stdlib.h>

double get_polygon_area(Point* vertices, int num_vertices) {
    double area = 0.0;
    for (int i = 0; i < num_vertices; i++) {
        int next = (i + 1) % num_vertices;
        area += vertices[i].x * vertices[next].y - vertices[next].x * vertices[i].y;
    }
    return fabs(area) / 2.0;
}

InertiaMoments get_absolute_moments_of_inertia(Point* vertices, int num_vertices) {
    InertiaMoments moments = {0, 0, 0};

    for (int i = 0; i < num_vertices - 1; i++) {
        double x_i = vertices[i].x;
        double y_i = vertices[i].y;
        double x_next = vertices[i + 1].x;
        double y_next = vertices[i + 1].y;

        double common_term = x_i * y_next - x_next * y_i;

        moments.i += (y_i * y_i + y_i * y_next + y_next * y_next) * common_term;
        moments.j += (x_i * x_i + x_i * x_next + x_next * x_next) * common_term;
        moments.ij += (x_i * y_next + 2 * x_i * y_i + 2 * x_next * y_next + x_next * y_i) * common_term;
    }

    moments.i = fabs(moments.i) / 12.0;
    moments.j = fabs(moments.j) / 12.0;
    moments.ij = fabs(moments.ij) / 24.0;

    return moments;
}

InertiaMoments get_baricentric_moments_of_inertia(Polygon* polygon) {
    InertiaMoments moments = polygon->absolute_moments_of_inertia;
    double area = polygon->area;
    Point barycenter = polygon->barycenter;

    moments.i -= area * barycenter.y * barycenter.y;
    moments.j -= area * barycenter.x * barycenter.x;
    moments.ij -= area * barycenter.x * barycenter.y;

    return moments;
}

Point get_overall_center_of_gravity(Polygon* polygons, int num_polygons) {
    double total_area = 0.0;
    Point overall_center = {0.0, 0.0};

    for (int i = 0; i < num_polygons; i++) {
        total_area += polygons[i].area;
        overall_center.x += polygons[i].barycenter.x * polygons[i].area;
        overall_center.y += polygons[i].barycenter.y * polygons[i].area;
    }

    overall_center.x /= total_area;
    overall_center.y /= total_area;

    return overall_center;
}

InertiaMoments get_combined_absolute_moment_of_inertia(Polygon* polygons, int num_polygons) {
    InertiaMoments combined_moments = {0, 0, 0};

    for (int i = 0; i < num_polygons; i++) {
        combined_moments.i += polygons[i].absolute_moments_of_inertia.i;
        combined_moments.j += polygons[i].absolute_moments_of_inertia.j;
        combined_moments.ij += polygons[i].absolute_moments_of_inertia.ij;
    }

    return combined_moments;
}

InertiaMoments get_combined_baricentric_moments_of_inertia(Polygon* polygons, int num_polygons, double x_G, double y_G) {
    InertiaMoments combined_moments = {0, 0, 0};

    for (int i = 0; i < num_polygons; i++) {
        InertiaMoments moments = polygons[i].absolute_moments_of_inertia;
        double area = polygons[i].area;
        Point barycenter = polygons[i].barycenter;

        moments.i -= area * barycenter.y * barycenter.y;
        moments.j -= area * barycenter.x * barycenter.x;
        moments.ij -= area * barycenter.x * barycenter.y;

        combined_moments.i += moments.i + area * (barycenter.y - y_G) * (barycenter.y - y_G);
        combined_moments.j += moments.j + area * (barycenter.x - x_G) * (barycenter.x - x_G);
        combined_moments.ij += moments.ij + area * (barycenter.x - x_G) * (barycenter.y - y_G);
    }

    return combined_moments;
}