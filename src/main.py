import asyncio
import pygame
import random

from Terrain import Terrain
from Player import Player

# Initialize Pygame
pygame.init()

screen_width = 800
screen_height = 600  
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fiery Ice")

# Initialize game components
terrain = Terrain(screen_width, screen_height)
player = Player()

async def main():
    

    # Game loop variables
    running = True
    clock = pygame.time.Clock()
    dt = 0
    ground = 3 * screen.get_height() // 4
    sceneDuration = random.randint(10000, 30000)

    # Main game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop

        # Update scene duration and toggle scene if necessary
        if sceneDuration <= 0:
            sceneDuration = random.randint(10000, 30000)
            terrain.toggle_scene()

        sceneDuration -= dt * 1000
        
        if not terrain.transitioning:
            if player.mode != terrain.mode:
                print("Game Over")
                
        for obstacle in terrain.obstacles:
            if player.rect.colliderect(obstacle.rect):  # Check for overlap
                print("Obstacle hit! ", obstacle.mode)


        # Update game logic
        player.playerMovement(ground, dt)
        terrain.update(dt)

        # Clear the screen and render terrain and player
        terrain.display(screen)
        player.draw(screen)

        # Update the display
        pygame.display.flip()

        # Manage time and frame rate
        dt = clock.tick(60) / 1000  # Delta time in seconds

        # Allow the browser to handle other tasks
        await asyncio.sleep(0)

    # Clean up
    pygame.quit()


# Run the game using asyncio
asyncio.run(main())
