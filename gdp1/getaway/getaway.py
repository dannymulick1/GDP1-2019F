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
  - Bug - checking on the wall group height if no wall exists in the first slot fails
f. What’s left at this stage, not what you might or might not do, etc. but what you plan to do
  - Implement other difficulty levels
  - Add sound design for music and sounds for point scoring
  - Add more detail to game over and
"""

import pygame
import random

# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

FEEDBACK_X = 0
FEEDBACK_Y = 430


# --- Classes ---
class WallGroup(pygame.sprite.Group):
    WALL_STYLES = [
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
        self.style = WallGroup.WALL_STYLES[sel]
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
    SPACER = 100
    RESET_Y = -100

    # def __init__(self):
    #     """ Constructor, create the image of the block. """
    #     super().__init__()
    #     self.image = pygame.Surface([Wall.WIDTH, Wall.HEIGHT])
    #     self.image.fill(BLACK)
    #     self.rect = self.image.get_rect()
    #     self.rect.x = Player.x_pos_list[random.randint(0, 2)] - Wall.WIDTH / 2
    #     self.checked = False
    def __init__(self, x_in, y_in):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([Wall.WIDTH, Wall.HEIGHT])
        self.image.fill(BLACK)
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
        self.image = pygame.Surface([20, 40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - (2 * self.rect.height)
        self.lives = 3
        self.x_pos = 1

    def update(self):
        """ Update the player location. """
        self.rect.x = Player.x_pos_list[self.x_pos]

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
    SCORE_LIMIT = 15

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False
        self.game_won = False

        # Create sprite lists
        self.wall_list = []
        self.all_sprites_list = pygame.sprite.Group()

        # Create the block sprites
        for i in range(10):
            wall_group = WallGroup(-Wall.SPACER * i)
            self.wall_list.append(wall_group)

        # Create the player
        self.player = Player()
        self.lives = self.player.lives
        self.all_sprites_list.add(self.player)

        pygame.mixer.music.load("Caffeine & Chaos Forever.mp3")
        pygame.mixer.music.play(-1, 0.0)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over or self.game_won:
                    self.__init__()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move_right()

        return False

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

                # See if the player block has collided with anything.
                wall_hit_list = pygame.sprite.spritecollide(self.player, wall_group, True)

                # Check the list of collisions.
                for _ in wall_hit_list:
                    self.lives -= 1

                # This spawns an error, need to work on fixing
                if wall_group.sprites()[0].rect.y > self.player.rect.y + self.player.rect.height:
                    if not wall_group.score_checked:
                        self.score += 1
                        wall_group.score_checked = True

                if wall_group.sprites()[0].rect.y > SCREEN_HEIGHT:
                    self.handle_wall_reset(wall_group)

            if self.lives < 1:
                self.game_over = True
                pygame.mixer.music.stop()

            if self.score > Game.SCORE_LIMIT:
                self.game_won = True
                pygame.mixer.music.stop()

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if self.game_won:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("You won! Click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over and not self.game_won:
            self.all_sprites_list.draw(screen)
            for wall_group in self.wall_list:
                wall_group.draw(screen)
            self.display_feedback(screen)
        pygame.display.flip()

    def display_feedback(self, screen_in):
        """ Display feedback about the current game session, score and remaining lives"""
        pygame.draw.rect(screen_in, BLUE, [FEEDBACK_X, FEEDBACK_Y, 100, 70], 0)
        score_str = "Score: " + str(self.score)
        font = pygame.font.SysFont("serif", 25)
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
        new_wall_group = WallGroup(wall_group_last_y - Wall.SPACER)
        self.wall_list.append(new_wall_group)


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
    pygame.mixer.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Getaway")

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

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