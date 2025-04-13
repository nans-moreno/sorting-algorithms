'''
Classe Star: Représente les étoiles d'arrière-plan avec effets de scintillement.
'''

import pygame
import random
from typing import Tuple


class Star:
    """Représente une étoile d'arrière-plan avec effet de scintillement."""
    
    def __init__(self, width: int, height: int):
        """Initialise une étoile avec une position et des caractéristiques aléatoires."""
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.size = random.uniform(0.5, 2.5)
        self.brightness = random.uniform(0.3, 1.0)
        
        # Taux de scintillement (vitesse et intensité du changement de luminosité)
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_direction = random.choice([-1, 1])
        self.min_brightness = random.uniform(0.1, 0.4)
        self.max_brightness = random.uniform(0.7, 1.0)
        
        # Couleur avec légère teinte aléatoire (blanc-bleu / blanc-rose)
        tint = random.uniform(0, 0.3)  # Intensité de la teinte
        if random.random() < 0.5:  # 50% de chance bleu, 50% rose
            self.color = (
                int(230 * (1 - tint / 3)),  # Légèrement réduit pour le rouge
                int(230 * (1 - tint / 3)),  # Légèrement réduit pour le vert
                min(255, int(230 * (1 + tint)))  # Augmenté pour le bleu
            )
        else:
            self.color = (
                min(255, int(230 * (1 + tint))),  # Augmenté pour le rouge
                int(230 * (1 - tint / 2)),  # Légèrement réduit pour le vert
                int(230 * (1 - tint / 2))   # Légèrement réduit pour le bleu
            )
    
    def update(self):
        """Met à jour la luminosité de l'étoile (effet de scintillement)."""
        # Faire varier la luminosité avec un effet de scintillement
        self.brightness += self.twinkle_speed * self.twinkle_direction
        
        # Inverser la direction si on atteint les limites
        if self.brightness <= self.min_brightness or self.brightness >= self.max_brightness:
            self.twinkle_direction *= -1
            
        # S'assurer que la luminosité reste dans les limites
        self.brightness = max(self.min_brightness, min(self.max_brightness, self.brightness))
    
    def draw(self, surface: pygame.Surface):
        """Dessine l'étoile sur la surface."""
        # Appliquer la luminosité à la couleur
        color = tuple(int(c * self.brightness) for c in self.color)
        
        # Pour les plus grandes étoiles, ajouter un effet de lueur
        if self.size > 1.2:
            # Surface avec canal alpha pour l'effet de halo
            glow_size = int(self.size * 5)
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            
            # Dessiner un cercle avec gradient sur la surface du halo
            glow_radius = glow_size
            glow_center = glow_size, glow_size
            
            # Dessiner plusieurs cercles concentriques avec opacité décroissante
            for i in range(3):
                alpha = int(100 * (1 - i / 3) * self.brightness)
                radius = glow_radius * (1 - i * 0.25)
                glow_color = (*color, alpha)
                pygame.draw.circle(glow_surface, glow_color, glow_center, radius)
            
            # Dessiner le halo sur la surface principale
            surface.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
        
        # Dessiner le point de l'étoile
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.size * self.brightness))) 