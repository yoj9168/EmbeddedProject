# Bring up Position Class
import random

from constants import WIDTH, HEIGHT, PLAYER_FILL, ENEMY_FILL, NORTH_RADIAN, SOUTH_RADIAN, EAST_RADIAN, WEST_RADIAN, \
    LIFE_FILL
from main import draw, player, button_U, button_D, button_L, button_R, enemy_list
from utils import draw_rectangle


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Player Class
class Player:
    x = 0
    y = 0
    # Player's information
    position = Position(x, y)

    moving_speed = 0
    size_WIDTH = 0
    size_height = 0

    def __init__(self):
        self.position = Position(self.x, self.y)

        # Player's information
        self.position.x = WIDTH/2  # Player's first position of x
        self.position.y = HEIGHT/2  # Player's first position of y
        self.moving_speed = 5
        self.size_width = 20
        self.size_height = 20

    # Make player
    @staticmethod
    def make_player():
        draw.rectangle(draw_rectangle(player.position.x, player.position.y, player.size_width, player.size_height),
                       outline=0, fill=PLAYER_FILL)

    # Player's move
    def player_move(self):
        # up pressed
        if not button_U.value:
            if self.position.y - (self.size_height / 2) > 0:  # If player's position is in the display
                self.position.y = self.position.y - self.moving_speed

        # down pressed
        if not button_D.value:
            if self.position.y + (self.size_height / 2) < HEIGHT:  # If player's position is in the display
                self.position.y = self.position.y + self.moving_speed

        # left pressed
        if not button_L.value:
            if self.position.x - (self.size_width / 2) > 0:  # If player's position is in the display
                self.position.x = self.position.x - self.moving_speed

        # right pressed
        if not button_R.value:
            if self.position.x + (self.size_width / 2) < WIDTH:  # If player's position is in the display
                self.position.x = self.position.x + self.moving_speed


# Enemy Class
class Enemy:
    x = 0
    y = 0
    # Enemy's Information
    position = Position(x, y)

    moving_speed = 0
    spawn_point = None
    radian = 0

    size_width = 0
    size_height = 0

    def __init__(self, score):
        # Enemy's information
        self.position = Position(self.x, self.y)

        self.moving_speed = random.choice([1.0, 1.5, 2.0, 2.5])
        self.spawn_point = random.choice(['NORTH', 'SOUTH', 'EAST', 'WEST'])

        self.size_width = random.choice([15, 20, 25, 30])
        self.size_height = self.size_width

        self.score = score

        # Enemy's spawn location
        if self.spawn_point == 'NORTH':
            self.position.x = random.randint(0, WIDTH)
            self.position.y = 0
            self.radian = random.choice(NORTH_RADIAN)

        elif self.spawn_point == 'SOUTH':
            self.position.x = random.randint(0, WIDTH)
            self.position.y = HEIGHT
            self.radian = random.choice(SOUTH_RADIAN)

        elif self.spawn_point == 'EAST':
            self.position.x = WIDTH
            self.position.y = random.randint(0, HEIGHT)
            self.radian = random.choice(EAST_RADIAN)

        elif self.spawn_point == 'WEST':
            self.position.x = 0
            self.position.y = random.randint(0, HEIGHT)
            self.radian = random.choice(WEST_RADIAN)

    # Make Enemy
    def make_enemy(self):
        draw.rectangle(draw_rectangle(self.position.x, self.position.y, self.size_width, self.size_height),
                       outline=0,
                       fill=ENEMY_FILL)

    # Enemy's move
    def enemy_move(self):
        self.position.x = self.position.x + (self.moving_speed * self.radian[0])
        self.position.y = self.position.y + (self.moving_speed * self.radian[1])

        # Check position in the Display
        def display_north():
            if self.position.y < 0:
                return True
            
        def display_south():
            if self.position.y > HEIGHT:
                return True
            
        def display_east():
            if self.position.x < 0:
                return True
            
        def display_west():
            if self.position.x > WIDTH:
                return True

        # If position is out of display, Remove
        # spawn point -> north
        if self.spawn_point == 'NORTH':
            if display_west() or display_south() or display_east():
                enemy_list.remove(self)
                self.score.increment()

        # spawn point -> south
        if self.spawn_point == 'SOUTH':
            if display_north() or display_east() or display_west():
                enemy_list.remove(self)
                self.score.increment()
                
        # spawn point -> east
        if self.spawn_point == 'EAST':
            if display_north() or display_south() or display_west():
                enemy_list.remove(self)
                self.score.increment()

        # spawn point -> west
        if self.spawn_point == 'WEST':
            if display_north() or display_south() or display_east():
                enemy_list.remove(self)
                self.score.increment()

    @staticmethod
    def skill_button_a():
        """Execute skill if you press the button A"""
        enemy_list.clear()

    # Collision
    def collision(self):
        if (
            abs(player.position.x - self.position.x) <= player.size_width
            and abs(player.position.y - self.position.y) <= player.size_height
        ):
            return True


# Life Class
class Life:
    x = 0
    y = 0

    # Life's Information
    position = Position(x, y)

    size_width = 0
    size_height = 0

    def __init__(self):
        self.position = Position(self.x, self.y)
        self.position.x = random.randint(0, WIDTH)
        self.position.y = random.randint(0, HEIGHT)

        self.size_width = 15
        self.size_height = 15

    # make Life
    def spawn_life(self):
        draw.rectangle(draw_rectangle(self.position.x, self.position.y, self.size_width, self.size_height),
                       outline=0,
                       fill=LIFE_FILL)

    # collision
    def collision(self):
        if (
                abs(player.position.x - self.position.x) <= player.size_width
                and abs(player.position.y - self.position.y) <= player.size_height
        ):
            return True


class Score:
    score = 0

    def increment(self):
        self.score += 1

    def get_score(self):
        return self.score
