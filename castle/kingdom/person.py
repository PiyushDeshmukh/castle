class Person:
    """
    A person's category is one of the mentioned in hierarchy
    """
    def __init__(self, name='Frank', rank=0, attack=0, defense=0, category='Ministerialis'):
        self.name = name
        self.rank = rank
        self.attack = attack
        self.defense = defense
        self.special = False
        self.category = category
