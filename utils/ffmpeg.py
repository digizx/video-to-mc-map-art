import os
import subprocess
import shutil
from pathlib import Path

ROOT_DIR = os.path.abspath(os.curdir)
INPUT_DIR = os.path.join(ROOT_DIR, 'src')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

def transform_video(
        path_input: str = None,
        path_output: str = None,
        out_size: str = '128',
        out_fps: int = 40
    ):
    """
    Function that takes information of an input video and produces
    a new video using FFMPEG
    """

    command = [
        'ffmpeg',
        '-y',  # overwrite output
        '-i', path_input,
        '-vf', 'crop=\'min(in_w\\,in_h)\':\'min(in_w\\,in_h)\',scale={0}:{0}:flags=spline'.format(out_size), # spline is the best looking one
        '-r', str(out_fps),
        path_output,
        '-hide_banner',
        '-loglevel', 'error'
    ]

    subprocess.run(command, check=True)

def video_to_frames(
    path_input: str = None,
    ):
    """
    Function that receives a video and outputs all it's frames
    """
    output_pattern = os.path.join(OUTPUT_DIR, 'frames', 'out%d.png')

    frames_dir = os.path.join(OUTPUT_DIR, 'frames')
    os.makedirs(frames_dir, exist_ok=True)

    command = [
        'ffmpeg',
        '-i', path_input,
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

    path_input_tr = os.path.join(INPUT_DIR, 'odore_china_test.mp4')
    path_output_tr = os.path.join(OUTPUT_DIR, 'temp.mp4')

    transform_video(
        path_input=path_input_tr,
        path_output=path_output_tr
    )

    path_input_vf = os.path.join(OUTPUT_DIR, 'temp.mp4')

    video_to_frames(
        path_input=path_input_vf
    )