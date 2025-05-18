import os
import subprocess

from config import ROOT_DIR, SRC_DIR, OUT_DIR
from io import BytesIO
from PIL import Image

class FfmpegUtils():
    def __init__(self):
        pass

    def read_video_and_transform(
        self,
        path_input: str = None,
        out_size: str = '128',
        out_fps: int = 40,
        codec : str = 'mp4'
        ):
        """
        Reads a video suing FFmpeg and returns the result as a BytesIO buffer.
        """
        buffer = BytesIO()

        command = [
            'ffmpeg',
            '-i', path_input,
            '-vf', 'crop=\'min(in_w\\,in_h)\':\'min(in_w\\,in_h)\',scale={0}:{0}:flags=spline'.format(out_size), # spline is the best looking one
            '-r', str(out_fps),
            '-f', codec,
            '-movflags', 'frag_keyframe+empty_moov', # Required form streaming output
            '-preset', 'ultrafast',
            '-loglevel', 'error',
            'pipe:1' # Output to stdout
        ]

        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode != 0:
            raise RuntimeError('FFmpeg error:', process.stderr.decode())

        buffer.write(process.stdout)
        buffer.seek(0)
        return buffer

    def video_to_frame_buffers(
        self,
        video_buffer: BytesIO
        ):
        """
        Reads a video bfufer, uses FFmpeg to extract frames, and returns a list of BytesIO images.
        """
        command = [
            'ffmpeg',
            '-i', 'pipe:0',
            '-f', 'image2pipe',
            '-vcodec', 'png',
            '-loglevel', 'error',
            'pipe:1'
        ]

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, _ = process.communicate(input=video_buffer.read())

        # PNG file signature
        PNG_SIG = b'\x89PNG\r\n\x1a\n'
        frames = []

        start = 0
        while True:
            start = stdout.find(PNG_SIG, start)
            if start == -1:
                break
            end = stdout.find(PNG_SIG, start + len(PNG_SIG))
            if end == -1:
                chunk = stdout[start:]
                start = len(stdout)
            else:
                chunk = stdout[start:end]
                start = end

            buffer = BytesIO(chunk)
            frames.append(buffer)
                
        return frames

if (__name__ == "__main__"):
    ffmpeg_utils = FfmpegUtils()

    path_video = os.path.join(SRC_DIR, 'odore_china_test.mp4')

    video_buf = ffmpeg_utils.read_video_and_transform(path_video)
    frames = ffmpeg_utils.video_to_frame_buffers(video_buf)

    for i, buf in enumerate(frames):
        img = Image.open(buf)
        print(f'Frame {i}: {img.size}')