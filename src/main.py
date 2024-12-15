import asyncio
import pygame
import random

from Game import Game

# Initialize Pygame
pygame.init()

screen_width = 800
screen_height = 600  
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fiery Ice")

#initializing Game
game = Game(screen_width, screen_height, screen)

async def main():
    

    # Game loop variables
    running = True
    

    # Main game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop


        #running Game
        isOver = game.run()
        print(isOver)
        
        
        
        # Update the display
        pygame.display.flip()

       

        # Allow the browser to handle other tasks
        await asyncio.sleep(0)

    # Clean up
    pygame.quit()


# Run the game using asyncio
asyncio.run(main())
