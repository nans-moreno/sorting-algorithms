'''
Classe Particle: Représente une particule visuelle pour les éléments à trier.
'''

import pygame
import math
import random
from typing import Tuple, List, Dict

# Import des constantes
from config import PARTICLE_MIN_RADIUS, PARTICLE_MAX_RADIUS


class Particle:
    """Représente un élément de données comme une particule énergétique."""
    
    def __init__(self, value: int, index: int, max_value: int, total_elements: int):
        self.value = value
        self.original_index = index
        self.max_value = max_value
        
        # Position: disposition initialement en cercle
        angle = 2 * math.pi * index / total_elements
        radius = min(pygame.display.get_surface().get_width(), 
                     pygame.display.get_surface().get_height()) * 0.35  # 35% de la taille de l'écran
        self.x = pygame.display.get_surface().get_width() // 2 + radius * math.cos(angle)
        self.y = pygame.display.get_surface().get_height() // 2 + radius * math.sin(angle)
        
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