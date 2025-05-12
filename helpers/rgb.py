from models.MinecraftColor import MinecraftColor
from utils.db import db
from numpy import uint8, int8, clip
from models.RGBColor import RGBColor
from utils.nbt import encode_into_map_nbt
from utils.dat import nbt_to_dat, save_dat_file

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
    return int8(input_id) if input_id < 128 else int8(input_id - 256)

def find_best_suitable_block(
    colors : list[MinecraftColor], 
    input_rgb : RGBColor
    ) -> int8:
    """
    Function that iterates through all available block colors and finds
    the most suitable option, then returns the respective ID that fits the best.
    """
    best_block_id : uint8 = 0
    closest_match = 255 # 0 is the best possible match. There's no diff between RGB colors
    for index, color in enumerate(colors):
        diff = diff_rgb_color(input_rgb, color.rgb)
        if diff <= closest_match:
            best_block_id = index
            closest_match = diff
            if closest_match <= 0:
                break
    
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
        print('Current row:', i + 1)
        for j in range(h):
            r, g, b = pix[j, i] # for some reason, it is rotated, so i just inverted it
            best_block_id = find_best_suitable_block(
                database.shaded_colors[4:], # exclude transparent shaded colors
                RGBColor(r, g, b)
            )
            blocks.append(best_block_id)
    
    # encode into a map nbt
    nbt_file =  encode_into_map_nbt(blocks)

    # encode into dat
    print(nbt_file)
    dat_file = nbt_to_dat(nbt_file)

    # return the dat file as a buffer
    output_dat_path = os.path.join(OUTPUT_DIR, 'map_1.dat')
    save_dat_file(dat_file, output_dat_path)

    # best_block_id = find_best_suitable_block(database, RGBColor(255, 0, 0))
    # print(best_block_id)