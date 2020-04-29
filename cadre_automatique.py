import time
from random import randint


def deplacement_automatique_x_y(temps, pos, pos_reel, sens_deplacement, vitesse, limite_up,
                                size, bord_atteint, bord_atteint_debut, debut_bord,
                                temps_restant_bord, temps_min, temps_max):
    if not bord_atteint:
        duree = time.time() - temps
        pos_reel += sens_deplacement * vitesse * duree
        pos = int(pos_reel)
        temps = time.time()
        bord_atteint = (pos <= 0) or (pos >= limite_up - size)
    else:
        if bord_atteint_debut:
            debut_bord = time.time()
            bord_atteint_debut = False
        duree_bord_atteint = time.time() - debut_bord
        if pos <= 0:
            pos = 0
        elif pos >= limite_up - size:
            pos = int(limite_up - size)
        if duree_bord_atteint > temps_restant_bord:
            sens_deplacement = - sens_deplacement
            bord_atteint = False
            bord_atteint_debut = True
            temps_restant_bord = randint(temps_min, temps_max)
            temps = time.time()
    return pos, pos_reel, temps, sens_deplacement, bord_atteint, bord_atteint_debut, temps_restant_bord, debut_bord
