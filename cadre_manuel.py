

def deplacement_manuel(pos_x, sens_deplacement_x, limite_up_x, size_x, vitesse_x,
                       pos_y, sens_deplacement_y, limite_up_y, size_y, vitesse_y, pygame, input_map):

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == input_map["move_right"]:
                sens_deplacement_x = 1
            if event.key == input_map["move_left"]:
                sens_deplacement_x = -1
            if event.key == input_map["move_up"]:
                sens_deplacement_y = -1
            if event.key == input_map["move_down"]:
                sens_deplacement_y = 1
    pos_x += int(sens_deplacement_x * vitesse_x / 10)
    pos_y += int(sens_deplacement_y * vitesse_y / 10)
    bord_atteint_x = (pos_x <= 0) or (pos_x >= limite_up_x - size_x)
    bord_atteint_y = (pos_y <= 0) or (pos_y >= limite_up_y - size_y)
    if pos_x <= 0:
        pos_x = 0
    elif pos_x >= limite_up_x - size_x:
        pos_x = int(limite_up_x - size_x)
    if pos_y <= 0:
        pos_y = 0
    elif pos_y >= limite_up_y - size_y:
        pos_y = int(limite_up_y - size_y)
    pos_x_reel = pos_x
    pos_y_reel = pos_y

    return pos_x, pos_x_reel, sens_deplacement_x, bord_atteint_x, pos_y, pos_y_reel, sens_deplacement_y, bord_atteint_y
