"""
BattleGround refers to the current state of the game.
It represents the current conditions and values
that the game has on this point
"""
import pygame
import json
from uuid import uuid4

from castle.kingdom.pawn import Pawn
from castle.kingdom.person import Person
from castle.kingdom.house import House
from castle.helpers.maze import Maze

class BattleGround:
    def __init__(self):
        self.action = 'INITIALIZING'
        self.maze = Maze(num_uniq_pawn_types=16)
        self.houses, self.configuration_houses = self.maze.get_all_houses()
        self.generate_centre_coordinate_to_conf_house_mapping()
        self.generate_centre_coordinate_to_house_mapping()
        self.maze.discover_all_neighbors(self)
        self.all_sprites = pygame.sprite.Group()
        self.all_resource_sprites = pygame.sprite.Group()
        self.initialize_all_warriors()
        self.action = 'INITIALIZED'
        self.msg_to_display = None
        self.display_msg_coordinates = (1500, 1000)# (col coordinate, row coordinate)


    def initialize_all_warriors(self, rank_file="./data/warriors.json"):
        """
        Initializes the playboard by creating the warriors
        """
        with open(rank_file) as fd:
            rank_data = json.load(fd)
        rank_data = rank_data["ranks"]
        # initialize configuration/resources grid
        for house, rank_obj in zip(self.configuration_houses, rank_data):
            for i in range(rank_obj['counts']):
                person = Person(category=rank_obj['titles'][0])
                pawn = Pawn(uuid4(), person, house)
                self.all_resource_sprites.add(pawn)
        for h in self.configuration_houses:
            print(h.pawn_count)

    def generate_centre_coordinate_to_house_mapping(self):
        """
        Generates a mapping between House central coordinates to
        the acutal House object
        """
        self.centre_coordinate_to_house_mapping = dict()
        for house in self.houses:
            col_coor, row_coor = house.centre_coordinates
            self.centre_coordinate_to_house_mapping[(int(col_coor), int(row_coor))] = house

    def generate_centre_coordinate_to_conf_house_mapping(self):
        """
        Generates a mapping between House central coordinates to
        the acutal House object
        """
        self.centre_coordinate_to_conf_house_mapping = dict()
        for house in self.configuration_houses:
            col_coor, row_coor = house.centre_coordinates
            self.centre_coordinate_to_conf_house_mapping[(int(col_coor), int(row_coor))] = house


    def to_json(self):
        pass

    def from_json(self, jsondata):
        pass
