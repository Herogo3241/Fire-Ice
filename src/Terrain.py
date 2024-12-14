import pygame
import random

class Terrain:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.mode = "fire"
        self.scroll_speed = 300  # pixels per second
        
        # Ground segments for scrolling
        self.segment_width = 100
        self.ground_height = 100
        self.segments = []
        
        # Initialize enough segments to fill screen plus buffer
        segments_needed = (self.width // self.segment_width) + 2
        for i in range(segments_needed):
            self.segments.append({
                'x': i * self.segment_width,
                'height_var': 0  # Slight height variation
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
        self.mode = "ice" if self.mode == "fire" else "fire"
        
    def get_colors(self):
        return self.fire_colors if self.mode == "fire" else self.ice_colors
        
    def update(self, dt):
        # Update segment positions
        scroll_amount = self.scroll_speed * dt
        
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
            
        # Update obstacles
        for obstacle in self.obstacles:
            obstacle['x'] -= scroll_amount
            
        # Remove off-screen obstacles
        self.obstacles = [obs for obs in self.obstacles if obs['x'] > -50]
        
        # Spawn new obstacles
        self.obstacle_spawn_timer += dt
        if self.obstacle_spawn_timer >= self.obstacle_spawn_delay:
            self.obstacle_spawn_timer = 0
            if random.random() < 0.5:  # 50% chance to spawn
                self.obstacles.append({
                    'x': self.width + 50,
                    'y': self.height - self.ground_height - 50,
                    'width': 30,
                    'height': 50,
                    'type': self.mode
                })
                
        # Update particles
        for particle in self.particles:
            particle['x'] -= scroll_amount * 1.2  # Slightly faster than ground
            particle['y'] += particle['vy'] * dt
            particle['life'] -= dt
            
        # Remove dead particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        
        # Add new particles
        if len(self.particles) < 20:
            if self.mode == "fire":
                self.add_fire_particle()
            else:
                self.add_ice_particle()
                
    def add_fire_particle(self):
        self.particles.append({
            'x': random.randint(0, self.width),
            'y': self.height - random.randint(0, self.ground_height),
            'size': random.randint(2, 4),
            'vy': -random.randint(50, 100),
            'life': random.uniform(0.5, 1.5)
        })
        
    def add_ice_particle(self):
        self.particles.append({
            'x': random.randint(0, self.width),
            'y': self.height - random.randint(0, self.ground_height),
            'size': random.randint(3, 6),
            'vy': -random.randint(20, 50),
            'life': random.uniform(0.8, 2.0)
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
            pygame.draw.rect(screen, colors['obstacles'],
                           pygame.Rect(obstacle['x'], obstacle['y'],
                                     obstacle['width'], obstacle['height']))
            
        # Draw particles
        for particle in self.particles:
            if self.mode == "fire":
                pygame.draw.circle(screen, colors['particles'],
                                 (int(particle['x']), int(particle['y'])),
                                 particle['size'])
            else:
                # Draw diamond shape for ice particles
                x, y = int(particle['x']), int(particle['y'])
                size = particle['size']
                points = [
                    (x, y - size),
                    (x + size, y),
                    (x, y + size),
                    (x - size, y)
                ]
                pygame.draw.polygon(screen, colors['particles'], points)