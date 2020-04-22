import configparser
import os

#On lit le fichier de configuration:
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

#On vérifie que le fichier n'est pas vide
if config.sections() == []:
    print("!!!! Le fichier config n'arrive pas a etre lu ou est vide !!!!")


"""On initialise différentes valeurs à partir du fichier de configuration:"""
#Pour la vidéo d'origine:
limitation_nombre_de_frame = config.getint("input_video", "limitation_nombre_de_frame")
path = config.get("input_video", "video")

#Pour le cadre:
deplacement_cadre = config.getboolean("cadre", "deplacement_cadre")
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
probabilite_changement_sens_y = config.getfloat("cadre", "probabilite_changement_sens_y")
probabilite_changement_selon_direction_y = config.getfloat("cadre", "probabilite_changement_selon_direction_y")

#Pour la tete de lecture:
probabilite_changement_sens_t = config.getfloat("tete_de_lecture", "probabilite_changement_sens_t")
probabilite_changement_selon_direction_t = config.getfloat("tete_de_lecture", "probabilite_changement_selon_direction_t")
temps_min_changement_t = config.getfloat("tete_de_lecture", "temps_min_changement_t")

#Pour l'output vidéo:
enregistrement = config.getboolean("output_video", "enregistrement")
output_file = config.get("output_video", "output_file")
codec = config.get("output_video", "codec")
framerate = config.getint("output_video", "framerate")

"""  Fin de l'importation de paramètres  """
