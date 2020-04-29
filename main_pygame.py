import pygame
import cv2
import time
import numpy as np
from random import randint
from deplacement_tete_de_lecture import deplacement_t
from cadre_manuel_2 import deplacement_manuel
from cadre_automatique import deplacement_automatique_x_y
from config import *


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
    cv2.imshow("Frame", frame)
    check, frame = cap.read()
    counter += 1
    print('%s / %d images' % (counter, nombre_de_frame))
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

"""Sens  lecture (ou sens_deplacement) correspond au sens dans lequel la tete de lecture (ou le cadre) va 
effectivement se déplacer tandis que direction_lecture (ou direction_deplacement) indique la direction privilégiée 
de lecture (ou déplacement). Toutes ces valeurs vont etre modifiées tout au long du programme"""
sens_lecture = 1
direction_lecture = 1
sens_deplacement_x = 1
direction_deplacement_x = 1
sens_deplacement_y = 1
direction_deplacement_y = 1

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


pygame.init()
pygame.display.set_caption("endless_landscape")
screen = pygame.display.set_mode((size_x, size_y))

pygame.key.set_repeat(1, 1)


while True:

    if not type_deplacement_cadre:
        print("x")
        pos_x, pos_x_reel, temps_x, sens_deplacement_x, bord_atteint_x, \
        bord_atteint_x_debut, temps_restant_bord_x, debut_bord_x = deplacement_automatique_x_y(
            temps_x, pos_x, pos_x_reel, sens_deplacement_x, vitesse_x, limite_up_x,
            size_x, bord_atteint_x, bord_atteint_x_debut, debut_bord_x, temps_restant_bord_x,
            temps_min_x, temps_max_x)


        print("y")
        pos_y, pos_y_reel, temps_y, sens_deplacement_y, bord_atteint_y, \
        bord_atteint_y_debut, temps_restant_bord_y, debut_bord_y = deplacement_automatique_x_y(
            temps_y, pos_y, pos_y_reel, sens_deplacement_y, vitesse_y, limite_up_y,
            size_y, bord_atteint_y, bord_atteint_y_debut, debut_bord_y, temps_restant_bord_y,
            temps_min_y, temps_max_y)

    if type_deplacement_cadre:
        pos_x, pos_x_reel, sens_deplacement_x, bord_atteint_x, pos_y, pos_y_reel, sens_deplacement_y, \
        bord_atteint_y = deplacement_manuel(
            pos_x, sens_deplacement_x, limite_up_x, size_x, vitesse_x, bord_atteint_x,
            pos_y, sens_deplacement_y, limite_up_y, size_y, vitesse_y, bord_atteint_y, pygame)

    lecture, sens_lecture, direction_lecture,\
        temps_lecture = deplacement_t(temps_lecture, lecture, nombre_de_frame, direction_lecture,
                                      sens_lecture, temps_min_changement_t, probabilite_changement_sens_t,
                                      probabilite_changement_selon_direction_t)

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
            if event.key == pygame.K_a:
                type_deplacement_cadre = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                type_deplacement_cadre = 1
                sens_deplacement_x = 0
                sens_deplacement_y = 0
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

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
