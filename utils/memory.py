'''
Gestion des opérations mémoire pour visualiser les étapes des algorithmes de tri.
'''

from typing import List, Dict, Any


class MemoryManager:
    """Gestionnaire des opérations mémoire pour visualiser les algorithmes de tri."""
    
    def __init__(self, max_operations: int = 100):
        """Initialise le gestionnaire de mémoire."""
        self.operations: List[Dict[str, Any]] = []
        self.max_operations = max_operations
    
    def add_operation(self, op_type: str, values: List[int], color: tuple):
        """
        Ajoute une opération à l'historique.
        
        Args:
            op_type: Type d'opération ('COMP', 'SWAP', etc.)
            values: Valeurs impliquées dans l'opération
            color: Couleur associée à l'opération
        """
        operation = {
            'type': op_type,
            'values': values,
            'color': color
        }
        
        self.operations.append(operation)
        
        # Limiter le nombre d'opérations stockées
        if len(self.operations) > self.max_operations:
            self.operations.pop(0)
    
    def add_comparison(self, values: List[int], color: tuple = (100, 100, 220)):
        """Ajoute une opération de comparaison."""
        self.add_operation('COMP', values, color)
    
    def add_swap(self, values: List[int], color: tuple = (220, 100, 100)):
        """Ajoute une opération d'échange."""
        self.add_operation('SWAP', values, color)
    
    def add_write(self, values: List[int], color: tuple = (100, 220, 100)):
        """Ajoute une opération d'écriture."""
        self.add_operation('WRITE', values, color)
    
    def clear(self):
        """Efface toutes les opérations."""
        self.operations.clear()
    
    def get_operations(self) -> List[Dict[str, Any]]:
        """Retourne la liste des opérations."""
        return self.operations

# Instance globale pour la compatibilité avec le code existant
memory_manager = MemoryManager() 