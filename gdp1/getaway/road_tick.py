import pygame

from constants import WHITE, SCREEN_HEIGHT


class RoadTick(pygame.sprite.Sprite):
    """ This class represents a wall made to oppose our player. """
    WIDTH = 5
    HEIGHT = 20
    SPEED = [2, 3, 4]
    SPACER = 70
    RESET_Y = -100

    def __init__(self, x_in, y_in, level_in=0):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([RoadTick.WIDTH, RoadTick.HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x_in - RoadTick.WIDTH / 2
        self.rect.y = y_in
        self.speed = RoadTick.SPEED[level_in]

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        self.rect.y = RoadTick.RESET_Y

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += self.speed

        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()
