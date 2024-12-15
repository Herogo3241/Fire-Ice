import random
import pygame
import math

class Gameover:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = "GAME OVER"
        
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 100)  # Increased font size
        self.menu_font = pygame.font.Font(None, 36)
        self.score_font = pygame.font.Font(None, 54)  # New font for score
        
        # Colors
        self.RED = (255, 50, 50)
        self.BLUE = (50, 50, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Menu options
        self.options = ["Menu", "Restart Game"]
        self.selected_option = 0
        
        # Animation variables
        self.animation_timer = 0
        self.color_shift = 0

        

        
    

    def button(self, text, y_position, selected):
        text_surface = self.menu_font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_position))
        
        if selected:
            # Create a split effect showing both fire and ice themes
            self.draw_selected_button(text, text_rect, y_position)
        else:
            # Unselected buttons get a subtle hover effect
            self.draw_unselected_button(text, text_rect, y_position)

    def draw_selected_button(self, text, text_rect, y_position):
        # Calculate animation values
        pulse = abs(math.sin(self.animation_timer * 0.05))
        wave = math.sin(self.animation_timer * 0.1) * 4
        
        # Create larger surface for the split effect
        button_width = text_rect.width + 60
        button_height = text_rect.height + 20
        button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        
        # Draw split background
        pygame.draw.rect(button_surface, (200, 50, 50, 150), 
                        (0, 0, button_width//2, button_height))
        pygame.draw.rect(button_surface, (50, 50, 200, 150), 
                        (button_width//2, 0, button_width//2, button_height))
        
        # Add gradient overlay
        for i in range(10):
            alpha = int(25 * pulse)
            pygame.draw.line(button_surface, (255, 255, 255, alpha),
                            (button_width//2 - 5 + i, 0),
                            (button_width//2 - 5 + i, button_height))
        
        # Draw border effects
        border_color_left = (255, int(100 + 155 * pulse), 50, 255)
        border_color_right = (50, int(100 + 155 * pulse), 255, 255)
        
        # Left border with fire effect
        for i in range(3):
            pygame.draw.rect(button_surface, border_color_left,
                            (i, i, button_width//2 - i, button_height - i*2), 1)
        
        # Right border with ice effect
        for i in range(3):
            pygame.draw.rect(button_surface, border_color_right,
                            (button_width//2 + i, i, button_width//2 - i, button_height - i*2), 1)
        
        # Draw the text with shadow effect
        text_surface = self.menu_font.render(text, True, self.WHITE)
        text_width = text_surface.get_rect().width
        
        # Add shadow
        shadow_surface = self.menu_font.render(text, True, (0, 0, 0))
        button_surface.blit(shadow_surface, 
                           (button_width//2 - text_width//2 + 2,
                            button_height//2 - text_surface.get_rect().height//2 + 2))
        
        # Draw main text
        button_surface.blit(text_surface, 
                           (button_width//2 - text_width//2,
                            button_height//2 - text_surface.get_rect().height//2))
        

        
        # Draw the final surface
        dest_rect = button_surface.get_rect(center=(self.screen_width//2, y_position))
        self.screen.blit(button_surface, dest_rect)
        
        # Draw side indicators with animation
        self.draw_side_indicators(dest_rect, y_position, wave)


    def draw_side_indicators(self, rect, y_position, wave):
        # Left fire indicator
        fire_points = [
            (rect.left - 20 - wave, y_position),
            (rect.left - 10 - wave, y_position - 8),
            (rect.left - 10 - wave, y_position + 8)
        ]
        pygame.draw.polygon(self.screen, self.RED, fire_points)
        
        # Right ice indicator
        ice_points = [
            (rect.right + 20 + wave, y_position),
            (rect.right + 10 + wave, y_position - 8),
            (rect.right + 10 + wave, y_position + 8)
        ]
        pygame.draw.polygon(self.screen, self.BLUE, ice_points)

    def draw_unselected_button(self, text, text_rect, y_position):
        # Subtle hover effect
        hover = math.sin(self.animation_timer * 0.05) * 0.2 + 0.8
        color = tuple(int(c * hover) for c in self.WHITE)
        
        # Draw text with slight transparency
        text_surface = self.menu_font.render(text, True, color)
        
        # Add subtle glow
        glow_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 20), pygame.SRCALPHA)
        glow_color = (*color[:3], 30)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=10)
        
        # Position and draw
        glow_rect = glow_surf.get_rect(center=(self.screen_width // 2, y_position))
        self.screen.blit(glow_surf, glow_rect)
        self.screen.blit(text_surface, text_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None
    
    def draw(self, score):
        # Update animation timer
        self.animation_timer += 1
        self.color_shift = (self.color_shift + 1) % 360
        
        # Fill background with a subtle gradient
        self.screen.fill(self.BLACK)
        
        # Draw animated background pattern
        for i in range(10):
            y = (self.animation_timer // 2 + i * 60) % self.screen_height
            color_value = abs(math.sin(y * 0.01 + self.animation_timer * 0.01)) * 30
            pygame.draw.line(self.screen, (color_value, color_value, color_value),
                           (0, y), (self.screen_width, y))
        
        # Enhanced Game Over title with fire and ice split effect
        title_parts = list(self.title)
        title_width = 0
        title_surfaces = []

        # Create individual letter surfaces with alternating colors
        for i, letter in enumerate(title_parts):
            color = self.RED if i % 2 == 0 else self.BLUE
            letter_surf = self.title_font.render(letter, True, color)
            title_surfaces.append(letter_surf)
            title_width += letter_surf.get_width()
        
        # Calculate starting x position to center the title
        start_x = (self.screen_width - title_width) // 2
        
        # Draw letters with slight vertical oscillation
        for i, letter_surf in enumerate(title_surfaces):
            # Add a subtle wave effect
            wave_offset = math.sin(self.animation_timer * 0.1 + i * 0.3) * 5
            self.screen.blit(letter_surf, 
                             (start_x, 100 + wave_offset))
            start_x += letter_surf.get_width()
        
        # Add score display
        score_text = f"Score: {score}"
        score_surf = self.score_font.render(score_text, True, self.WHITE)
        score_rect = score_surf.get_rect(center=(self.screen_width // 2, 200))
        
        # Score animation (pulsing effect)
        pulse = abs(math.sin(self.animation_timer * 0.05))
        score_scale = 1 + pulse * 0.1
        scaled_score_surf = pygame.transform.scale(
            score_surf, 
            (int(score_rect.width * score_scale), int(score_rect.height * score_scale))
        )
        scaled_score_rect = scaled_score_surf.get_rect(center=score_rect.center)
        self.screen.blit(scaled_score_surf, scaled_score_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            self.button(option, 300 + i * 70, i == self.selected_option)
        
        # Draw footer text with pulsing effect
        footer_text = "Use ↑↓ to select, Enter to confirm"
        footer_color = abs(math.sin(self.animation_timer * 0.05)) * 55 + 200
        footer_surf = self.menu_font.render(footer_text, True, (footer_color, footer_color, footer_color))
        footer_rect = footer_surf.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(footer_surf, footer_rect)