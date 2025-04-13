'''
CosmiSort: Visualiseur d'algorithmes de tri futuriste.

Une nébuleuse cybernétique où les nombres se transforment en
particules énergétiques qui s'organisent selon différents algorithmes de tri.
'''

import pygame
import pygame.gfxdraw
import random
import math
import time
import sys
import sorting
from typing import List, Dict, Any, Callable, Tuple
from config import SHOW_COMPARISON, WIDTH, HEIGHT, ANIMATION_DELAY
from ui.visualizer import CosmiSort

# --- Configuration ---
WIDTH, HEIGHT = 1600, 900  # Agrandissement de la fenêtre pour plus d'impact visuel
PARTICLE_MIN_RADIUS = 15  # Augmentation de la taille minimum
PARTICLE_MAX_RADIUS = 40  # Augmentation de la taille maximum
BACKGROUND_COLOR = (0, 0, 20)  # Bleu très foncé / noir
NUM_ELEMENTS = 20  # Légèrement réduit pour éviter l'encombrement avec les particules plus grandes
MAX_VALUE = 100
ANIMATION_DELAY = 30  # Millisecondes entre chaque étape
STARS_COUNT = 150  # Plus d'étoiles d'arrière-plan

# Nouvelle configuration pour la zone de mémoire/étapes
MEMORY_ZONE_HEIGHT = 120  # Hauteur de la zone de mémoire en bas
MEMORY_SLOT_SIZE = 30     # Taille des emplacements de mémoire
MEMORY_OPERATIONS = []    # Liste pour stocker les opérations (comparaisons, échanges, etc.)

# Configuration pour le graphique de comparaison
COMPARISON_HEIGHT = 300   # Hauteur du panneau de comparaison

# --- Initialisation de Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CosmiSort: Nébuleuse du Tri")
clock = pygame.time.Clock()

# --- Polices ---
try:
    font = pygame.font.Font("arial.ttf", 16)
except:
    font = pygame.font.SysFont("Arial", 16)
    
try:
    large_font = pygame.font.Font("arial.ttf", 24)
except:
    large_font = pygame.font.SysFont("Arial", 24)

# --- Classes et Fonctions ---
class Particle:
    """Représente un élément de données comme une particule énergétique."""
    
    def __init__(self, value: int, index: int, max_value: int, total_elements: int):
        self.value = value
        self.original_index = index
        self.max_value = max_value
        
        # Position: disposition initialement en cercle
        angle = 2 * math.pi * index / total_elements
        radius = min(WIDTH, HEIGHT) * 0.35  # 35% de la taille de l'écran
        self.x = WIDTH // 2 + radius * math.cos(angle)
        self.y = HEIGHT // 2 + radius * math.sin(angle)
        
        # Position cible (position finale après animation)
        self.target_x = self.x
        self.target_y = self.y
        
        # Taille et couleur déterminées par la valeur
        self.radius = self._calculate_radius()
        self.color = self._calculate_color()
        self.highlight_color = None  # Pour les animations
        self.trail = []  # Pour l'effet de traînée
        
        # Particules d'énergie autour de l'élément (effet visuel)
        self.energy_particles = []
        self._generate_energy_particles()
        
    def _calculate_radius(self) -> float:
        """Calcule le rayon en fonction de la valeur."""
        return PARTICLE_MIN_RADIUS + (PARTICLE_MAX_RADIUS - PARTICLE_MIN_RADIUS) * (self.value / self.max_value)
    
    def _calculate_color(self) -> Tuple[int, int, int]:
        """Attribue une couleur basée sur la valeur (du bleu au rose)."""
        # Gradient de couleur du bleu au violet/rose
        normalized = self.value / self.max_value
        r = int(50 + normalized * 205)  # 50-255
        g = int(50 + (1 - normalized) * 100)  # 50-150
        b = int(150 + normalized * 105)  # 150-255
        return (r, g, b)
    
    def _generate_energy_particles(self):
        """Génère de petites particules d'énergie autour de l'élément principal."""
        num_particles = int(3 + (self.value / self.max_value) * 7)  # 3-10 particules
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            distance = self.radius * 1.5 + random.uniform(0, self.radius * 2)
            px = distance * math.cos(angle)
            py = distance * math.sin(angle)
            size = random.uniform(1, 3)
            # Couleur légèrement plus claire que la particule principale
            color = tuple(min(c + 50, 255) for c in self.color)
            self.energy_particles.append({
                'offset_x': px, 
                'offset_y': py, 
                'size': size, 
                'color': color,
                'angle': angle,
                'distance': distance,
                'speed': random.uniform(0.02, 0.1)
            })
    
    def update_energy_particles(self):
        """Anime les particules d'énergie autour de l'élément."""
        for particle in self.energy_particles:
            # Faire tourner légèrement les particules
            particle['angle'] += particle['speed']
            particle['offset_x'] = particle['distance'] * math.cos(particle['angle'])
            particle['offset_y'] = particle['distance'] * math.sin(particle['angle'])
    
    def set_target_position(self, x: float, y: float):
        """Définit la position cible pour l'animation."""
        if len(self.trail) == 0 or ((self.target_x, self.target_y) != (x, y)):
            # Ajouter la position actuelle à la traînée uniquement lors d'un changement de destination
            self.trail = [(self.x, self.y)]
        self.target_x = x
        self.target_y = y
    
    def update(self):
        """Met à jour la position de la particule (interpolation vers la cible)."""
        # Mouvement fluide vers la position cible
        speed = 0.1  # Vitesse d'interpolation: 0-1
        self.x = self.x + (self.target_x - self.x) * speed
        self.y = self.y + (self.target_y - self.y) * speed
        
        # Mettre à jour les particules d'énergie
        self.update_energy_particles()
        
        # Mettre à jour la traînée
        if len(self.trail) > 0:
            if abs(self.x - self.target_x) < 1 and abs(self.y - self.target_y) < 1:
                # Arrivé à destination, effacer la traînée
                self.trail = []
            elif len(self.trail) < 10 and random.random() < 0.3:
                # Ajouter de nouveaux points à la traînée pendant le déplacement
                self.trail.append((self.x, self.y))
    
    def draw(self, surface: pygame.Surface):
        """Dessine la particule et ses effets visuels."""
        # Dessiner la traînée
        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                alpha = int(255 * (1 - i / len(self.trail)))  # Fondu progressif
                color = (min(self.color[0], 255), min(self.color[1], 255), min(self.color[2], 255))
                color_with_alpha = (*color, alpha)
                
                pygame.draw.line(
                    surface, 
                    color_with_alpha,
                    self.trail[i-1], 
                    self.trail[i], 
                    max(1, int(self.radius * 0.5 * (1 - i / len(self.trail))))
                )
        
        # Dessiner les particules d'énergie
        for particle in self.energy_particles:
            pygame.draw.circle(
                surface,
                particle['color'],
                (int(self.x + particle['offset_x']), int(self.y + particle['offset_y'])),
                int(particle['size'])
            )
        
        # Dessiner la particule principale
        # Cercle de base
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
        
        # Lueur (effet de halo) si surbrillance
        if self.highlight_color:
            # Cercle extérieur semi-transparent
            s = pygame.Surface((int(self.radius * 2.5) * 2, int(self.radius * 2.5) * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                s, 
                (*self.highlight_color, 100),  # Couleur avec alpha
                (s.get_width() // 2, s.get_height() // 2), 
                int(self.radius * 2.5)
            )
            surface.blit(s, (self.x - s.get_width() // 2, self.y - s.get_height() // 2))
        
        # Éclat interne (effet de brillance)
        pygame.draw.circle(
            surface,
            (min(self.color[0] + 50, 255), min(self.color[1] + 50, 255), min(self.color[2] + 50, 255)),
            (int(self.x), int(self.y)),
            int(self.radius * 0.7)
        )
        
        # Reflet (petit cercle blanc pour effet 3D)
        highlight_pos = (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3))
        pygame.draw.circle(surface, (255, 255, 255), highlight_pos, int(self.radius * 0.2))
        
        # NOUVEAU: Afficher la valeur numérique à l'intérieur de la particule
        # Choisir une taille de police proportionnelle au rayon
        font_size = max(12, min(24, int(self.radius * 0.8)))
        
        try:
            value_font = pygame.font.SysFont("Arial", font_size, bold=True)
            # Texte blanc avec bord noir pour être visible sur toutes les couleurs
            value_text = value_font.render(str(self.value), True, (255, 255, 255))
            # Centrer le texte dans la particule
            text_x = self.x - value_text.get_width() // 2
            text_y = self.y - value_text.get_height() // 2
            
            # Option 1: Texte simple
            surface.blit(value_text, (text_x, text_y))
            
            # Option 2: Ajouter un léger effet d'ombre pour meilleure lisibilité
            shadow_text = value_font.render(str(self.value), True, (0, 0, 0))
            surface.blit(shadow_text, (text_x + 1, text_y + 1))
            surface.blit(value_text, (text_x, text_y))
        except:
            # En cas d'erreur avec la police, on continue sans afficher le nombre
            pass


class Star:
    """Étoile d'arrière-plan pour l'effet cosmos."""
    
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 2)
        self.brightness = random.uniform(0.3, 1.0)
        self.pulse_speed = random.uniform(0.01, 0.05)
        self.pulse_offset = random.uniform(0, 2 * math.pi)
    
    def update(self):
        """Met à jour la brillance de l'étoile (effet de pulsation)."""
        self.pulse_offset += self.pulse_speed
        self.brightness = 0.5 + 0.5 * math.sin(self.pulse_offset)
    
    def draw(self, surface: pygame.Surface):
        """Dessine l'étoile avec sa brillance actuelle."""
        color = (
            int(200 * self.brightness), 
            int(200 * self.brightness), 
            int(255 * self.brightness)
        )
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class CosmiSort:
    """Classe principale du visualiseur d'algorithmes de tri."""
    
    def __init__(self):
        self.particles = []
        self.stars = [Star() for _ in range(STARS_COUNT)]
        self.sorting_generator = None
        self.current_algorithm = None
        self.is_sorting = False
        self.sort_step = 0
        self.current_state = None
        self.sort_start_time = 0
        self.sort_end_time = 0
        self.algorithm_stats = {}  # Pour stocker les temps d'exécution
        
        # Nouvelles variables pour le suivi et la comparaison
        self.original_data = []  # Sauvegarder les données d'origine pour comparaison
        self.current_dataset_id = 0  # Identifiant du jeu de données actuel
        
        # Générer les données initiales et configurer la visualisation
        self.generate_data()
    
    def generate_data(self):
        """Génère un nouveau jeu de données aléatoires."""
        self.data = [random.randint(1, MAX_VALUE) for _ in range(NUM_ELEMENTS)]
        self.original_data = self.data.copy()  # Sauvegarder pour comparaison future
        self.current_dataset_id += 1  # Incrémenter l'ID à chaque nouveau jeu de données
        
        # Réinitialiser les statistiques lorsqu'on change de jeu de données
        self.algorithm_stats = {}
        
        self.setup_visualization()
    
    def shuffle_data(self):
        """Mélange les données actuelles sans en générer de nouvelles."""
        if self.is_sorting:
            return  # Ne pas mélanger pendant un tri
        
        # Restaurer d'abord les données originales
        self.data = self.original_data.copy()
        
        # Puis les mélanger de façon aléatoire
        random.shuffle(self.data)
        
        self.setup_visualization()
    
    def reset_to_original(self):
        """Restaure les données à leur état d'origine (avant tout tri)."""
        if self.is_sorting:
            return  # Ne pas restaurer pendant un tri
        
        self.data = self.original_data.copy()
        self.setup_visualization()
    
    def setup_visualization(self):
        """Initialise les particules en fonction des données."""
        self.particles = []
        max_val = max(self.data)
        
        for i, value in enumerate(self.data):
            self.particles.append(Particle(value, i, max_val, len(self.data)))
    
    def start_sort(self, algorithm_visual, name):
        """Démarre le processus de tri avec l'algorithme spécifié."""
        if self.is_sorting:
            return
        
        self.current_algorithm = name
        self.sorting_generator = algorithm_visual(self.data.copy())
        self.is_sorting = True
        self.sort_step = 0
        self.current_state = None
        self.sort_start_time = time.time()
        
        # Réinitialiser les opérations de mémoire
        global MEMORY_OPERATIONS
        MEMORY_OPERATIONS = []
    
    def update_visualization(self, state):
        """Met à jour les particules en fonction de l'état du tri."""
        data = state.get('data', [])
        if not data:
            return
        
        n = len(data)
        max_val = max(data)
        
        # Réorganiser les particules sur la ligne horizontale
        # Créer un dictionnaire qui compte les occurrences de chaque valeur
        value_counts = {}
        sorted_values = sorted(data)
        
        # Première passe : compter les occurrences de chaque valeur
        for value in sorted_values:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
        
        # Deuxième passe : créer un dictionnaire qui mappe chaque occurrence de chaque valeur à une position
        value_to_positions = {}
        value_seen_counts = {}
        
        for i, value in enumerate(sorted_values):
            if value not in value_seen_counts:
                value_seen_counts[value] = 0
            else:
                value_seen_counts[value] += 1
            
            current_occurrence = value_seen_counts[value]
            if value not in value_to_positions:
                value_to_positions[value] = []
            
            # Calculer la position de base pour cette valeur
            base_position = i
            value_to_positions[value].append(base_position)
        
        # Mettre à jour chaque particule
        for i, value in enumerate(data):
            # Trouver l'indice de cette occurrence spécifique dans les données actuelles
            # Pour cela, on compte combien de fois la valeur apparaît avant l'indice i
            occurrences_before = data[:i].count(value)
            
            # Vérifier si nous avons suffisamment de positions pour cette valeur
            if value in value_to_positions and occurrences_before < len(value_to_positions[value]):
                # Obtenir la position correspondant à cette occurrence
                position = value_to_positions[value][occurrences_before]
                
                # Calculer la position horizontale finale
                total_positions = n
                x = WIDTH * (0.2 + 0.6 * (position / (total_positions - 1 if total_positions > 1 else 1)))
                y = HEIGHT * 0.5 - MEMORY_ZONE_HEIGHT/2
            else:
                # Fallback pour les cas problématiques (ne devrait pas arriver normalement)
                # Utiliser une position basée sur l'index actuel
                x = WIDTH * (0.2 + 0.6 * (i / (n - 1 if n > 1 else 1)))
                y = HEIGHT * 0.5 - MEMORY_ZONE_HEIGHT/2
            
            # Mettre à jour les propriétés de la particule
            self.particles[i].value = value
            self.particles[i].max_value = max_val
            self.particles[i].radius = self.particles[i]._calculate_radius()
            self.particles[i].color = self.particles[i]._calculate_color()
            self.particles[i].set_target_position(x, y)
        
        # Réinitialiser les mises en évidence
        for particle in self.particles:
            particle.highlight_color = None
        
        # Appliquer les mises en évidence en fonction des opérations
        memory_operation = None
        
        if 'compare' in state and len(state['compare']) == 2:
            idx1, idx2 = state['compare']
            if idx1 < len(self.particles): 
                self.particles[idx1].highlight_color = (255, 255, 0)  # Jaune
            if idx2 < len(self.particles): 
                self.particles[idx2].highlight_color = (255, 255, 0)
            
            # Ajouter l'opération à la mémoire
            memory_operation = {
                'type': 'compare',
                'indices': [idx1, idx2],
                'values': [data[idx1], data[idx2]] if idx1 < len(data) and idx2 < len(data) else [],
                'color': (255, 255, 0)
            }
        
        if 'swap' in state and len(state['swap']) == 2:
            idx1, idx2 = state['swap']
            if idx1 < len(self.particles): 
                self.particles[idx1].highlight_color = (255, 100, 0)  # Orange
            if idx2 < len(self.particles): 
                self.particles[idx2].highlight_color = (255, 100, 0)
            
            # Ajouter l'opération à la mémoire
            memory_operation = {
                'type': 'swap',
                'indices': [idx1, idx2],
                'values': [data[idx1], data[idx2]] if idx1 < len(data) and idx2 < len(data) else [],
                'color': (255, 100, 0)
            }
        
        if 'highlight' in state:
            indices = state['highlight']
            for idx in indices:
                if idx < len(self.particles): 
                    self.particles[idx].highlight_color = (0, 255, 255)  # Cyan
            
            # Ajouter l'opération à la mémoire
            if indices:
                memory_operation = {
                    'type': 'highlight',
                    'indices': indices,
                    'values': [data[idx] for idx in indices if idx < len(data)],
                    'color': (0, 255, 255)
                }
        
        if 'min_candidate' in state:
            idx = state['min_candidate']
            if idx < len(self.particles): 
                self.particles[idx].highlight_color = (100, 100, 255)  # Bleu clair
            
            # Ajouter l'opération à la mémoire
            memory_operation = {
                'type': 'min_candidate',
                'indices': [idx],
                'values': [data[idx]] if idx < len(data) else [],
                'color': (100, 100, 255)
            }
        
        if 'insert' in state:
            indices = state['insert']
            for idx in indices:
                if idx < len(self.particles): 
                    self.particles[idx].highlight_color = (255, 0, 255)  # Magenta
            
            # Ajouter l'opération à la mémoire
            if indices:
                memory_operation = {
                    'type': 'insert',
                    'indices': indices,
                    'values': [data[idx] for idx in indices if idx < len(data)],
                    'color': (255, 0, 255)
                }
        
        if 'final' in state:
            indices = state['final']
            for idx in indices:
                if idx < len(self.particles): 
                    self.particles[idx].highlight_color = (0, 255, 0)  # Vert
            
            # Ajouter l'opération à la mémoire seulement s'il y a peu d'éléments finaux
            # (pour éviter de remplir la mémoire quand tous les éléments sont finaux)
            if indices and len(indices) <= 5:
                memory_operation = {
                    'type': 'final',
                    'indices': indices,
                    'values': [data[idx] for idx in indices if idx < len(data)],
                    'color': (0, 255, 0)
                }
        
        # Ajouter l'opération à la liste globale des opérations de mémoire
        if memory_operation:
            global MEMORY_OPERATIONS
            MEMORY_OPERATIONS.append(memory_operation)
            # Limiter la taille de la liste pour éviter les ralentissements
            if len(MEMORY_OPERATIONS) > WIDTH // MEMORY_SLOT_SIZE:
                MEMORY_OPERATIONS = MEMORY_OPERATIONS[-WIDTH // MEMORY_SLOT_SIZE:] # Garder les plus récentes
    
    def update(self):
        """Met à jour l'état de la visualisation."""
        # Mettre à jour les étoiles
        for star in self.stars:
            star.update()
        
        # Mettre à jour les particules
        for particle in self.particles:
            particle.update()
        
        # Procéder à l'étape de tri suivante si en cours
        if self.is_sorting and self.sorting_generator:
            try:
                self.current_state = next(self.sorting_generator)
                self.update_visualization(self.current_state)
                self.sort_step += 1
            except StopIteration:
                self.sorting_generator = None
                self.is_sorting = False
                self.sort_end_time = time.time()
                sort_time = self.sort_end_time - self.sort_start_time
                self.algorithm_stats[self.current_algorithm] = {
                    'time': sort_time,
                    'steps': self.sort_step
                }
                print(f"{self.current_algorithm} terminé en {sort_time:.4f} secondes ({self.sort_step} étapes)")
                
                # Marquer tous les éléments comme triés
                if self.current_state and 'data' in self.current_state:
                    final_state = {
                        'data': self.current_state['data'],
                        'final': list(range(len(self.current_state['data'])))
                    }
                    self.update_visualization(final_state)
    
    def draw_performance_comparison(self):
        """Dessine un graphique comparant les performances des algorithmes."""
        global SHOW_COMPARISON, COMPARISON_HEIGHT
        
        if not SHOW_COMPARISON or len(self.algorithm_stats) < 1:
            return  # Ne rien afficher s'il n'y a pas assez de données ou si le mode est désactivé
        
        # Définir les dimensions et la position du panneau
        panel_width = WIDTH - 40  # Marge de 20px de chaque côté
        panel_height = COMPARISON_HEIGHT
        panel_x = 20
        panel_y = HEIGHT - panel_height - 20  # 20px de marge en bas
        
        # Créer une surface semi-transparente pour le fond
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((20, 20, 40, 200))  # Bleu très foncé semi-transparent
        
        # Dessiner le cadre
        pygame.draw.rect(panel, (100, 100, 150), (0, 0, panel_width, panel_height), 2)
        
        # Titre du panneau
        title = large_font.render(f"Comparaison des Performances - Dataset #{self.current_dataset_id}", True, (220, 220, 255))
        panel.blit(title, (panel_width // 2 - title.get_width() // 2, 10))
        
        # Calculer les statistiques pour chaque métrique
        time_stats = {algo: stats['time'] for algo, stats in self.algorithm_stats.items()}
        steps_stats = {algo: stats['steps'] for algo, stats in self.algorithm_stats.items()}
        
        # Trouver les valeurs max pour normalisation
        max_time = max(time_stats.values()) if time_stats else 1
        max_steps = max(steps_stats.values()) if steps_stats else 1
        
        # Définir les couleurs pour chaque algorithme
        algo_colors = {
            "Tri par sélection": (220, 100, 100),
            "Tri à bulles": (100, 220, 100),
            "Tri par insertion": (100, 100, 220),
            "Tri fusion": (220, 220, 100),
            "Tri rapide": (220, 100, 220),
            "Tri par tas": (100, 220, 220),
            "Tri à peigne": (180, 180, 180)
        }
        
        # Calculer les dimensions des barres
        bar_area_width = panel_width - 200  # Espace pour les barres
        bar_area_height = panel_height - 100  # Hauteur de la zone des barres
        bar_width = (bar_area_width // len(algo_colors)) - 10  # Largeur d'une barre avec espace
        time_bar_y = 60  # Position Y pour les barres de temps
        steps_bar_y = time_bar_y + bar_area_height // 2  # Position Y pour les barres d'étapes
        
        # Dessiner les barres pour chaque algorithme
        x_offset = 100  # Décalage initial
        
        # Trier les algorithmes par ordre d'utilisation standard
        order = ["Tri par sélection", "Tri à bulles", "Tri par insertion", 
                "Tri fusion", "Tri rapide", "Tri par tas", "Tri à peigne"]
        sorted_algos = [algo for algo in order if algo in self.algorithm_stats]
        
        for algo in sorted_algos:
            if algo in time_stats:
                # Couleur de l'algorithme
                color = algo_colors.get(algo, (200, 200, 200))
                
                # Dessiner le nom de l'algorithme (vertical pour gagner de l'espace)
                algo_name = font.render(algo.split(" ")[-1], True, color)  # Ne prendre que la partie après "Tri par"
                panel.blit(algo_name, (x_offset + bar_width // 2 - algo_name.get_width() // 2, 40))
                
                # Barre pour le temps
                time_ratio = time_stats[algo] / max_time
                time_height = max(5, int(time_ratio * (bar_area_height // 2 - 20)))
                time_rect = pygame.Rect(x_offset, time_bar_y + (bar_area_height // 2 - 20) - time_height,
                                     bar_width, time_height)
                pygame.draw.rect(panel, color, time_rect)
                pygame.draw.rect(panel, (255, 255, 255), time_rect, 1)
                
                # Texte pour le temps - Déplacer le temps à droite de la barre au lieu d'au-dessus
                time_text = font.render(f"{time_stats[algo]:.2f}s", True, (220, 220, 255))
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
                steps_text = font.render(f"{steps_stats[algo]}", True, (220, 220, 255))
                panel.blit(steps_text, (x_offset + bar_width + 5,
                                     steps_bar_y + (bar_area_height // 4) - steps_text.get_height()//2))
                
                x_offset += bar_width + max(50, time_text.get_width() + 15)  # Augmenter l'espace entre les barres
        
        # Légendes
        time_legend = font.render("Temps (secondes)", True, (220, 220, 255))
        panel.blit(time_legend, (10, time_bar_y))
        
        steps_legend = font.render("Nombre d'étapes", True, (220, 220, 255))
        panel.blit(steps_legend, (10, steps_bar_y))
        
        # Afficher le panneau sur l'écran
        screen.blit(panel, (panel_x, panel_y))

    def draw(self):
        """Dessine tous les éléments visuels sur l'écran."""
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
        memory_zone_rect = pygame.Rect(0, memory_zone_y, WIDTH, MEMORY_ZONE_HEIGHT)
        # Rectangle semi-transparent pour la zone de mémoire
        s = pygame.Surface((WIDTH, MEMORY_ZONE_HEIGHT), pygame.SRCALPHA)
        s.fill((30, 30, 60, 180))  # Bleu foncé semi-transparent
        screen.blit(s, (0, memory_zone_y))
        
        # Dessiner une bordure pour la zone de mémoire
        pygame.draw.rect(screen, (60, 60, 100), memory_zone_rect, 2)
        
        # Ajouter un titre pour la zone de mémoire
        memory_title = font.render("Opérations en mémoire ↓", True, (180, 180, 220))
        screen.blit(memory_title, (WIDTH // 2 - memory_title.get_width() // 2, memory_zone_y + 5))
        
        # Dessiner les opérations de mémoire comme des "slots"
        global MEMORY_OPERATIONS
        slot_width = MEMORY_SLOT_SIZE
        max_slots = WIDTH // slot_width
        
        # Calculer combien d'opérations afficher
        num_operations = min(len(MEMORY_OPERATIONS), max_slots)
        
        # Calculer le X de départ pour centrer les opérations
        start_x = (WIDTH - (num_operations * slot_width)) // 2
        
        # Dessiner les opérations existantes
        for i, op in enumerate(MEMORY_OPERATIONS[-num_operations:]):
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
            op_type = font.render(op['type'][:4], True, (255, 255, 255))
            screen.blit(op_type, (x + (slot_width - op_type.get_width()) // 2, y + 5))
            
            # Afficher les valeurs concernées
            if op['values']:
                for j, value in enumerate(op['values'][:2]):  # Limiter à 2 valeurs max
                    val_text = font.render(str(value), True, (255, 255, 255))
                    screen.blit(val_text, (x + (slot_width - val_text.get_width()) // 2, y + 25 + j * 20))
        
        # Dessiner le graphique de comparaison si activé
        if SHOW_COMPARISON:
            self.draw_performance_comparison()
        
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Afficher le titre
        title = large_font.render("CosmiSort: La Nébuleuse du Tri", True, (200, 220, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        
        # Afficher l'algorithme actuel et l'ID du jeu de données
        if self.current_algorithm:
            algo_text = font.render(f"Algorithme: {self.current_algorithm} - Dataset #{self.current_dataset_id}", True, (200, 200, 255))
            screen.blit(algo_text, (20, 20))
        else:
            dataset_text = font.render(f"Dataset #{self.current_dataset_id}", True, (200, 200, 255))
            screen.blit(dataset_text, (20, 20))
        
        # Afficher les statistiques de tri
        y_offset = 60
        for algo, stats in self.algorithm_stats.items():
            stat_text = font.render(
                f"{algo}: {stats['time']:.4f}s ({stats['steps']} étapes)", 
                True, 
                (180, 180, 220)
            )
            screen.blit(stat_text, (20, y_offset))
            y_offset += 25
        
        # Afficher un compteur d'étapes en cours pour l'algorithme actuel
        if self.is_sorting:
            step_text = font.render(f"Étapes: {self.sort_step}", True, (220, 220, 255))
            screen.blit(step_text, (WIDTH - step_text.get_width() - 20, 20))
        
        # Définir la position de départ pour les instructions
        if SHOW_COMPARISON:
            y_start = memory_zone_y - 120
        else:
            y_start = memory_zone_y
        
        # Afficher les instructions
        instructions = [
            "Appuyez sur [1-7] pour lancer un algorithme de tri:",
            "1: Sélection    2: Bulles    3: Insertion    4: Fusion    5: Rapide    6: Tas    7: Peigne",
            "R: Nouvelles données    S: Mélanger    O: Données originales    C: Graphique comparatif    Esc: Quitter"
        ]
        
        y_offset = y_start - len(instructions) * 25 - 20
        for inst in instructions:
            inst_text = font.render(inst, True, (160, 160, 200))
            screen.blit(inst_text, (20, y_offset))
            y_offset += 25


def main():
    """Fonction principale du programme."""
    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CosmiSort: Nébuleuse du Tri")
    clock = pygame.time.Clock()
    
    # Initialisation du visualiseur
    cosmi_sort = CosmiSort()
    
    # --- Boucle principale ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Régénérer les données
                    cosmi_sort.generate_data()
                elif event.key == pygame.K_1 and not cosmi_sort.is_sorting:
                    # Tri par sélection
                    cosmi_sort.start_sort(sorting.selection_sort_visual, "Tri par sélection")
                elif event.key == pygame.K_2 and not cosmi_sort.is_sorting:
                    # Tri à bulles
                    cosmi_sort.start_sort(sorting.bubble_sort_visual, "Tri à bulles")
                elif event.key == pygame.K_3 and not cosmi_sort.is_sorting:
                    # Tri par insertion
                    cosmi_sort.start_sort(sorting.insertion_sort_visual, "Tri par insertion")
                elif event.key == pygame.K_4 and not cosmi_sort.is_sorting:
                    # Tri fusion
                    cosmi_sort.start_sort(sorting.merge_sort_visual, "Tri fusion")
                elif event.key == pygame.K_5 and not cosmi_sort.is_sorting:
                    # Tri rapide
                    cosmi_sort.start_sort(sorting.quick_sort_visual, "Tri rapide")
                elif event.key == pygame.K_6 and not cosmi_sort.is_sorting:
                    # Tri par tas
                    cosmi_sort.start_sort(sorting.heap_sort_visual, "Tri par tas")
                elif event.key == pygame.K_7 and not cosmi_sort.is_sorting:
                    # Tri à peigne
                    cosmi_sort.start_sort(sorting.comb_sort_visual, "Tri à peigne")
                elif event.key == pygame.K_s and not cosmi_sort.is_sorting:
                    # Mélanger les données actuelles
                    cosmi_sort.shuffle_data()
                elif event.key == pygame.K_o and not cosmi_sort.is_sorting:
                    # Restaurer les données d'origine (non triées)
                    cosmi_sort.reset_to_original()
                elif event.key == pygame.K_c:
                    # Activer/désactiver le comparateur de performances
                    global SHOW_COMPARISON
                    SHOW_COMPARISON = not SHOW_COMPARISON
        
        # Mise à jour et dessin
        cosmi_sort.update()
        cosmi_sort.draw()
        
        # Rafraîchir l'écran
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        
        # Ajouter un délai pour ralentir l'animation du tri
        if cosmi_sort.is_sorting:
            time.sleep(ANIMATION_DELAY / 1000)
    
    # Libérer les ressources
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()  