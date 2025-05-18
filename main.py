import gzip
import io
import json
import os
import time
from zipfile import ZipFile

from numpy import int8
from utils.dat import nbt_to_dat, save_dat_file
from utils.nbt import encode_into_map_nbt
from utils.read_image_pixels import read_image_pixels
from utils.ffmpeg import read_video_and_transform, video_to_frame_buffers

def main():
    ROOT_DIR = os.path.abspath(os.curdir)
    SRC_DIR = os.path.join(ROOT_DIR, 'src')
    OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

    # Output related
    dat_files = []
    path_output = os.path.join(OUTPUT_DIR, 'maps.zip')

    # load video into frames

    path_video = os.path.join(SRC_DIR, 'odore_china_test.mp4')

    video_buf = read_video_and_transform(path_video)
    frames = video_to_frame_buffers(video_buf)

    # read hashmap colors dictionary
    start = time.time()
    path_hashmap_colors = os.path.join(SRC_DIR, 'hashmap_colors.json.gz')
    with gzip.open(path_hashmap_colors, 'rt', encoding='utf-8') as file:
        hashmap_colors = json.load(file)
    end = time.time()

    print('Time to load colors hashmap:', end - start)

    # iterate through all frames

    start_loop = time.time()

    for index, frame in enumerate(frames):

        start = time.time()
        pix, w, h = read_image_pixels(frame)

        # look for each color in the hash map
        blocks : list[int8] = []
        for i in range(w):
            # print('Current row:', i + 1)
            for j in range(h):
                r, g, b = pix[j, i] # the list fills up column by column, so the axis are inverted
                key = f'{r},{g},{b}'
                best_block_id = hashmap_colors[key]
                blocks.append(best_block_id)
        end = time.time()

        print(f'Time to load frame {index}:', end - start)

        # encode into a map nbt
        nbt_file = encode_into_map_nbt(blocks)

        # encode into dat
        dat_file = nbt_to_dat(nbt_file)

        # save into a list
        dat_files.append(dat_file)

    # Save in a zip file
    with ZipFile(path_output, 'w') as zipf:
        for index, dat_file in enumerate(dat_files):
            filename = f'map_{index}.dat'
            zipf.writestr(filename, dat_file)

    end_loop = time.time()

    print('Total time for processing the video:', end_loop - start_loop)

if __name__ == '__main__':
    main()