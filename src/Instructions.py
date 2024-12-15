import math
import pygame

class Instructions:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        
        # Colors
        self.RED = (255, 50, 50)
        self.BLUE = (50, 50, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Back button properties
        self.back_button = pygame.Rect(50, self.screen_height - 70, 100, 40)
        self.button_hover = False
        
    
        
        # Animation variables
        self.animation_timer = 0
        
    def draw_ascii_art(self, art, x, y, color):
        lines = art.strip().split('\n')
        for i, line in enumerate(lines):
            text = self.text_font.render(line, True, color)
            self.screen.blit(text, (x, y + i * 30))
            
    def draw_button(self):
        color = (180, 180, 180) if self.button_hover else (120, 120, 120)
        pygame.draw.rect(self.screen, color, self.back_button, border_radius=5)
        text = self.text_font.render("Back", True, self.BLACK)
        text_rect = text.get_rect(center=self.back_button.center)
        self.screen.blit(text, text_rect)
        
    def handle_input(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.button_hover = self.back_button.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_hover:
                return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
        return False
        
    def draw(self):
        self.screen.fill(self.BLACK)
        self.animation_timer += 1
        
        # Draw title
        title = self.title_font.render("How to Play", True, self.WHITE)
        title_rect = title.get_rect(centerx=self.screen_width//2, y=30)
        self.screen.blit(title, title_rect)
        
        # Draw instruction sections with ASCII art
        y_pos = 100
        spacing = 40
        
        # Mode switching instruction
        text = self.text_font.render("Press 'M' to switch between modes", True, self.WHITE)
        self.screen.blit(text, (50, y_pos))
        
        # Show both player modes with animation
        
        
        
        # Terrain matching instruction
        y_pos += spacing 
        text = self.text_font.render("Match your mode to the terrain", True, self.WHITE)
        
        # Jumping instruction
        y_pos += spacing
        text = self.text_font.render("Press SPACE to jump over obstacles", True, self.WHITE)
        self.screen.blit(text, (50, y_pos))
        
 
        
        # Tips section
        y_pos += spacing + 20
        tips = [
            "• Switch modes before terrain changes",
            "• Time your jumps carefully",
            "• Watch for mode cooldown period"
        ]
        
        for tip in tips:
            text = self.text_font.render(tip, True, self.WHITE)
            self.screen.blit(text, (50, y_pos))
            y_pos += 35
            
        # Draw back button
        self.draw_button()