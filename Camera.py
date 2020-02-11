class Camera:
    def __init__(self, distance, height, width, _x, _y, _z):
        # distance between projection plane and the camera
        self.projection_plane_distance = distance
        # projection plane width
        self.projection_plane_height = height
        # projection plane height
        self.projection_plane_width = width
        # coordinates of the camera
        self.x = _x
        self.y = _y
        self.z = _z

    def is_visible(self, point):
        if point.y >= self.y + self.projection_plane_distance:
            return True
        else:
            return False

    def get_width(self):
        return self.projection_plane_width
