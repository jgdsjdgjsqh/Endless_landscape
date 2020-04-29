
def deplacement_manuel(pos_x, sens_deplacement_x, limite_up_x, size_x, vitesse_x, bord_atteint_x,
                           pos_y, sens_deplacement_y, limite_up_y, size_y, vitesse_y, bord_atteint_y,pygame):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sens_deplacement_x = -1
            if event.key == pygame.K_RIGHT:
                sens_deplacement_x = 1
            if event.key == pygame.K_UP:
                sens_deplacement_y = -1
            if event.key == pygame.K_DOWN:
                sens_deplacement_y = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                sens_deplacement_x = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                sens_deplacement_y = 0
        pos_x += int(sens_deplacement_x * vitesse_x / 10)
        pos_y += int(sens_deplacement_y * vitesse_y / 10)
        if pos_x <= 0:
            pos_x = 0
        elif pos_x >= limite_up_x - size_x:
            pos_x = int(limite_up_x - size_x)
        if pos_y <= 0:
            pos_y = 0
        elif pos_y >= limite_up_y - size_y:
            pos_y = int(limite_up_y - size_y)
    bord_atteint_x = (pos_x <= 0) or (pos_x >= limite_up_x - size_x)
    bord_atteint_y = (pos_y <= 0) or (pos_y >= limite_up_y - size_y)
    pos_x_reel = pos_x
    pos_y_reel = pos_y
    return pos_x, pos_x_reel, sens_deplacement_x, bord_atteint_x, pos_y, pos_y_reel, sens_deplacement_y, bord_atteint_y
