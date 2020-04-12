"""
BattleGround refers to the current state of the game.
It represents the current conditions and values
that the game has on this point
"""
import pygame

from castle.kingdom.pawn import Pawn
from castle.kingdom.person import Person
from castle.kingdom.house import House
from castle.helpers.maze import Maze

class BattleGround:
    def __init__(self):
        self.action = 'INITIALIZING'
        self.maze = Maze()
        self.houses = self.maze.get_all_houses()
        self.generate_centre_coordinate_to_house_mapping()
        self.maze.discover_all_neighbors(self)
        self.all_sprites = pygame.sprite.Group()
        self.initialize_all_warriors()
        self.action = 'INITIALIZED'


    def initialize_all_warriors(self, rank_file="../../data/ranks.json"):
        """
        Initializes the playboard by creating the warriors
        """
        for house in self.houses:
            if house.centre_coordinates[0] < 300:
                person = Person(category='QUEEN')
                pawn = Pawn(person, house)
                self.all_sprites.add(pawn)

    def generate_centre_coordinate_to_house_mapping(self):
        """
        Generates a mapping between House central coordinates to
        the acutal House object
        """
        self.centre_coordinate_to_house_mapping = dict()
        for house in self.houses:
            col_coor, row_coor = house.centre_coordinates
            self.centre_coordinate_to_house_mapping[(int(col_coor), int(row_coor))] = house

    def build_army(self, rank_file="../../data/ranks.json"):
        """
        Reads from the json file rank_file and writes
        """
        pass
