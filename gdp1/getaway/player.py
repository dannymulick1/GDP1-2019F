import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    X_CHANGE = 100
    x_pos_list = [[(SCREEN_WIDTH / 2) - X_CHANGE,
                   SCREEN_WIDTH / 2,
                   (SCREEN_WIDTH / 2) + X_CHANGE],
                  [(SCREEN_WIDTH / 2) - X_CHANGE * 2,
                   (SCREEN_WIDTH / 2) - X_CHANGE,
                   SCREEN_WIDTH / 2,
                   (SCREEN_WIDTH / 2) + X_CHANGE,
                   (SCREEN_WIDTH / 2) + X_CHANGE * 2],
                  [(SCREEN_WIDTH / 2) - X_CHANGE * 2,
                   (SCREEN_WIDTH / 2) - X_CHANGE,
                   SCREEN_WIDTH / 2,
                   (SCREEN_WIDTH / 2) + X_CHANGE,
                   (SCREEN_WIDTH / 2) + X_CHANGE * 2]]

    def __init__(self, level_in=0):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("images/car_red.png"), (25, 50))
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - (2 * self.rect.height)
        self.lives = 3
        self.x_pos_list = Player.x_pos_list[level_in]
        self.x_pos = len(self.x_pos_list) // 2

    def update(self):
        """ Update the player location. """
        self.rect.x = self.x_pos_list[self.x_pos] - \
            self.image.get_rect().size[0] / 2

    def move_left(self):
        if self.x_pos > 0:
            self.x_pos -= 1
        else:
            pass
            # Suggestion: Implement minor shake or play a
            # sound to denote you can't go left

    def move_right(self):
        if self.x_pos < len(self.x_pos_list):
            self.x_pos += 1
        else:
            pass
            # Suggestion: Implement minor shake or play a
            # sound to denote you can't go right
