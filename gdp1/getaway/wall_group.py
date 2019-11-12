import random

import pygame

from wall import Wall


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