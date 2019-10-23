# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

x_fig = 10
y_fig = 10
X_SPEED = 10
Y_SPEED = 3


def draw_stick_figure(screen, x, y):
    # Head
    pygame.draw.ellipse(screen, WHITE, [1 + x, y, 10, 10], 0)

    # Legs
    pygame.draw.line(screen, WHITE, [5 + x, 17 + y], [10 + x, 27 + y], 2)
    pygame.draw.line(screen, WHITE, [5 + x, 17 + y], [x, 27 + y], 2)

    # Body
    pygame.draw.line(screen, GREEN, [5 + x, 17 + y], [5 + x, 7 + y], 2)

    # Arms
    pygame.draw.line(screen, BLUE, [5 + x, 7 + y], [9 + x, 17 + y], 2)
    pygame.draw.line(screen, BLUE, [5 + x, 7 + y], [1 + x, 17 + y], 2)


# Setup
pygame.init()

# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Danny's Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(1)

# Select the font to use, size, bold, italics
font = pygame.font.SysFont('Calibri', 25, True, False)

# Render the text. "True" means anti-aliased text.
# Black is the color. This creates an image of the
# letters, but does not put it on the screen
text = font.render("You're IT!", True, WHITE)

# -------- Main Program Loop -----------
while not done:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

    # Call draw stick figure function
    pos = pygame.mouse.get_pos()
    x_mouse = pos[0]
    y_mouse = pos[1]

    sx = x_mouse - x_fig
    sy = y_mouse - y_fig

    theta = math.atan2(sx, sy)

    dx = X_SPEED * math.sin(theta)
    dy = Y_SPEED * math.cos(theta)

    # If fig is within dx or dy units from the mouse, set it to mouse coords to stop stuttering
    if abs(x_fig - x_mouse) < dx:
        x_fig = x_mouse
    else:
        x_fig += dx
    if abs(y_fig - y_mouse) < dy:
        y_fig = y_mouse
    else:
        y_fig += dy

    # Fill the screen to create background, then draw stick figure on the screen
    screen.fill(BLACK)
    draw_stick_figure(screen, x_fig, y_fig)

    if (x_fig == x_mouse) and (y_fig == y_mouse):
        # Put the image of the text on the screen up and to the right of the stick figure
        screen.blit(text, [x_fig + 10, y_fig - 25])

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
