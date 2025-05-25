import io
import os
import zipfile
from config import ROOT_DIR, SRC_DIR, OUT_DIR

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
        direction: DirectionEnum = None
        ):
        self.name = name
        self.initial_map_id = initial_map_id
        self.total_frames = total_frames
        self.x = x
        self.y = y
        self.z = z
        self.direction = direction

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
        buffer_blocks = self.generate_place_initial_blocks()
        buffer_item_frames = self.summon_item_frames()

        path_datapack = os.path.join(OUT_DIR, f'datapack_{self.name}.zip')
        with zipfile.ZipFile(path_datapack, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Write mcmeta
            content_mcmeta = '{ "pack": { "description": "Animation as Map Art in Minecraft!!!!!!!!", "pack_format": 71 } }'
            zipf.writestr('pack.mcmeta', data=content_mcmeta)

            # Write mfcuntions
            path_mcfunction = os.path.join('data', self.name.lower(), 'function')
            path_initial_blocks = os.path.join(path_mcfunction, 'place_initial_blocks.mcfunction')
            path_summon_item_frames = os.path.join(path_mcfunction, 'summon_item_frames.mcfunction')
            path_build = os.path.join(path_mcfunction, 'build.mcfunction')
            path_clean_item_frames = os.path.join(path_mcfunction, 'clean.mcfunction')

            zipf.writestr(path_initial_blocks, buffer_blocks.getvalue())
            zipf.writestr(path_summon_item_frames, buffer_item_frames.getvalue())
            zipf.writestr(path_build, f'execute as @p run function {self.name}:place_initial_blocks\nexecute as @p run function {self.name}:summon_item_frames')
            
            # cleaning str
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


    def generate_place_initial_blocks(self):
        commands : list[str] = []

        # set commands required for each frame
        if self.direction == DirectionEnum.NORTH.value:
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
            # top
            commands.append(self.get_command_set_block('quartz_block',  self.x,     self.y + 1, '{0}')) # {0} the northest, Y decreases more
            commands.append(self.get_command_set_block('air',           self.x - 1, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x - 2, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x - 3, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('air',           self.x - 4, self.y + 1, '{0}'))
            commands.append(self.get_command_set_block('quartz_block',  self.x - 5, self.y + 1, '{0}'))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                        self.x,     self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_stairs[facing=west,half=top]', self.x - 1, self.y, '{0}'))
            commands.append(self.get_command_set_block('air',                                 self.x - 2, self.y, '{0}'))
            commands.append(self.get_command_set_block('air',                                 self.x - 3, self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_stairs[facing=east,half=top]', self.x - 4, self.y, '{0}'))
            commands.append(self.get_command_set_block('quartz_block',                        self.x - 5, self.y, '{0}'))
            # ice
            commands.append(self.get_command_set_block('packed_ice', self.x - 1, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x - 2, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x - 3, self.y - 1, '{0}'))
            commands.append(self.get_command_set_block('packed_ice', self.x - 4, self.y - 1, '{0}'))
        if self.direction == DirectionEnum.WEST.value:
            # top
            commands.append(self.get_command_set_block('quartz_block',  '{0}', self.y + 1, self.z    )) # {0} the westest, X decreases more
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z - 1))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z - 2))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z - 3))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z - 4))
            commands.append(self.get_command_set_block('quartz_block',  '{0}', self.y + 1, self.z - 5))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                          '{0}', self.y, self.z    ))
            commands.append(self.get_command_set_block('quartz_stairs[facing=north,half=top]',  '{0}', self.y, self.z - 1))
            commands.append(self.get_command_set_block('air',                                   '{0}', self.y, self.z - 2))
            commands.append(self.get_command_set_block('air',                                   '{0}', self.y, self.z - 3))
            commands.append(self.get_command_set_block('quartz_stairs[facing=south,half=top]',  '{0}', self.y, self.z - 4))
            commands.append(self.get_command_set_block('quartz_block',                          '{0}', self.y, self.z - 5))
            # ice
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 2))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 3))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 4))

        # set the commands
        parsed_commands = []
        for index in range(self.total_frames):
            index *= self.mult
            for command in commands:
                parsed_command = ''
                if self.x_axis:
                    parsed_command = command.format(self.x + index)
                else:
                    parsed_command = command.format(self.z + index)
                parsed_commands.append(parsed_command)

        # Store in a buffer and return
        buffer = io.BytesIO()

        for command in parsed_commands:
            buffer.write((command + '\n').encode('utf-8'))
        buffer.seek(0)

        return buffer

    def summon_item_frames(self):
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
        for index in range(self.total_frames):
            parsed_command = ''
            if self.x_axis:
                parsed_command = command.format(
                    x=(x + (self.mult * index)), 
                    y=y, 
                    z=z, 
                    facing=facing_direction, 
                    map_id=(self.initial_map_id + index)
                )
            else:
                parsed_command = command.format(
                    x=x, 
                    y=y, 
                    z=(z + (self.mult * index)), 
                    facing=facing_direction, 
                    map_id=(self.initial_map_id + index)
                )
            parsed_commands.append(parsed_command)

        # Store in a buffer and return
        buffer = io.BytesIO()

        for command in parsed_commands:
            buffer.write((command + '\n').encode('utf-8'))
        buffer.seek(0)

        return buffer

    def get_command_set_block(self, block_name, x, y, z):
        return f'setblock {x} {y} {z} {block_name}'

if __name__ == '__main__':
    datapack_utils = DatapackGeneratorUtils(
        total_frames=4,
        x=-43,
        y=122,
        z=-60,
        direction=DirectionEnum.WEST.value
    )

    datapack_utils.generate_datapack()