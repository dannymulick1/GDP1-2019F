"""
 Template used from: progamarcadegames.com/python_examples
 Author: Mulick, Danny
"""

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Danny's Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # --- Game logic should go here

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    # Add code for drawing house here
    # Chimney of house
    pygame.draw.rect(screen, BLACK, [120, 150, 20, 30], 0)
    # Roof of house
    pygame.draw.polygon(screen, BLACK, [[100, 200], [300, 200], [200, 100]], 5)
    pygame.draw.polygon(screen, WHITE, [[100, 200], [300, 200], [200, 100]], 0)
    # Body of house
    pygame.draw.rect(screen, RED, [100, 200, 200, 200], 0)
    # For loop for windows
    for i in range(4):
        pygame.draw.rect(screen, GREEN, [120 + (50 * i), 250, 10, 30], 0)
    # Draw dat door
    pygame.draw.rect(screen, BLUE, [190, 350, 20, 50], 0)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

