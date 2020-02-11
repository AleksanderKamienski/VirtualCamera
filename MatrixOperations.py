from math import *
from math import pi


def ox_translation(view, orientation):
    if orientation == "+":
        translation_value = 100
    elif orientation == "-":
        translation_value = -100
    matrix = [[1, 0, 0, translation_value], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    view.points_transformation(matrix)
    return view.lines


def oz_translation(view, orientation):
    if orientation == "+":
        translation_value = 100
    elif orientation == "-":
        translation_value = -100
    matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, translation_value], [0, 0, 0, 1]]
    view.points_transformation(matrix)
    return view.lines


def oy_translation(view, orientation):
    if orientation == "+":
        translation_value = 100
    elif orientation == "-":
        translation_value = -100
    matrix = [[1, 0, 0, 0], [0, 1, 0, translation_value], [0, 0, 1, 0], [0, 0, 0, 1]]
    view.points_transformation(matrix)
    return view.lines


def ox_rotation(view, orientation):
    if orientation == "+":
        rotation_value = pi / 12
    elif orientation == "-":
        rotation_value = -pi / 12
    matrix = [[1, 0, 0, 0], [0, cos(rotation_value), -sin(rotation_value), 0],
              [0, sin(rotation_value), cos(rotation_value), 0], [0, 0, 0, 1]]
    view.points_transformation(matrix)
    return view.lines


def oy_rotation(view, orientation):
    if orientation == "+":
        rotation_value = pi / 12
    elif orientation == "-":
        rotation_value = -pi / 12
    matrix = [[cos(rotation_value), 0, sin(rotation_value), 0], [0, 1, 0, 0],
              [-sin(rotation_value), 0, cos(rotation_value), 0], [0, 0, 0, 1]]
    view.points_transformation(matrix)
    return view.lines


def oz_rotation(view, orientation):
    if orientation == "+":
        rotation_value = pi / 12
    elif orientation == "-":
        rotation_value = -pi / 12
    matrix = [[cos(rotation_value), -sin(rotation_value), 0, 0], [sin(rotation_value), cos(rotation_value), 0, 0],
              [0, 0, 1, 0], [0, 0, 0, 1]]
    view.points_transformation(matrix)
    return view.lines


def zoom(view, orientation):
    if orientation == "+":
        zoom_value = 5
    elif orientation == "-":
        zoom_value = -5
    # zoom limit
    if view.camera.projection_plane_distance > 5 or zoom_value > 0:
        view.camera.projection_plane_distance += zoom_value
    return view.camera
