import time

def deplacement_manuel(arret_x,arret_y,temps_x,temps_y, posX, sens_deplacement_x, limite_up_x, size_window_x, vitesse_x,posY, sens_deplacement_y, limite_up_y, size_window_y, vitesse_y, pos_x_reel,pos_y_reel,keys, input_map):


    if keys[input_map["move_right"]]:
        sens_deplacement_x = 1
        arret_x=False
    elif keys[input_map["move_left"]]:
        sens_deplacement_x = -1
        arret_x=False
    if keys[input_map["move_up"]]:
        sens_deplacement_y = -1
        arret_y=False
    elif keys[input_map["move_down"]]:
        sens_deplacement_y = 1
        arret_y=False


    duree_x = time.time() - temps_x
    duree_y=time.time() -temps_y
    pos_x_reel+=sens_deplacement_x * vitesse_x * duree_x
    pos_y_reel+=sens_deplacement_y * vitesse_y * duree_y

    posX =int(pos_x_reel)
    posY=int(pos_y_reel)
    temps_x,temps_y = time.time(),time.time()
    bord_atteint_x = posX == size_window_x // 2 + size_window_x % 2 - 1 or posX == limite_up_x - size_window_x // 2
    bord_atteint_y = posY == size_window_y // 2 + size_window_y % 2 - 1 or posY == limite_up_y - size_window_y // 2
    if posX <= size_window_x // 2 + size_window_x % 2 - 1:
        posX = size_window_x // 2 + size_window_x % 2 - 1
    elif posX >= limite_up_x - size_window_x // 2:
        posX = limite_up_x - size_window_x // 2
    if posY <= size_window_y // 2 + size_window_y % 2 - 1:
        posY = size_window_y // 2 + size_window_y % 2 - 1
    elif posY >= limite_up_y - size_window_y // 2:
        posY = limite_up_y - size_window_y // 2

    return arret_x,arret_y,temps_x,temps_y, posX, pos_x_reel, sens_deplacement_x, bord_atteint_x, posY, pos_y_reel, sens_deplacement_y, bord_atteint_y
