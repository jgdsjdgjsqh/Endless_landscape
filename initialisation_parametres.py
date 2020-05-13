import time
from random import randint
from preparation_video import *

#Position initiale de la tete de lecture
lecture = randint(0, nombre_de_frame)

#Initialisation de la taille de la fenêtre
size_window_x = size_x
size_window_y = size_y

#Choix de la position initiale du cadre selon x:
if limite_up_x - size_window_x + 1 == 0:
    posX = size_window_x//2 + size_window_x%2 -1
elif limite_up_x - size_window_x + 1 < 0:
    print("!!!! Le cadre est trop grand pour la taille de la vidéo originale !!!!")
else:
    posX = randint(size_window_x//2 + size_window_x % 2 - 1, limite_up_x - size_window_x//2)


#Choix de la position initiale du cadre selon y:
if limite_up_y - size_window_y + 1 == 0:
    posY = size_window_y // 2 + size_window_y % 2-1
elif limite_up_y - size_window_y + 1 < 0:
    print("!!!! Le cadre est trop grand pour la taille de la vidéo originale !!!!")
else:
    posY = randint(size_window_y//2 + size_window_y%2 -1 , limite_up_y - size_window_y//2)


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

if posX == limite_up_x - size_window_x//2:
    sens_deplacement_x = -1
    direction_deplacement_x = -1
else:
    sens_deplacement_x = 1
    direction_deplacement_x = 1

if posY == limite_up_y - size_window_y//2:
    sens_deplacement_y = -1
    direction_deplacement_y = -1
else:
    sens_deplacement_y = 1
    direction_deplacement_y = 1

"""postion réelle en float permet d'actualiser plus régulièrement le déplacement pour avoir une vidéo plus fluide"""
pos_x_reel = posX
pos_y_reel = posY

"""permet de savoir si le bord est atteint:"""
bord_atteint_x = posX== size_window_x//2 + size_window_x%2 -1 or posX== limite_up_x - size_window_x//2
bord_atteint_y = posY== size_window_y//2 + size_window_y%2 -1 or posY== limite_up_y - size_window_y//2

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
temps_changement_zoom=time.time()   #permet de calculer la durée qui s'est écoulé avant le zoom précédent
temps_debut_zoom=0


#Initialisation Zoom:

zoom_en_cours_Auto = False
zoom_en_cours_manuel = False





zmax = 2
zmin = max([size_x/limite_up_x, size_y/limite_up_y])
listZoomAuto = [zmin+k*(zmax-zmin)/9 for k in range(10)]


indiceZoomDefault=0
while listZoomAuto[indiceZoomDefault] < 1:        #placer le zoom 1 dans la liste
    indiceZoomDefault += 1
indiceZoomDefault -= 1
listZoomAuto[indiceZoomDefault] = 1
indice_zoom = indiceZoomDefault
listZoomManuel = [1]+listZoomAuto[:indiceZoomDefault]+listZoomAuto[indiceZoomDefault+1:]

zinit = 1
zf = 1
Zt = zinit
directionZoom = 1

deplacement_automatique = True
compteur_de_frame = 0

arret_x = False
arret_y = False

modes = pygame.display.list_modes()
accroche_x = (modes[0][0] - size_x) / 2
accroche_y = (modes[0][1] - size_y) / 2


"""   Fin de l'initialisation   """