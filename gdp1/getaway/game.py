import pygame

from constants import SCREEN_HEIGHT, BLACK, WHITE, SCREEN_WIDTH, YELLOW, SAND, BLUE, FEEDBACK_X, FEEDBACK_Y
from player import Player
from wall import Wall
from wall_group import WallGroup


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
    SCORE_LIMITS = [15, 20, 25]
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

    def __init__(self, level_in):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.level = level_in
        self.x_pos_list = Player.x_pos_list[level_in]
        self.game_over = False
        self.game_won = False
        self.done = False
        self.splash = True

        # Create sprite lists
        self.wall_list = []
        self.all_sprites_list = pygame.sprite.Group()

        # Create the block sprites
        for i in range(10):
            wall_group = WallGroup(-Wall.EASY_SPACER * i, level_in=self.level)
            self.wall_list.append(wall_group)

        # Create the player
        self.player = Player(level_in=self.level)
        self.lives = self.player.lives
        self.all_sprites_list.add(self.player)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        if not pygame.mixer.music.get_busy() and not self.game_over and not self.game_won:
            pygame.mixer.music.load("audio/Caffeine & Chaos Forever.mp3")
            pygame.mixer.music.play(-1, 0.0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move_right()
                if event.key == pygame.K_SPACE:
                    if self.game_over or self.game_won:
                        self.__init__(self.level)

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

            if self.score >= Game.SCORE_LIMITS[self.level]:
                self.level += 1
                if self.level >= len(Game.SCORE_LIMITS):
                    self.game_won = True
                    self.level = 0
                    pygame.mixer.music.fadeout(200)
                else:
                    self.__init__(self.level)

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
        # screen.blit(pygame.Surface([Wall.WIDTH, Wall.HEIGHT]), [500, 70])
        pygame.draw.rect(screen, YELLOW, [500, 50, Wall.WIDTH, Wall.HEIGHT], 0)
        pygame.draw.rect(screen, YELLOW, [420, 50, Wall.WIDTH, Wall.HEIGHT], 0)
        pygame.draw.rect(screen, YELLOW, [580, 50, Wall.WIDTH, Wall.HEIGHT], 0)

        screen.blit(pygame.transform.scale(pygame.image.load("images/car_red.png"), (25, 50)), [500, 160])

        screen.blit(pygame.transform.scale(pygame.image.load("images/car_yellow.png"), (25, 50)), [500, 350])
        screen.blit(pygame.transform.scale(pygame.image.load("images/car_blue.png"), (25, 50)), [540, 380])
        screen.blit(pygame.transform.scale(pygame.image.load("images/car_yellow.png"), (25, 50)), [470, 400])

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
        pygame.draw.rect(screen_in, BLUE, [FEEDBACK_X, FEEDBACK_Y, 140, 100], 0)
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
        level_str = "Highway " + str(self.level + 1)
        level_x = lives_x
        level_y = lives_y + 25
        level_text = font.render(level_str, True, WHITE)
        screen_in.blit(level_text, [level_x, level_y])

    def handle_wall_reset(self, wall_group_first):
        wall_group_last_y = self.wall_list[-1].sprites()[0].rect.y
        # for wall_sprite in wall_group_first.sprites():
        wall_sprite = wall_group_first.sprites()[0]
        # Basically remove the 0th element, but add it to the end using the y from the last one
        self.wall_list.pop(0)
        new_wall_group = WallGroup(wall_group_last_y - Wall.EASY_SPACER, level_in=self.level)
        self.wall_list.append(new_wall_group)

    def create_background(self, screen_in):
        # self.all_sprites_list.add()
        pygame.draw.rect(screen_in, BLACK, [self.x_pos_list[0] - Wall.WIDTH, 0,
                                            self.x_pos_list[-1] - self.x_pos_list[0] + Wall.WIDTH * 2,
                                            SCREEN_HEIGHT], 0)
        for i in range(len(self.x_pos_list)-1):
            road_line_x = (self.x_pos_list[i] + self.x_pos_list[i+1]) / 2 - 2
            pygame.draw.rect(screen_in, WHITE, [road_line_x, 0, 5, SCREEN_HEIGHT], 0)
