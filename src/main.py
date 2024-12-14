import pygame
import Terrain
import Player
import random


def Main():
    # Initialize Pygame
    pygame.init()
    terrain = Terrain.Terrain()
    player = Player.Player()

    # Set up the display
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption("Fiery Ice")


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
                running = False
            
            
        if sceneDuration <= 0:
            sceneDuration = random.randint(10000, 30000)
            terrain.toggle_scene();
        
        
        sceneDuration -= dt * 1000
            
        

        # Update game logic
        player.playerMovement(ground, dt)
        
        terrain.update(dt)
        
        
        # Clear the screen
        terrain.display(screen) 
        
        # Draw player
        player.draw(screen)

        # Update the display
        pygame.display.flip()
        
        # Manage time and frame rate
        dt = clock.tick(60) / 1000  

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    Main()
