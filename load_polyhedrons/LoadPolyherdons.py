from figures_points_lines_definition.Point3D import Point3D
from figures_points_lines_definition.Line3D import Line3D
from figures_points_lines_definition.Figure import Figure


def get_lines():
    lines = []
    f = open("load_polyhedrons/polyhedrons.txt", "r")
    for x in f:
        if x[0] == "/":
            continue
        else:
            current_input = x.split(";")
            point1 = Point3D(float(current_input[0]), float(current_input[1]), float(current_input[2]))
            point2 = Point3D(float(current_input[3]), float(current_input[4]), float(current_input[5]))
            lines.append(Line3D(point1, point2))
    f.close()
    return lines


def get_figures(lines):
    # Every cuboid is defined by 12 lines. Every wall of cuboid (rectangle)is defined by 2 lines (it can be defined
    # by various combination of 2 lines but it doesnt matter). One cuboid has 6 walls. example representation of
    # lines is shown below: 1st wall - line 0 and line 7 2nd wall - line 0 and line 11 3rd wall - line 8 and line 11
    # 4th wall - line 7 and line 8 5th wall - line 4 and line 6 6th wall - line 3 and line 9
    figures = []
    modulo_leap = 12
    counter = 1
    for i in range(len(lines) + 1):
        if i % modulo_leap == 0 and i > 0:
            figures.append(
                Figure(line_0.points[0], line_0.points[1], line_7.points[1], line_7.points[0], "przód" + str(counter)))
            counter += 1
            figures.append(
                Figure(line_0.points[0], line_0.points[1], line_11.points[1], line_11.points[0], "dół" + str(counter)))
            counter += 1
            figures.append(
                Figure(line_8.points[0], line_8.points[1], line_11.points[1], line_11.points[0], "tył" + str(counter)))
            counter += 1
            figures.append(
                Figure(line_7.points[0], line_7.points[1], line_8.points[1], line_8.points[0], "góra" + str(counter)))
            counter += 1
            figures.append(
                Figure(line_4.points[0], line_4.points[1], line_6.points[1], line_6.points[0], "lewo" + str(counter)))
            counter += 1
            figures.append(
                Figure(line_3.points[0], line_3.points[1], line_9.points[1], line_9.points[0], "prawo" + str(counter)))
            counter += 1
            if i < len(lines):
                line_0 = lines[i]
        elif i % modulo_leap == 0:
            line_0 = lines[i]
        elif i % modulo_leap == 3:
            line_3 = lines[i]
        elif i % modulo_leap == 4:
            line_4 = lines[i]
        elif i % modulo_leap == 6:
            line_6 = lines[i]
        elif i % modulo_leap == 7:
            line_7 = lines[i]
        elif i % modulo_leap == 8:
            line_8 = lines[i]
        elif i % modulo_leap == 9:
            line_9 = lines[i]
        elif i % modulo_leap == 11:
            line_11 = lines[i]

    return figures
