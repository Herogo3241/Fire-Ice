import pygame


class Player():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.width = 30
        self.height = 60
        self.playerSpeed = 300
        self.gravity = 500
        self.mode = "fire"
        self.playerVelocityY = 0
        self.jumping = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Position tracking with sub-pixel precision
        self.exact_y = float(self.y)  # Store exact position as float
        
        # Jump buffer to prevent stuck states
        self.ground_buffer = 1  # 1 pixel buffer for ground detection
        
        # Cooldown system
        self.cooldown_duration = 5000
        self.current_cooldown = 0
        self.can_switch = True
        
        # Color schemes (rest of the color definitions remain the same)
        self.fire_colors = {
            'main': (255, 68, 68),
            'detail': (255, 102, 102),
            'accent': (255, 221, 68),
        }
        self.ice_colors = {
            'main': (68, 68, 255),
            'detail': (102, 102, 255),
            'accent': (68, 221, 255),
        }
        
    def get_colors(self):
        return self.fire_colors if self.mode == "fire" else self.ice_colors
        
    def update_cooldown(self, dt):
        if not self.can_switch:
            self.current_cooldown -= dt * 1000  # Convert dt to milliseconds
            if self.current_cooldown <= 0:
                self.can_switch = True
                self.current_cooldown = 0
        
    def switch_mode(self):
        if self.can_switch:
            self.mode = "ice" if self.mode == "fire" else "fire"
            self.can_switch = False
            self.current_cooldown = self.cooldown_duration
        
    def playerMovement(self, ground, dt):
        
        keys = pygame.key.get_pressed()
        
        # Mode switching with cooldown
        if keys[pygame.K_m]:
            self.switch_mode()
            
        # Update cooldown
        self.update_cooldown(dt)
        
        # Ground check with buffer
        is_on_ground = self.exact_y + self.ground_buffer >= ground
        
        # Jump only if on ground and not already jumping
        if keys[pygame.K_SPACE] and is_on_ground and not self.jumping:
            self.jumping = True
            self.playerVelocityY = -self.playerSpeed
        
        # Apply gravity
        if not is_on_ground:
            # Clamp gravity to prevent excessive speeds
            max_fall_speed = 1000
            self.playerVelocityY = min(self.playerVelocityY + self.gravity * dt, max_fall_speed)
        else:
            # If on ground, stop falling
            if self.playerVelocityY > 0:
                self.playerVelocityY = 0
                self.exact_y = ground
                self.jumping = False
        
        # Update exact position
        self.exact_y += self.playerVelocityY * dt
        
        # Clamp to ground
        if self.exact_y > ground:
            self.exact_y = ground
            self.playerVelocityY = 0
            self.jumping = False
        
        # Update integer position for rendering
        self.y = int(self.exact_y)
        
        self.rect.topleft = (self.x, self.y)
        
    def draw(self, screen):
        colors = self.get_colors()
        
        # Draw body
        pygame.draw.rect(screen, colors['main'], 
                        (self.x + 5, self.y + 10, 20, 40))
        
        # Draw helmet
        pygame.draw.rect(screen, colors['detail'], 
                        (self.x + 5, self.y + 10, 20, 10))
        # Helmet curve
        pygame.draw.arc(screen, colors['detail'],
                       (self.x + 5, self.y + 5, 20, 20),
                       3.14, 0, 3)
        
        # Draw visor
        pygame.draw.rect(screen, colors['accent'],
                        (self.x + 8, self.y + 13, 14, 4))
        
        # Draw chest armor
        points = [(self.x + 5, self.y + 20),
                 (self.x + 25, self.y + 20),
                 (self.x + 23, self.y + 35),
                 (self.x + 7, self.y + 35)]
        pygame.draw.polygon(screen, colors['detail'], points)
        
        # Draw boots
        pygame.draw.rect(screen, colors['detail'],
                        (self.x + 5, self.y + 45, 20, 5))
        
        # Draw energy lines
        pygame.draw.line(screen, colors['accent'],
                        (self.x + 10, self.y + 25),
                        (self.x + 10, self.y + 33), 2)
        pygame.draw.line(screen, colors['accent'],
                        (self.x + 20, self.y + 25),
                        (self.x + 20, self.y + 33), 2)
        
        # Draw cooldown indicator if in cooldown
        if not self.can_switch:
            cooldown_percentage = self.current_cooldown / self.cooldown_duration
            indicator_width = self.width * cooldown_percentage
            pygame.draw.rect(screen, (128, 128, 128),
                           (self.x, self.y - 10, indicator_width, 3))