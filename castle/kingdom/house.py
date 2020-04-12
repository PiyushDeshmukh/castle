import math
from itertools import cycle

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
        self._neighbors = list()
        self.pawn = None

    def calculate_neighbor_coords(self):
        """
        Returns the coordinates from right top in
        clockwise fashion
        """
        self._col_coor, self._row_coor = self.centre_coordinates
        coorse = (self._col_coor + House._beta, self._row_coor - 3 * House._alpha)
        coorsd = (self._col_coor + 2 * House._beta, self._row_coor)
        coorsc = (self._col_coor + House._beta, self._row_coor + 3 * House._alpha)
        coorsz = (self._col_coor - House._beta, self._row_coor + 3 * House._alpha)
        coorsa = (self._col_coor - 2 * House._beta, self._row_coor)
        coorsq = (self._col_coor - House._beta, self._row_coor - 3 * House._alpha)
        return [coorse, coorsd, coorsc, coorsz, coorsa, coorsq]


    def discover_neighbors(self, bt_instance):
        self._neighbors = self.calculate_neighbor_coords()
        if hasattr(bt_instance, 'centre_coordinate_to_house_mapping'):
            invalid_neighbor = list()
            for neighbor in self._neighbors:
                col_coor, row_coor = neighbor
                col_coor, row_coor = int(col_coor), int(row_coor)
                if (col_coor, row_coor) not in bt_instance.centre_coordinate_to_house_mapping:
                    invalid_neighbor.append(neighbor)
            for neighbor in invalid_neighbor:
                self._neighbors.remove(neighbor)
        else:
            raise Exception("Generate centre_coordinate_to_house_mapping before building valid neighbors list")
        self.neighbors = cycle(self._neighbors)

    def __repr__(self):
        return "<House(centre_coordinates=)>" + str(self.centre_coordinates)
