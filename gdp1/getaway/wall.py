import pygame

from constants import SCREEN_HEIGHT
from player import Player


class Wall(pygame.sprite.Sprite):
    """ This class represents a wall made to oppose our player. """
    WIDTH = 60
    HEIGHT = 40
    SPEED = [2, 3, 4]
    SPACER = 170
    RESET_Y = -100

    def __init__(self, x_in, y_in, level_in=0):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("images/barrier.png"), (Wall.WIDTH, Wall.HEIGHT))
        self.rect = self.image.get_rect()
        self.x_pos = Player.x_pos_list[level_in]
        self.rect.x = self.x_pos[x_in] - Wall.WIDTH / 2
        self.rect.y = y_in
        self.checked = False
        self.speed = Wall.SPEED[level_in]

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        self.checked = False

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += self.speed

        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()
