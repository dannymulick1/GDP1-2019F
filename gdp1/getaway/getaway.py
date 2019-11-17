"""
Getaway! The driving, wall avoiding game
Author: Danny Mulick
Sources:
    - Images: Obtained from online services and will fill this in later
    - Audio:
      Caffeine and Chaos Forever: Kaminakat https://www.newgrounds.com/audio/listen/859250

b. Version - 0.2.1
c. What the code does
 - Splash screen appears and will click to pass
 - This game runs the first level (Easy) of the game so far. It spawns the player, the obstacles, and moves them down
    the screen.
 - Get 15 points to win, or lose all lives to lose
d. A brief description of how to play the game
 - You play the game using either WASD or the arrow keys, moving left or right in order to avoid oncoming walls.
 - Score 15 points in order to win this level, or lose all three lives to lose it.
e. What’s not working and known bugs and limitations at this stage

f. What’s left at this stage, not what you might or might not do, etc. but what you plan to do
  - Implement other difficulty levels
  - Add sound design for music and sounds for point scoring
  - Add more detail to game over and
"""

import pygame

# --- Global constants ---
from constants import *


# --- Classes ---
from game import Game


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
    pygame.mixer.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Getaway")

    # Create our objects and set the data
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game(0)

    # Make and display splash screen
    while game.splash:
        game.splash = game.handle_splash()
        game.display_splash(screen)

    # Main game loop
    while not game.done:
        # Process events (keystrokes, mouse clicks, etc)
        game.done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
