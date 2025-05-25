import io
import os
import pprint
import zipfile
from config import ROOT_DIR, SRC_DIR, OUT_DIR
from typing import final

from enums.DirectionEnum import DirectionEnum

class DatapackGeneratorUtils():
    def __init__(
        self,
        name: str = 'default',
        initial_map_id: int = 0,
        total_frames: int = 0,
        x: int = 0,
        y: int = 0,
        z: int = 0,
        direction: DirectionEnum = None,
        delay: int = 0
        ):
        self.name = name
        self.initial_map_id = initial_map_id
        self.total_frames = total_frames
        self.x = x
        self.y = y
        self.z = z
        self.direction = direction
        self.delay = delay

        self.FRAMES_PER_SECOND: final = 40
        self.MAX_COMMANDS_PER_FILE: final = 1000
        self.DELAY_IN_FRAMES: final = self.delay * self.FRAMES_PER_SECOND

        # check if it's either x or z
        self.x_axis: bool = True
        if self.direction == DirectionEnum.NORTH.value or self.direction == DirectionEnum.SOUTH.value:
            self.x_axis = False

        # {0} the northest, Z decreases more
        # {0} the westest, X decreases more
        # {0} the southest, Z increases more
        # {0} the eastest, Z increases more
        self.mult = 1 # My brain isn't brain enough to name this properly
        if self.direction == DirectionEnum.NORTH.value or self.direction == DirectionEnum.WEST.value:
            self.mult = -1

    def generate_datapack(self):
        PLACE_BOAT_NAME: final = 'place_boat'
        PLACE_BLOCKS_NAME: final = 'place_initial_blocks'
        SUMMON_ITEM_FRAMES_NAME: final = 'summon_item_frames'
        CLEAN_NAME: final = 'clean'
        BUILD_NAME: final = 'build'

        buffer_dict_place_blocks = self.generate_place_initial_blocks()
        buffer_dict_item_frames = self.summon_item_frames()

        path_datapack = os.path.join(OUT_DIR, f'datapack_{self.name}.zip')
        with zipfile.ZipFile(path_datapack, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Write mcmeta
            content_mcmeta = '{ "pack": { "description": "Animation as Map Art in Minecraft!!!!!!!!", "pack_format": 71 } }' # 1.21.4
            zipf.writestr('pack.mcmeta', data=content_mcmeta)

            # Write mfcuntions
            path_mcfunction = os.path.join('data', self.name.lower(), 'function')

            path_build = os.path.join(path_mcfunction, f'{BUILD_NAME}.mcfunction')
            path_clean_item_frames = os.path.join(path_mcfunction, f'{CLEAN_NAME}.mcfunction')
            path_place_boat = os.path.join(path_mcfunction, f'{PLACE_BOAT_NAME}.mcfunction')

            # place boat
            place_boat_command = self.get_place_boat_command()
            zipf.writestr(path_place_boat, place_boat_command)

            # place initial blocks & summon item frames
            self.save_command_batches(zipf, path_mcfunction, buffer_dict_place_blocks, PLACE_BLOCKS_NAME)
            self.save_command_batches(zipf, path_mcfunction, buffer_dict_item_frames, SUMMON_ITEM_FRAMES_NAME)

            # doing both placing blocks and later summoning item frames
            str_build = (
                f'execute as @p run function {self.name}:{PLACE_BOAT_NAME}\n' +
                f'execute as @p run function {self.name}:{PLACE_BLOCKS_NAME}\n' +
                f'execute as @p run function {self.name}:{SUMMON_ITEM_FRAMES_NAME}\n'
            )
            zipf.writestr(path_build, str_build)
            
            # cleaning str (it doens't work properly. it only deletes the item frames in the chunks loaded for the player)
            cleaning_str = ''
            cleaning_cmd = [
                'forceload add {x} {z}\n',
                'summon armor_stand {x} {y} {z} {{Tags: [item_frames_killer]}}\n',
                'execute as @e[tag=item_frames_killer] run execute at @s run kill @e[type=item_frame,tag={item_frame_name}]\n'
                'execute as @e[tag=item_frames_killer] run kill\n',
                'forceload remove all\n',
            ]

            for index in range(0, self.total_frames, 16):
                cmd_copy = cleaning_cmd.copy()

                if self.direction == DirectionEnum.NORTH.value:
                    cmd_copy[0] = cmd_copy[0].format(x=self.x, z=(self.z - index))
                    cmd_copy[1] = cmd_copy[1].format(x=self.x, y=self.y, z=(self.z - index))
                if self.direction == DirectionEnum.EAST.value:
                    cmd_copy[0] = cmd_copy[0].format(x=(self.x + index), z=self.z)
                    cmd_copy[1] = cmd_copy[1].format(x=(self.x + index), y=self.y, z=self.z)
                if self.direction == DirectionEnum.SOUTH.value:
                    cmd_copy[0] = cmd_copy[0].format(x=self.x, z=(self.z + index))
                    cmd_copy[1] = cmd_copy[1].format(x=self.x, y=self.y, z=(self.z + index))
                if self.direction == DirectionEnum.WEST.value:
                    cmd_copy[0] = cmd_copy[0].format(x=(self.x - index), z=self.z)
                    cmd_copy[1] = cmd_copy[1].format(x=(self.x - index), y=self.y, z=self.z)
                cmd_copy[2] = cmd_copy[2].format(item_frame_name=self.name)
                
                for cmd in cmd_copy:
                    cleaning_str += cmd

            zipf.writestr(path_clean_item_frames, cleaning_str)


    def generate_place_initial_blocks(self) -> dict[str, io.BytesIO]:
        commands : list[str] = []

        # set commands required for each frame
        if self.direction == DirectionEnum.NORTH.value:
            # barriers covering from gravity blocks
            commands.append(self.get_command_set_block('barrier',       self.x + 1, self.y + 2, '{0}'))
            commands.append(self.get_command_set_block('barrier',       self.x + 2, self.y + 2, '{0}'))
            commands.append(self.get_command_set_block('barrier',       self.x + 3, self.y + 2, '{0}'))
            commands.append(self.get_command_set_block('barrier',       self.x + 4, self.y + 2, '{0}'))
            # top
            commands.append(self.get_command_set_block('quartz_block',  self.x,     self.y + 1, '{0}')) # {0} the northest, Y decreases more
            commands.append(self.get_command_set_block('air',           self.x + 1, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x + 2, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x + 3, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x + 4, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('quartz_block',  self.x + 5, self.y + 1, '{0}'))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                        self.x,     self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_stairs[facing=west,half=top]', self.x + 1, self.y, '{0}'))
            commands.append(self.get_command_set_block('air',                                 self.x + 2, self.y, '{0}'))
            commands.append(self.get_command_set_block('air',                                 self.x + 3, self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_stairs[facing=east,half=top]', self.x + 4, self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_block',                        self.x + 5, self.y, '{0}'))
            # ice
            commands.append(self.get_command_set_block('packed_ice', self.x + 1, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x + 2, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x + 3, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x + 4, self.y - 1, '{0}'))
        if self.direction == DirectionEnum.EAST.value:
            # barriers covering from gravity blocks
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z + 1))
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z + 2))
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z + 3))
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z + 4))
            # top
            commands.append(self.get_command_set_block('quartz_block',  '{0}', self.y + 1, self.z    )) # {0} the westest, X decreases more
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z + 1))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z + 2))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z + 3))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z + 4))
            commands.append(self.get_command_set_block('quartz_block',  '{0}', self.y + 1, self.z + 5))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                          '{0}', self.y, self.z    ))
            commands.append(self.get_command_set_block('quartz_stairs[facing=north,half=top]',  '{0}', self.y, self.z + 1))
            commands.append(self.get_command_set_block('air',                                   '{0}', self.y, self.z + 2))
            commands.append(self.get_command_set_block('air',                                   '{0}', self.y, self.z + 3))
            commands.append(self.get_command_set_block('quartz_stairs[facing=south,half=top]',  '{0}', self.y, self.z + 4))
            commands.append(self.get_command_set_block('quartz_block',                          '{0}', self.y, self.z + 5))
            # ice
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z + 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z + 2))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z + 3))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z + 4))
        if self.direction == DirectionEnum.SOUTH.value:
            # barriers covering from gravity blocks
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z - 1))
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z - 2))
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z - 3))
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z - 4))
            # top
            commands.append(self.get_command_set_block('quartz_block',  self.x,     self.y + 1, '{0}')) # {0} the northest, Y decreases more
            commands.append(self.get_command_set_block('air',           self.x - 1, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x - 2, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x - 3, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x - 4, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('quartz_block',  self.x - 5, self.y + 1, '{0}'))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                        self.x,     self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_stairs[facing=east,half=top]', self.x - 1, self.y, '{0}'))
            commands.append(self.get_command_set_block('air',                                 self.x - 2, self.y, '{0}'))
            commands.append(self.get_command_set_block('air',                                 self.x - 3, self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_stairs[facing=west,half=top]', self.x - 4, self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_block',                        self.x - 5, self.y, '{0}'))
            # ice
            commands.append(self.get_command_set_block('packed_ice', self.x - 1, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x - 2, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x - 3, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x - 4, self.y - 1, '{0}'))
        if self.direction == DirectionEnum.WEST.value:
            # barriers covering from gravity blocks
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z - 1))
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z - 2))
            commands.append(self.get_command_set_block('barrier',       '{0}', self.y + 2, self.z - 3))
            # top
            commands.append(self.get_command_set_block('quartz_block',  '{0}', self.y + 1, self.z    )) # {0} the westest, X decreases more
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z - 1))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z - 2))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z - 3))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z - 4))
            commands.append(self.get_command_set_block('quartz_block',  '{0}', self.y + 1, self.z - 5))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                          '{0}', self.y, self.z    ))
            commands.append(self.get_command_set_block('quartz_stairs[facing=south,half=top]',  '{0}', self.y, self.z - 1))
            commands.append(self.get_command_set_block('air',                                   '{0}', self.y, self.z - 2))
            commands.append(self.get_command_set_block('air',                                   '{0}', self.y, self.z - 3))
            commands.append(self.get_command_set_block('quartz_stairs[facing=north,half=top]',  '{0}', self.y, self.z - 4))
            commands.append(self.get_command_set_block('quartz_block',                          '{0}', self.y, self.z - 5))
            # ice
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 2))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 3))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 4))

        # set the commands
        parsed_commands = []
        for index in range(self.total_frames + self.DELAY_IN_FRAMES):
            index *= self.mult
            for command in commands:
                parsed_command = ''
                if self.x_axis:
                    parsed_command = command.format(self.x + index)
                else:
                    parsed_command = command.format(self.z + index)
                parsed_commands.append(parsed_command)

        return self.generate_command_batches(parsed_commands, 'place_initial_blocks')

    def summon_item_frames(self) -> dict[str, io.BytesIO]:
        # Item Frames have 6 possible places they face.
        # We're deciding the facing direction according the direction requested
        # Double bracket is used in order to escape literal curly braces in a format string avoiding python interpreter
        facing_direction = 0
        x = self.x
        y = self.y + 1
        z = self.z
        command = 'summon item_frame {x} {y} {z} {{Tags: [' + self.name + '], Facing:{facing}b, Item:{{id: "minecraft:filled_map", components:{{"minecraft:map_id":{map_id}}}}}}}'
        if self.direction == DirectionEnum.NORTH.value:
            facing_direction = 5
            x = self.x + 1
        if self.direction == DirectionEnum.EAST.value:
            facing_direction = 3
            z = self.z + 1
        if self.direction == DirectionEnum.SOUTH.value:
            facing_direction = 4
            x = self.x - 1
        if self.direction == DirectionEnum.WEST.value:
            facing_direction = 2
            z = self.z - 1
        
        parsed_commands: list[str] = []

        # delay
        for index in range(self.DELAY_IN_FRAMES):
            parsed_command = ''
            if self.x_axis:
                parsed_command = command.format(
                    x=(x + (self.mult * index)), 
                    y=y, 
                    z=z, 
                    facing=facing_direction, 
                    map_id=(self.initial_map_id)
                )
            else:
                parsed_command = command.format(
                    x=x, 
                    y=y, 
                    z=(z + (self.mult * index)), 
                    facing=facing_direction, 
                    map_id=(self.initial_map_id)
                )
            parsed_commands.append(parsed_command)

        # actual frames
        for index in range(self.DELAY_IN_FRAMES, self.total_frames + self.DELAY_IN_FRAMES):
            parsed_command = ''
            if self.x_axis:
                parsed_command = command.format(
                    x=(x + (self.mult * index)), 
                    y=y, 
                    z=z, 
                    facing=facing_direction, 
                    map_id=(self.initial_map_id + index - self.DELAY_IN_FRAMES)
                )
            else:
                parsed_command = command.format(
                    x=x, 
                    y=y, 
                    z=(z + (self.mult * index)), 
                    facing=facing_direction, 
                    map_id=(self.initial_map_id + index - self.DELAY_IN_FRAMES)
                )
            parsed_commands.append(parsed_command)

        return self.generate_command_batches(parsed_commands, 'summon_item_frames')

    def get_place_boat_command(self) -> str:
        command = 'summon minecraft:birch_boat {x} {y} {z} {{Rotation:[{x_rotation}f,0.0f]}}'
        x_rotation: float = 0
        x: float = self.x
        y: float = self.y
        z: float = self.z
        if self.direction == DirectionEnum.NORTH.value:
            x += 2.0
            x_rotation = 180.0
            pass
        if self.direction == DirectionEnum.EAST.value:
            z += 2.0
            x_rotation = -90.0
            pass
        if self.direction == DirectionEnum.SOUTH.value:
            x -= 2.0
            x_rotation = 0
            pass
        if self.direction == DirectionEnum.WEST.value:
            z -= 2.0
            x_rotation = 90.0
            pass

        return command.format(
            x=str(round(x, 1)),
            y=str(round(y, 1)),
            z=str(round(z, 1)),
            x_rotation=str(round(x_rotation, 1))
        )

    def generate_command_batches(
        self,
        commands: list[str],
        filename: str
        ) -> dict[str, io.BytesIO]:
        # Store commands in a buffer list
        buffers: dict[str, io.BytesIO] = {}

        counter = 1
        first_iteration = 1
        for index, cmd in enumerate(commands):
            if index % self.MAX_COMMANDS_PER_FILE == 0:
                if not first_iteration:
                    buffer.seek(0)
                    buffers[f'{filename}_{counter}'] = buffer
                    counter += 1
                buffer = io.BytesIO()
                first_iteration = 0

            buffer.write((cmd + '\n').encode('utf-8'))

        if index % self.MAX_COMMANDS_PER_FILE != 0:
            buffer.seek(0)
            buffers[f'{filename}_{counter}'] = buffer
        
        return buffers

    def save_command_batches(
        self,
        zipf: zipfile.ZipFile,
        base_path: str,
        buffer_dict: dict[str, io.BytesIO],
        filename: str
        ):
        path_main = os.path.join(base_path, f'{filename}.mcfunction')
        path_main_folder = os.path.join(base_path, filename)
        buffer = io.BytesIO()
        counter = 1
        for key, value in buffer_dict.items():
            # save ith buffer
            curr_path = os.path.join(path_main_folder, f'{key}.mcfunction')
            zipf.writestr(curr_path, value.getvalue())
            # add to general place initial block call
            command = f'schedule function {self.name}:{filename}/{key} {counter}t'
            counter += 1
            buffer.write((command + '\n').encode('utf-8'))
        # save general place initial block buffer into a file
        buffer.seek(0)
        zipf.writestr(path_main, buffer.getvalue())
        pass

    def get_command_set_block(self, block_name, x, y, z):
        return f'setblock {x} {y} {z} {block_name}'

if __name__ == '__main__':
    datapack_utils = DatapackGeneratorUtils(
        name='odore_china',
        total_frames=1000,
        x=-10,
        y=-60,
        z=120,
        direction=DirectionEnum.NORTH.value
    )
    
    datapack_utils.generate_datapack()
    
    # d = datapack_utils.generate_place_initial_blocks()
    # for key, value in d.items():
    #     print(key, value.getvalue())

