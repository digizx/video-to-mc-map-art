import nbtlib
from numpy import int8

def encode_into_nbt(data):
    """
    Function that turns data into NBT format the input data
    """
    pass

def encode_into_map_nbt(map_colors : list[int8]) -> nbtlib.Compound:
    
    data = nbtlib.Compound({
        'zCenter': nbtlib.Int(0),
        'unlimitedTracking': nbtlib.Byte(0),
        'trackingPosition': nbtlib.Byte(0),
        'frames': nbtlib.List([]),
        'scale': nbtlib.Byte(0),
        'locked': nbtlib.Byte(1),
        'dimension': nbtlib.String('minecraft:overworld'),
        'banners': nbtlib.List([]),
        'xCenter': nbtlib.Int(0),
        'colors': nbtlib.ByteArray(map_colors)
    })
    
    return nbtlib.File({
        'data': data,
        'DataVersion': nbtlib.Int(4189)
    })

if __name__ == "__main__":
    
    import os

    ROOT_DIR = os.path.abspath(os.curdir)
    SRC_DIR = os.path.join(ROOT_DIR, 'src')
    OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

    colors : int8 = []

    colors.append(1)
    colors.append(2)
    colors.append(3)
    colors.append(4)
    colors.append(5)

    # nbt_file = encode_into_map_nbt(colors)
    nbt_file = nbtlib.load(os.path.join(SRC_DIR, 'map_4.dat'))

    print(nbt_file)

    # encode_into_nbt(data)