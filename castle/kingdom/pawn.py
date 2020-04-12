import pygame
from castle.kingdom.person import Person
from castle.kingdom.thing import Thing

class Pawn(pygame.sprite.Sprite):
    """
    Pawn can be of 2 categories: Person or Thing
    """
    def __init__(self, value, house):
        """
        `value` should be Thing or Person object
        """
        super(Pawn, self).__init__()
        if isinstance(value, Person):
            self.category = Person
        elif isinstance(value, Thing):
            self.category = Thing
        else:
            raise Exception("Invalid category of a Pawn tried to be initialized")
        self.value = value
        self.hidden = False
        self.ismine = True
        self.house = house
        self.house.pawn = self
        self.battleground_attack = 0
        self.battleground_defense = 0
        self.image_file = self.get_icon_filename()
        self.surf = pygame.image.load(self.image_file).convert_alpha()
        self.surf.set_colorkey((255, 255, 255))
        self.icon_coordinates = self.house.icon_coordinates

    @property
    def rect(self):
        return self.surf.get_rect()

    def get_icon_filename(self):
        _mapper = {
            'SOLDIER': './data/images/soldier.png',
            'WALL'   : './data/images/wall.png',
            'KING'   : './data/images/king.png',
            'QUEEN'  : './data/images/queen.png',
            'CASTLE' : './data/images/castle.png',
            'HIDDEN' : './data/images/swords.png'
        }
        if self.ismine or (not self.ismine and not self.hidden):
            if self.category == Person:
                if self.value.category not in ['KING', 'QUEEN']:
                    return _mapper['SOLDIER']
            return _mapper[self.value.category]
        return _mapper['HIDDEN']

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
