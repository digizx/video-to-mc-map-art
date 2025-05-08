import gzip
import io

def nbt_to_dat(nbt_file):
    """
    Function that turns NBT information into a DAT file
    """
    try:
        buffer = io.BytesIO() # We're going to these depths to not early safe the nbt lol
        nbt_file.write(buffer)
        uncompressed_data = buffer.getvalue()
    except:
        print('There was a problem with the uncompressed data buffer!')
    
    return gzip.compress(uncompressed_data)

if __name__ == '__main__':
    
    import os
    from nbt import encode_into_map_nbt
    from numpy import int8

    ROOT_DIR = os.path.abspath(os.curdir)
    SRC_DIR = os.path.join(ROOT_DIR, 'src')
    OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

    colors : int8 = []

    colors.append(1)
    colors.append(2)
    colors.append(3)
    colors.append(4)
    colors.append(5)

    nbt_file = encode_into_map_nbt(colors)

    # print(nbt_file)

    dat_file = nbt_to_dat(nbt_file)

    print(dat_file)