import pygame
from config import *

FONT = pygame.font.Font(None, 40)

BG_COLOR = pygame.Color('gray12')
GREEN = pygame.Color('lightseagreen')


def create_key_list(input_map):
    """A list of surfaces of the action names + assigned keys, rects and the actions."""
    key_list = []
    for y, (action, value) in enumerate(input_map.items()):
        surf = FONT.render('{}: {}'.format(action, pygame.key.name(value)), True, GREEN)
        rect = surf.get_rect(topleft=(40, y*40+20))
        key_list.append([surf, rect, action])
    return key_list


def assignment_menu(input_map, screen):
    """Allow the user to change the key assignments in this menu.

    The user can click on an action-key pair to select it and has to press
    a keyboard key to assign it to the action in the `input_map` dict.
    """
    selected_action = None
    key_list = create_key_list(input_map)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if selected_action is not None:
                    # Assign the pygame key to the action in the input_map dict.
                    input_map[selected_action] = event.key
                    key_config.set('keyboard input', selected_action, str(event.key))
                    selected_action = None
                    # Need to re-render the surfaces.
                    key_list = create_key_list(input_map)
                    with open(os.path.join(os.path.dirname(__file__), "key.ini"), "w") as f:
                        key_config.write(f)
                if event.key == pygame.K_F1:  # Leave the menu.
                    # Return the updated input_map dict to the main function.
                    return input_map
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_action = None
                for surf, rect, action in key_list:
                    # See if the user clicked on one of the rects.
                    if rect.collidepoint(event.pos):
                        selected_action = action

        screen.fill(BG_COLOR)
        # Blit the action-key table. Draw a rect around the
        # selected action.
        for surf, rect, action in key_list:
            screen.blit(surf, rect)
            if selected_action == action:
                pygame.draw.rect(screen, GREEN, rect, 2)

        pygame.display.flip()