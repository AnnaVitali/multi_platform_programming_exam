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
    InertiaMoments moments;
    double area = polygon->area;
    double x_g = polygon->barycenter_x;
    double y_g = polygon->barycenter_y;
    double jx = polygon->absolute_moments_of_inertia[0];
    double jy = polygon->absolute_moments_of_inertia[1];
    double jxy = polygon->absolute_moments_of_inertia[2];
    double angle_rad = polygon->angle;
    double cos_angle = cos(angle_rad);
    double sin_angle = sin(angle_rad);

    double i_prime = jx - y_g * y_g * area;
    double j_prime = jy - x_g * x_g * area;
    double ij_prime = jxy - y_g * x_g * area;

    moments.i = i_prime * cos_angle * cos_angle + j_prime * sin_angle * sin_angle - ij_prime * 2 * sin_angle * cos_angle;
    moments.j = i_prime * sin_angle * sin_angle + j_prime * cos_angle * cos_angle + ij_prime * 2 * sin_angle * cos_angle;
    moments.ij = (i_prime - j_prime) * sin_angle * cos_angle + ij_prime * (cos_angle * cos_angle - sin_angle * sin_angle);

    return moments;
}

Point get_overall_center_of_gravity(Polygon* polygons, int num_polygons) {
    Point center_of_gravity = {0, 0};
    double total_area = 0;
    double weighted_cx_sum = 0;
    double weighted_cy_sum = 0;

    for (int i = 0; i < num_polygons; i++) {
        double area = polygons[i].area;
        double barycenter_x = polygons[i].barycenter_x;
        double barycenter_y = polygons[i].barycenter_y;

        total_area += area;
        weighted_cx_sum += area * barycenter_x;
        weighted_cy_sum += area * barycenter_y;
    }

    center_of_gravity.x = weighted_cx_sum / total_area;
    center_of_gravity.y = weighted_cy_sum / total_area;

    return center_of_gravity;
}

InertiaMoments get_combined_absolute_moment_of_inertia(Polygon* polygons, int num_polygons) {
    InertiaMoments moments = {0, 0, 0};

    for (int i = 0; i < num_polygons; i++) {
        moments.i += polygons[i].absolute_moments_of_inertia[0];
        moments.j += polygons[i].absolute_moments_of_inertia[1];
        moments.ij += polygons[i].absolute_moments_of_inertia[2];
    }

    return moments;
}

InertiaMoments get_combined_baricentric_moments_of_inertia(Polygon* polygons, int num_polygons, double x_G, double y_G) {
    InertiaMoments moments = {0, 0, 0};
    double area_total = 0;

    for (int i = 0; i < num_polygons; i++) {
        moments.i += polygons[i].absolute_moments_of_inertia[0];
        moments.j += polygons[i].absolute_moments_of_inertia[1];
        moments.ij += polygons[i].absolute_moments_of_inertia[2];
        area_total += polygons[i].area;
    }

    double jx = moments.i - y_G * y_G * area_total;
    double jy = moments.j - x_G * x_G * area_total;
    double jxy = moments.ij - y_G * x_G * area_total;

    moments.i = (jx + jy) / 2 - 0.5 * sqrt((jx - jy) * (jx - jy) + 4 * jxy * jxy);
    moments.j = (jx + jy) / 2 + 0.5 * sqrt((jx - jy) * (jx - jy) + 4 * jxy * jxy);

    return moments;
}