from random import randint


def choix(poids, nombre_frame_affile, actuel, limite_up, limite_down, preference_sens_lecture, rint=False):
    Continue = True
    choix_sens_lecture = 0
    while Continue:
        a = randint(0, poids)
        if a == 0 and actuel - nombre_frame_affile >= limite_down:
            choix_sens_lecture = -1
            Continue = False
        if a == 1 and actuel + nombre_frame_affile <= limite_up:
            choix_sens_lecture = 1
            Continue = False
        if a >= 2:
            if actuel + preference_sens_lecture * nombre_frame_affile >=limite_down:
                if actuel + preference_sens_lecture * nombre_frame_affile <= limite_up:
                    choix_sens_lecture = preference_sens_lecture
                    Continue = False
    return choix_sens_lecture
