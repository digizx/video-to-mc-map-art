from utils.db import db
from numpy import uint8, int8, clip
from typing import final
from models.RGBColor import RGBColor
from utils.nbt import encode_into_map_nbt
from utils.dat import nbt_to_dat, save_dat_file

def shade_rgb_color(
    color : uint8,
    shade : uint8
    ) -> uint8:
    """
    Based on Minecraft Map Art, it turns a color into a certain degre of shade.
    """
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
    diff_r = abs(int(a.r) - int(b.r))
    diff_g = abs(int(a.g) - int(b.g))
    diff_b = abs(int(a.b) - int(b.b))

    total_diff = diff_r + diff_g + diff_b
    return clip(total_diff, 0, 255)

def best_block_sorcery(
    input_id : uint8
    ) -> int8:
    """
    Function that transforms the uint8 into int8 format which Minecraft accepts
    """
    if input_id >= 128:
        return 127 - input_id
    return input_id

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
        shaded_variations = find_shade_variations(
            RGBColor(color.rgb["r"], color.rgb["g"], color.rgb["b"])
        )
        shaded_colors.extend(shaded_variations)
    
    best_block_id : uint8 = -1
    closest_match = 255 # 0 is the best possible match. There's no diff between RGB colors
    for index, rgb_color in enumerate(shaded_colors):
        diff = diff_rgb_color(input_rgb, rgb_color)
        if diff <= closest_match:
            best_block_id = index
            closest_match = diff
    
    final_best_block_id : int8 = best_block_sorcery(best_block_id)

    return final_best_block_id
    
if __name__ == '__main__':

    import os
    from utils.read_image_pixels import read_image_pixels

    ROOT_DIR = os.path.abspath(os.curdir)
    SRC_DIR = os.path.join(ROOT_DIR, 'src')
    OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

    database = db()
    
    # load the image

    path_image = os.path.join(SRC_DIR, 'miku.png')
    pix, w, h = read_image_pixels(path_image)

    # iterate through each pixel
    blocks : list[int8] = []
    for i in range(w):
        for j in range(h):
            r, g, b = pix[i, j]
            best_block_id = find_best_suitable_block(database, RGBColor(r, g, b))
            blocks.append(best_block_id)
    
    # encode into a map nbt
    nbt_file =  encode_into_map_nbt(blocks)

    # encode into dat
    dat_file = nbt_to_dat(nbt_file)

    # return the dat file as a buffer
    output_dat_path = os.path.join(OUTPUT_DIR, 'map_1.dat')
    save_dat_file(dat_file, output_dat_path)

    # best_block_id = find_best_suitable_block(database, RGBColor(255, 0, 0))
    # print(best_block_id)