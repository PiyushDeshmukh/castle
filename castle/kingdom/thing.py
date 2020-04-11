class Thing:
    """
    A Thing can be of 3 categories:
      - CASTLE
      - WALL
      - ARTILLARY
    """
    def __init__(self, category):
        self.category = category
        self.attack = 0
        self.defense = 100# Infinity
