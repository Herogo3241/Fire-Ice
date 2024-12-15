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
        self.score = 0;
        self.font = pygame.font.Font(None, 36)
        
    def run(self):
        
        

        if self.sceneDuration <= 0:
            self.sceneDuration = random.randint(10000, 30000)
            self.terrain.toggle_scene()

        self.sceneDuration -= self.dt * 1000
        
        if not self.terrain.transitioning:
            if self.player.mode != self.terrain.mode:
                return True, self.score // 100
                
        for obstacle in self.terrain.obstacles:
            if self.player.rect.colliderect(obstacle.rect): 
                return True, self.score // 100
        self.score += int(self.dt * 1000) 
        
        
        

        # Update game logic
        self.player.playerMovement(self.ground, self.dt)
        self.terrain.update(self.dt)


        self.terrain.display(self.screen)
        self.player.draw(self.screen)
        
        
        score_text = self.font.render(f"{self.score // 100}", True, (255, 255, 255))
    
   
        self.screen.blit(score_text, (10, 10))
        
         # Manage time and frame rate
        self.dt = self.clock.tick(60) / 1000  # Delta time in seconds
        
        
        return False, self.score // 100
    
        
    