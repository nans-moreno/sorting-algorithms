'''
Visualiseur principal des algorithmes de tri.
'''

import pygame
import math
import random
from typing import List, Dict, Any, Generator, Callable

from config import (
    WIDTH, HEIGHT, BACKGROUND_COLOR, STARS_COUNT, NUM_ELEMENTS, 
    MAX_VALUE, MEMORY_ZONE_HEIGHT, MEMORY_SLOT_SIZE, SHOW_COMPARISON,
    COMPARISON_HEIGHT
)
from models.particle import Particle
from models.star import Star
from models.sort_data import SortData
from utils.memory import memory_manager
from ui.comparison import PerformanceComparison


class CosmiSort:
    """Visualiseur principal des algorithmes de tri avec effet cosmique."""
    
    def __init__(self):
        """Initialise le visualiseur."""
        # Initialisation des données
        self.sort_data = SortData(NUM_ELEMENTS, MAX_VALUE)
        
        # Particules représentant les données
        self.particles: List[Particle] = []
        self._initialize_particles()
        
        # Étoiles d'arrière-plan
        self.stars: List[Star] = []
        self._initialize_stars()
        
        # Initialiser les polices
        self.font = pygame.font.SysFont("Arial", 16)
        self.large_font = pygame.font.SysFont("Arial", 24)
        
        # Initialiser le comparateur de performances
        self.performance_comparison = PerformanceComparison(self.font, self.large_font)
        
        # Générateur pour le tri en cours
        self.sort_generator = None
    
    def _initialize_particles(self):
        """Initialise les particules représentant les données."""
        self.particles = []
        data = self.sort_data.get_data()
        max_value = self.sort_data.get_max_value()
        
        for i, value in enumerate(data):
            self.particles.append(Particle(value, i, max_value, len(data)))
    
    def _initialize_stars(self):
        """Initialise les étoiles d'arrière-plan."""
        self.stars = []
        for _ in range(STARS_COUNT):
            self.stars.append(Star(WIDTH, HEIGHT))
    
    def generate_data(self):
        """Génère un nouvel ensemble de données et met à jour les particules."""
        self.sort_data.generate_data()
        self._initialize_particles()
    
    def shuffle_data(self):
        """Mélange les données actuelles et met à jour les particules."""
        self.sort_data.shuffle_data()
        self._initialize_particles()
    
    def reset_to_original(self):
        """Restaure les données d'origine et met à jour les particules."""
        self.sort_data.reset_to_original()
        self._initialize_particles()
    
    def start_sort(self, sort_algorithm: Callable, algorithm_name: str):
        """
        Démarre le tri avec l'algorithme spécifié.
        
        Args:
            sort_algorithm: Fonction de tri à utiliser
            algorithm_name: Nom de l'algorithme pour les statistiques
        """
        self.sort_generator = self.sort_data.start_sort(sort_algorithm, algorithm_name)
    
    def update_visualization(self, state: Dict[str, Any]):
        """
        Met à jour la visualisation en fonction de l'état actuel du tri.
        
        Args:
            state: État actuel du tri (données, comparaisons, etc.)
        """
        # Mettre à jour les positions des particules en fonction des données
        if 'data' in state:
            # Arranger les particules en cercle
            for i, value in enumerate(state['data']):
                # Trouver la particule correspondant à cette valeur
                for particle in self.particles:
                    if particle.value == value:
                        # Calculer la nouvelle position (en cercle)
                        angle = 2 * math.pi * i / len(state['data'])
                        radius = min(WIDTH, HEIGHT) * 0.35
                        target_x = WIDTH // 2 + radius * math.cos(angle)
                        target_y = HEIGHT // 2 + radius * math.sin(angle)
                        
                        # Définir la position cible pour l'animation
                        particle.set_target_position(target_x, target_y)
                        break
        
        # Ajouter les opérations de mémoire
        if 'compare' in state:
            # Ajouter une opération de comparaison
            values = [state['data'][i] for i in state['compare'] if i < len(state['data'])]
            memory_manager.add_comparison(values)
            
            # Mettre en surbrillance les particules comparées
            for i, particle in enumerate(self.particles):
                particle.highlight_color = None
                if 'data' in state and particle.value in [state['data'][j] for j in state['compare'] if j < len(state['data'])]:
                    particle.highlight_color = (100, 100, 220)  # Bleu pour les comparaisons
        
        # Mettre en surbrillance les éléments modifiés
        if 'highlight' in state:
            for i in state['highlight']:
                if i < len(state['data']):
                    for particle in self.particles:
                        if particle.value == state['data'][i]:
                            particle.highlight_color = (220, 100, 100)  # Rouge pour les modifications
        
        # Marquer les éléments comme triés
        if 'final' in state:
            sorted_values = [state['data'][i] for i in state['final']]
            for particle in self.particles:
                if particle.value in sorted_values and not particle.highlight_color:
                    particle.highlight_color = (100, 220, 100)  # Vert pour les éléments triés
    
    def update(self):
        """Met à jour les éléments animés."""
        # Mettre à jour les étoiles
        for star in self.stars:
            star.update()
        
        # Mettre à jour les particules
        for particle in self.particles:
            particle.update()
        
        # Si un tri est en cours, avancer d'une étape
        if self.sort_generator:
            try:
                state = next(self.sort_generator)
                self.update_visualization(state)
            except StopIteration:
                self.sort_generator = None
                # Marquer tous les éléments comme triés si le tri est terminé
                if self.sort_data.current_state and 'data' in self.sort_data.current_state:
                    final_state = {
                        'data': self.sort_data.current_state['data'],
                        'final': list(range(len(self.sort_data.current_state['data'])))
                    }
                    self.update_visualization(final_state)
    
    def draw_memory_zone(self, screen: pygame.Surface, memory_zone_y: int):
        """
        Dessine la zone de mémoire montrant les opérations.
        
        Args:
            screen: Surface Pygame où dessiner
            memory_zone_y: Position Y de la zone de mémoire
        """
        # Dessiner la zone de mémoire
        memory_zone_rect = pygame.Rect(0, memory_zone_y, WIDTH, MEMORY_ZONE_HEIGHT)
        # Rectangle semi-transparent pour la zone de mémoire
        s = pygame.Surface((WIDTH, MEMORY_ZONE_HEIGHT), pygame.SRCALPHA)
        s.fill((30, 30, 60, 180))  # Bleu foncé semi-transparent
        screen.blit(s, (0, memory_zone_y))
        
        # Dessiner une bordure pour la zone de mémoire
        pygame.draw.rect(screen, (60, 60, 100), memory_zone_rect, 2)
        
        # Ajouter un titre pour la zone de mémoire
        memory_title = self.font.render("Opérations en mémoire ↓", True, (180, 180, 220))
        screen.blit(memory_title, (WIDTH // 2 - memory_title.get_width() // 2, memory_zone_y + 5))
        
        # Dessiner les opérations de mémoire comme des "slots"
        operations = memory_manager.get_operations()
        slot_width = MEMORY_SLOT_SIZE
        max_slots = WIDTH // slot_width
        
        # Calculer combien d'opérations afficher
        num_operations = min(len(operations), max_slots)
        
        # Calculer le X de départ pour centrer les opérations
        start_x = (WIDTH - (num_operations * slot_width)) // 2
        
        # Dessiner les opérations existantes
        for i, op in enumerate(operations[-num_operations:]):
            x = start_x + i * slot_width
            y = memory_zone_y + 30
            
            # Rectangle de fond pour l'opération avec la couleur correspondante
            slot_rect = pygame.Rect(x, y, slot_width - 2, MEMORY_ZONE_HEIGHT - 40)
            slot_color = (*op['color'], 150)  # Couleur avec transparence
            
            # Surface semi-transparente
            slot_surface = pygame.Surface((slot_width - 2, MEMORY_ZONE_HEIGHT - 40), pygame.SRCALPHA)
            slot_surface.fill(slot_color)
            screen.blit(slot_surface, (x, y))
            
            # Bordure
            pygame.draw.rect(screen, op['color'], slot_rect, 1)
            
            # Afficher le type d'opération
            op_type = self.font.render(op['type'][:4], True, (255, 255, 255))
            screen.blit(op_type, (x + (slot_width - op_type.get_width()) // 2, y + 5))
            
            # Afficher les valeurs concernées
            if op['values']:
                for j, value in enumerate(op['values'][:2]):  # Limiter à 2 valeurs max
                    val_text = self.font.render(str(value), True, (255, 255, 255))
                    screen.blit(val_text, (x + (slot_width - val_text.get_width()) // 2, y + 25 + j * 20))
    
    def draw_instructions(self, screen: pygame.Surface, y_start: int):
        """
        Dessine les instructions pour l'utilisateur.
        
        Args:
            screen: Surface Pygame où dessiner
            y_start: Position Y de départ pour les instructions
        """
        instructions = [
            "Appuyez sur [1-7] pour lancer un algorithme de tri:",
            "1: Sélection    2: Bulles    3: Insertion    4: Fusion    5: Rapide    6: Tas    7: Peigne",
            "R: Nouvelles données    S: Mélanger    O: Données originales    C: Graphique comparatif    Esc: Quitter"
        ]
        
        y_offset = y_start - len(instructions) * 25 - 20
        for inst in instructions:
            inst_text = self.font.render(inst, True, (160, 160, 200))
            screen.blit(inst_text, (20, y_offset))
            y_offset += 25
    
    def draw(self):
        """Dessine tous les éléments visuels sur l'écran."""
        screen = pygame.display.get_surface()
        
        # Effacer l'écran avec la couleur de fond
        screen.fill(BACKGROUND_COLOR)
        
        # Dessiner les étoiles
        for star in self.stars:
            star.draw(screen)
        
        # Si le comparateur est actif, ajuster la hauteur de la zone de mémoire
        memory_zone_y = HEIGHT - MEMORY_ZONE_HEIGHT
        if SHOW_COMPARISON:
            memory_zone_y = HEIGHT - MEMORY_ZONE_HEIGHT - COMPARISON_HEIGHT - 40
        
        # Dessiner la zone de mémoire
        self.draw_memory_zone(screen, memory_zone_y)
        
        # Dessiner le graphique de comparaison si activé
        if SHOW_COMPARISON:
            panel_y = HEIGHT - COMPARISON_HEIGHT - 20
            self.performance_comparison.draw(
                screen, 
                self.sort_data.algorithm_stats, 
                self.sort_data.current_dataset_id,
                panel_y
            )
        
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Afficher le titre
        title = self.large_font.render("CosmiSort: La Nébuleuse du Tri", True, (200, 220, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        
        # Afficher l'algorithme actuel et l'ID du jeu de données
        if self.sort_data.current_algorithm:
            algo_text = self.font.render(
                f"Algorithme: {self.sort_data.current_algorithm} - Dataset #{self.sort_data.current_dataset_id}", 
                True, 
                (200, 200, 255)
            )
            screen.blit(algo_text, (20, 20))
        else:
            dataset_text = self.font.render(f"Dataset #{self.sort_data.current_dataset_id}", True, (200, 200, 255))
            screen.blit(dataset_text, (20, 20))
        
        # Afficher les instructions
        self.draw_instructions(screen, memory_zone_y)
    
    @property
    def is_sorting(self):
        """Indique si un tri est en cours."""
        return self.sort_data.is_sorting 