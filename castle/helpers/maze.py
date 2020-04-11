import math
from castle.kingdom.house import House

class Maze:
    def __init__(self):
        self.houses = []
        self.hexagon_coordinates = []

    def generate_coordinates(self):
        col_start = 70
        row_start = 70
        _height = 75 # match this with _height internal to the House class
        alpha, beta = get_alpha_beta_from_height(_height)
        houses = list()
        height_diff = 6 * alpha
        width_diff = 2 * beta
        for col in range(28):
            for row in range(8):
                col_coor = col_start + col*width_diff
                row_coor = row_start + row*height_diff
                self.hexagon_coordinates.append((col_coor, row_coor))
                col_coor = col_start + col*width_diff + beta
                row_coor = row_start + row*height_diff + 3*alpha
                self.hexagon_coordinates.append((col_coor, row_coor))

    def get_all_houses(self):
        """
        Generates a maze of hexagons on basis of
        their center coordinates
        """
        self.generate_coordinates()
        for coordinates in self.hexagon_coordinates:
            col_coor = coordinates[0]
            row_coor = coordinates[1]
            self.houses.append(House((col_coor, row_coor)))
        return self.houses

def get_alpha_beta_from_height(height):
    _alpha = height / 4
    _beta = math.sqrt(3) * _alpha
    return (_alpha, _beta)
