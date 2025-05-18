import os
import PIL

from config import ROOT_DIR, SRC_DIR, OUT_DIR
from io import BytesIO

class ReadImagePixelsUtils():
    def __init__(self):
        pass
    
    def print_image_pixels(
        self,
        pixels_array,
        width,
        height,
        ):
        for i in range(width):
            for j in range(height):
                print(pixels_array[i, j])

    def read_image_pixels(
        self,
        buffer: BytesIO
        ):
        im = PIL.Image.open(buffer).convert('RGB')
        pix = im.load()
        w, h = im.size

        return pix, w, h

if (__name__ == "__main__"):

    pix_utils = ReadImagePixelsUtils()

    path_sample_image = os.path.join(SRC_DIR, 'miku.png')
    print(path_sample_image)

    pix, w, h = pix_utils.read_image_pixels(path_sample_image)

    pix_utils.print_image_pixels(pix, w, h)