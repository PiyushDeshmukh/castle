import pygame
import math
from castle.kingdom.house import House
from castle.helpers.maze import Maze, get_alpha_beta_from_height
from castle.kingdom.pawn import Pawn
from castle.kingdom.person import Person

CURRENT_HOUSE_COLOR = (80, 80, 40) # Blackish
TARGET_HOUSE_COLOR = (200, 40, 40) # Redish
SELECTED_HOUSE_COLOR = (40, 200, 40) # Greenish
UNSELECTED_HOUSE_COLOR = (150, 150, 70) # Yellowish Grey

pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

font = pygame.font.SysFont('Comic Sans MS', 30)

maze = Maze()
houses = maze.get_all_houses()

all_sprites = pygame.sprite.Group()
house_to_pawn_mapping = dict()
for house in houses:
    if house.centre_coordinates[0] < 300:
        person = Person(category='QUEEN')
        pawn = Pawn(person, house)
        all_sprites.add(pawn)
        house_to_pawn_mapping[house] = pawn

current_house = houses[0]
target_house = None
target_selected = False
selected_houses = list()
_height = 75 # match this with what is specified in maze.py
_alpha = _height / 4
_beta = math.sqrt(3) * _alpha
centre_coordinate_to_house_mapping = dict()
for house in houses:
    col_coor, row_coor = house.centre_coordinates
    centre_coordinate_to_house_mapping[(int(col_coor), int(row_coor))] = house

# Run until the user asks to quit
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # When launched in full screen mode, use key
            # 'q' to quit
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_k:
                # use k key to select a kill target
                if not target_selected:
                    # Target is not selected, lock the target
                    target_house = current_house
                    target_selected = True
                else:
                    if len(selected_houses) == 0:
                        # unlock the previously selected target
                        target_house = None
                        target_selected = False
                    else:
                        #TODO Destroy Pawn at this House, not the house
                        # use a custom function because we will need a lot of
                        # functionality
                        pawn = house_to_pawn_mapping.get(target_house, None)
                        if pawn is not None:
                            all_sprites.remove(pawn)
                            print("Pawn destroyed")
                            target_house = None
                            target_selected = False
                            selected_houses = list()
            elif event.key == pygame.K_SPACE:
                if target_selected:
                    if current_house not in selected_houses:
                        selected_houses.append(current_house)
                    else:
                        selected_houses.remove(current_house)
                else:
                    selected_house = list()
            elif event.key == pygame.K_RIGHT:
                row_change = 0
                col_change = 2 * _beta
            elif event.key == pygame.K_LEFT:
                row_change = 0
                col_change = -2 * _beta
            elif event.key == pygame.K_UP:
                row_change = -3 * _alpha
                col_change = _beta
            elif event.key == pygame.K_DOWN:
                row_change = 3 * _alpha
                col_change = _beta
            col_coor, row_coor = current_house.centre_coordinates
            col_coor, row_coor = col_coor + col_change, row_coor + row_change
            current_house = centre_coordinate_to_house_mapping[(int(col_coor), int(row_coor))]


    # Fill the background
    screen.fill((200, 200, 50))
    textsurface = font.render('Click to Exit', True, (40, 40, 10))
    screen.blit(textsurface, (40, 1000))

    # Draw all the general houses
    for house in houses:
        pointlist = house.vertex_coordinates
        pygame.draw.lines(screen, UNSELECTED_HOUSE_COLOR, True, pointlist, 5)

    # Draw currently positioned house
    if current_house is not None:
        pygame.draw.lines(screen, CURRENT_HOUSE_COLOR, True, current_house.vertex_coordinates, 5)

    # Draw currently selected houses
    for selected_house in selected_houses:
        pygame.draw.lines(screen, SELECTED_HOUSE_COLOR, True, selected_house.vertex_coordinates, 5)

    # Draw targeted house
    if target_house is not None:
        pygame.draw.lines(screen, TARGET_HOUSE_COLOR, True, target_house.vertex_coordinates, 5)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.icon_coordinates)

    # Flip the display
    pygame.display.update()

# Done! Time to quit.
pygame.quit()
