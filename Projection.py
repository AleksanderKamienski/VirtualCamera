from figures_points_lines_definition.Point2D import Point2D
from figures_points_lines_definition.Line2D import Line2D

_x = 0
_z = 0


def projection(lines, camera):
    # half of projection plane width
    _x = camera.projection_plane_width / 2
    # half of projection plane height
    _z = camera.projection_plane_height / 2
    projected_lines = []
    for line3D in lines:
        point1 = line3D.points[0]
        point2 = line3D.points[1]

        if camera.is_visible(point1) and camera.is_visible(point2):
            line2d = normal_projection(point1, point2, camera)
            projected_lines.append(line2d)
        elif camera.is_visible(point1) and not camera.is_visible(point2):
            line2d = cut_projection(point1, point2, camera)
            projected_lines.append(line2d)
        elif not camera.is_visible(point1) and camera.is_visible(point2):
            line2d = cut_projection(point2, point1, camera)
            projected_lines.append(line2d)
    return projected_lines


def normal_projection(point1, point2, camera):
    point2D_1 = point_projection(point1, camera)
    point2D_2 = point_projection(point2, camera)
    if not point2D_1 == point2D_2:
        return Line2D(point2D_1, point2D_2)


def cut_projection(point1, point2, camera):
    if point1.y == camera.y + camera.projection_plane_distance:
        _t = Point2D(int(point1.x + _x), int(_z - point1.z))
        _l = Point2D(_t.x, _t.y)
        return Line2D(_t, _l)
    else:
        tmp = (point1.y - point2.y) / (point1.y - (camera.y + camera.projection_plane_distance))
        _t = point1.x + ((point2.x - point1.x) * tmp)
        _l = point1.z + ((point2.z - point1.z) * tmp)
        return Line2D(point_projection(point1, camera), Point2D(int(_t + _t), int(_l - _l)))


def point_projection(point, camera):
    tmp = camera.projection_plane_distance / (point.y - camera.y)
    x_coordinate = int(tmp * point.x + _x)
    z_coordinate = int(_z - tmp * point.z)
    return Point2D(x_coordinate, z_coordinate)
