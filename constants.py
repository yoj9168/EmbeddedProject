from PIL import Image, ImageFont
from main import disp

BAUDRATE = 24000000

# Make sure to create image with mode 'RGB' for color.
WIDTH = disp.width
HEIGHT = disp.height
IMAGE = Image.new("RGB", (WIDTH, HEIGHT))

# Colors and font
PLAYER_FILL = "#00BFFF"  # DeepSkyblue
ENEMY_FILL = "#FF1493"  # DeepPink
LIFE_FILL = "#00FF00"  # Green
FNT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
FNT2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
FNT3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",30)

# Enemy
NORTH_RADIAN = [(3, 1), (2, 1), (2, 2), (1, 2), (1, 3), (0, 3), (-3, 1), (-2, 1), (-2, 2), (-1, 2), (-1, 3)]
SOUTH_RADIAN = [(3, -1), (2, -1), (2, -2), (1, -2), (1, -3), (0, -3), (-3, -1), (-2, -1), (-2, -2), (-1, -2), (-1, -3)]
EAST_RADIAN = [(-1, 3), (-1, 2), (-2, 2), (-2, 1), (-3, 1), (-3, 0), (-1, -3), (-1, -2), (-2, -2), (-2, -1), (-3, -1)]
WEST_RADIAN = [(1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (1, -3), (1, -2), (2, -2), (2, -1), (3, -1)]
