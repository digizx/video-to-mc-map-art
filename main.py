import gzip
import json
import os
import time

from numpy import int8
from utils import ffmpeg
from utils.dat import nbt_to_dat, save_dat_file
from utils.db import db
from utils.nbt import encode_into_map_nbt
from utils.read_image_pixels import read_image_pixels

def main():
    ROOT_DIR = os.path.abspath(os.curdir)
    SRC_DIR = os.path.join(ROOT_DIR, 'src')
    OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

    ffmpeg.

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
    nbt_file = encode_into_map_nbt(blocks)

    # encode into dat
    # print(nbt_file)
    dat_file = nbt_to_dat(nbt_file)

    # return the dat file as a buffer
    output_dat_path = os.path.join(OUTPUT_DIR, 'map_1.dat')
    save_dat_file(dat_file, output_dat_path)

if __name__ == '__main__':
    main()