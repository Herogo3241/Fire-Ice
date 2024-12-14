import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Fiery Ice")

LAVA = (244, 114, 9)
ICE = (185,232,234)
BLACK = (0, 0, 0)

# Game loop variables
running = True
clock = pygame.time.Clock()
dt = 0
playerX = 100
playerY = 400
playerSpeed = 300  # Jump speed (pixels per second)
gravity = 500      # Gravity strength
ground = 3 * screen.get_height() // 4
playerVelocityY = 0  # Vertical velocity
jumping = False
Color = [LAVA, BLACK, ICE]

# Player movement function
def PlayerMovement(playerY, playerVelocityY, jumping):
    keys = pygame.key.get_pressed()

    # Jumping logic (only when the player is on the ground)
    if keys[pygame.K_SPACE] and playerY >= ground and not jumping:
        jumping = True
        playerVelocityY = -playerSpeed  # Set initial jump velocity

    # Apply gravity when the player is in the air
    if playerY < ground:
        playerVelocityY += gravity * dt  # Gravity affects the velocity
    else:
        playerY = ground  # Stop at ground level
        if playerVelocityY > 0:  # If the player has hit the ground
            jumping = False  # Stop jumping
    
    playerY += playerVelocityY * dt  # Update player position based on velocity

    return playerY, playerVelocityY, jumping


color = 0
# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            color = (color + 1) % 3

    # Update game logic
    playerY, playerVelocityY, jumping = PlayerMovement(playerY, playerVelocityY, jumping)
    
    
    # Clear the screen
    screen.fill(Color[color])  
    
    # if(playerY < ground):
    #     screen.fill(ICE)
    # Draw the player
    pygame.draw.rect(screen, (255, 0, 0), (playerX, playerY, 30, 60))  # Red rectangle

    # Update the display
    pygame.display.flip()
    
    # Manage time and frame rate
    dt = clock.tick(60) / 1000  # Delta time in seconds

# Quit Pygame
pygame.quit()
