import pygame
import cv2
import time
import numpy as np
from random import randint
from deplacement_tete_de_lecture import deplacement_t
from cadre_manuel import deplacement_manuel
from cadre_automatique import deplacement_automatique_x_y
from config import *
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption("endless_landscape")
screen = pygame.display.set_mode((350, 200), pygame.NOFRAME)
pygame.display.update()

"""  Préparation de la video  """
#On crée une liste pour mettre les images en buffer afin de pouvoir les utiliser plus rapidement
frame_list = []

#on  récupère la vidéo a l'aide du chemin fourni
cap = cv2.VideoCapture(path)

#On récupère certaines données de la vidéo:
nombre_de_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
limite_up_x = cap.get(cv2.CAP_PROP_FRAME_WIDTH) - 1     #Nombre de pixel max en x de la vidéo
limite_up_y = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 1    #Nombre de pixel max en y de la vidéo

#On parcourt la vidéo pour mettre les images une a une dans la liste buffer:
check, frame = cap.read()
counter = 0
while check and counter < limitation_nombre_de_frame:
    frame_list.append(frame)
    #cv2.imshow("Frame", frame)
    check, frame = cap.read()
    counter += 1
    print('%s / %d images' % (counter, min(nombre_de_frame, limitation_nombre_de_frame)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("fin de la mise en cache des images")
cap.release()
cv2.destroyAllWindows()

nombre_de_frame = len(frame_list)
print("Nombre d'images final : %d" % nombre_de_frame)

#Fin de la préparation des images


"""   Initialisation des paramètres:   """

#Position initiale de la tete de lecture
lecture = randint(0, nombre_de_frame)

#Choix de la position initiale du cadre selon x:
if limite_up_x - size_x + 1 == 0:
    pos_x = 0
elif limite_up_x - size_x + 1 < 0:
    print("!!!! Le cadre est trop grand pour la taille de la vidéo originale !!!!")
else:
    pos_x = randint(0, limite_up_x - size_x + 1)


#Choix de la position initiale du cadre selon y:
if limite_up_y - size_y + 1 == 0:
    pos_y = 0
elif limite_up_y - size_y + 1 < 0:
    print("!!!! Le cadre est trop grand pour la taille de la vidéo originale !!!!")
else:
    pos_y = randint(0, limite_up_y - size_y + 1)


#Temps que le cadre va rester sur les bords la premiere fois qu'il les touche:
temps_restant_bord_x = randint(temps_min_x, temps_max_x)
temps_restant_bord_y = randint(temps_min_y, temps_max_y)

if enregistrement:#Création de la vidéo de sortie (l'enregistrement), vide pour le moment, on ajoute les images apres
    codec = cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])
    video_output = cv2.VideoWriter(output_file, codec, framerate, (size_x, size_y))
    if video_output.isOpened():
        print("L'objet vidéo a bien été initialisée")
    else:
        print("!!!! L'objet vidéo n'a pas pu etre initialisé !!!!")

"""
Sens  lecture (ou sens_deplacement) correspond au sens dans lequel la tete de lecture (ou le cadre) va 
effectivement se déplacer tandis que direction_lecture (ou direction_deplacement) indique la direction privilégiée 
de lecture (ou déplacement). Toutes ces valeurs vont etre modifiées tout au long du programme
Ici in procède a l'initiation de ces variables en fonction des positions de la tete de lecture
et du cadre.
"""

if lecture == nombre_de_frame:
    sens_lecture = -1
    direction_lecture = -1
else:
    sens_lecture = 1
    direction_lecture = 1

if pos_x == limite_up_x - size_x:
    sens_deplacement_x = -1
    direction_deplacement_x = -1
else:
    sens_deplacement_x = 1
    direction_deplacement_x = 1

if pos_y == limite_up_y - size_y:
    sens_deplacement_y = -1
    direction_deplacement_y = -1
else:
    sens_deplacement_y = 1
    direction_deplacement_y = 1


print(sens_lecture, direction_lecture)
print(sens_deplacement_x, direction_deplacement_x)
print(sens_deplacement_y, direction_deplacement_y)


"""postion réelle en float permet d'actualiser plus régulièrement le déplacement pour avoir une vidéo plus fluide"""
pos_x_reel = pos_x
pos_y_reel = pos_y

"""permet de savoir si le bord est atteint:"""
bord_atteint_x = pos_x == 0 or pos_x == limite_up_x - size_x
bord_atteint_y = pos_y == 0 or pos_y == limite_up_y - size_y

"""Variables servant uniquement lors du premier contact en x ou y:"""
bord_atteint_x_debut = True
bord_atteint_y_debut = True


deplacement_automatique = True
compteur_de_frame = 0

#Initialisation des temps:
temps_debut_calcul_fps_final = time.time()
temps_debut_calcul_fps_continu = time.time()
temps_lecture = time.time()         #permet de calculer la durée qui s'est écoulé entre de changement de sens de lecture
temps_x_changement=time.time()      #permet de calculer la durée qui s'est écoulé entre de changement de direction de déplacement du cadre selon x
temps_x = time.time()               #permet de calculer la durée écouler dans la boucle pour calculer le déplacement selon x
temps_y_changement=time.time()      #permet de calculer la durée qui d'est écoulé entre de changement de direction de déplacement du cadre selon y
temps_y = time.time()               #permet de calculer la durée écouler dans la boucle pour calculer le déplacement selon y
debut_bord_x = time.time()          #Permet de calculer la durée que reste le cadre ur le bord de l'image en x
debut_bord_y = time.time()          #Permet de calculer la durée que reste le cadre ur le bord de l'image en y

"""   Fin de l'initialisation   """


"""   Début de la boucle infini de choix d'image et d'affichage   """






screen = pygame.display.set_mode((size_x, size_y))
#pygame.display.toggle_fullscreen()
modes = pygame.display.list_modes()
print(modes)
if fullscreen:
    pygame.display.set_mode((size_x, size_y), pygame.FULLSCREEN)
pygame.key.set_repeat(100, 100)
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


def assignment_menu(input_map):
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

arret_x = False
arret_y = False

running = True


while running:

    #Permet de "relancer" le déplacement du cadre en x apres avoir attendu X secondes apres avoir appuyer sur
    #la touche d'arret de déplacement en x
    if arret_x and time.time() - temps_arret_x_debut > temps_arret_x:
        arret_x = False
        temps_x_changement = time.time() - temps_min_changement_x
        temps_x = time.time()
        if pos_x == limite_up_x - size_x:
            sens_deplacement_x = -1
            direction_deplacement_x = -1
        else:
            sens_deplacement_x = 1
            direction_deplacement_x = 1

    #Pareil pour y
    if arret_y and time.time() - temps_arret_y_debut > temps_arret_y:
        arret_y = False
        temps_y_changement = time.time() - temps_min_changement_y
        temps_y = time.time()
        if pos_y == limite_up_y - size_y:
            sens_deplacement_y = -1
            direction_deplacement_y = -1
        else:
            sens_deplacement_y = 1
            direction_deplacement_y = 1


    if not type_deplacement_cadre:
        if not arret_x:
            pos_x, pos_x_reel, temps_x, sens_deplacement_x, direction_deplacement_x, bord_atteint_x, \
            bord_atteint_x_debut, temps_restant_bord_x, debut_bord_x, temps_x_changement = deplacement_automatique_x_y(
                temps_x, pos_x, pos_x_reel, sens_deplacement_x, direction_deplacement_x, vitesse_x, limite_up_x,
                size_x, bord_atteint_x, bord_atteint_x_debut, debut_bord_x, temps_restant_bord_x,
                temps_min_x, temps_max_x, temps_min_changement_x, probabilite_changement_sens_x,
                probabilite_changement_selon_direction_x, temps_x_changement)

        if not arret_y:
            pos_y, pos_y_reel, temps_y, sens_deplacement_y, direction_deplacement_y, bord_atteint_y, \
            bord_atteint_y_debut, temps_restant_bord_y, debut_bord_y, temps_y_changement = deplacement_automatique_x_y(
                temps_y, pos_y, pos_y_reel, sens_deplacement_y, direction_deplacement_y, vitesse_y, limite_up_y,
                size_y, bord_atteint_y, bord_atteint_y_debut, debut_bord_y, temps_restant_bord_y,
                temps_min_y, temps_max_y, temps_min_changement_y, probabilite_changement_sens_y,
                probabilite_changement_selon_direction_y, temps_y_changement)

    if type_deplacement_cadre:
        pos_x, pos_x_reel, sens_deplacement_x, bord_atteint_x, pos_y, pos_y_reel, sens_deplacement_y, \
        bord_atteint_y = deplacement_manuel(
            pos_x, sens_deplacement_x, limite_up_x, size_x, vitesse_x,
            pos_y, sens_deplacement_y, limite_up_y, size_y, vitesse_y, pygame, input_map)


    if not type_deplacement_tete:
        lecture, sens_lecture, direction_lecture,\
            temps_lecture = deplacement_t(temps_lecture, lecture, nombre_de_frame, direction_lecture,
                                          sens_lecture, temps_min_changement_t, probabilite_changement_sens_t,
                                          probabilite_changement_selon_direction_t)

    lecture = lecture + sens_lecture
    if lecture <= 0:
        lecture = 0
        sens_lecture = - sens_lecture
    elif lecture >= nombre_de_frame - 1:
        lecture = nombre_de_frame - 1
        sens_lecture = -sens_lecture

    print(lecture, "/", nombre_de_frame,"     sens de lecture : ", sens_lecture)

    """On affiche l'image selectionnée:"""
    img = frame_list[lecture]
    img = img[pos_y: pos_y + size_y,  pos_x: pos_x + size_x]
    #cv2.imshow("frame", img)
    compteur_de_frame += 1

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = np.rot90(img)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, (0, 0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_F1:
                input_map = assignment_menu(input_map)

            elif event.key == input_map["mode_automatique_cadre"]:
                type_deplacement_cadre = 0

                #Permet de prendre en compte le temps écoulé pendant le déplacement manuel
                #afin de ne pas avoir de changement brusque en repassant en manuel
                temps_x_changement = time.time() - temps_min_changement_x
                temps_y_changement = time.time() - temps_min_changement_y
                temps_x = time.time()
                temps_y = time.time()

                #Permet de s'assurer que le cadre se déplace lorsqu'on repasse en automatique
                if pos_x == limite_up_x - size_x:
                    sens_deplacement_x = -1
                    direction_deplacement_x = -1
                else:
                    sens_deplacement_x = 1
                    direction_deplacement_x = 1

                if pos_y == limite_up_y - size_y:
                    sens_deplacement_y = -1
                    direction_deplacement_y = -1
                else:
                    sens_deplacement_y = 1
                    direction_deplacement_y = 1
                print("déplacement du cadre en mode automatique")

            elif event.key == input_map["mode_manuel_cadre"]:
                print("déplacement du cadre en mode manuel")
                type_deplacement_cadre = 1
                sens_deplacement_x = 0
                sens_deplacement_y = 0

            elif event.key == input_map["mode_manuel_lecture"]:
                type_deplacement_tete = 1
                sens_lecture = 0

            elif event.key == input_map["mode_automatique_lecture"]:
                type_deplacement_tete = 0

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
                if event.key == input_map["zoom_"+str(i)]:
                    print(i)

        if event.type == pygame.QUIT:
            running = False

    """On ajoute l'image a la vidéo enregistrée si on a choisit de le faire"""
    if enregistrement:
        video_output.write(img)

    """Si on affiche les images trop vite par rapport au framerate voulu, on fait une pause"""
    temps_fin_calcul_fps_continu = time.time()
    if (1 / framerate) - (temps_fin_calcul_fps_continu - temps_debut_calcul_fps_continu) > 0:
        time.sleep((1 / framerate) - (temps_fin_calcul_fps_continu - temps_debut_calcul_fps_continu))
    temps_debut_calcul_fps_continu = time.time()
    #TODO: une fonction qui alerte en cas de chute de fps

cv2.destroyAllWindows()
pygame.quit()
temps_fin_calcul_fps_final = time.time()
fps_moy = compteur_de_frame / (temps_fin_calcul_fps_final - temps_debut_calcul_fps_final)
print("Nombre moyen d'images par seconde : %d" % fps_moy)
