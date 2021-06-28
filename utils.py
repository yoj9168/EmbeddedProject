from constants import WIDTH, HEIGHT


def calculate_text_position(text_width, text_height, top_margin=0, bottom_margin=0, left_margin=0, right_margin=0):
    x = (WIDTH - text_width / 2) + left_margin - right_margin
    y = (HEIGHT - text_height / 2) + top_margin - bottom_margin
    return x, y


def draw_rectangle(x, y, size_width, size_height):
    left_top = x - size_width / 2, y - size_height / 2
    right_bottom = x + size_width / 2, y + size_height / 2
    return *left_top, *right_bottom
