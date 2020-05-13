from numpy.random import uniform
import time


def tirage(probabilite):  # marche aléatoire
        return uniform() <= probabilite


def deplacement_t(temps_lecture, lecture, direction_lecture, nombre_de_frame,
                  sens_lecture, temps_min_changement_t, probabilite_sens, probabilite_direction):

        duree_lecture_changement = time.time() - temps_lecture
        if lecture >= 0 and lecture <= nombre_de_frame - 1 and \
                duree_lecture_changement > temps_min_changement_t:

                # Tirage tête de lecture
                tirage_sens_lecture = tirage(probabilite_sens)
                tirage_direction_lecture = tirage(probabilite_direction)

                if tirage_sens_lecture:
                        sens_lecture = -sens_lecture
                        temps_lecture = time.time()

                if tirage_direction_lecture:
                        sens_lecture = direction_lecture
                        temps_lecture = time.time()

        return lecture, sens_lecture, direction_lecture, temps_lecture
