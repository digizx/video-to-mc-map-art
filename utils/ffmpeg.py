import os
import subprocess
import shutil
from pathlib import Path

ROOT_DIR = os.path.abspath(os.curdir)
INPUT_DIR = os.path.join(ROOT_DIR, 'src')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

def transform_video(
        input_path: str = None,
        input_filename: str = None,
        output_path: str = None,
        output_filename: str = None,
        out_size: str = '128',
        out_fps: int = 40
    ):
    """
    Function that takes information of an input video and produces
    a new video using FFMPEG
    """

    input_file = os.path.join(input_path, input_filename)
    output_file = os.path.join(output_path, output_filename)

    command = [
        'ffmpeg',
        '-y',  # overwrite output
        '-i', input_file,
        '-vf', 'crop=\'min(in_w\\,in_h)\':\'min(in_w\\,in_h)\',scale={0}:{0}:flags=spline'.format(out_size), # spline is the best looking one
        '-r', str(out_fps),
        output_file,
        '-hide_banner',
        '-loglevel', 'error'
    ]

    subprocess.run(command, check=True)

def video_to_frames(
    input_path: str = None,
    input_filename: str = None
    ):
    """
    Function that receives a video and outputs all it's frames
    """
    input_file = os.path.join(input_path, input_filename)
    output_pattern = os.path.join(OUTPUT_DIR, 'frames', 'out%d.png')

    frames_dir = os.path.join(input_path, 'frames')
    os.makedirs(frames_dir, exist_ok=True)

    command = [
        'ffmpeg',
        '-i', input_file,
        output_pattern,
        '-hide_banner',
        '-loglevel', 'error'
    ]

    subprocess.run(command, check=True)

def clean_up_out():
    """
    Function that deletes all the files and folders inside the folder out
    """
    shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

if (__name__ == "__main__"):

    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    clean_up_out()

    transform_video(
        input_path=INPUT_DIR,
        input_filename='odore_china_test.mp4',
        output_path=OUTPUT_DIR,
        output_filename='temp.mp4',
    )

    video_to_frames(
        input_path=OUTPUT_DIR,
        input_filename='temp.mp4'
    )