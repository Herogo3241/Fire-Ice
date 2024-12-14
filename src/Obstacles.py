import pygame
import random


class Obstacle:
    def __init__(self, x, y, mode, width=30, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mode = mode

        # Define colors based on mode
        self.colors = {
            'fire': (255, 100, 0),
            'ice': (200, 240, 255)
        }
        
    def update(self, scroll_amount):
        self.x -= scroll_amount
        
    def is_visible(self):
        return self.x > -100
        
    def draw(self, screen):
        color = self.colors[self.mode]
        pygame.draw.rect(screen, color,
                        self.get_rect())
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)