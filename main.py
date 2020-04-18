import cv2
from choix import tirage
import time
from random import randint

#Paramètre modifiable

limitation_frame = 1000     #Permet de limiter le nombre d'images de la vidéo à utiliser

size_x = 1680   #taille du cadre selon x
size_y = 1050    #taille du cadre selon y
vitesse_x = 30    #nombre de pixel par seconde
compteur_de_frame = 0       #nombre total de frame affiché depuis l'instant t=0
frame_rate = 18


probabilite_sens = 0.05 #probabilite changer le sens
probabilite_direction = 0.02

probabilite_x = 0.2#probabilite de déplacer le cadre si on touche le bord


#Préparation de la video
frame_list = []

cap = cv2.VideoCapture("/home/simon/Bureau/Manif.mp4")

nombre_de_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
limite_up_x = cap.get(cv2.CAP_PROP_FRAME_WIDTH) - 1  # nombre de pixel max en x de la vidéo
limite_up_y = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 1  # nombre de pixel max en y de la vidéo

check, frame = cap.read()
counter = 0
while check:
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

lecture = randint(0, nombre_de_frame)# Position initiale de la tete de lecture
pos_x = randint(0, limite_up_x - size_x)# Position initiale du cadre selon x
pos_y = randint(0, limite_up_y - size_y)# Position initiale du cadre selon y

time_debut = time.time()

sens_lecture = 1
direction_lecture = 1

sens_deplacement_x = 1

temps_lecture = time.time() #permet de calculer la durée qui d'est écoulé entre de changement de sens de lecture

temps_x_changement=time.time()  #permet de calculer la durée qui d'est écoulé entre de changement de direction de déplacement du cadre
temps_x = time.time()     #permet de calculer la durée écouler dans la boucle pour calculer le déplacement selon x
pos_x_reel = pos_x        #postion de x réel en float permet d'actualiser plus régulière le déplacement pour avoir une vidéo plus fluide
bord_atteind_x = pos_x == 0 or pos_x == limite_up_x - size_x   #permet de savoir si le bord est atteind
bord_atteind_x_debut = True  #le bord x vient d'être atteind

time_avant = time.time()

while True:

    #Déplacement du cadre

    #déplacement selon x

    if not bord_atteind_x:
        duree_x = time.time() - temps_x
        pos_x_reel += sens_deplacement_x * vitesse_x * duree_x
        pos_x = int(pos_x_reel)
        temps_x = time.time()
        bord_atteind_x = pos_x <= 0 or pos_x >= limite_up_x - size_x

    if bord_atteind_x:
        if bord_atteind_x_debut:
            debut_bord_x = time.time()
            bord_atteind_x_debut = False
        duree_bord_atteind = time.time() - debut_bord_x
        if pos_x <= 0:
            pos_x = 0
        elif pos_x >= limite_up_x - size_x:
            pos_x = int(limite_up_x - size_x)

        if duree_bord_atteind > 5:#On reste 5 secondes sur le bord de l'image
            sens_deplacement_x = -sens_deplacement_x
            bord_atteind_x = False
            bord_atteind_x_debut = True
            temps_x = time.time()




    #Tête de Lecture
    duree_lecture_changement = time.time() - temps_lecture
    if lecture == 0 or lecture == len(frame_list) - 1:
        direction_lecture = -direction_lecture
        sens_lecture = -sens_lecture

    if duree_lecture_changement > 0.5:#Permet de limiter les changements de sens de lecture

        # Tirage tête de lecture
        tirage_sens_lecture = tirage(probabilite_sens)
        tirage_direction_lecture = tirage(probabilite_direction)

        if tirage_sens_lecture:
            sens_lecture = -sens_lecture
            temps_lecture = time.time()

        if tirage_direction_lecture:
            sens_lecture = direction_lecture
            temps_lecture = time.time()

    lecture = lecture + sens_lecture

    img = frame_list[lecture]

    img = img[ pos_y : pos_y + size_y,  pos_x : pos_x + size_x]


    cv2.imshow('frame', img)
    compteur_de_frame += 1

    time_apres = time.time()
    if (1 / frame_rate) - (time_apres - time_avant) > 0:
        time.sleep((1 / frame_rate) - (
                    time_apres - time_avant))  # Si l'image est affiché trop vide par rapport au framerate désiré, on attends
    time_avant = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
time_fin = time.time()

print("Nombre d'images par seconde en moyenne : ", compteur_de_frame / (time_fin - time_debut))
