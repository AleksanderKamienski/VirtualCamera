from Camera import Camera
from View import View
from Animation import Animation
from load_polyhedrons.LoadPolyherdons import get_lines, get_figures


lines = get_lines()

figures = get_figures(lines)

_camera = Camera(100,500,500,0,900,0)

view = View(lines,_camera)

animation = Animation(view)

animation.camera_animation()

