from numpy.random import uniform
import time


def tirage(probabilite): #marche aléatoire

        a = uniform()
        return a<=probabilite


def deplacement_t(temps_lecture, lecture, nombre_de_frame, direction_lecture,
                  sens_lecture, temps_min_changement_t, probabilite_sens, probabilite_direction):

        duree_lecture_changement = time.time() - temps_lecture
        if lecture == 0 or lecture == nombre_de_frame - 1:
                direction_lecture = -direction_lecture
                sens_lecture = -sens_lecture

        if duree_lecture_changement > temps_min_changement_t:

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
        if lecture <= 0:
                lecture = 0
        elif lecture >= nombre_de_frame - 1:
                lecture = nombre_de_frame - 1
        return lecture, sens_lecture, direction_lecture, temps_lecture
