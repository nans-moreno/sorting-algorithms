'''
Gestion des données à trier et de leurs statistiques.
'''

import random
import time
from typing import List, Dict, Any, Callable, Tuple, Generator

from config import NUM_ELEMENTS, MAX_VALUE
from utils.memory import memory_manager


class SortData:
    """Gère les données à trier et les statistiques associées."""
    
    def __init__(self, num_elements: int = NUM_ELEMENTS, max_value: int = MAX_VALUE):
        """Initialise les données avec des valeurs aléatoires."""
        self.num_elements = num_elements
        self.max_value = max_value
        self.data: List[int] = []
        self.original_data: List[int] = []
        self.current_dataset_id = 0
        
        # Statistiques pour chaque algorithme
        self.algorithm_stats: Dict[str, Dict[str, float]] = {}
        
        # État actuel de la visualisation
        self.current_state: Dict[str, Any] = {}
        self.current_algorithm: str = ""
        self.is_sorting: bool = False
        
        # Génération des données
        self.generate_data()
    
    def generate_data(self):
        """Génère un nouvel ensemble de données aléatoires."""
        self.current_dataset_id += 1
        self.data = [random.randint(1, self.max_value) for _ in range(self.num_elements)]
        self.original_data = self.data.copy()
        self.algorithm_stats.clear()
        memory_manager.clear()
    
    def shuffle_data(self):
        """Mélange les données actuelles."""
        random.shuffle(self.data)
        memory_manager.clear()
    
    def reset_to_original(self):
        """Restaure l'ensemble de données original."""
        self.data = self.original_data.copy()
        memory_manager.clear()
    
    def get_data(self) -> List[int]:
        """Retourne les données actuelles."""
        return self.data
    
    def get_max_value(self) -> int:
        """Retourne la valeur maximale possible."""
        return self.max_value
    
    def start_sort(self, sort_algorithm: Callable, algorithm_name: str) -> None:
        """
        Démarre le tri avec l'algorithme spécifié.
        
        Args:
            sort_algorithm: Fonction de tri à utiliser
            algorithm_name: Nom de l'algorithme pour les statistiques
        """
        if self.is_sorting:
            return
        
        self.is_sorting = True
        self.current_algorithm = algorithm_name
        
        # Préparer les données pour le tri
        data_copy = self.data.copy()
        memory_manager.clear()
        
        # Chronométrer le tri
        start_time = time.time()
        step_count = 0
        
        # Exécuter le tri et compter les étapes
        for state in sort_algorithm(data_copy):
            step_count += 1
            self.current_state = state
            # Le traitement est fait dans update_visualization par l'appelant
            yield state
        
        # Calculer le temps écoulé
        elapsed_time = time.time() - start_time
        
        # Enregistrer les statistiques
        self.algorithm_stats[algorithm_name] = {
            'time': elapsed_time,
            'steps': step_count
        }
        
        # Mettre à jour les données triées
        if 'data' in self.current_state:
            self.data = self.current_state['data']
        
        self.is_sorting = False 