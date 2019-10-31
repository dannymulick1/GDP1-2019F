"""
 Culebra game.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

Edits made by Mulickd
"""

import pygame

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

SEGMENT_COUNT = 15
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class HeadSegment(Segment):
    """ Class to represent the head of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__(x, y)

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(GREEN)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('Snake Example')
snake_segments = []
allspriteslist = pygame.sprite.Group()
segment_group = pygame.sprite.Group()


def snake_init():
    global game_over, snake_segments, x_change, y_change
    x_change = segment_width + segment_margin
    y_change = 0
    game_over = False
    allspriteslist.empty()
    segment_group.empty()

    # Create an initial snake
    snake_segments = []
    for i in range(SEGMENT_COUNT):
        x = 250 - (segment_width + segment_margin) * i
        y = 30
        if i == SEGMENT_COUNT - 1:
            segment = HeadSegment(x, y)
        else:
            segment = Segment(x, y)
        snake_segments.append(segment)
        allspriteslist.add(segment)
        segment_group.add(segment)


snake_init()

clock = pygame.time.Clock()
done = False
game_over = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                snake_init()

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)

    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    snake_segments[0].image.fill(WHITE)
    old_segment = snake_segments.pop()
    allspriteslist.remove(old_segment)
    segment_group.remove(old_segment)

    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    head = HeadSegment(x, y)

    # Insert new segment into the list
    snake_segments.insert(0, head)

    head_collision_detect = pygame.sprite.spritecollide(head, segment_group, False)

    if head_collision_detect:
        print("Game over")
        game_over = True

    else:
        allspriteslist.add(head)
        segment_group.add(head)

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    if game_over:
        font = pygame.font.SysFont("serif", 25)
        text = font.render("Game Over, click to restart", True, WHITE)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

    else:
        allspriteslist.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(5)

pygame.quit()