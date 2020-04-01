import cv2
from choix import choix
import time


lecture = 100   #position de la tete de lecture
pos_x = 600     #position du cadre en x
pos_y = 100     #position du cadre en y
size_x = 600    #taille du cadre selon x
size_y = 900    #taille du cadre selon y

compteur_de_frame = 0       #nombre total de frame affiché depuis l'instant t=0

limite_up_x = 1919          #nombre de pixel max en x de la vidéo
limite_up_y = 1079          #nombre de pixel max en y de la vidéo

#nombre de frame pendant lesquelles la direction en t, x et y ne vont pas changer
#Il peut etre interessant de changer la frame de départ pour chacune des variables afin d'éviter que toutes changent en meme temps
nombre_frame_affile_time = 30
nombre_frame_affile_x = 30
nombre_frame_affile_y = 30

#choix du sens de lecture en t, x et y a chaque frame affiché
#initialement a 0
choix_sens_lecture_time = 0
choix_sens_lecture_x = 0
choix_sens_lecture_y = 0

#préférence initiale des directions t, x et y
preference_sens_lecture_time = -1
preference_sens_lecture_x = 1
preference_sens_lecture_y = -1

#poids des choix, a chaque choix, la proba de choisir la direction favorisée est de :
# poids / (poids+1)
poids_time = 2
poids_x = 2
poids_y = 2

frame_list = []

cap = cv2.VideoCapture("/home/simon/Bureau/Manif.mp4")

nombre_de_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

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


time_debut = time.time()
while True:

    #Déplacement de la tete de lecture
    if compteur_de_frame % nombre_frame_affile_time == 0:
        choix_sens_lecture_time = choix(poids_time, nombre_frame_affile_time, lecture, nombre_de_frame - 1, 0, preference_sens_lecture_time)

        if (lecture <= nombre_frame_affile_time and preference_sens_lecture_time == -1) or (preference_sens_lecture_time == 1 and lecture >= nombre_de_frame - nombre_frame_affile_time):
            preference_sens_lecture_time = preference_sens_lecture_time * -1

    lecture = lecture + choix_sens_lecture_time
    #fin du déplacement de la tete de lecture

    img = frame_list[lecture]


    #Déplacement du cadre dans l'image selon x
    if compteur_de_frame % nombre_frame_affile_x == 0:
        choix_sens_lecture_x = choix(poids_x, nombre_frame_affile_x, pos_x, limite_up_x - size_x, 0, preference_sens_lecture_x,rint=True)

        if (pos_x <= nombre_frame_affile_x and preference_sens_lecture_x == -1) or (pos_x >= limite_up_x - size_x - nombre_frame_affile_x and preference_sens_lecture_x == 1):
            preference_sens_lecture_x = preference_sens_lecture_x * -1
    pos_x = pos_x + choix_sens_lecture_x
    #fin du déplacement dans l'image selon x

    #Déplacement du cadre dans l'image selon y
    if compteur_de_frame % nombre_frame_affile_y == 0:
        choix_sens_lecture_y = choix(poids_y, nombre_frame_affile_y, pos_y, limite_up_y - size_y, 0, preference_sens_lecture_y)

        if (pos_y <= nombre_frame_affile_y and preference_sens_lecture_y == -1) or (
                pos_y >= limite_up_y - size_y - nombre_frame_affile_y and preference_sens_lecture_y == 1):
            preference_sens_lecture_y = preference_sens_lecture_y * -1

    pos_y = pos_y + choix_sens_lecture_y
    #fin du déplacement dans l'image selon y

    img = img[pos_y : pos_y + size_y, pos_x : pos_x + size_x]
    #fin du déplacement du cadre dans l'image

    cv2.imshow('frame', img)
    compteur_de_frame += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
time_fin = time.time()

print("Nombre d'images par seconde en moyenne : ", compteur_de_frame / (time_fin - time_debut))
