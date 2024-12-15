import pygame
import random
from Player import Player
from Terrain import Terrain

class Game():
    
    def __init__(self, screen_width, screen_height, screen):
        self.player = Player();
        self.terrain = Terrain(screen_width, screen_height)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.ground = 3 * screen.get_height() // 4
        self.screen = screen
        self.sceneDuration = random.randint(10000, 30000)
        
    def run(self):
                # Update scene duration and toggle scene if necessary
        if self.sceneDuration <= 0:
            self.sceneDuration = random.randint(10000, 30000)
            self.terrain.toggle_scene()

        self.sceneDuration -= self.dt * 1000
        
        if not self.terrain.transitioning:
            if self.player.mode != self.terrain.mode:
                return True
                
        for obstacle in self.terrain.obstacles:
            if self.player.rect.colliderect(obstacle.rect):  # Check for overlap
                return True


        # Update game logic
        self.player.playerMovement(self.ground, self.dt)
        self.terrain.update(self.dt)

        # Clear the screen and render terrain and player
        self.terrain.display(self.screen)
        self.player.draw(self.screen)
        
         # Manage time and frame rate
        self.dt = self.clock.tick(60) / 1000  # Delta time in seconds
        
        
        return False
    
        
    