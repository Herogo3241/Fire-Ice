import math
import pygame
import random
import Obstacles

class Terrain:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.mode = "fire"
        self.scroll_speed = 300  # pixels per second
        
        self.totalPixelTraversed = 0;
        self.speed_scaling = 1.1;

        
        # Transition variables
        self.transitioning = False
        self.transition_progress = 0
        self.transition_speed = 2.0  # Speed of transition (seconds)
        self.transition_from_mode = None
        
        # Ground segments for scrolling
        self.segment_width = 100
        self.ground_height = 100
        self.segments = []
        
        # Initialize enough segments to fill screen plus buffer
        segments_needed = (self.width // self.segment_width) + 2
        for i in range(segments_needed):
            self.segments.append({
                'x': i * self.segment_width,
                'height_var': 0  
            })
            
        # Clouds for parallax effect
        self.clouds = []
        self.cloud_parallax_factor = 0.7  # Clouds move slower than ground
        self.init_clouds()
            
        # Obstacles
        self.obstacles = []
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_delay = 2  # seconds
        
        # Colors for different modes
        self.fire_colors = {
            'background': (40, 0, 0),
            'ground': (70, 20, 0),
            'obstacles': (255, 100, 0),
            'particles': (255, 150, 0),
            'clouds': (100, 30, 30)
        }
        
        self.ice_colors = {
            'background': (0, 20, 40),
            'ground': (100, 150, 255),
            'obstacles': (200, 240, 255),
            'particles': (220, 240, 255),
            'clouds': (150, 180, 200)
        }
        
        # Particles for visual effect
        self.particles = []
    def speedScaling(self):
        pass
            
    def init_clouds(self):
        # Create initial set of clouds
        clouds_needed = 5  # Number of clouds to maintain
        for _ in range(clouds_needed):
            self.add_new_cloud(random.randint(0, self.width))

    def add_new_cloud(self, x_pos=None):
        if x_pos is None:
            x_pos = self.width + 100
            
        # Create a cloud with multiple segments for more natural look
        segments = []
        base_y = random.randint(50, self.height // 3)  # Keep clouds in upper third
        base_width = random.randint(60, 120)
        base_height = random.randint(30, 50)
        
        # Add 2-4 segments per cloud for varied shapes
        num_segments = random.randint(2, 4)
        for i in range(num_segments):
            segment = {
                'x': x_pos + (i * base_width // 2),
                'y': base_y + random.randint(-10, 10),
                'width': base_width + random.randint(-20, 20),
                'height': base_height + random.randint(-10, 10)
            }
            segments.append(segment)
            
        self.clouds.append({
            'segments': segments,
            'speed_variation': random.uniform(0.8, 1.2)  # Slight speed variation between clouds
        })
        
    def toggle_scene(self):
        
        if not self.transitioning:
            self.transitioning = True
            self.transition_progress = 0
            self.transition_from_mode = self.mode

            self.mode = "ice" if self.mode == "fire" else "fire"
            
    def interpolate_color(self, color1, color2, t):
        """Smoothly interpolate between two colors."""
        return tuple(
            int(color1[i] + (color2[i] - color1[i]) * t)
            for i in range(3)
        )
    
    def get_colors(self):
        # During transition, blend colors
        if self.transitioning:
            from_colors = self.fire_colors if self.transition_from_mode == "fire" else self.ice_colors
            to_colors = self.ice_colors if self.transition_from_mode == "fire" else self.fire_colors
            
            # Interpolate each color component
            blended_colors = {}
            for key in from_colors.keys():
                blended_colors[key] = self.interpolate_color(
                    from_colors[key], 
                    to_colors[key], 
                    self.transition_progress
                )
            return blended_colors
        
        # Normal mode selection
        return self.fire_colors if self.mode == "fire" else self.ice_colors
    
    def spawn_obstacle(self):
        new_obstacle = Obstacles.Obstacle(
            x=self.width + 50,
            y=self.height - self.ground_height - 50,
            mode=self.mode
        )
        self.obstacles.append(new_obstacle)
        
   
        
    def update(self, dt):
        # Handle scene transition
        if self.transitioning:
            self.particles.clear()
            self.transition_progress += dt / self.transition_speed
            if self.transition_progress >= 1:
                self.transitioning = False
                self.transition_progress = 0

        # Rest of the update method remains the same as in the original code
        # Update segment positions
        scroll_amount = self.scroll_speed * dt
        self.totalPixelTraversed += self.scroll_speed
        self.speedScaling()
        
        # Update ground segments
        for segment in self.segments:
            segment['x'] -= scroll_amount
            
        # Remove off-screen segments and add new ones
        while self.segments and self.segments[0]['x'] + self.segment_width < 0:
            self.segments.pop(0)
            new_x = self.segments[-1]['x'] + self.segment_width
            self.segments.append({
                'x': new_x,
                'height_var': 0
            })

        # Update cloud positions with parallax effect
        for cloud in self.clouds:
            parallax_scroll = scroll_amount * self.cloud_parallax_factor * cloud['speed_variation']
            for segment in cloud['segments']:
                segment['x'] -= parallax_scroll

        # Remove off-screen clouds and add new ones
        self.clouds = [cloud for cloud in self.clouds if any(seg['x'] > -150 for seg in cloud['segments'])]
        if len(self.clouds) < 5:  # Maintain minimum number of clouds
            self.add_new_cloud()
            
        # Update and filter obstacles
        for obstacle in self.obstacles:
            obstacle.update(scroll_amount)
        self.obstacles = [obs for obs in self.obstacles if obs.is_visible()]
        
        # Spawn new obstacles
        self.obstacle_spawn_timer += dt
        if self.obstacle_spawn_timer >= self.obstacle_spawn_delay:
            self.obstacle_spawn_timer = 0
            self.obstacle_spawn_timer += dt
            if self.obstacle_spawn_timer >= 0.5:  
                self.obstacle_spawn_timer = 0
            if random.random() < 0.8:  
                self.spawn_obstacle()
                
        # Update particles with snow-specific movement
        for particle in self.particles:
            # Horizontal drift and vertical fall
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            
            # Add wobble effect
            if self.mode == "ice":
                # Calculate wobble using sine wave
                wobble = particle['wobble_amplitude'] * math.sin(
                    particle['wobble_frequency'] * pygame.time.get_ticks() / 1000 + 
                    particle['wobble_offset']
                )
                particle['x'] += wobble * dt
            
            particle['life'] -= dt
            
        # Remove dead particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        
        particleCount = 20 if self.mode == "fire" else 40
        
        # Add new particles with transition consideration
        if len(self.particles) < particleCount:
            spawn_mode = self.mode if not self.transitioning else self.transition_from_mode
            if spawn_mode == "fire":
                self.add_fire_particle()
            else:
                self.add_ice_particle()
                
    def add_fire_particle(self):
        self.particles.append({
            'x': random.randint(0, self.width),
            'y': self.height - random.randint(0, self.ground_height) + self.ground_height,
            'size': random.randint(2, 4),
            'vx': random.randint(-100, 50),
            'vy': -random.randint(50, 100),
            'life': random.uniform(2.5, 3.5),
            'wobble_amplitude': 0,
            'wobble_frequency': 0,
            'wobble_offset': 0
        })
    def add_ice_particle(self):
        # Create more complex snow particles
        x = random.randint(0, self.width)
        y = random.randint(0, self.ground_height) - self.ground_height
        
        # Add variation to snow particle movement
        size = random.randint(2, 5)
        
        # Create more natural snow falling patterns
        drift_speed = random.uniform(-20, 20)  # Horizontal drift
        fall_speed = random.randint(50, 100)  # Vertical fall speed
        
        # Add wobble effect to simulate natural snow movement
        wobble_amplitude = random.uniform(5, 15)
        wobble_frequency = random.uniform(2, 5)
        
        self.particles.append({
            'x': x,
            'y': y,
            'size': size,
            'vx': drift_speed,
            'vy': fall_speed,
            'wobble_amplitude': wobble_amplitude,
            'wobble_frequency': wobble_frequency,
            'wobble_offset': random.uniform(0, math.pi * 2),  # Random starting point in wobble cycle
            'life': random.uniform(3.0, 6.0)  # Longer life for snow
        })
        
    def display(self, screen):
        colors = self.get_colors()
        
        # Draw background
        screen.fill(colors['background'])

        # Draw clouds
        for cloud in self.clouds:
            for segment in cloud['segments']:
                # Draw each cloud segment as a soft rectangle
                cloud_rect = pygame.Rect(
                    segment['x'],
                    segment['y'],
                    segment['width'],
                    segment['height']
                )
                pygame.draw.ellipse(screen, colors['clouds'], cloud_rect)
        
        # Draw ground segments
        for segment in self.segments:
            ground_rect = pygame.Rect(
                segment['x'],
                self.height - self.ground_height + segment['height_var'],
                self.segment_width,
                self.ground_height
            )
            pygame.draw.rect(screen, colors['ground'], ground_rect)
            
            # Add detail lines on ground
            y_pos = self.height - self.ground_height + segment['height_var']
            pygame.draw.line(screen, colors['obstacles'],
                           (segment['x'], y_pos),
                           (segment['x'] + self.segment_width, y_pos), 2)
            
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            
        # Draw particles
        for particle in self.particles:
            if (self.mode == "fire" and not self.transitioning) or \
               (self.transitioning and self.transition_from_mode == "fire"):
                pygame.draw.circle(screen, colors['particles'],
                                 (int(particle['x']), int(particle['y'])),
                                 particle['size'])
            else:
                # Snow particles with more varied rendering
                x, y = int(particle['x']), int(particle['y'])
                size = particle['size']
                
                # Multiple rendering styles for snow
                snow_styles = [
                    # Simple circle
                    lambda: pygame.draw.circle(screen, colors['particles'], (x, y), size),
                    
                    # Fuzzy snowflake-like shape
                    lambda: pygame.draw.circle(screen, colors['particles'], (x, y), size, 1),
                    
                    # Star-like snowflake
                    lambda: pygame.draw.line(screen, colors['particles'], 
                                             (x, y-size), (x, y+size), 1),
                    lambda: pygame.draw.line(screen, colors['particles'], 
                                             (x-size, y), (x+size, y), 1),
                    lambda: pygame.draw.line(screen, colors['particles'], 
                                             (x-size//2, y-size//2), 
                                             (x+size//2, y+size//2), 1),
                    lambda: pygame.draw.line(screen, colors['particles'], 
                                             (x-size//2, y+size//2), 
                                             (x+size//2, y-size//2), 1)
                ]
                
                # Randomly choose a snow rendering style
                snow_styles[hash(particle['x']) % len(snow_styles)]()