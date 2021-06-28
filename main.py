import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from constants import BAUDRATE, HEIGHT, WIDTH, IMAGE, FNT3, FNT, FNT2
from objects import Player, Enemy, Life, Score
from utils import calculate_text_position

cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Get drawing object to draw on image.
draw = ImageDraw.Draw(IMAGE)

# First Clear display.
draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=(255, 0, 0))
disp.image(IMAGE)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(IMAGE)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)


# Enemy's Set
enemy_list = list()

# Life List
life_list = list()
tag_life = True
life_count = 0

# Make Player
player = Player()

# Player's Life & Difficulty & skill
player_life = 3
skill = 3
score = Score()

difficulty = 0
difficulty_control = 5
difficulty_list = list()
for i in range(10, 700, 20):
    difficulty_list.append(i)

# Center print
text = {'game_over': "GAME OVER", 'special_skill': "Special Skill!", 'score': "Your Score : "}
text_size_over = draw.textsize(text['game_over'], font=FNT3)
text_size_skill = draw.textsize(text['special_skill'], font=FNT)
text_size_score = draw.textsize(text['score'], font=FNT)


game_loop = True
# Game Loop Start
while game_loop:
    # initialize Display
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    # Make Player
    player.make_player()
    # Player move
    player.player_move()

    if score.get_score() >= difficulty_list[difficulty]:
        difficulty += 1
    if difficulty + difficulty_control >= len(enemy_list):
        enemy_list.append(Enemy(score))

    # Enemy make & moving
    for i in enemy_list:
        i.make_enemy()
        i.enemy_move()
        # Collision
        if i.collision():
            player_life -= 1
            enemy_list.remove(i)
            if player_life == 0:
                draw.text(calculate_text_position(*text_size_over), text['game_over'], (255,0,0), font=FNT3)
                draw.text(calculate_text_position(*text_size_score, top_margin=30), text['score'], font=FNT)
                draw.text(
                    calculate_text_position(*text_size_score, left_margin=text_size_score[0]),
                    str(score.get_score()),
                    font=FNT,
                )
                game_loop = False

    # Player's skill - Erase all enemy
    if not button_A.value:  # A pressed
        if skill > 0:
            Enemy().skill_button_a()
            draw.text(calculate_text_position(*text_size_skill), text['special_skill'], (255, 0, 0), font=FNT)
            skill -= 1
        else:
            skill = 0

    # Make Life
    if score.get_score() % 20 == 0 and score.get_score() != 0:
        if tag_life:
            life_list.append(Life())
            tag_life = False
    else:
        tag_life = True

    # Eat Life
    for i in life_list:
        i.spawn_life()
        # Collision
        if i.collision():
            life_list.remove(i)
            player_life += 1

    # print score & skill & life
    draw.text((150, 20), "Score : ", font=FNT2)
    draw.text((200, 20), str(score.get_score()), font=FNT2)

    draw.text((150, 40), "Skill : ", font=FNT2)
    draw.text((200, 40), str(skill), font=FNT2)

    draw.text((150, 60), "Life : ", font=FNT2)
    draw.text((200, 60), str(player_life), font=FNT2)

    # Display the Image
    disp.image(IMAGE)

    time.sleep(0.01)
