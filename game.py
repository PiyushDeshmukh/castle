import pygame
import math
from castle.kingdom.house import House
from castle.helpers.battleground import BattleGround
from castle.kingdom.pawn import Pawn
from castle.kingdom.person import Person

CURRENT_HOUSE_COLOR = (80, 80, 40) # Blackish
TARGET_HOUSE_COLOR = (200, 40, 40) # Redish
SELECTED_HOUSE_COLOR = (40, 200, 40) # Greenish
UNSELECTED_HOUSE_COLOR = (150, 150, 70) # Yellowish Grey
BACKGROUND_COLOR = (200, 210, 50) # Greenish-Yellowish
CENTRAL_NEIGHBOR_COLOR = (80, 80, 200) # Blueish

pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

font = pygame.font.SysFont('Comic Sans MS', 30)

battleground = BattleGround()
houses = battleground.houses

current_house = houses[0]
target_house = None
target_selected = False
selected_houses = list()
last_neighbor_operated_house = None

# Run until the user asks to quit
running = True

while running:
    for event in pygame.event.get():
        battleground.action = 'DUMMY'
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # When launched in full screen mode, use key
            # 'q' to quit
            if event.key == pygame.K_ESCAPE:
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
                        pawn = target_house.pawn
                        if pawn is not None:
                            battleground.all_sprites.remove(pawn)
                            target_house.pawn = None
                            target_house = None
                            target_selected = False
                            selected_houses = list()
            elif event.key == pygame.K_SPACE:
                if target_selected:
                    if target_house is not current_house:
                        if current_house not in selected_houses:
                            selected_houses.append(current_house)
                        else:
                            selected_houses.remove(current_house)
                else:
                    selected_house = list()
            elif event.key == pygame.K_n:
                battleground.action = 'BROWSE_NEIGHBORS'
                if last_neighbor_operated_house is None:
                    last_neighbor_operated_house = current_house
                    neighbor_coors = next(last_neighbor_operated_house.neighbors)
                    col_coor, row_coor = neighbor_coors
                    current_house = battleground.centre_coordinate_to_house_mapping.get((int(col_coor), int(row_coor)), current_house)
                else:
                    neighbor_coors = next(last_neighbor_operated_house.neighbors)
                    col_coor, row_coor = neighbor_coors
                    current_house = battleground.centre_coordinate_to_house_mapping.get((int(col_coor), int(row_coor)), current_house)

            elif event.key == pygame.K_RIGHT:
                row_change = 0
                col_change = 2 * House._beta
                battleground.action = 'HOUSE_MOVED'
            elif event.key == pygame.K_LEFT:
                row_change = 0
                col_change = -2 * House._beta
                battleground.action = 'HOUSE_MOVED'
            elif event.key == pygame.K_UP:
                row_change = -3 * House._alpha
                col_change = House._beta
                battleground.action = 'HOUSE_MOVED'
            elif event.key == pygame.K_DOWN:
                row_change = 3 * House._alpha
                col_change = House._beta
                battleground.action = 'HOUSE_MOVED'

            # Pawn moving operations from top-right clockwise around the House
            # e, d, c, z, a, q
            elif event.key == pygame.K_e:
                row_change = -3 * House._alpha
                col_change = House._beta
                battleground.action = 'PAWN_MOVED'
            elif event.key == pygame.K_d:
                row_change = 0
                col_change = 2 * House._beta
                battleground.action = 'PAWN_MOVED'
            elif event.key == pygame.K_c:
                row_change = 3 * House._alpha
                col_change = House._beta
                battleground.action = 'PAWN_MOVED'
            elif event.key == pygame.K_z:
                row_change = 3 * House._alpha
                col_change = -1 * House._beta
                battleground.action = 'PAWN_MOVED'
            elif event.key == pygame.K_a:
                row_change = 0
                col_change = -2 * House._beta
                battleground.action = 'PAWN_MOVED'
            elif event.key == pygame.K_q:
                row_change = -3 * House._alpha
                col_change = -1 * House._beta
                battleground.action = 'PAWN_MOVED'

            # check the battleground actions
            if battleground.action == 'HOUSE_MOVED':
                battleground.action = 'PROCESSING'
                col_coor, row_coor = current_house.centre_coordinates
                col_coor, row_coor = col_coor + col_change, row_coor + row_change
                current_house = battleground.centre_coordinate_to_house_mapping.get((int(col_coor), int(row_coor)), current_house)
            elif battleground.action == 'PAWN_MOVED':
                battleground.action = 'PROCESSING'
                col_coor, row_coor = current_house.centre_coordinates
                col_coor, row_coor = col_coor + col_change, row_coor + row_change
                new_house = battleground.centre_coordinate_to_house_mapping.get((int(col_coor), int(row_coor)), current_house)
                if new_house is not current_house and current_house.pawn is not None:
                    new_house.pawn = current_house.pawn
                    new_house.pawn.house = new_house
                    new_house.pawn.icon_coordinates = new_house.icon_coordinates
                    current_house.pawn = None

            if battleground.action != 'BROWSE_NEIGHBORS':
                last_neighbor_operated_house = None

    # Fill the background
    screen.fill(BACKGROUND_COLOR)
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

    # Draw central neighbor house
    if last_neighbor_operated_house is not None:
        pygame.draw.lines(screen, CENTRAL_NEIGHBOR_COLOR, True, last_neighbor_operated_house.vertex_coordinates, 5)

    # Draw targeted house
    if target_house is not None:
        pygame.draw.lines(screen, TARGET_HOUSE_COLOR, True, target_house.vertex_coordinates, 5)

    # Draw all sprites
    for entity in battleground.all_sprites:
        screen.blit(entity.surf, entity.icon_coordinates)

    # Flip the display
    pygame.display.update()

# Done! Time to quit.
pygame.quit()
