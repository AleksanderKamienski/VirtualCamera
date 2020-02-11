from load_polyhedrons.LoadPolyherdons import get_lines, get_figures
from figures_points_lines_definition.Point3D import Point3D
from Projection import projection
from figures_points_lines_definition.Line3D import Line3D
from shapely.geometry import Polygon


# Animation.py asks this function tu return lines2d in proper order
def sorted_figures(lines, _camera):
    figures = get_figures(lines)

    sorted_figures_in_depth = sort_figures(figures, _camera)

    sorted_figures_resolve_ambiguity = check_overlaps(sorted_figures_in_depth, _camera)

    _lines = []
    for i in range(len(sorted_figures_resolve_ambiguity)):
        _lines.append(Line3D(sorted_figures_resolve_ambiguity[i].point1, sorted_figures_resolve_ambiguity[i].point2))
        _lines.append(Line3D(sorted_figures_resolve_ambiguity[i].point2, sorted_figures_resolve_ambiguity[i].point3))
        _lines.append(Line3D(sorted_figures_resolve_ambiguity[i].point3, sorted_figures_resolve_ambiguity[i].point4))
        _lines.append(Line3D(sorted_figures_resolve_ambiguity[i].point4, sorted_figures_resolve_ambiguity[i].point1))

    lines2d = projection(_lines, _camera)
    return lines2d


# depth sort (y coordinate)
def sort_figures(figures, _camera):
    # order according to the largest y value (depth value)
    for i in range(len(figures)):
        for j in range(0, len(figures) - i - 1):
            if (max(figures[j].point1.y, figures[j].point2.y, figures[j].point3.y, figures[j].point4.y) <
                    max(figures[j + 1].point1.y, figures[j + 1].point2.y, figures[j + 1].point3.y,
                        figures[j + 1].point4.y)):
                figures[j], figures[j + 1] = figures[j + 1], figures[j]
    return figures


# check overlaps in depth and resolve ambiguities
def check_overlaps(figures, _camera):
    # number of figures that current figure(figures[i]) covers
    count = 0
    # sorted array which function returns
    result = []
    # while loop loops 20 times in our case. We don't want infinite loop.
    max_while_loop = len(figures)
    iterator = 0
    # loops while result array is full but no more than len(figures) times.
    while len(result) < len(figures):
        iterator += 1
        if iterator > max_while_loop:
            return result
        for i in range(len(figures)):
            if figures[i] not in result:
                for j in range(len(figures)):
                    if figures[j] not in result and j != i:
                        if covers_test(figures[i], figures[j], _camera):
                            count += 1
                if count == 0:
                    if figures[i] not in result:
                        result.append(figures[i])
                count = 0

    return result


# 4 tests in depth sort when overlap occures
def covers_test(figure1, figure2, camera):
    ymin_figure1 = min(figure1.point1.y, figure1.point2.y, figure1.point3.y, figure1.point4.y)
    ymax_figure1 = max(figure1.point1.y, figure1.point2.y, figure1.point3.y, figure1.point4.y)
    ymin_figure2 = min(figure2.point1.y, figure2.point2.y, figure2.point3.y, figure2.point4.y)
    ymax_figure2 = max(figure2.point1.y, figure2.point2.y, figure2.point3.y, figure2.point4.y)
    test_count = 0
    if ymin_figure1 > ymax_figure2:
        return False

    elif ymin_figure1 <= ymin_figure2 <= ymax_figure1 or ymin_figure2 <= ymin_figure1 <= ymax_figure2:
        # test_count increases when test passes

        # test 1
        xmin_figure1 = min(figure1.point1.x, figure1.point2.x, figure1.point3.x, figure1.point4.x)
        xmax_figure1 = max(figure1.point1.x, figure1.point2.x, figure1.point3.x, figure1.point4.x)
        zmin_figure1 = min(figure1.point1.z, figure1.point2.z, figure1.point3.z, figure1.point4.z)
        zmax_figure1 = max(figure1.point1.z, figure1.point2.z, figure1.point3.z, figure1.point4.z)

        xmin_figure2 = min(figure2.point1.x, figure2.point2.x, figure2.point3.x, figure2.point4.x)
        xmax_figure2 = max(figure2.point1.x, figure2.point2.x, figure2.point3.x, figure2.point4.x)
        zmin_figure2 = min(figure2.point1.z, figure2.point2.z, figure2.point3.z, figure2.point4.z)
        zmax_figure2 = max(figure2.point1.z, figure2.point2.z, figure2.point3.z, figure2.point4.z)
        if not ((xmin_figure1 <= xmin_figure2 <= xmax_figure1 or xmin_figure2 <= xmin_figure1 <= xmax_figure2) or
                (zmin_figure1 <= zmin_figure2 <= zmax_figure1 or zmin_figure2 <= zmin_figure1 <= zmax_figure2)):
            test_count += 1

        # test 2
        if covers(figure2, figure1, camera):
            test_count += 1
        # test 3
        if front(figure2, figure1, camera):
            test_count += 1
        # test 4
        figure1_projected = projection([Line3D(figure1.point1, figure1.point2),
                                        Line3D(figure1.point2, figure1.point3),
                                        Line3D(figure1.point3, figure1.point4),
                                        Line3D(figure1.point4, figure1.point1)],
                                       camera)
        figure2_projected = projection([Line3D(figure2.point1, figure2.point2),
                                        Line3D(figure2.point2, figure2.point3),
                                        Line3D(figure2.point3, figure2.point4),
                                        Line3D(figure2.point4, figure2.point1)],
                                       camera)

        if len(figure1_projected) > 0 and len(figure2_projected) > 0:
            p1 = Polygon([(figure1_projected[0].points[0].x, figure1_projected[0].points[0].y),
                          (figure1_projected[0].points[1].x, figure1_projected[0].points[1].y),
                          (figure1_projected[2].points[0].x, figure1_projected[2].points[0].y),
                          (figure1_projected[2].points[1].x, figure1_projected[2].points[1].y)])

            p2 = Polygon([(figure2_projected[0].points[0].x, figure2_projected[0].points[0].y),
                          (figure2_projected[0].points[1].x, figure2_projected[0].points[1].y),
                          (figure2_projected[2].points[0].x, figure2_projected[2].points[0].y),
                          (figure2_projected[2].points[1].x, figure2_projected[2].points[1].y)])

            if p2.is_valid and p1.is_valid:
                if not p1.intersects(p2):
                    test_count += 1

    if test_count > 0:
        return False
    elif test_count == 0:
        return True


# check if figure 1 covers figure2
def covers(figure1, figure2, camera):
    A = Point3D(figure1.point1.x, figure1.point1.y, figure1.point1.z)
    B = Point3D(figure1.point2.x, figure1.point2.y, figure1.point2.z)
    C = Point3D(figure1.point3.x, figure1.point3.y, figure1.point3.z)
    X1 = Point3D(figure2.point1.x, figure2.point1.y, figure2.point1.z)
    X2 = Point3D(figure2.point2.x, figure2.point2.y, figure2.point2.z)
    X3 = Point3D(figure2.point3.x, figure2.point3.y, figure2.point3.z)
    X4 = Point3D(figure2.point4.x, figure2.point4.y, figure2.point4.z)
    _B = Point3D(B.x - A.x, B.y - A.y, B.z - A.z)
    _C = Point3D(C.x - A.x, C.y - A.y, C.z - A.z)
    _X1 = Point3D(X1.x - A.x, X1.y - A.y, X1.z - A.z)
    det_X1 = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [_X1.x, _X1.y, _X1.z]])
    _X2 = Point3D(X2.x - A.x, X2.y - A.y, X2.z - A.z)
    det_X2 = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [_X2.x, _X2.y, _X2.z]])
    _X3 = Point3D(X3.x - A.x, X3.y - A.y, X3.z - A.z)
    det_X3 = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [_X3.x, _X3.y, _X3.z]])
    _X4 = Point3D(X4.x - A.x, X4.y - A.y, X4.z - A.z)
    det_X4 = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [_X4.x, _X4.y, _X4.z]])

    camera_XYZ = Point3D(camera.x - A.x, camera.y - A.y, camera.z - A.z)
    det_camera_XYZ = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [camera_XYZ.x, camera_XYZ.y, camera_XYZ.z]])

    if det_camera_XYZ <= 0 and (det_X1 >= 0 and det_X2 >= 0 and det_X3 >= 0 and det_X4 >= 0):
        return True
    elif det_camera_XYZ >= 0 and (det_X1 <= 0 and det_X2 <= 0 and det_X3 <= 0 and det_X4 <= 0):
        return True
    else:
        return False


# check if figure 1 is in front of figure2
def front(figure1, figure2, camera):
    A = Point3D(figure2.point1.x, figure2.point1.y, figure2.point1.z)
    B = Point3D(figure2.point2.x, figure2.point2.y, figure2.point2.z)
    C = Point3D(figure2.point3.x, figure2.point3.y, figure2.point3.z)
    X1 = Point3D(figure1.point1.x, figure1.point1.y, figure1.point1.z)
    X2 = Point3D(figure1.point2.x, figure1.point2.y, figure1.point2.z)
    X3 = Point3D(figure1.point3.x, figure1.point3.y, figure1.point3.z)
    X4 = Point3D(figure1.point4.x, figure1.point4.y, figure1.point4.z)
    _B = Point3D(B.x - A.x, B.y - A.y, B.z - A.z)
    _C = Point3D(C.x - A.x, C.y - A.y, C.z - A.z)
    _X1 = Point3D(X1.x - A.x, X1.y - A.y, X1.z - A.z)
    det_X1 = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [_X1.x, _X1.y, _X1.z]])
    _X2 = Point3D(X2.x - A.x, X2.y - A.y, X2.z - A.z)
    det_X2 = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [_X2.x, _X2.y, _X2.z]])
    _X3 = Point3D(X3.x - A.x, X3.y - A.y, X3.z - A.z)
    det_X3 = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [_X3.x, _X3.y, _X3.z]])
    _X4 = Point3D(X4.x - A.x, X4.y - A.y, X4.z - A.z)
    det_X4 = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [_X4.x, _X4.y, _X4.z]])

    camera_XYZ = Point3D(camera.x - A.x, camera.y - A.y, camera.z - A.z)
    det_camera_XYZ = dete([[_B.x, _B.y, _B.z], [_C.x, _C.y, _C.z], [camera_XYZ.x, camera_XYZ.y, camera_XYZ.z]])

    if det_camera_XYZ <= 0 and det_X1 <= 0 and det_X2 <= 0 and det_X3 <= 0 and det_X4 <= 0:
        return True
    elif det_camera_XYZ >= 0 and det_X1 >= 0 and det_X2 >= 0 and det_X3 >= 0 and det_X4 >= 0:
        return True
    else:
        return False


# determinant calculation
def dete(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
            - a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
            + a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))
