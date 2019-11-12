"""
Getaway! The driving, wall avoiding game
Author: Danny Mulick

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
import random

# --- Global constants ---
from constants import *


# --- Classes ---
class WallGroup(pygame.sprite.Group):
    WALL_STYLES_EASY = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ]

    def __init__(self, y_group_in, *sprites):
        super().__init__(*sprites)
        sel = random.randint(0, 5)
        self.style = WallGroup.WALL_STYLES_EASY[sel]
        self.collided = False
        self.score_checked = False
        for i in range(len(self.style)):
            if self.style[i] == 1:
                item = Wall(i, y_group_in)
                self.add(item)

    def update(self):
        super().update()


class Wall(pygame.sprite.Sprite):
    """ This class represents a wall made to oppose our player. """
    WIDTH = 60
    HEIGHT = 20
    EASY_SPEED = 2
    EASY_SPACER = 130
    RESET_Y = -100

    def __init__(self, x_in, y_in):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([Wall.WIDTH, Wall.HEIGHT])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = Player.x_pos_list[x_in] - Wall.WIDTH / 2
        self.rect.y = y_in
        self.checked = False

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        # self.rect.y = Wall.RESET_Y
        # self.rect.x = Player.x_pos_list[random.randint(0, 2)] - Wall.WIDTH / 2
        self.checked = False

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += Wall.EASY_SPEED

        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()


class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    X_CHANGE = 100
    x_pos_list = [(SCREEN_WIDTH / 2) - X_CHANGE, SCREEN_WIDTH / 2, (SCREEN_WIDTH / 2) + X_CHANGE]

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/car_red.png"), (25, 50))
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - (2 * self.rect.height)
        self.lives = 3
        self.x_pos = 1

    def update(self):
        """ Update the player location. """
        self.rect.x = Player.x_pos_list[self.x_pos] - self.image.get_rect().size[0] / 2

    def move_left(self):
        if self.x_pos > 0:
            self.x_pos -= 1
        else:
            pass
            # Suggestion: Implement minor shake or play a sound to denote you can't go left

    def move_right(self):
        if self.x_pos < 2:
            self.x_pos += 1
        else:
            pass
            # Suggestion: Implement minor shake or play a sound to denote you can't go right


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
    SCORE_LIMIT_EASY = 15
    INSTRUCTIONS = ["You are an agent on the run, and today is your escape.",
                    "Drive away to safety while avoiding the barriers set up to stop you.",
                    "Use your arrow keys or A and D to avoid the walls.",
                    "Press space to continue..."]
    WIN_TEXT = ["You have escaped your pursuers and lived another day",
                "Tune in next time to continue your..."
                "Getaway!"]
    LOSE_TEXT = ["You have been captured!",
                 "Try again another day to make your...",
                 "Getaway!"]

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False
        self.game_won = False
        self.done = False
        self.splash = True

        # Create sprite lists
        self.wall_list = []
        self.all_sprites_list = pygame.sprite.Group()

        # Create the block sprites
        for i in range(10):
            wall_group = WallGroup(-Wall.EASY_SPACER * i)
            self.wall_list.append(wall_group)

        # Create the player
        self.player = Player()
        self.lives = self.player.lives
        self.all_sprites_list.add(self.player)

        pygame.mixer.music.load("audio/Caffeine & Chaos Forever.mp3")

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        if not pygame.mixer.music.get_busy() and not self.game_over and not self.game_won:
            pygame.mixer.music.play(-1, 0.0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move_right()
                if event.key == pygame.K_SPACE:
                    if self.game_over or self.game_won:
                        self.__init__()

        return False

    def handle_splash(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
        return True

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over and not self.game_won:
            # Move all the sprites
            self.all_sprites_list.update()
            for wall_group in self.wall_list:
                wall_group.update()

                for wall in wall_group.sprites():
                    if wall is not None:
                        # This spawns an error, need to work on fixing
                        if wall.rect.y > self.player.rect.y + self.player.rect.height:
                            if not wall_group.score_checked:
                                self.score += 1
                                wall_group.score_checked = True

                    if wall.rect.y > SCREEN_HEIGHT:
                        self.handle_wall_reset(wall_group)
                    break

                # See if the player block has collided with anything.
                wall_hit_list = pygame.sprite.spritecollide(self.player, wall_group, True)

                # Check the list of collisions.
                for _ in wall_hit_list:
                    self.lives -= 1

            if self.lives < 1:
                self.game_over = True
                pygame.mixer.music.fadeout(200)

            if self.score > Game.SCORE_LIMIT_EASY:
                self.game_won = True
                pygame.mixer.music.fadeout(200)

    def display_splash(self, screen):
        """ Display everything to the screen for splash of the game
            Title
            My name
            Background for the game
            Means to transition
        """
        screen.fill(BLACK)

        title_font = pygame.font.SysFont("helvetica", 50)
        font = pygame.font.SysFont("helvetica", 20)

        title_text = title_font.render("Getaway!", True, WHITE)
        center_x = (SCREEN_WIDTH // 2) - (title_text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 2) - (title_text.get_height() // 2)
        screen.blit(title_text, [center_x - 40, center_y - 50])

        name_text = font.render("Danny Mulick", True, WHITE)
        screen.blit(name_text, [center_x, center_y])
        for i in range(len(Game.INSTRUCTIONS)):
            instruction_text = font.render(Game.INSTRUCTIONS[i], True, WHITE)
            screen.blit(instruction_text, [60, center_y + 50 + (20*i)])

        # Draw a red car, chased by some yellow cars, heading towards some walls

        pygame.display.flip()

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(SAND)

        if self.game_over:
            font = pygame.font.SysFont("helvetica", 25)
            text = font.render("Game Over, press space to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
            for i in range(len(Game.LOSE_TEXT)):
                game_over_text = font.render(Game.LOSE_TEXT[i], True, BLACK)
                screen.blit(game_over_text, [60, center_y + 50 + (20 * i)])

        if self.game_won:
            font = pygame.font.SysFont("helvetica", 25)
            text = font.render("You won! Press space to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
            for i in range(len(Game.WIN_TEXT)):
                game_won_text = font.render(Game.WIN_TEXT[i], True, BLACK)
                screen.blit(game_won_text, [60, center_y + 50 + (20 * i)])

        if not self.game_over and not self.game_won:
            # Create background
            self.create_background(screen)
            self.all_sprites_list.draw(screen)
            for wall_group in self.wall_list:
                wall_group.draw(screen)
            self.display_feedback(screen)
        pygame.display.flip()

    def display_feedback(self, screen_in):
        """ Display feedback about the current game session, score and remaining lives"""
        pygame.draw.rect(screen_in, BLUE, [FEEDBACK_X, FEEDBACK_Y, 120, 80], 0)
        score_str = "Score: " + str(self.score)
        font = pygame.font.SysFont("helvetica", 25)
        score_text = font.render(score_str, True, WHITE)
        score_x = FEEDBACK_X + 5
        score_y = FEEDBACK_Y + 5
        screen_in.blit(score_text, [score_x, score_y])
        lives_str = "Lives: " + str(self.lives)
        lives_text = font.render(lives_str, True, WHITE)
        lives_x = score_x
        lives_y = score_y + 25
        screen_in.blit(lives_text, [lives_x, lives_y])

    def handle_wall_reset(self, wall_group_first):
        wall_group_last_y = self.wall_list[-1].sprites()[0].rect.y
        # for wall_sprite in wall_group_first.sprites():
        wall_sprite = wall_group_first.sprites()[0]
        # Basically remove the 0th element, but add it to the end using the y from the last one
        self.wall_list.pop(0)
        new_wall_group = WallGroup(wall_group_last_y - Wall.EASY_SPACER)
        self.wall_list.append(new_wall_group)

    def create_background(self, screen_in):
        # self.all_sprites_list.add()
        pygame.draw.rect(screen_in, BLACK, [Player.x_pos_list[0] - Wall.WIDTH, 0,
                                            Player.x_pos_list[-1] - Player.x_pos_list[0] + Wall.WIDTH * 2,
                                            SCREEN_HEIGHT], 0)
        road_line1_x = (Player.x_pos_list[0] + Player.x_pos_list[1]) / 2 - 2
        pygame.draw.rect(screen_in, WHITE, [road_line1_x, 0, 5, SCREEN_HEIGHT], 0)
        road_line2_x = (Player.x_pos_list[1] + Player.x_pos_list[2]) / 2 - 2
        pygame.draw.rect(screen_in, WHITE, [road_line2_x, 0, 5, SCREEN_HEIGHT], 0)


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
    game = Game()

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
