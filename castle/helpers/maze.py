import math
import random
from castle.kingdom.house import House

class Maze:
    def __init__(self):
        self.houses = []
        self.hexagon_central_coordinates = []

    def get_house_generation_probability(self, col, row, num_rows, num_cols):
        """
        Returns probability with which the house should be generated randomly.
        Return p as percent.
        """
        top_and_bottom_row_centers = (row == 0 or row == num_rows-1) and (col > 2*num_cols/5 and col < 3*num_cols/5)
        first_and_last_col_blocks = (col == 0 or col == num_cols-1) and (row > num_rows/5 and row < 2*num_rows/5 or row > 3*num_rows/5 and row < 4*num_rows/5)
        if top_and_bottom_row_centers or first_and_last_col_blocks:
            return 0
        elif (row == 0 or row == num_rows-1 and (col not in [0, 1, num_cols-1, num_cols-2])):
            return 65
        return 100


    def generate_central_coordinates(self):
        col_start = 70
        row_start = 70
        _height = House._height # match this with _height internal to the House class
        alpha, beta = get_alpha_beta_from_height(_height)
        houses = list()
        height_diff = 6 * alpha
        width_diff = 2 * beta
        num_cols = 28
        num_rows = 8
        for col in range(num_cols):
            for row in range(num_rows):
                p = self.get_house_generation_probability(col, row, num_rows, num_cols)
                if not random.choice([True]*p + [False]*(100-p)):
                    # skip generating this house
                    continue
                col_coor = col_start + col*width_diff
                row_coor = row_start + row*height_diff
                self.hexagon_central_coordinates.append((col_coor, row_coor))
                col_coor = col_start + col*width_diff + beta
                row_coor = row_start + row*height_diff + 3*alpha
                self.hexagon_central_coordinates.append((col_coor, row_coor))

    def get_all_houses(self):
        """
        Generates a maze of hexagons on basis of
        their center coordinates
        """
        self.generate_central_coordinates()
        for coordinates in self.hexagon_central_coordinates:
            col_coor = coordinates[0]
            row_coor = coordinates[1]
            self.houses.append(House((col_coor, row_coor)))
        return self.houses

    def discover_all_neighbors(self, bt_instance):
        """
        Populates the neighbor attributes of all Houses
        """
        for house in self.houses:
            house.discover_neighbors(bt_instance)

def get_alpha_beta_from_height(height):
    _alpha = height / 4
    _beta = math.sqrt(3) * _alpha
    return (_alpha, _beta)
