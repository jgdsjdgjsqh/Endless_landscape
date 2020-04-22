import os
import cv2
import time
from random import randint
import configparser
from cadre_automatique import deplacement_automatique_x_y
from deplacement_tete_de_lecture import deplacement_t


#On lit le fichier de configuration:
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

#On vérifie que le fichier n'est pas vide
if config.sections() == []:
    print("!!!! Le fichier config n'arrive pas a etre lu ou est vide !!!!")


"""On initialise différentes valeurs à partir du fichier de configuration:"""
#Pour la vidéo d'origine:
limitation_nombre_de_frame = config.getint("input_video", "limitation_nombre_de_frame")
path = config.get("input_video", "video")

#Pour le cadre:
deplacement_cadre = config.getboolean("cadre", "deplacement_cadre")
size_x = config.getint("cadre", "size_x")
size_y = config.getint("cadre", "size_y")
vitesse_x = config.getint("cadre", "vitesse_deplacement_x")
vitesse_y = config.getint("cadre", "vitesse_deplacement_y")
temps_min_x = config.getint("cadre", "temps_min_x")
temps_max_x = config.getint("cadre", "temps_max_x")
temps_min_y = config.getint("cadre", "temps_min_y")
temps_max_y = config.getint("cadre", "temps_max_y")
probabilite_changement_sens_x = config.getfloat("cadre", "probabilite_changement_sens_x")
probabilite_changement_selon_direction_x = config.getfloat("cadre", "probabilite_changement_selon_direction_x")
probabilite_changement_sens_y = config.getfloat("cadre", "probabilite_changement_sens_y")
probabilite_changement_selon_direction_y = config.getfloat("cadre", "probabilite_changement_selon_direction_y")

#Pour la tete de lecture:
probabilite_changement_sens_t = config.getfloat("tete_de_lecture", "probabilite_changement_sens_t")
probabilite_changement_selon_direction_t = config.getfloat("tete_de_lecture", "probabilite_changement_selon_direction_t")
temps_min_changement_t = config.getfloat("tete_de_lecture", "temps_min_changement_t")

#Pour l'output vidéo:
enregistrement = config.getboolean("output_video", "enregistrement")
output_file = config.get("output_video", "output_file")
codec = config.get("output_video", "codec")
framerate = config.getint("output_video", "framerate")

"""  Fin de l'importation de paramètres  """


"""  Préparation de la video  """
#On crée une liste pour mettre les images en buffer afin de pouvoir les utiliser plus rapidement
frame_list = []

#Si le chemin n'est pas absolu, on le complete pour qu'il le soit
if not os.path.isabs(path):
    path = os.path.join(os.path.dirname(__file__), path)

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
    if codec == "MJPG":
        video_output = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), framerate, (size_x, size_y))
        if video_output.isOpened():
            print("L'objet vidéo a bien été initialisée")

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


while True:

    """Déplacement de la tete de lecture :"""

    lecture, sens_lecture, direction_lecture,\
        temps_lecture = deplacement_t(temps_lecture, lecture,nombre_de_frame, direction_lecture,
                                      sens_lecture, temps_min_changement_t, probabilite_changement_sens_t,
                                      probabilite_changement_selon_direction_t)

    """Déplacement du cadre:
    Premier cas: on est en automatique"""
    if deplacement_cadre:
        if deplacement_automatique:
            # Déplacement selon x:
            pos_x, pos_x_reel, temps_x, sens_deplacement_x, bord_atteint_x,\
                bord_atteint_x_debut, debut_bord_x, temps_restant_bord_x = deplacement_automatique_x_y(
                    bord_atteint_x, temps_x, pos_x, pos_x_reel, sens_deplacement_x, vitesse_x,
                    limite_up_x, size_x, bord_atteint_x_debut, temps_min_x, temps_max_x,
                    debut_bord_x, temps_restant_bord_x)

            #Déplacement selon y:
            pos_y, pos_y_reel, temps_y, sens_deplacement_y, bord_atteint_y, \
                bord_atteint_y_debut, debut_bord_y, temps_restant_bord_y = deplacement_automatique_x_y(
                    bord_atteint_y, temps_y, pos_y, pos_y_reel, sens_deplacement_y, vitesse_y,
                    limite_up_y, size_y, bord_atteint_y_debut, temps_min_y, temps_max_y,
                    debut_bord_y, temps_restant_bord_y)

        #Second cas: on est en manuel
        else:
            #TODO: Faire le cas manuel dans le fichier cadre_manuel.py
            pass


    #TODO : Gestion du zoom, a faire dans le fichier zoom.py

    """On affiche l'image selectionnée:"""
    img = frame_list[lecture][pos_y: pos_y + size_y,  pos_x: pos_x + size_x]
    cv2.imshow("frame", img)
    compteur_de_frame += 1

    """On ajoute l'image a la vidéo enregistrée si on a choisit de le faire"""
    if enregistrement:
        video_output.write(img)#On ajoute l'image à la vidéo enregistrée


    """Si on affiche les images trop vite par rapport au framerate voulu, on fait une pause"""
    temps_fin_calcul_fps_continu = time.time()
    if (1 / framerate) - (temps_fin_calcul_fps_continu - temps_debut_calcul_fps_continu) > 0:
        time.sleep((1 / framerate) - (temps_fin_calcul_fps_continu - temps_debut_calcul_fps_continu))
    temps_debut_calcul_fps_continu = time.time()
    #TODO: une fonction qui alerte en cas de chute de fps

    """Gestion du clavier:
    Si on appuie sur la touche q, on sort de la boucle.
    Si on appuie sur la touche a, on passe en mode automatique pour le déplacement du cadre
    et si on appuie sur la touche e, on passe en mode manuel.
    cv2.waitKey(delay) waits for a key event for delay millisecond"""
    #TODO: le changement manuel/automatique ne marche pas tres bien et j'ai l'impression qu'il faut rester appuyé
    #TODO super longtemps pour que ca marche, meme pour la touche q alors que c'etait tres rapide avant
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('a'):
        deplacement_automatique = True
    elif cv2.waitKey(1) & 0xFF == ord('e'):
        deplacement_automatique = False


cv2.destroyAllWindows()
temps_fin_calcul_fps_final = time.time()
fps_moy = compteur_de_frame / (temps_fin_calcul_fps_final - temps_debut_calcul_fps_final)
print("Nombre moyen d'images par seconde : %d" % fps_moy)
