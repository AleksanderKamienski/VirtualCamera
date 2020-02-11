from figures_points_lines_definition.Point3D import Point3D
from figures_points_lines_definition.Point2D import Point2D
from figures_points_lines_definition.Line2D import Line2D
from figures_points_lines_definition.Line3D import Line3D


def multiplying(matrix, point):
    result = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            result[i] += matrix[i][j] * point[j]
    return result


class View:

    def __init__(self, lines, camera):
        # array of lines which build polyhedrons
        self.lines = lines
        # camera
        self.camera = camera
        # half of projection plane width
        self._x = self.camera.projection_plane_width / 2
        # half of projection plane height
        self._z = self.camera.projection_plane_height / 2

    def is_visible(self, point):
        if point.y >= self.camera.y + self.camera.projection_plane_distance:
            return True
        else:
            return False

    # change focal length
    def change_focal_length(self, val):
        self.camera.projection_plane_distance += val

    def points_transformation(self, matrix):
        current_point = [0, 0, 0, 0]
        point1 = Point3D
        counter = 0

        for line in self.lines:

            for j in range(2):
                # normalized coordinates
                current_point[0] = line.points[j].x
                current_point[1] = line.points[j].y
                current_point[2] = line.points[j].z
                current_point[3] = 1
                # point transformation

                current_point = multiplying(matrix, current_point)
                current_point = [int(x) for x in current_point]

                # normalization
                if j == 0:
                    point1 = Point3D(current_point[0] / current_point[3], current_point[1] / current_point[3],
                                     current_point[2] / current_point[3])
                elif j == 1:
                    point2 = Point3D(current_point[0] / current_point[3], current_point[1] / current_point[3],
                                     current_point[2] / current_point[3])
                    self.lines[counter] = Line3D(point1, point2)
                    counter += 1

    # returns array of 2D lines
    def projection(self):
        projected_lines = []
        for line3D in self.lines:
            point1 = line3D.points[0]
            point2 = line3D.points[1]

            if self.camera.is_visible(point1) and self.camera.is_visible(point2):
                line2d = self.normal_projection(point1, point2)
                projected_lines.append(line2d)
            elif self.camera.is_visible(point1) and not self.camera.is_visible(point2):
                line2d = self.cut_projection(point1, point2)
                projected_lines.append(line2d)
            elif not self.camera.is_visible(point1) and self.camera.is_visible(point2):
                line2d = self.cut_projection(point2, point1)
                projected_lines.append(line2d)
        return projected_lines

    def normal_projection(self, point1, point2):
        point2D_1 = self.point_projection(point1)
        point2D_2 = self.point_projection(point2)
        if not point2D_1 == point2D_2:
            return Line2D(point2D_1, point2D_2)

    def cut_projection(self, point1, point2):
        if point1.y == self.camera.y + self.camera.projection_plane_distance:
            _x = Point2D(int(point1.x + self._x), int(self._z - point1.z))
            _z = Point2D(_x.x, _x.y)
            return Line2D(_x, _z)
        else:
            tmp = (point1.y - point2.y) / (point1.y - (self.camera.y + self.camera.projection_plane_distance))
            _x = point1.x + ((point2.x - point1.x) * tmp)
            _z = point1.z + ((point2.z - point1.z) * tmp)
            return Line2D(self.point_projection(point1), Point2D(int(_x + self._x), int(self._z - _z)))

    def point_projection(self, point):
        tmp = self.camera.projection_plane_distance / (point.y - self.camera.y)
        x_coordinate = int(tmp * point.x + self._x)
        z_coordinate = int(self._z - tmp * point.z)
        return Point2D(x_coordinate, z_coordinate)
