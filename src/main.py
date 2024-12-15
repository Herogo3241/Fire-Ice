import asyncio
import pygame
import time
from Game import Game
from Menu import Menu
from Instructions import Instructions
from Gameover import Gameover

# Initialize Pygame
pygame.init()

screen_width = 800
screen_height = 600  
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fiery Ice")

# Game states
MENU = "MENU"
PLAYING = "PLAYING"
INSTRUCTIONS = "INSTRUCTIONS"
GAMEOVER = "GAMEOVER"

# Initialize screens
menu = Menu(screen, screen_width, screen_height)
game = Game(screen_width, screen_height, screen)
instructions = Instructions(screen, screen_width, screen_height)
gameover = Gameover(screen, screen_width, screen_height)

# Initialize clock for controlling frame rate
clock = pygame.time.Clock()

async def main():
    running = True
    current_state = MENU
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if current_state == MENU:
                selected_option = menu.handle_input(event) 
                if selected_option:
                    if selected_option == "Start Game":
                        game = Game(screen_width, screen_height, screen)
                        current_state = PLAYING
                    elif selected_option == "How to Play":
                        current_state = INSTRUCTIONS
                    elif selected_option == "Quit":
                        running = False
                    
            elif current_state == INSTRUCTIONS:
                instructions.draw()
                if instructions.handle_input(event):
                    current_state = MENU 
                    
            elif current_state == GAMEOVER:
                gameover.draw(score)
                selected_option = gameover.handle_input(event)
                if selected_option:
                    if selected_option == "Restart Game":
                        game = Game(screen_width, screen_height, screen)
                        current_state = PLAYING
                    elif selected_option == "Menu":
                        current_state = MENU
                    elif selected_option == "Quit":
                        running = False
                      
        
        # Update and render based on current state
        if current_state == MENU:
            menu.draw()
            
        elif current_state == PLAYING:
            game_over, score = game.run()
            if game_over:
                current_state = GAMEOVER
                

         
            
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(60)
        
        # Required for Pygbag to work properly
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())