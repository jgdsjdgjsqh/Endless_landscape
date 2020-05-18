import pygame
from initialisation_parametres import *
from config import *



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()

    # condition de fermeture

    if keys[pygame.K_ESCAPE]:
        running = False

    # MAPPING DES TOUCHES
    elif keys[pygame.K_F1]:
        input_map = assignment_menu(input_map, screen)
        screen.fill((0, 0, 0))


    elif keys[input_map["mode_automatique"]]:
        print("auto")
        manuel_auto = 0
        type_deplacement_cadre = 0
        type_deplacement_tete = 0
        type_zoom = 0


    elif keys[input_map["mode_manuel"]]:
        print('manuel')
        print("manu")
        manuel_auto = 1
        type_deplacement_cadre = 1
        type_deplacement_tete = 1
        type_zoom = 1

    if keys[input_map["stop_cadre_x"]]:
        sens_deplacement_x = 0
        arret_x = True

    if keys[input_map["stop_cadre_y"]]:
        sens_deplacement_x = 0
        arret_y = True

    if keys[input_map["changement_lecture"]]:
        if sens_lecture == 0:
            sens_lecture = -1
        sens_lecture = -sens_lecture

    print(type_zoom,sens_lecture,sens_deplacement_x,sens_deplacement_y,arret_x,arret_y)

    for i in range(len(keys)):
        if keys[i]==1:
            print(i)
    time.sleep(1)
