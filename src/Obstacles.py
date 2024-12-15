import pygame
import random


class Obstacle:
    def __init__(self, x, y, mode, width=40, height=60):
        self.x = x
        self.y = y
        self.mode = mode
        self.width = width + random.randint(-10, 10)
        self.height = height + random.randint(-10, 10)

        # Define colors based on mode
        self.colors = {
            'fire': (255, 69, 0),  # Magma color
            'ice': (173, 216, 230)  # Icicle color
        }

        # Adjust collision rect to match the visual shape
        if mode == 'fire':
            self.rect = pygame.Rect(self.x, self.y + self.height // 2, self.width, self.height // 2)
        elif mode == 'ice':
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, scroll_amount):
        self.x -= scroll_amount
        self.rect.topleft = (self.x, self.rect.y)  # Update rect position based on new x

    def is_visible(self):
        return self.x > -100

    def draw(self, screen):
        if self.mode == 'fire':
            self.draw_magma_rock(screen)
        elif self.mode == 'ice':
            self.draw_icicle(screen)

    def draw_magma_rock(self, screen):
        # Draw magma rock as a jagged polygon
        color = self.colors['fire']
        points = [
            (self.x, self.y + self.height),  # Bottom-left
            (self.x + self.width // 4, self.y + self.height - 10),  # Jagged point 1
            (self.x + self.width // 2, self.y + self.height),  # Bottom-center
            (self.x + 3 * self.width // 4, self.y + self.height - 10),  # Jagged point 2
            (self.x + self.width, self.y + self.height),  # Bottom-right
            (self.x + self.width - 10, self.y + self.height // 2),  # Right-point
            (self.x + 10, self.y + self.height // 2)  # Left-point
        ]
        pygame.draw.polygon(screen, color, points)

    def draw_icicle(self, screen):
        # Draw icicle as a triangle
        color = self.colors['ice']
        points = [
            (self.x + self.width // 2, self.y),  # Tip of the icicle
            (self.x, self.y + self.height),  # Bottom-left
            (self.x + self.width, self.y + self.height)  # Bottom-right
        ]
        pygame.draw.polygon(screen, color, points)
