import numpy as np
from deplacement_tete_de_lecture import deplacement_t
from cadre_manuel import deplacement_manuel
from cadre_automatique import deplacement_automatique_x_y
from zoom import *

from initialisation_parametres import *


screen = pygame.display.set_mode((size_x, size_y))
if fullscreen:
    pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
pygame.key.set_repeat(100, 100)

running = True

from keyboard_config_file_update import assignment_menu

"""   Début de la boucle infini de choix d'image et d'affichage   """

while running:

    keys = pygame.key.get_pressed()
    Mode=type_zoom

    if not type_zoom:
        # ZOOM AUTO
        if zoom_en_cours_manuel:

            Zt, indice_zoom, temps_debut_zoom, zinit, zf, zoom_en_cours_manuel \
                = Zoom_Manuel(Zt, vitesse_x, vitesse_y, vzoom, posX, posY, size_x, size_y, limite_up_x, limite_up_y,
                              temps_debut_zoom, listZoomManuel,
                              zinit, zf, zoom_en_cours_manuel, indice_zoom, indiceZoomDefault, pygame, input_map)

        else:
            temps_debut_zoom, directionZoom, zinit, zf, indice_zoom, zoom_en_cours_Auto, temps_changement_zoom, Zt \
                = zoom_automatique(Zt, vitesse_x, vitesse_y, vzoom, posX, posY, size_x, size_y, limite_up_x,
                                   limite_up_y, temps_debut_zoom,
                                   listZoomAuto, directionZoom, zinit, zf, indice_zoom, zoom_en_cours_Auto,
                                   temps_changement_zoom, attente_min, attente_max)

    else:
        # ZOOM MANUEL
        if zoom_en_cours_Auto:
            temps_debut_zoom, directionZoom, zinit, zf, indice_zoom, zoom_en_cours_Auto, \
            temps_changement_zoom, Zt = zoom_automatique(Zt, vitesse_x, vitesse_y, vzoom, posX, posY, size_x, size_y,
                                                         limite_up_x,
                                                         limite_up_y, temps_debut_zoom, listZoomAuto, directionZoom,
                                                         zinit, zf, indice_zoom, zoom_en_cours_Auto,
                                                         temps_changement_zoom, attente_min, attente_max)
        else:

            Zt, indice_zoom, temps_debut_zoom, zinit, zf, zoom_en_cours_manuel \
                = Zoom_Manuel(Zt, vitesse_x, vitesse_y, vzoom, posX, posY, size_x, size_y, limite_up_x, limite_up_y,
                              temps_debut_zoom, listZoomManuel,
                              zinit, zf, zoom_en_cours_manuel, indice_zoom, indiceZoomDefault, keys, input_map)

    size_window_x=int(size_x/Zt)
    size_window_y=int(size_y/Zt)

    # Permet de "relancer" le déplacement du cadre en x apres avoir attendu X secondes apres avoir appuyer sur
    # la touche d'arret de déplacement en x
    if arret_x and time.time() - temps_arret_x_debut > temps_arret_x:
        arret_x = False
        temps_x_changement = time.time() - temps_min_changement_x
        temps_x = time.time()
        if posX == limite_up_x - size_window_x//2:
            sens_deplacement_x = -1
            direction_deplacement_x = -1
        else:
            sens_deplacement_x = 1
            direction_deplacement_x = 1

    # Pareil pour y
    if arret_y and time.time() - temps_arret_y_debut > temps_arret_y:
        arret_y = False
        temps_y_changement = time.time() - temps_min_changement_y
        temps_y = time.time()
        if posY == limite_up_y - size_window_y//2:
            sens_deplacement_y = -1
            direction_deplacement_y = -1
        else:
            sens_deplacement_y = 1
            direction_deplacement_y = 1

    if not type_deplacement_cadre:
        if not arret_x:
            posX, pos_x_reel, temps_x, sens_deplacement_x, direction_deplacement_x, bord_atteint_x, \
            bord_atteint_x_debut, temps_restant_bord_x, debut_bord_x, temps_x_changement = deplacement_automatique_x_y(
                temps_x, posX, pos_x_reel, sens_deplacement_x, direction_deplacement_x, vitesse_x, limite_up_x,
                size_window_x, bord_atteint_x, bord_atteint_x_debut, debut_bord_x, temps_restant_bord_x,
                temps_min_x, temps_max_x, temps_min_changement_x, probabilite_changement_sens_x,
                probabilite_changement_selon_direction_x, temps_x_changement)

        if not arret_y:
            posY, pos_y_reel, temps_y, sens_deplacement_y, direction_deplacement_y, bord_atteint_y, \
            bord_atteint_y_debut, temps_restant_bord_y, debut_bord_y, temps_y_changement = deplacement_automatique_x_y(
                temps_y, posY, pos_y_reel, sens_deplacement_y, direction_deplacement_y, vitesse_y, limite_up_y,
                size_window_y, bord_atteint_y, bord_atteint_y_debut, debut_bord_y, temps_restant_bord_y,
                temps_min_y, temps_max_y, temps_min_changement_y, probabilite_changement_sens_y,
                probabilite_changement_selon_direction_y, temps_y_changement)

    if type_deplacement_cadre:
        temps_x, posX, pos_x_reel, sens_deplacement_x, bord_atteint_x, posY, pos_y_reel, sens_deplacement_y, \
        bord_atteint_y = deplacement_manuel(
            temps_x, posX, sens_deplacement_x, limite_up_x, size_window_x, vitesse_x,
            posY, sens_deplacement_y, limite_up_y, size_window_y, vitesse_y, keys, input_map)

    if not type_deplacement_tete:
        lecture, sens_lecture, direction_lecture,\
            temps_lecture = deplacement_t(temps_lecture, lecture, direction_lecture, nombre_de_frame,
                                          sens_lecture, temps_min_changement_t, probabilite_changement_sens_t,
                                          probabilite_changement_selon_direction_t)

    """On affiche l'image selectionnée:"""
    lecture += sens_lecture
    if lecture < 0 or lecture > nombre_de_frame - 1:
        direction_lecture = -direction_lecture
        sens_lecture = -sens_lecture
        lecture += sens_lecture


    img = frame_list[lecture]
    img = img[posY - size_window_y //2 + 1 - size_y % 2 :posY + size_window_y // 2, posX - size_window_x //2 +1 -size_x%2:posX + size_window_x //2 ]

    img = cv2.resize(img, (size_x, size_y))

    compteur_de_frame += 1

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = np.rot90(img)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.flip(frame, True, False)
    if fullscreen:
        screen.blit(frame, (accroche_x, accroche_y))
    else:
        screen.blit(frame, (0, 0))

    pygame.display.update()
    print(lecture)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_F1:
                input_map = assignment_menu(input_map, screen)
                screen.fill((0, 0, 0))

            elif event.key == input_map["mode_automatique"]:
                print("auto")
                manuel_auto = 0
                type_deplacement_cadre = 0
                type_deplacement_tete = 0
                type_zoom = 0

                # Permet de prendre en compte le temps écoulé pendant le déplacement manuel
                # afin de ne pas avoir de changement brusque en repassant en manuel
                temps_x_changement = time.time() - temps_min_changement_x
                temps_y_changement = time.time() - temps_min_changement_y
                temps_x = time.time()
                temps_y = time.time()

                # Permet de s'assurer que le cadre se déplace lorsqu'on repasse en automatique
                if posX == limite_up_x - size_window_x//2:
                    sens_deplacement_x = -1
                    direction_deplacement_x = -1
                elif posX == limite_up_x + size_window_x//2:
                    sens_deplacement_x = 1
                    direction_deplacement_x = 1
                if sens_deplacement_x == 0:
                    sens_deplacement_x = direction_deplacement_x

                if posY == limite_up_y - size_window_y//2:
                    sens_deplacement_y = -1
                    direction_deplacement_y = -1
                elif posY == limite_up_y + size_window_y//2:
                    sens_deplacement_y = 1
                    direction_deplacement_y = 1
                if sens_deplacement_y == 0:
                    sens_deplacement_y = direction_deplacement_y

            elif event.key == input_map["mode_manuel"]:
                print("manu")
                manuel_auto = 1
                type_deplacement_cadre = 1
                type_deplacement_tete = 1
                type_zoom = 1

            elif event.key == input_map["stop_cadre_x"]:
                sens_deplacement_x = 0
                if not type_deplacement_cadre:
                    temps_arret_x_debut = time.time()
                    arret_x = True

            elif event.key == input_map["stop_cadre_y"]:
                sens_deplacement_y = 0
                if not type_deplacement_cadre:
                    temps_arret_y_debut = time.time()
                    arret_y = True

            elif event.key == input_map["changement_lecture"]:
                sens_lecture = - sens_lecture
                if sens_lecture == 0:
                    sens_lecture = -1
            for i in range(10):
                if not zoom_en_cours_manuel:
                    if event.key == input_map["zoom_" + str(i)] and zoomPossible(zinit, listZoomAuto[i], vitesse_x, vitesse_y, vzoom, posX, posY, size_x, size_y, limite_up_x, limite_up_y):
                        zf = listZoomAuto[i]
                        print(i)
                        temps_debut_zoom = time.time()
                        zoom_en_cours_manuel = True
                        if i == 0:
                            indice_zoom = indiceZoomDefault
                        else:
                            indice_zoom=i


        if event.type == pygame.QUIT:
            running = False

        keys=pygame.key.get_pressed()



    """On ajoute l'image a la vidéo enregistrée si on a choisit de le faire"""
    if enregistrement:
        video_output.write(img)

    """Si on affiche les images trop vite par rapport au framerate voulu, on fait une pause"""
    temps_fin_calcul_fps_continu = time.time()
    if (1 / framerate) - (temps_fin_calcul_fps_continu - temps_debut_calcul_fps_continu) > 0:
        time.sleep((1 / framerate) - (temps_fin_calcul_fps_continu - temps_debut_calcul_fps_continu))
    temps_debut_calcul_fps_continu = time.time()


cv2.destroyAllWindows()
pygame.quit()
temps_fin_calcul_fps_final = time.time()
fps_moy = compteur_de_frame / (temps_fin_calcul_fps_final - temps_debut_calcul_fps_final)
print("Nombre moyen d'images par seconde : %d" % fps_moy)
