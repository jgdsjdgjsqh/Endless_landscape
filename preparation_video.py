import cv2
import pygame
from config import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption("endless_landscape")
screen = pygame.display.set_mode((350, 200), pygame.NOFRAME)
g_texte = pygame.font.Font('freesansbold.ttf', 30)
text_surf = g_texte.render("Endless Landscape", True, (255,255,255))
text_rect = text_surf.get_rect()
text_rect.center = (175, 75)
screen.blit(text_surf, text_rect)
pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(25, 130, 300, 10), 1)
pygame.display.update()

"""  Préparation de la video  """
# On crée une liste pour mettre les images en buffer afin de pouvoir les utiliser plus rapidement
frame_list = []

# On  récupère la vidéo a l'aide du chemin fourni
cap = cv2.VideoCapture(path)

# On récupère certaines données de la vidéo:
nombre_de_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
limite_up_x = cap.get(cv2.CAP_PROP_FRAME_WIDTH) - 1     # Nombre de pixel max en x de la vidéo
limite_up_y = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 1    # Nombre de pixel max en y de la vidéo
limite_up_x = int(limite_up_x)
limite_up_y = int(limite_up_y)

# On parcourt la vidéo pour mettre les images une a une dans la liste buffer:
check, frame = cap.read()
counter = 0
while check and counter < limitation_nombre_de_frame:
    frame_list.append(frame)
    check, frame = cap.read()
    counter += 1
    pygame.draw.rect(screen, (255, 255, 255),
                     pygame.Rect(25, 130, 300 * counter / min(nombre_de_frame, limitation_nombre_de_frame), 10))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break
        elif event.type == pygame.QUIT:
            pygame.quit()
            break

cap.release()
cv2.destroyAllWindows()

nombre_de_frame = len(frame_list)
if nombre_de_frame == 0:
    print("!!!! Attention aucune image n'est chargée !!!!")

# Fin de la préparation des images


"""   Initialisation des paramètres:   """