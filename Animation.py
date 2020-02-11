from tkinter import *
import MatrixOperations
from figures_points_lines_definition import Line2D
import FiguresSort
from Camera import Camera
import copy


class Animation:
    def __init__(self, view):

        self.camera = view.camera

        self.view = view

        self.first_camera = Camera(self.camera.projection_plane_distance, self.camera.projection_plane_height,
                                   self.camera.projection_plane_width, self.camera.x, self.camera.y,
                                   self.camera.z)

        self.first_view = copy.deepcopy(view)

        self.master = Tk()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def camera_animation(self):

        def key(event):
            # OX "+" translation
            if event.keysym == 'Right':
                self.view.lines = MatrixOperations.ox_translation(self.view, "-")
            # OX "-" translation
            elif event.keysym == 'Left':
                self.view.lines = MatrixOperations.ox_translation(self.view, "+")
            # OZ "+" translation
            elif event.keysym == 'Down':
                self.view.lines = MatrixOperations.oz_translation(self.view, "+")
            # OZ "-" translation
            elif event.keysym == 'Up':
                self.view.lines = MatrixOperations.oz_translation(self.view, "-")
            # OY "+" translation
            elif event.keysym == 'k':
                self.view.lines = MatrixOperations.oy_translation(self.view, "+")
            # OY "-" translation
            elif event.keysym == 'l':
                self.view.lines = MatrixOperations.oy_translation(self.view, "-")
            # OY "+" rotation
            elif event.keysym == 'q':
                self.view.lines = MatrixOperations.oy_rotation(self.view, "+")
            # OY "-" rotation
            elif event.keysym == 'w':
                self.view.lines = MatrixOperations.oy_rotation(self.view, "-")
            # OX "+" rotation
            elif event.keysym == 'a':
                self.view.lines = MatrixOperations.ox_rotation(self.view, "+")
            # OX "-" rotation
            elif event.keysym == 's':
                self.view.lines = MatrixOperations.ox_rotation(self.view, "-")
            # OZ "+" rotation
            elif event.keysym == 'z':
                self.view.lines = MatrixOperations.oz_rotation(self.view, "+")
            # OZ "-" rotation
            elif event.keysym == 'x':
                self.view.lines = MatrixOperations.oz_rotation(self.view, "-")
            # zoom "+"
            elif event.keysym == 'o':
                self.camera = MatrixOperations.zoom(self.view, "-")
            # zoom "-"
            elif event.keysym == 'p':
                self.camera = MatrixOperations.zoom(self.view, "+")
            change_canvas()

        def change_canvas():
            w.delete(ALL)
            for line in self.view.projection():
                if type(line) is Line2D.Line2D:
                    w.create_line(line.points[0].x, line.points[0].y, line.points[1].x, line.points[1].y)

        def back_to_first_position():
            w.delete(ALL)
            self.view = copy.deepcopy(self.first_view)
            self.first_view = copy.deepcopy(self.view)
            self.camera = self.first_camera
            change_canvas()

        self.master.destroy()
        self.master = Tk()

        w = Canvas(self.master, width=500, height=500)
        w.focus_set()
        w.pack(padx=5, pady=20, side=LEFT)

        frame = Frame(self.master)
        frame.pack(padx=5, pady=20, side=LEFT)

        text = "go to hidden surface determination"
        button = Button(frame, text=text, command=self.hidden_surface_determination)
        button.pack(padx=5, pady=20, side=BOTTOM)

        text = "back to first position"
        button = Button(frame, text=text, command=back_to_first_position)
        button.pack(padx=5, pady=20, side=BOTTOM)

        text = "REMEMBER TO CLICK ON THE WINDOW\n" \
               "TO ENABLE APPLICATION TO CAPTURE\n" \
               "KEY CLICK EVENTS:\n\n" \
               "Camera control: \n" \
               "right/left translation: →/←\n" \
               "up/down translation: ↑/↓\n" \
               "forward/backward translation: l/k\n" \
               "OY rotation: q/w\n" \
               "OX rotation: a/s\n" \
               "OZ rotation: z/x\n" \
               "zoom +/-: o/p"
        label = Label(frame, text=text)
        label.pack(padx=5, pady=20, side=BOTTOM)

        back_to_first_position()

        self.master.bind("<Key>", key)
        self.master.mainloop()

    def hidden_surface_determination(self):

        def key(event):
            # OX "+" translation
            if event.keysym == 'Right':
                self.view.lines = MatrixOperations.ox_translation(self.view, "-")
            # OX "-" translation
            elif event.keysym == 'Left':
                self.view.lines = MatrixOperations.ox_translation(self.view, "+")
            # OZ "+" translation
            elif event.keysym == 'Down':
                self.view.lines = MatrixOperations.oz_translation(self.view, "+")
            # OZ "-" translation
            elif event.keysym == 'Up':
                self.view.lines = MatrixOperations.oz_translation(self.view, "-")
            # OY "+" translation
            elif event.keysym == 'k':
                self.view.lines = MatrixOperations.oy_translation(self.view, "+")
            # OY "-" translation
            elif event.keysym == 'l':
                self.view.lines = MatrixOperations.oy_translation(self.view, "-")
            # OZ "+" rotation
            elif event.keysym == 'z':
                self.view.lines = MatrixOperations.oz_rotation(self.view, "+")
            # OZ "-" rotation
            elif event.keysym == 'x':
                self.view.lines = MatrixOperations.oz_rotation(self.view, "-")
            # zoom "+"
            elif event.keysym == 'o':
                self.camera = MatrixOperations.zoom(self.view, "-")
            # zoom "-"
            elif event.keysym == 'p':
                self.camera = MatrixOperations.zoom(self.view, "+")
            labelText.set("")
            change_canvas()

        def change_canvas():
            w.delete(ALL)
            for line in self.view.projection():
                if type(line) is Line2D.Line2D:
                    w.create_line(line.points[0].x, line.points[0].y, line.points[1].x, line.points[1].y)

        def hide_surfaces():
            w.delete(ALL)
            move = 250
            ymin = self.view.lines[0].points[0].y
            ymax = self.view.lines[0].points[0].y
            for line in self.view.lines:
                for i in range(2):
                    if line.points[i].y > ymax:
                        ymax = line.points[i].y
                    if line.points[i].y < ymin:
                        ymin = line.points[i].y

                if ymax >= self.camera.y + self.camera.projection_plane_distance >= ymin:
                    labelText.set("THE PROJECTION PLANE MUST\n"
                                  "BE AWAY FROM THE OBJECTS")
                    change_canvas()
                    return
            lines2d = FiguresSort.sorted_figures(self.view.lines, self.camera)
            if len(lines2d) != 2*len(self.view.lines):
                back_to_first_position()
            else:
                for i in range(int(len(lines2d) / 4)):
                    w.create_polygon([lines2d[0 + 4 * i].points[0].x + move, lines2d[0 + 4 * i].points[0].y + move,
                                      lines2d[0 + 4 * i].points[1].x + move, lines2d[0 + 4 * i].points[1].y + move,
                                      lines2d[2 + 4 * i].points[0].x + move, lines2d[2 + 4 * i].points[0].y + move,
                                      lines2d[2 + 4 * i].points[1].x + move, lines2d[2 + 4 * i].points[1].y + move],
                                     outline='#f11',
                                     fill='#1f1', width=1)

        def back_to_first_position():
            w.delete(ALL)
            self.view = copy.deepcopy(self.first_view)
            self.first_view = copy.deepcopy(self.view)
            self.camera = self.first_camera
            change_canvas()

        self.master.destroy()
        self.master = Tk()

        w = Canvas(self.master, width=500, height=500)
        w.focus_set()

        w.pack(padx=5, pady=20, side=LEFT)

        frame = Frame(self.master)
        frame.pack(padx=5, pady=20, side=LEFT)

        text = "back to camera control animation"
        button = Button(frame, text=text, command=self.camera_animation)
        button.pack(padx=5, pady=20, side=BOTTOM)

        text = "back to first position"
        button = Button(frame, text=text, command=back_to_first_position)
        button.pack(padx=5, pady=20, side=BOTTOM)

        text = "hide"
        button = Button(frame, text=text, command=hide_surfaces)
        button.pack(padx=5, pady=20, side=BOTTOM)

        text = "REMEMBER TO CLICK ON THE WINDOW\n" \
               "TO ENABLE APPLICATION TO CAPTURE\n" \
               "KEY CLICK EVENTS:\n\n" \
               "Camera control:\n" \
               "right/left translation: →/←\n" \
               "up/down translation: ↑/↓\n" \
               "forward/backward translation: l/k\n" \
               "OZ rotation: z/x\n" \
               "zoom +/-: o/p"

        label = Label(frame, text=text)
        label.pack(padx=5, pady=20, side=BOTTOM)

        labelText = StringVar()
        error = Label(frame, textvariable=labelText, fg="red")
        error.pack(padx=5, pady=10, side=BOTTOM)

        back_to_first_position()

        self.master.bind("<Key>", key)
        self.master.mainloop()
