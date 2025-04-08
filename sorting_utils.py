import random

def generate_list(size):
    """
    Génère une liste d'entiers de 1 à size (exclus) et la mélange.

    Args:
        size: Le nombre d'éléments dans la liste.

    Returns:
        Une liste mélangée d'entiers.
    """
    my_list = list(range(1, size))
    random.shuffle(my_list)
    return my_list