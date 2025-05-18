from io import BytesIO
import os
import PIL
from PIL import ImageCms

ROOT_DIR = os.path.abspath(os.curdir)
SRC_DIR = os.path.join(ROOT_DIR, 'src')

def print_image_pixels(
        pixels_array,
        width,
        height,
    ):
    for i in range(width):
        for j in range(height):
            print(pixels_array[i, j])

def read_image_pixels(
        buffer: BytesIO
    ):
    im = PIL.Image.open(buffer).convert('RGB')
    pix = im.load()
    w, h = im.size

    return pix, w, h

if (__name__ == "__main__"):

    path_sample_image = os.path.join(SRC_DIR, 'miku.png')
    print(path_sample_image)

    pix, w, h = read_image_pixels(path_sample_image)

    print_image_pixels(pix, w, h)