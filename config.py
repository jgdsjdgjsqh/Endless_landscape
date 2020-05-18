import configparser
import os

#On lit le fichier de configuration:
config = configparser.ConfigParser(allow_no_value=True)
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

#On vérifie que le fichier n'est pas vide
if config.sections() == []:
    print("!!!! Le fichier config.ini n'arrive pas a etre lu ou est vide !!!!")


"""On initialise différentes valeurs à partir du fichier de configuration:"""

#Pour la vidéo d'origine:
limitation_nombre_de_frame = config.getint("input_video", "limitation_nombre_de_frame")
path = config.get("input_video", "video")

#Pour le cadre:
manuel_auto = config.getint("cadre", "manuel_auto")
type_deplacement_cadre = manuel_auto
size_x = config.getint("cadre", "size_x")
size_y = config.getint("cadre", "size_y")
vitesse_x = config.getint("cadre", "vitesse_deplacement_x")
vitesse_y = config.getint("cadre", "vitesse_deplacement_y")
temps_min_x = config.getint("cadre", "temps_min_x")
temps_max_x = config.getint("cadre", "temps_max_x")
temps_min_y = config.getint("cadre", "temps_min_y")
temps_max_y = config.getint("cadre", "temps_max_y")
probabilite_changement_sens_x = config.getfloat("cadre", "probabilite_changement_sens_x")
probabilite_changement_selon_direction_x = config.getfloat("cadre", "probabilite_changement_selon_direction_x")
temps_min_changement_x = config.getint("cadre", "temps_min_changement_x")
probabilite_changement_sens_y = config.getfloat("cadre", "probabilite_changement_sens_y")
probabilite_changement_selon_direction_y = config.getfloat("cadre", "probabilite_changement_selon_direction_y")
temps_min_changement_y = config.getint("cadre", "temps_min_changement_y")

temps_arret_x = config.getint("cadre", "temps_arret_x")
temps_arret_y = config.getint("cadre", "temps_arret_y")

#ZOOM
type_zoom = manuel_auto
vzoom = config.getfloat("ZOOM", "vitesse de zoom")
attente_min = config.getfloat("ZOOM", "attente_min")
attente_max = config.getfloat("ZOOM", "attente_max")

#Pour la tete de lecture:
type_deplacement_tete = manuel_auto
probabilite_changement_sens_t = config.getfloat("tete_de_lecture", "probabilite_changement_sens_t")
probabilite_changement_selon_direction_t = config.getfloat("tete_de_lecture", "probabilite_changement_selon_direction_t")
temps_min_changement_t = config.getfloat("tete_de_lecture", "temps_min_changement_t")

#Pour l'output vidéo:
enregistrement = config.getboolean("output_video", "enregistrement")
output_file = config.get("output_video", "output_file")
codec = config.get("output_video", "codec")
framerate = config.getint("output_video", "framerate")
fullscreen = config.getboolean("output_video", "fullscreen")

#Pour les inputs clavier:

key_config = configparser.ConfigParser(allow_no_value=True)
key_config.read(os.path.join(os.path.dirname(__file__), "key.ini"))
input_map = dict(key_config.items("keyboard input"))
for key in input_map:
    input_map[key] = int(input_map[key])

"""  Fin de l'importation de paramètres  """

#Si le chemin n'est pas absolu, on le complète pour qu'il le soit
if not os.path.isabs(path):
    path = os.path.join(os.path.dirname(__file__), path)
