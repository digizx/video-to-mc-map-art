import gzip
import json
import time

from models.MinecraftColor import MinecraftColor
from models.RGBColor import RGBColor
from numpy import uint8, int8, clip
from utils.DatUtils import nbt_to_dat, save_dat_file
from utils.db import db
from utils.NbtUtils import encode_into_map_nbt

class RgbUtils():
    def __init__(self):
        pass

    def diff_rgb_color(
        self,
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
        self,
        input_id : uint8
        ) -> int8:
        """
        Function that transforms the uint8 into int8 format which Minecraft accepts
        """
        return int8(input_id) if input_id < 128 else int8(input_id - 256)

    def find_best_suitable_block(
        self,
        colors : list[MinecraftColor], 
        input_rgb : RGBColor
        ) -> int8:
        """
        Function that iterates through all available block colors and finds
        the most suitable option, then returns the respective ID that fits the best.
        """
        best_block_id : uint8 = 0
        closest_match = 255 # 0 is the best possible match. There's no diff between RGB colors
        for color in colors:
            diff = self.diff_rgb_color(input_rgb, color.rgb)
            if diff <= closest_match:
                best_block_id = color.id
                closest_match = diff
                if closest_match <= 0:
                    break
        
        final_best_block_id : int8 = self.best_block_sorcery(best_block_id)

        return final_best_block_id
    
if __name__ == '__main__':

    import os
    from config import ROOT_DIR, SRC_DIR, OUT_DIR
    from utils.ReadImagePixelsUtils import read_image_pixels

    database = db()
    
    # load the image

    path_image = os.path.join(SRC_DIR, 'miku.png')
    pix, w, h = read_image_pixels(path_image)

    # start timer
    start = time.time()

    # read hashmap colors dictionary
    path_hashmap_colors = os.path.join(SRC_DIR, 'hashmap_colors.json.gz')
    with gzip.open(path_hashmap_colors, 'rt', encoding='utf-8') as file:
        hashmap_colors = json.load(file)
    
    # end timer
    end = time.time()

    print('Time to load colors hashmap:', end - start)

    start = time.time()
    
    # look for each color
    blocks : list[int8] = []
    for i in range(w):
        # print('Current row:', i + 1)
        for j in range(h):
            r, g, b = pix[j, i] # for some reason, it is rotated, so i just inverted it
            key = f'{r},{g},{b}'
            best_block_id = hashmap_colors[key]
            blocks.append(best_block_id)

    end = time.time()
    print('Time to find all +16k best combinations:', end - start)
    
    # encode into a map nbt
    nbt_file =  encode_into_map_nbt(blocks)

    # encode into dat
    # print(nbt_file)
    dat_file = nbt_to_dat(nbt_file)

    # return the dat file as a buffer
    output_dat_path = os.path.join(OUT_DIR, 'map_1.dat')
    save_dat_file(dat_file, output_dat_path)

    # best_block_id = find_best_suitable_block(database, RGBColor(255, 0, 0))
    # print(best_block_id)