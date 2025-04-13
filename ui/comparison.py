'''
Module pour afficher le graphique comparatif des performances des algorithmes.
'''

import pygame
from typing import Dict, List

from config import ALGORITHM_COLORS, ALGORITHM_ORDER, COMPARISON_HEIGHT, WIDTH


class PerformanceComparison:
    """Visualisation graphique des performances des algorithmes de tri."""
    
    def __init__(self, font, large_font):
        """Initialise le visualiseur de performances."""
        self.font = font
        self.large_font = large_font
    
    def draw(self, screen: pygame.Surface, stats: Dict[str, Dict[str, float]], dataset_id: int, panel_y: int):
        """
        Dessine le graphique de comparaison des performances.
        
        Args:
            screen: Surface Pygame où dessiner
            stats: Statistiques des algorithmes (temps et étapes)
            dataset_id: ID du jeu de données actuel
            panel_y: Position Y du panneau
        """
        if not stats or len(stats) < 1:
            return
        
        # Définir les dimensions et la position du panneau
        panel_width = WIDTH - 40  # Marge de 20px de chaque côté
        panel_height = COMPARISON_HEIGHT
        panel_x = 20
        
        # Créer une surface semi-transparente pour le fond
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((20, 20, 40, 200))  # Bleu très foncé semi-transparent
        
        # Dessiner le cadre
        pygame.draw.rect(panel, (100, 100, 150), (0, 0, panel_width, panel_height), 2)
        
        # Titre du panneau
        title = self.large_font.render(f"Comparaison des Performances - Dataset #{dataset_id}", True, (220, 220, 255))
        panel.blit(title, (panel_width // 2 - title.get_width() // 2, 10))
        
        # Calculer les statistiques pour chaque métrique
        time_stats = {algo: stats[algo]['time'] for algo in stats}
        steps_stats = {algo: stats[algo]['steps'] for algo in stats}
        
        # Trouver les valeurs max pour normalisation
        max_time = max(time_stats.values()) if time_stats else 1
        max_steps = max(steps_stats.values()) if steps_stats else 1
        
        # Calculer les dimensions des barres
        bar_area_width = panel_width - 200  # Espace pour les barres
        bar_area_height = panel_height - 100  # Hauteur de la zone des barres
        bar_width = (bar_area_width // len(ALGORITHM_COLORS)) - 10  # Largeur d'une barre avec espace
        time_bar_y = 60  # Position Y pour les barres de temps
        steps_bar_y = time_bar_y + bar_area_height // 2  # Position Y pour les barres d'étapes
        
        # Dessiner les barres pour chaque algorithme
        x_offset = 100  # Décalage initial
        
        # Trier les algorithmes par ordre d'utilisation standard
        sorted_algos = [algo for algo in ALGORITHM_ORDER if algo in stats]
        
        for algo in sorted_algos:
            if algo in time_stats:
                # Couleur de l'algorithme
                color = ALGORITHM_COLORS.get(algo, (200, 200, 200))
                
                # Dessiner le nom de l'algorithme (vertical pour gagner de l'espace)
                algo_name = self.font.render(algo.split(" ")[-1], True, color)  # Ne prendre que la partie après "Tri par"
                panel.blit(algo_name, (x_offset + bar_width // 2 - algo_name.get_width() // 2, 40))
                
                # Barre pour le temps
                time_ratio = time_stats[algo] / max_time
                time_height = max(5, int(time_ratio * (bar_area_height // 2 - 20)))
                time_rect = pygame.Rect(x_offset, time_bar_y + (bar_area_height // 2 - 20) - time_height,
                                     bar_width, time_height)
                pygame.draw.rect(panel, color, time_rect)
                pygame.draw.rect(panel, (255, 255, 255), time_rect, 1)
                
                # Texte pour le temps - Déplacer le temps à droite de la barre au lieu d'au-dessus
                time_text = self.font.render(f"{time_stats[algo]:.2f}s", True, (220, 220, 255))
                panel.blit(time_text, (x_offset + bar_width + 5,
                                    time_bar_y + (bar_area_height // 4) - time_text.get_height()//2))
                
                # Barre pour les étapes
                steps_ratio = steps_stats[algo] / max_steps
                steps_height = max(5, int(steps_ratio * (bar_area_height // 2 - 20)))
                steps_rect = pygame.Rect(x_offset, steps_bar_y + (bar_area_height // 2 - 20) - steps_height,
                                      bar_width, steps_height)
                pygame.draw.rect(panel, color, steps_rect)
                pygame.draw.rect(panel, (255, 255, 255), steps_rect, 1)
                
                # Texte pour les étapes - Déplacer le nombre d'étapes à droite de la barre
                steps_text = self.font.render(f"{steps_stats[algo]}", True, (220, 220, 255))
                panel.blit(steps_text, (x_offset + bar_width + 5,
                                     steps_bar_y + (bar_area_height // 4) - steps_text.get_height()//2))
                
                x_offset += bar_width + max(50, time_text.get_width() + 15)  # Augmenter l'espace entre les barres
        
        # Légendes
        time_legend = self.font.render("Temps (secondes)", True, (220, 220, 255))
        panel.blit(time_legend, (10, time_bar_y))
        
        steps_legend = self.font.render("Nombre d'étapes", True, (220, 220, 255))
        panel.blit(steps_legend, (10, steps_bar_y))
        
        # Afficher le panneau sur l'écran
        screen.blit(panel, (panel_x, panel_y)) 