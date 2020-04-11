import math

class House:
    """
    Vertex Coordinates are maintained starting from top
    and going clockwise direction on hexagon
    """
    _height = 75 # match this with what is specified in maze.py
    _alpha = _height / 4
    _beta = math.sqrt(3) * _alpha
    _vertices = [
        (0, -2 * _alpha),
        (_beta, -1 * _alpha),
        (_beta, _alpha),
        (0, 2 * _alpha),
        (-1 * _beta,  _alpha),
        (-1 * _beta, -1 * _alpha),
    ]
    def __init__(self, centre_coordinates):
        self.centre_coordinates = centre_coordinates
        self.icon_coordinates = centre_coordinates[0]-15, centre_coordinates[1]-15
        self.vertex_coordinates = list()
        for point in type(self)._vertices:
            col_coor = self.centre_coordinates[0] + point[0]
            row_coor = self.centre_coordinates[1] + point[1]
            self.vertex_coordinates.append((col_coor, row_coor))
        self.neighbors = []
