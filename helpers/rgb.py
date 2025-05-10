from utils.db import db
from numpy import uint8, int8, clip
from typing import final
from models.rgb import RGBColor

def shade_rgb_color(
    color : uint8,
    shade : uint8
    ) -> uint8:
    shaded_color = (color / shade) * 255
    return uint8(clip(shaded_color, 0, 255))

def find_shade_variations(
    input_rgb : RGBColor
    ) -> tuple[
        RGBColor, # Four possible RGBs
        RGBColor, 
        RGBColor, 
        RGBColor
    ]:
    """
    Function that receives an input RGB as a parameter and turns it into
    the 4 Minecraft shade variations
    """
    result = []
    SHADES : final = [135, 180, 220, 255]

    from pprint import pprint
    pprint(vars(input_rgb))
    for shade in SHADES:
        shaded_r = shade_rgb_color(input_rgb.r, shade)
        shaded_g = shade_rgb_color(input_rgb.g, shade)
        shaded_b = shade_rgb_color(input_rgb.b, shade)
        shaded_rgb = RGBColor(shaded_r, shaded_g, shaded_b)
        result.append(shaded_rgb)
    
    return result

def diff_rgb_color(
    a : RGBColor,
    b : RGBColor
    ) -> uint8:
    """
    Returns the difference as an 8-bit unsinged integer between
    two pairs of RGBColor.
    """
    return (
        abs(a.r - b.r) + abs(a.g - b.g) + abs(a.b - b.b)
    )

def find_best_suitable_block(
    database : db, 
    input_rgb : RGBColor
    ) -> int8:
    """
    Function that iterates through all available block colors and finds
    the most suitable option, then returns the respective ID that fits the best.
    """
    shaded_colors = []
    for color in database.colors:
        shaded_variations = find_shade_variations(color)
        shaded_colors.extend(shaded_variations)
    
    best_block_id = -1
    closest_match = 255 # 0 is the best possible match. There's no diff between RGB colors
    for index, rgb_color in enumerate(shaded_colors):
        diff = diff_rgb_color(input_rgb, rgb_color)
        if diff <= closest_match:
            best_block_id = index
            closest_match = diff
    return best_block_id
    
if __name__ == '__main__':
    database = db()
    find_best_suitable_block(database, RGBColor(255, 0, 0))