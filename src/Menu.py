import random
import pygame
import math

class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = "Fire and Ice"
        
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 74)
        self.menu_font = pygame.font.Font(None, 36)
        
        # Colors
        self.RED = (255, 50, 50)
        self.BLUE = (50, 50, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Menu options
        self.options = ["Start Game", "How to Play"]
        self.selected_option = 0
        
        # Animation variables
        self.animation_timer = 0
        self.color_shift = 0
        
        # Particle systems
        self.particles = []
        self.spawn_particle_timer = 0
        
    def create_particle(self, x, y, is_fire=True):
        base_speed = random.random() * 2 + 1
        angle = random.uniform(-math.pi/3, math.pi/3)  # Constrain initial angle
        return {
            'x': x + random.uniform(-5, 5),  # Add slight horizontal variation in spawn
            'y': y + random.uniform(-2, 2),
            'dx': math.cos(angle) * base_speed,
            'dy': -math.sin(angle) * base_speed,
            'lifetime': random.randint(45, 75),  # Varying lifetimes
            'max_lifetime': 75,  # Store initial max lifetime for color calculations
            'is_fire': is_fire,
            'size': random.uniform(2, 6),
            'alpha': 255,  # Add alpha for fade out
            'wobble': random.uniform(-0.1, 0.1),  # Add wobble effect
            'temperature': random.uniform(0.8, 1.2)  # Varies particle heat/cold intensity
        }

    def update_particles(self):
        # Spawn new particles
        self.spawn_particle_timer += 1
        if self.spawn_particle_timer >= 3:  # Increased spawn rate
            self.spawn_particle_timer = 0
            for _ in range(2):  # Spawn multiple particles per cycle
                # Fire particles
                self.particles.append(self.create_particle(self.screen_width // 2 - 50, 130, True))
                # Ice particles
                self.particles.append(self.create_particle(self.screen_width // 2 + 50, 130, False))
        
        # Update existing particles
        for particle in self.particles[:]:
            # Add wobble to horizontal movement
            particle['dx'] += math.sin(self.animation_timer * 0.1) * particle['wobble']
            
            # Update position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Different behavior for fire and ice
            if particle['is_fire']:
                # Fire rises and spreads
                particle['dy'] -= 0.05 * particle['temperature']  # Accelerate upward
                particle['dx'] *= 0.98  # Slight horizontal dampening
                # Add flicker effect
                particle['size'] *= random.uniform(0.95, 1.05)
            else:
                # Ice falls and crystallizes
                particle['dy'] += 0.01  # Slight downward acceleration
                particle['dx'] *= 0.95  # More horizontal dampening
                particle['size'] *= 0.98  # Gradually shrink
            
            # Update lifetime and alpha
            particle['lifetime'] -= 1
            particle['alpha'] = (particle['lifetime'] / particle['max_lifetime']) * 255
            
            # Remove dead particles
            if particle['lifetime'] <= 0 or particle['alpha'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self):
        for particle in self.particles:
            # Calculate base color based on temperature and lifetime
            life_ratio = particle['lifetime'] / particle['max_lifetime']
            
            if particle['is_fire']:
                # Fire color transition from white to yellow to red
                red = 255
                green = max(0, min(255, 220 * life_ratio * particle['temperature']))
                blue = max(0, min(255, 150 * (life_ratio ** 2) * particle['temperature']))
                color = (red, green, blue)
            else:
                # Ice color transition from white to light blue to deep blue
                blue = 255
                green = max(0, min(255, 220 * life_ratio + 35))
                red = max(0, min(255, 180 * life_ratio))
                color = (red, green, blue)
            
            # Calculate alpha-adjusted color
            color = tuple(min(255, max(0, int(c * (particle['alpha'] / 255)))) for c in color)
            
            # Draw main particle
            size = max(1, particle['size'] * (particle['lifetime'] / particle['max_lifetime']))
            pygame.draw.circle(self.screen, color, 
                            (int(particle['x']), int(particle['y'])), 
                            int(size))
            
            # Draw glow effect
            glow_size = size * 1.5
            glow_surface = pygame.Surface((int(glow_size * 2 + 2), int(glow_size * 2 + 2)), pygame.SRCALPHA)
            glow_color = tuple(list(color[:3]) + [int(particle['alpha'] * 0.3)])  # Semi-transparent glow
            pygame.draw.circle(glow_surface, glow_color,
                            (int(glow_size + 1), int(glow_size + 1)),
                            int(glow_size))
            self.screen.blit(glow_surface, 
                            (int(particle['x'] - glow_size), int(particle['y'] - glow_size)),
                            special_flags=pygame.BLEND_ALPHA_SDL2)

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
    
    def draw(self):
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
        
        # Update and draw particles
        self.update_particles()
        self.draw_particles()
        
        # Draw title with enhanced fire and ice effect
        title_surf = self.title_font.render(self.title, True, self.WHITE)
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, 100))
        
        # Create split effect for title with glow
        fire_surf = self.title_font.render("Fire", True, self.RED)
        ice_surf = self.title_font.render("Ice", True, self.BLUE)
        fire_rect = fire_surf.get_rect(midright=(self.screen_width // 2 - 10, 100))
        ice_rect = ice_surf.get_rect(midleft=(self.screen_width // 2 + 10, 100))
        
        # Draw glowing divider
        glow_intensity = abs(math.sin(self.animation_timer * 0.05)) * 3
        for i in range(3):
            pygame.draw.line(self.screen, 
                           (100 + i*50, 100 + i*50, 100 + i*50),
                           (self.screen_width // 2, 70 - i*glow_intensity),
                           (self.screen_width // 2, 130 + i*glow_intensity),
                           2)
        
        # Draw title elements with subtle hovering effect
        hover_offset = math.sin(self.animation_timer * 0.05) * 3
        self.screen.blit(fire_surf, (fire_rect.x, fire_rect.y + hover_offset))
        self.screen.blit(ice_surf, (ice_rect.x, ice_rect.y - hover_offset))
        
        # Draw menu options
        for i, option in enumerate(self.options):
            self.button(option, 250 + i * 70, i == self.selected_option)
        
        # Draw footer text with pulsing effect
        footer_text = "Use ↑↓ to select, Enter to confirm"
        footer_color = abs(math.sin(self.animation_timer * 0.05)) * 55 + 200
        footer_surf = self.menu_font.render(footer_text, True, (footer_color, footer_color, footer_color))
        footer_rect = footer_surf.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(footer_surf, footer_rect)