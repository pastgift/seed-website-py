# -*- coding: utf-8 -*-

import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

basedir = os.path.abspath(os.path.dirname(__file__))
CHARS = '345679abcdefghjkmnpqrstuvwxyACEFGHJKMNPQRSTUVWXY'

def gen_captcha(size=(200, 50),
                chars=CHARS,
                image_type='GIF',
                color=(0, 0, 0),
                bg_color=(255, 255, 255),
                font_size=26,
                length=4,
                draw_lines=10,
                draw_points=5,
                in_memory=False):

    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)

    # Draw lines
    if draw_lines:
        for i in xrange(draw_lines):
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            end   = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line((begin, end), fill=color)

    # Draw points
    if draw_points:
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                roll_score = random.randint(0, 100)
                if roll_score > draw_points:
                    continue

                draw.point((x, y), fill=color)

    # Create CAPTCHA
    char_samples     = random.sample(chars, length)
    captcha_code     = ''.join(char_samples)
    captcha_code_str = ' %s ' % ' '.join(char_samples)

    font = ImageFont.truetype('SourceCodePro-Bold.ttf', font_size)
    font_width, font_height = font.getsize(captcha_code_str)

    draw.text(((size[0] - font_width) / 4, (size[1] - font_height) / 4),
            captcha_code_str,
            font=font,
            fill=color)

    # Picture tranform
    params = [
        1 - float(random.randint(1, 2)) / 100,
        0,
        0,
        0,
        1 - float(random.randint(1, 10)) / 100,
        float(random.randint(1, 2)) / 500,
        0.001,
        float(random.randint(1, 2)) / 500,
    ]

    img = img.transform(size, Image.PERSPECTIVE, params)
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return captcha_code, img

if __name__ == "__main__":
    captcha_code, img = gen_captcha()
    img.save(captcha_code + '.gif', 'GIF')
