'''
Configuration globale pour CosmiSort
'''

# --- Configuration ---
WIDTH, HEIGHT = 1600, 900  # Dimensions de la fenêtre
PARTICLE_MIN_RADIUS = 15
PARTICLE_MAX_RADIUS = 40
BACKGROUND_COLOR = (0, 0, 20)  # Bleu très foncé / noir
NUM_ELEMENTS = 20  # Nombre d'éléments à trier
MAX_VALUE = 100
ANIMATION_DELAY = 30  # Millisecondes entre chaque étape
STARS_COUNT = 150  # Nombre d'étoiles d'arrière-plan

# Configuration pour la zone de mémoire/étapes
MEMORY_ZONE_HEIGHT = 120  # Hauteur de la zone de mémoire en bas
MEMORY_SLOT_SIZE = 30     # Taille des emplacements de mémoire
MEMORY_OPERATIONS = []    # Liste pour stocker les opérations

# Configuration pour le graphique de comparaison
SHOW_COMPARISON = False   # Afficher le comparateur de performances
COMPARISON_HEIGHT = 300   # Hauteur du panneau de comparaison

# Dictionnaire des couleurs des algorithmes
ALGORITHM_COLORS = {
    "Tri par sélection": (220, 100, 100),
    "Tri à bulles": (100, 220, 100),
    "Tri par insertion": (100, 100, 220),
    "Tri fusion": (220, 220, 100),
    "Tri rapide": (220, 100, 220),
    "Tri par tas": (100, 220, 220),
    "Tri à peigne": (180, 180, 180)
}

# Ordre standard des algorithmes pour l'affichage
ALGORITHM_ORDER = [
    "Tri par sélection", 
    "Tri à bulles", 
    "Tri par insertion", 
    "Tri fusion", 
    "Tri rapide", 
    "Tri par tas", 
    "Tri à peigne"
] 