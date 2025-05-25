import argparse
import gzip
import json
import os
import time

from config import SRC_DIR, OUT_DIR
from numpy import int8
from enums.DirectionEnum import DirectionEnum
from utils.DatapackGeneratorUtils import DatapackGeneratorUtils
from utils.DatUtils import DatUtils
from utils.FfmpegUtils import FfmpegUtils
from utils.NbtUtils import NbtUtils
from utils.ReadImagePixelsUtils import ReadImagePixelsUtils
from zipfile import ZipFile

def main(args):
    # Utils used
    dat_utils = DatUtils()
    ffmpeg_utils = FfmpegUtils()
    nbt_utils = NbtUtils()
    pixels_utils = ReadImagePixelsUtils()

    # Output related
    dat_files = []
    path_output = os.path.join(OUT_DIR, f'maps_{args.name}.zip')

    # load video into frames

    path_video = os.path.join(args.path)
    if not os.path.isfile(path_video):
        raise Exception('The video wasn\'t found. Send a correct video')

    video_buf = ffmpeg_utils.read_video_and_transform(path_video)
    frames, amount_frames = ffmpeg_utils.video_to_frame_buffers(video_buf)

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
        pix, w, h = pixels_utils.read_image_pixels(frame)

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

        print(f'Time to load frame {index}/{amount_frames}:', end - start)

        # encode into a map nbt
        nbt_file = nbt_utils.encode_into_map_nbt(blocks)

        # encode into dat
        dat_file = dat_utils.nbt_to_dat(nbt_file)

        # save into a list
        dat_files.append(dat_file)

    # Save in a zip file
    with ZipFile(path_output, 'w') as zipf:
        for index, dat_file in enumerate(dat_files):
            filename = f'map_{index + int(args.index)}.dat'
            zipf.writestr(filename, dat_file)

    end_loop = time.time()

    print('Total time for processing the video:', end_loop - start_loop)

    # Generate datapack

    start_datapack_time = time.time()

    if args.x is None or args.y is None or args.y is None or args.direction is None:
        raise Exception('Datapack wasn\t generated because coordinates or direction weren\'t specified.')

    # Get Direction Enum value based on the input
    args_direction = args.direction.upper()
    direction = DirectionEnum[args_direction].value

    # amount_frames = 8780
    datapack_utils = DatapackGeneratorUtils(
        initial_map_id=int(args.index),
        name=args.name,
        total_frames=amount_frames if args.frames is None else int(args.frames),
        x=int(args.x),
        y=int(args.y),
        z=int(args.z),
        direction=direction,
        delay=int(args.delay)
    )
    datapack_utils.generate_datapack()

    end_datapack_time = time.time()

    print('Total time for processing the datapack:', end_datapack_time - start_datapack_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--name', help='Name for the zip file that is going to be saved')
    parser.add_argument('-p', '--path', help='Path of the file that is going to be processed into Minecraft format')

    parser.add_argument('-x', '--x', help='X coordinates in Minecraft')
    parser.add_argument('-y', '--y', help='Y coordinates in Minecraft')
    parser.add_argument('-z', '--z', help='Z coordinates in Minecraft')
    parser.add_argument('-d', '--direction', help='The options are North, East, South and West. If none selected then the datapack won\'nt be generated.')

    parser.add_argument('-i', '--index', help='Indicates the first map number it\'ll be saved. By default is 0.', default=0)
    parser.add_argument('-f', '--frames', help='Indicates the amount of frames that will be shown in the game. By default is max.', default=None)

    parser.add_argument('-de', '--delay', help='Indicates the amount of seconds that the first frames will be repeated. By default 0.', default=0)

    args = parser.parse_args()

    if args.name is None or args.path is None:
        raise Exception('Name or path wasn\'t added as an argument.')

    main(args)