'''

'''
import sys
from pathlib import Path
from os import remove
from json import dump, load

class PathConstants():
    '''
    The MainPaths class is responsible for defining the paths to various
    directories and files used in the program.

    Example Usage:
    paths = MainPaths()
    print(paths.CURRENT_PATH)  # Output: The current working directory
    print(paths.DATA_PATH)  # Output: The path to the 'Data' directory
    print(paths.RESOURCES_PATH)  # Output: The path to the 'Resources' directory
    print(paths.SOLUTIONS_PATH)  # Output: The path to the 'Solutions' directory
    ...

    Fields:
    - CURRENT_PATH: Represents the current working directory.
    - DATA_PATH: Represents the path to the 'Data' directory.
    - RESOURCES_PATH: Represents the path to the 'Resources' directory.
    - SOLUTIONS_PATH: Represents the path to the 'Solutions' directory.
    - SOUNDS_PATH: Represents the path to the 'Sounds' directory.
    - STRINGS_PATH: Represents the path to the 'Strings' directory.
    - TEXTURES_PATH: Represents the path to the 'Textures' directory.
    - WORLDS_PATH: Represents the path to the 'Worlds' directory.

    - FACES_PATH: Represents the path to the 'Faces' directory.
    - ICONS_PATH: Represents the path to the 'Icons' directory.

    - GLOBALS_PATH: Represents the path to the 'Globals.json' file.
    - OVERLAYS_PATH: Represents the path to the 'Walk_Overlays.json' file.
    - ACTIVITIES_PATH: Represents the path to the 'Activities.json' file.
    '''

    def __init__(self):
        '''
        Initializes the MainPaths object and sets the paths to various
        directories and files used in the program.
        '''

        self.CURRENT_PATH: Path = self._get_current_path()
        self.DATA_PATH: Path = self.CURRENT_PATH / 'Data'

        self.RESOURCES_PATH: Path = self.DATA_PATH / 'Resources'
        self.SOLUTIONS_PATH: Path = self.DATA_PATH / 'Solutions'
        self.SOUNDS_PATH: Path = self.DATA_PATH / 'Sounds'
        self.STRINGS_PATH: Path = self.DATA_PATH / 'Strings'
        self.TEXTURES_PATH: Path = self.DATA_PATH / 'Textures'
        self.WORLDS_PATH: Path = self.DATA_PATH / 'Worlds'

        self.FACES_PATH: Path = self.TEXTURES_PATH / 'Faces'
        self.ICONS_PATH: Path = self.RESOURCES_PATH / 'Icons'

        self.GLOBALS_PATH: Path = self.STRINGS_PATH / 'Globals.json'
        self.OVERLAYS_PATH: Path = self.STRINGS_PATH / 'Walk_Overlays.json'
        self.ACTIVITIES_PATH: Path = self.STRINGS_PATH / 'Activities.json'

    def _get_current_path(self) -> Path:
        '''
        Returns the current working directory.

        Returns:
        Path object representing the current working directory.
        '''

        if hasattr(sys, 'frozen') and hasattr(sys, "_MEIPASS"):
            return Path(sys.executable).resolve().parent
        else:
            return Path.cwd()
        
    def get_globals(self) -> dict:
        '''
        Return Globals.json as a dictionary.

        Returns:
        A dictionary representing the contents of the Globals.json file.
        '''
        return load(open(paths.GLOBALS_PATH))


    def get_overlays(self) -> dict:
        '''
        Return Walk_Overlays.json as a dictionary.

        Returns:
        A dictionary representing the contents of the Walk_Overlays.json file.
        '''
        return load(open(paths.OVERLAYS_PATH))


    def get_activities(self) -> dict:
        '''
        Return Activities.json as a dictionary.

        Returns:
        A dictionary representing the contents of the Activities.json file.
        '''
        return load(open(paths.ACTIVITIES_PATH))
        
paths = PathConstants()

class Profile():
    '''
    The `Profile` class provides methods for creating and deleting NPC solution files.

    Methods:
    - load_profiles(cls) -> list: Load NPC solutions from paths.SOLUTIONS_PATH as a list of filenames without extensions.
    - create_profile(cls, name: str): Create a new NPC solution file.
    - delete_profile(cls, name: str): Delete specified NPC solution file.
    '''

    def __init__(self):
        pass

    @classmethod
    def load_profiles(cls) -> list:
        '''
        Load NPC solutions from paths.SOLUTIONS_PATH as a list of filenames
        without extensions.

        Returns:
        - A list of filenames without extensions, representing the NPC solution files in the specified directory.
        '''
        return [i.stem for i in paths.SOLUTIONS_PATH.iterdir() if '.json' in str(i)]

    @classmethod 
    def create_profile(cls, name: str):
        '''
        Create a new NPC solution file.

        Args:
            name (str): The name of the NPC solution file to be created.

        Returns:
            None

        Example Usage:
            profile = Profile()
            profile.create_profile('npc_solution')

        Code Analysis:
            - Open a file with the specified name and '.json' extension in the specified path using the `open` function.
            - Use the `dump` function from the `json` module to write an empty string to the file.
            - Close the file.
        '''
        with open(paths.SOLUTIONS_PATH / f'{name}.json', 'w') as profile:
            dump('', profile)

    @classmethod
    def delete_profile(cls, name: str):
        '''
        Delete specified NPC solution file.

        Args:
            name (str): The name of the NPC solution file to be deleted.

        Returns:
            None

        Example Usage:
            profile = Profile()
            profile.delete_profile('npc_solution')
        '''
        remove(paths.SOLUTIONS_PATH / f'{name}.json')

    @classmethod
    def extract_data(cls, widget: dict) -> tuple[dict, dict]:
        '''
        '''
        attributes_control: str = widget['Stats'].var_radio_option.get()
        melee_equipped: bool = bool(
            widget['Inventory'].var_label_equipped_melee.get()
        )
        ranged_equipped: bool = bool(
            widget['Inventory'].var_label_equipped_ranged.get()
        )
        
        routine_exists: bool = bool(
            widget['Routine'].routines
        )

        solution_info = dict()

        solution_info['level'] = widget['Main'].var_entry_level.get()
        solution_info['id'] = widget['Main'].var_entry_id.get()
        solution_info['name'] = widget['Main'].var_entry_name.get()
        solution_info['guild'] = widget['Main'].var_combo_guild.get()
        solution_info['voice'] = widget['Main'].var_combo_voice.get().replace('SVM_','')
        solution_info['flags'] = widget['Main'].var_combo_flag.get()
        solution_info['npctype'] = widget['Main'].var_combo_type.get()
        
        visual_params = list()
        visual_params.append(widget['Visual'].var_radio_gender.get())
        visual_params.append(widget['Visual'].var_combo_head.get())
        visual_params.append(widget['Visual'].var_listbox_face.get())
        visual_params.append(widget['Visual'].var_combo_skin.get())
        visual_params.append(widget['Visual'].var_combo_outfit.get())

        solution_info['B_SetNpcVisual'] = visual_params

        solution_info['Mdl_SetModelFatness'] = round(widget['Visual'].var_scale_fatness.get(), 2)
        solution_info['Mdl_ApplyOverlayMds'] = widget['Visual'].var_combo_walk_overlay.get()

        solution_info['fight_tactic'] = widget['Stats'].var_combo_fight_tactic.get() 
        solution_info['B_GiveNpcTalents'] = widget['Stats'].var_check_talents.get()
        solution_info['B_SetFightSkills'] = widget['Stats'].var_entry_fightskill.get()


        match attributes_control:
            case 'manual':
                solution_info['ATR_HITPOINTS_MAX'] = widget['Stats'].var_current_stat[4].get()
                solution_info['ATR_MANA_MAX'] = widget['Stats'].var_current_stat[5].get()
                solution_info['ATR_STRENGTH'] = widget['Stats'].var_current_stat[6].get()
                solution_info['ATR_DEXTERITY'] = widget['Stats'].var_current_stat[7].get()
            case 'auto':
                solution_info['B_SetAttributesToChapter'] = widget['Stats'].var_spinbox_chapter.get()

        melee = str()
        ranged = str()
        
        if melee_equipped:
            melee = ' '.join(widget['Inventory'].var_label_equipped_melee.get().split()[1::])
            solution_info['EquipItem'] = melee
        if ranged_equipped:
            ranged = ' '.join(widget['Inventory'].var_label_equipped_ranged.get().split()[1::])
            solution_info['EquipItem'] = ranged
        if melee_equipped and ranged_equipped:
            solution_info['EquipItem'] = [
                melee,
                ranged
            ]

        item_ids = widget['Inventory'].treeview_inv.get_children('')
        items = list()
        for item_id in item_ids:
            items.append(
                [
                    widget['Inventory'].treeview_inv.item(item_id)['values'][1],
                    widget['Inventory'].treeview_inv.item(item_id)['values'][2]
                ]
            )

        solution_info['CreateInvItems'] = items
        solution_info['B_CreateAmbientInv'] = widget['Inventory'].var_check_add_amb_inv.get()

        if routine_exists:
            for rtn_name in widget['Routine'].routines.keys():
                if 'start_' in rtn_name.lower():
                    solution_info['daily_routine'] = rtn_name

        return (solution_info, widget['Routine'].routines)
    
    @classmethod
    def construct_script(cls, data: tuple[dict, dict]) -> str:
        routines: dict = data[1]
        solution: dict = data[0]

        strings = list()
        for data_type in solution:
            if not any(
                [
                    'B_SetAttributesToChapter' in data_type,
                    'B_GiveNpcTalents' in data_type,
                    'B_SetFightSkills' in data_type,
                    'EquipItem' in data_type,
                    'B_CreateAmbientInv' in data_type,
                    'Mdl_SetModelFatness' in data_type,
                    'Mdl_ApplyOverlayMds' in data_type,
                    'B_SetNpcVisual' in data_type,
                    'CreateInvItems' in data_type
                ]
            ):
                if 'ATR_' in data_type:
                    string = f'attribute[{data_type}] = {solution[data_type]};'
                    strings.append('\t' + string)
                    continue
                if data_type == 'name':
                    string = f'{data_type} = "{solution[data_type]}";'
                    strings.append('\t' + string)
                    continue
                string = f'{data_type} = {solution[data_type]};'
                strings.append('\t' + string)
            else:
                match data_type:
                    case 'B_SetAttributesToChapter':
                        string = f'{data_type} (self, {solution[data_type]});'
                        strings.append('\t' + string)
                    case 'B_GiveNpcTalents':
                        if solution[data_type]:
                            string = f'{data_type} (self);'
                            strings.append('\t' + string)
                    case 'B_SetFightSkills':
                        string = f'{data_type} (self, {solution[data_type]});'
                        strings.append('\t' + string)
                    case 'EquipItem':
                        if isinstance(solution[data_type], list):
                            for item in solution[data_type]:
                                string = f'{data_type} (self, {item});'
                                strings.append('\t' + string)
                        else:
                            string = f'{data_type} (self, {solution[data_type]});'
                            strings.append('\t' + string)
                    case 'B_CreateAmbientInv':
                        if solution[data_type]:
                            string = f'{data_type} (self);'
                            strings.append('\t' + string)
                    case 'Mdl_SetModelFatness':
                        string = f'{data_type} (self, {solution[data_type]});'
                        strings.append('\t' + string)
                    case 'Mdl_ApplyOverlayMds':
                        string = f'{data_type} (self, "{solution[data_type]}.mds");'
                        strings.append('\t' + string)
                    case 'B_SetNpcVisual':
                        string = '{d} (self, {g}, {h}, {f}, {s}, {o});'.format(
                            d = data_type,
                            g = solution[data_type][0],
                            h = solution[data_type][1],
                            f = solution[data_type][2],
                            s = solution[data_type][3],
                            o = solution[data_type][4]
                        )
                        strings.append('\t' + string)
                    case 'CreateInvItems':
                        for item in solution[data_type]:
                            string = f'{data_type} (self, {item[0]}, {item[1]});'
                            strings.append('\t' + string)
        
        if solution['guild']:
            script = f"instance {solution['guild'].split('_')[1]}_{solution['name']}_{solution['id']} (NPC_Default)"
        else:
            script = f"instance NONE_{solution['name']}_{solution['id']} (NPC_Default)"
        script += ' {\n'
        script += '\n'.join(strings)
        script += '\n};\n'
        
        for routine_name in routines:
            script += '\n'
            script += f'func void {routine_name} ()'
            script += ' {\n'
            for entry in routines[routine_name]:
                activity = entry["activity"]
                start = ', '.join(entry["start_time"].split())
                end = ', '.join(entry["end_time"].split())
                waypoint = entry["waypoint"]
                script += f'\t{activity} ({start}, {end}, "{waypoint}");\n'
            script += '\n'
            script += '};\n'
        
        print(script)
        return script

class NPC():
    """
    The `NPC` class provides methods for retrieving and manipulating data related to NPCs (non-player characters) in a game. It includes methods for getting guilds, voices, types, outfits, fight tactics, and actions. It also includes methods for adding and removing overlays, head meshes, and skin textures. Additionally, it has a method for creating NPC routines.

    Example Usage:
        npc = NPC()

        # Get the default and custom guilds
        guilds = npc.get_guilds(constants_path)
        print(guilds)  # Output: {'default': [...], 'custom': [...]}

        # Get the default and custom voices
        voices = npc.get_voices(svm_path)
        print(voices)  # Output: {'default': [...], 'custom': [...]}

        # Get the default and custom types
        types = npc.get_types(ai_constants_path)
        print(types)  # Output: {'default': [...], 'custom': [...]}

        # Get the default and custom outfits
        outfits = npc.get_outfits(items_path)
        print(outfits)  # Output: {'default': ([...], [...]), 'custom': ([...], [...])}

        # Get the default and custom fight tactics
        fight_tactics = npc.get_fight_tactics(ai_constants_path)
        print(fight_tactics)  # Output: {'default': [...], 'custom': [...]}

        # Get the default and custom actions
        actions = npc.get_actions(ta_path)
        print(actions)  # Output: {'default': [...], 'custom': [...]}

        # Add an overlay
        npc.add_overlay(name)

        # Delete an overlay
        npc.delete_overlay(name)

        # Add a head mesh
        npc.add_head_mesh(name, gender)

        # Remove a head mesh
        npc.remove_head_mesh(name, gender)

        # Add a skin texture
        npc.add_skin_tex(name, gender)

        # Remove a skin texture
        npc.remove_skin_tex(name, gender)

        # Create an NPC routine
        routine = npc.create_routine(activity, start_time, end_time, waypoint)
        print(routine)  # Output: {'activity': ..., 'start_time': ..., 'end_time': ..., 'waypoint': ...}

    Main functionalities:
    - Get guilds: Retrieves the default and custom guilds for NPCs.
    - Get voices: Retrieves the default and custom voices for NPCs.
    - Get types: Retrieves the default and custom types for NPCs.
    - Get outfits: Retrieves the default and custom outfits for NPCs.
    - Get fight tactics: Retrieves the default and custom fight tactics for NPCs.
    - Get actions: Retrieves the default and custom actions for NPCs.
    - Add overlay: Adds a custom overlay for NPCs.
    - Delete overlay: Deletes a custom overlay for NPCs.
    - Add head mesh: Adds a custom head mesh for NPCs.
    - Remove head mesh: Removes a custom head mesh for NPCs.
    - Add skin texture: Adds a custom skin texture for NPCs.
    - Remove skin texture: Removes a custom skin texture for NPCs.
    - Create routine: Creates an NPC routine with specified activity, start time, end time, and waypoint.

    Methods:
    - get_guilds(constants_path: str) -> dict: Retrieves the default and custom guilds for NPCs based on the constants file path.
    - get_voices(svm_path: str) -> dict: Retrieves the default and custom voices for NPCs based on the SVM file path.
    - get_types(ai_constants_path: str) -> dict: Retrieves the default and custom types for NPCs based on the AI constants file path.
    - get_outfits(items_path: str) -> dict: Retrieves the default and custom outfits for NPCs based on the items file path.
    - get_fight_tactics(ai_constants_path: str) -> dict: Retrieves the default and custom fight tactics for NPCs based on the AI constants file path.
    - get_actions(ta_path: str) -> dict: Retrieves the default and custom actions for NPCs based on the TA file path.
    - add_overlay(name: str): Adds a custom overlay for NPCs with the specified name.
    - delete_overlay(name: str): Deletes a custom overlay for NPCs with the specified name.
    - add_head_mesh(name: str, gender: int): Adds a custom head mesh for NPCs with the specified name and gender.
    - remove_head_mesh(name: str, gender: int): Removes a custom head mesh for NPCs with the specified name and gender.
    - add_skin_tex(name: str, gender: int): Adds a custom skin texture for NPCs with the specified name and gender.
    - remove_skin_tex(name: str, gender: int): Removes a custom skin texture for NPCs with the specified name and gender.
    - create_routine(activity: str, start_time: str, end_time: str, waypoint: str) -> dict: Creates an NPC routine with the specified activity, start time, end time, and waypoint.

    Fields:
    None.
    """
    def __init__(self):
        pass       
    
    @classmethod
    def get_guilds(cls, constants_path: str) -> dict:
        """
        Retrieves the default and custom guilds for NPCs based on the constants file path.

        Args:
            constants_path (str): The path to the constants file.

        Returns:
            dict: A dictionary with the default and custom guilds for NPCs.
        """
        if not constants_path or not Path(constants_path).is_dir():
            return
        
        path = Path(constants_path) / 'Constants.d'
        guilds : list = list()

        with open(
            path,
            'rt',
            encoding = 'Windows-1252'
        ) as constants:
            lines = constants.readlines()
            for line in lines:
                if 'GIL_EMPTY_D' in line:
                    break
                if 'GIL_HUMAN' in line:
                    continue
                if 'const int GIL_' in line:
                    guilds.append(line.split()[2])
        buffer : dict = paths.get_globals()
        default_guilds : list = buffer['NPC']['guild']['default']
        custom_guilds : list = list()

        for guild in guilds:
            if guild in default_guilds:
                continue
            else:
                custom_guilds.append(guild)

        buffer['NPC']['guild']['custom'] = custom_guilds

        with open(paths.GLOBALS_PATH, 'w') as globals:
            dump(buffer, globals, indent=4)

        return {'default': default_guilds, 'custom': custom_guilds}
    
    @classmethod
    def get_voices(cls, svm_path: str) -> dict:
        """
        Retrieves the default and custom voices for NPCs based on the SVM file path.

        Args:
            svm_path (str): The path to the SVM file.

        Returns:
            dict: A dictionary with the default and custom voices for NPCs.
        """
        if not svm_path or not Path(svm_path).is_dir():
            return
        
        path = Path(svm_path) / 'SVM.d'
        voices : list = list()

        with open(
            path,
            'rt',
            encoding = 'Windows-1252'
        ) as svms:
            lines = svms.readlines()
            for line in lines:
                if 'instance' and '(C_SVM)' in line:
                    index = lines.index(line)
                    if not '}' in lines[index+3]:
                        voices.append(line.split()[1])
        buffer : dict = paths.get_globals()
        default_voices : list = buffer['NPC']['voice']['default']
        custom_voices : list = list()

        for voice in voices:
            if voice in default_voices:
                continue
            else:
                custom_voices.append(voice)

        buffer['NPC']['voice']['custom'] = custom_voices

        with open(paths.GLOBALS_PATH, 'w') as globals:
            dump(buffer, globals, indent=4)

        return {'default': default_voices, 'custom': custom_voices}
    
    @classmethod
    def get_types(cls, ai_constants_path: str) -> dict:
        """
        Retrieves the default and custom types for NPCs based on the AI constants file path.
    
        Args:
            ai_constants_path (str): The path to the AI constants file.
    
        Returns:
            dict: A dictionary with the default and custom types for NPCs.
    
        Example Usage:
            npc = NPC()
            types = npc.get_types(ai_constants_path)
            print(types)  # Output: {'default': [...], 'custom': [...]}    
        """
        if not ai_constants_path or not Path(ai_constants_path).is_dir():
            return
        
        path = Path(ai_constants_path) / 'AI_Constants.d'
        types: list = list()
        buffer : dict = paths.get_globals()
        default_types : list = buffer['NPC']['type']['default']
        custom_types : list = list()

        with open(
            path,
            'rt',
            encoding='Windows-1252'
        ) as ai_constants:
            lines = ai_constants.readlines()
            for line in lines:
                if 'const int NPCTYPE_' in line:
                    types.append(line.split()[2])

        for type in types:
            if type in default_types:
                continue
            else:
                custom_types.append(type)

        buffer['NPC']['type']['custom'] = custom_types

        with open(paths.GLOBALS_PATH, 'w') as globals:
            dump(buffer, globals, indent=4)

        return {'default': default_types, 'custom': custom_types}
    
    @classmethod
    def get_outfits(cls, items_path: str) -> dict:
        """
        Retrieves the default and custom outfits for NPCs based on the items file path.

        Args:
            items_path (str): The path to the items file.

        Returns:
            dict: A dictionary with the default and custom outfits for NPCs. The default outfits are grouped by gender ('male' and 'female'), and the custom outfits are also grouped by gender.
        """
        if not items_path or not Path(items_path).is_dir():
            return

        path1 = Path(items_path) / 'IT_Armor.d'
        path2 = Path(items_path) / 'IT_Addon_Armor.d'
        buffer : dict = paths.get_globals()
        outfits : list = list()
        default : list = [
            i.lower() for i in
            buffer['NPC']['outfit']['default']['male']
            +buffer['NPC']['outfit']['default']['female']
        ]
        custom : dict = dict()

        with open(
            path1,
            'rt'
        ) as data:
            lines = data.readlines()
            for line in lines:
                if any(
                    'INSTANCE' in line,
                    'instance' in line
                ) and any(
                    '(C_ITEM)' in line,
                    '(C_Item)' in line
                ) and not all(
                    [
                        'ITAR_DJG_BABE' in line
                    ]
                ):
                    outfit = line.split()[1].replace('(C_ITEM)','')
                    outfit = outfit.replace('(C_Item)','')
                    if outfit.lower() not in default:
                        outfits.append(outfit)
                    
        with open(
            path2,
            'rt'
        ) as data:
            lines = data.readlines()
            for line in lines:
                if any(
                    'INSTANCE' in line,
                    'instance' in line
                ) and any(
                    '(C_ITEM)' in line,
                    '(C_Item)' in line
                ):
                    outfit = line.split()[1].replace('(C_ITEM)','')
                    outfit = outfit.replace('(C_Item)','')
                    if outfit.lower() not in default:
                        outfits.append(outfit)

        custom['male'] = outfits
        custom['female'] = outfits
        buffer['NPC']['outfit']['custom'] = custom

        with open(paths.GLOBALS_PATH, 'w') as globals:
            dump(buffer, globals, indent=4)
    
        return {
            'default': (
                    paths.get_globals()['NPC']['outfit']['default']['male'],
                    paths.get_globals()['NPC']['outfit']['default']['female']
                ),
            'custom': (
                    custom['male'],
                    custom['female']
                )
            }

    @classmethod
    def get_fight_tactics(cls, ai_constants_path: str) -> dict:
        """
        Retrieves the default and custom fight tactics for NPCs based on the AI constants file path.

        Args:
            ai_constants_path (str): The path to the AI constants file.

        Returns:
            dict: A dictionary with the default and custom fight tactics for NPCs. The dictionary has the keys 'default' and 'custom', and the values are lists of fight tactic names.
        """
        if not ai_constants_path or not Path(ai_constants_path).is_dir():
            return

        path = Path(ai_constants_path) / 'AI_Constants.d'
        fight_tactics: list = list()
        buffer : dict = paths.get_globals()
        default_fight_tactics : list = buffer['NPC']['fight_tactic']['default']
        custom_fight_tactics : list = list()

        with open(
            path,
            'rt',
            encoding='Windows-1252'
        ) as ai_constants:
            lines = ai_constants.readlines()
            for line in lines:
                if 'const int FAI_HUMAN_' in line:
                    fight_tactics.append(line.split()[2])

        for fight_tactic in fight_tactics:
            if fight_tactic in default_fight_tactics:
                continue
            else:
                custom_fight_tactics.append(fight_tactic)

        buffer['NPC']['fight_tactic']['custom'] = custom_fight_tactics

        with open(paths.GLOBALS_PATH, 'w') as globals:
            dump(buffer, globals, indent=4)

        return {'default': default_fight_tactics, 'custom': custom_fight_tactics}
    
    @classmethod
    def get_actions(cls, ta_path: str) -> dict:
        """
        Retrieves the default and custom actions for NPCs based on the TA file path.

        Args:
            ta_path (str): The path to the TA file.

        Returns:
            dict: A dictionary with the default and custom actions for NPCs. The keys are 'default' and 'custom', and the values are lists of activity names.
        """
        if not ta_path or not Path(ta_path).is_dir():
            return
        
        path = Path(ta_path) / 'TA.d'
        activities = list()
        buffer : dict = paths.get_activities()
        default_activities : list = buffer['default']
        custom_activities = list()

        with open(
            path,
            'rt',
            encoding='Windows-1252'
        ) as ta:
            lines = ta.readlines()
            for line in lines:
                if 'func void TA_' in line:
                    activities.append(line.split()[2])

        for activity in activities:
            if activity in default_activities:
                continue
            else:
                custom_activities.append(activity)

        buffer['custom'] = custom_activities

        with open(paths.ACTIVITIES_PATH, 'w') as activities_json:
            dump(buffer, activities_json, indent=4)

        return {'default': default_activities, 'custom': custom_activities}
    
    @classmethod
    def add_overlay(cls, name: str):
        """
        Adds a custom overlay for NPCs by appending the overlay name to the 'custom' list in the 'overlay' dictionary.
        The updated dictionary is then saved to a JSON file.

        :param name: The name of the custom overlay to be added.
        :type name: str
        :return: None
        """
        result: dict = dict()
        buffer: dict = load(
            open(paths.STRINGS_PATH / f'Walk_Overlays.json')
        )['overlay']

        buffer['custom'].append(name)
        result['overlay'] = buffer

        with open(
            paths.STRINGS_PATH / f'Walk_Overlays.json', 'w'
        ) as profile:
            dump(result, profile, indent=4)

    @classmethod
    def delete_overlay(cls, name: str):
        """
        Deletes a custom overlay for NPCs.

        Args:
            name (str): The name of the custom overlay to be deleted.

        Returns:
            None
        """
        result : dict = dict()
        buffer : dict = load(
            open(paths.STRINGS_PATH / f'Walk_Overlays.json')
        )['overlay']

        buffer['custom'].remove(name)
        result['overlay'] = buffer

        with open(
            paths.STRINGS_PATH / f'Walk_Overlays.json', 'w'
        ) as profile:
            dump(result, profile, indent=4)

    @classmethod
    def add_head_mesh(cls, name: str, gender: int):
        """
        Add a custom head mesh for NPCs based on the specified name and gender.

        Args:
            name (str): The name of the custom head mesh.
            gender (int): The gender of the NPCs for which the custom head mesh is being added.
            0 represents male and 1 represents female.

        Returns:
            None
        """
        match gender:
            case 0:
                buffer : dict = paths.get_globals()
                default : list = buffer['NPC']['head']['male']['default']
                custom : list = list()
                if name not in default:
                    custom.append(name)
                buffer['NPC']['head']['male']['custom'] = custom
                with open(paths.GLOBALS_PATH, 'w') as globals:
                    dump(buffer, globals, indent=4)
            case 1:
                buffer : dict = paths.get_globals()
                default : list = buffer['NPC']['head']['female']['default']
                custom : list = list()
                if name not in default:
                    custom.append(name)
                buffer['NPC']['head']['female']['custom'] = custom
                with open(paths.GLOBALS_PATH, 'w') as globals:
                    dump(buffer, globals, indent=4)

    @classmethod
    def remove_head_mesh(cls, name: str, gender: int):
        """
        Removes a custom head mesh for NPCs based on the specified name and gender.

        Args:
            name (str): The name of the custom head mesh to be removed.
            gender (int): The gender of the NPCs for which the custom head mesh should be removed. 
                          0 represents male NPCs and 1 represents female NPCs.

        Returns:
            None

        Example Usage:
            npc = NPC()
            npc.remove_head_mesh('mesh_name', 0)
        """
        match gender:
            case 0:
                buffer : dict = paths.get_globals()
                custom : list = buffer['NPC']['head']['male']['custom']
                if name in custom:
                    custom.remove(name)
                buffer['NPC']['head']['male']['custom'] = custom
                with open(paths.GLOBALS_PATH, 'w') as globals:
                    dump(buffer, globals, indent=4)
            case 1:
                buffer : dict = paths.get_globals()
                custom : list = buffer['NPC']['head']['female']['custom']
                if name in custom:
                    custom.remove(name)
                buffer['NPC']['head']['female']['custom'] = custom
                with open(paths.GLOBALS_PATH, 'w') as globals:
                    dump(buffer, globals, indent=4)

    @classmethod
    def add_skin_tex(cls, name: str, gender: int):
        """
        Adds a custom skin texture for NPCs based on the specified name and gender.

        Args:
            name (str): The name of the custom skin texture to be added.
            gender (int): The gender of the NPCs for which the custom skin texture should be added. 
                          0 represents male NPCs and 1 represents female NPCs.

        Returns:
            None

        Example Usage:
            npc = NPC()
            npc.add_skin_tex('custom_skin', 0)
        """
        match gender:
            case 0:
                buffer : dict = paths.get_globals()
                default : list = buffer['NPC']['skin']['male']['default']
                custom : list = list()
                if name not in default:
                    custom.append(name)
                buffer['NPC']['skin']['male']['custom'] = custom
                with open(paths.GLOBALS_PATH, 'w') as globals:
                    dump(buffer, globals, indent=4)
            case 1:
                buffer : dict = paths.get_globals()
                default : list = buffer['NPC']['skin']['female']['default']
                custom : list = list()
                if name not in default:
                    custom.append(name)
                buffer['NPC']['skin']['female']['custom'] = custom
                with open(paths.GLOBALS_PATH, 'w') as globals:
                    dump(buffer, globals, indent=4)

    @classmethod
    def remove_skin_tex(cls, name: str, gender: int):
        """
        Remove a custom skin texture for NPCs.

        Args:
            name (str): The name of the skin texture to be removed.
            gender (int): The gender of the NPC. 0 represents male and 1 represents female.

        Returns:
            None

        Raises:
            None

        Example Usage:
            npc = NPC()
            npc.remove_skin_tex('skin_texture_1', 0)
        """
        match gender:
            case 0:
                buffer : dict = paths.get_globals()
                custom : list = buffer['NPC']['skin']['male']['custom']
                if name in custom:
                    custom.remove(name)
                buffer['NPC']['skin']['male']['custom'] = custom
                with open(paths.GLOBALS_PATH, 'w') as globals:
                    dump(buffer, globals, indent=4)
            case 1:
                buffer : dict = paths.get_globals()
                custom : list = buffer['NPC']['skin']['female']['custom']
                if name in custom:
                    custom.remove(name)
                buffer['NPC']['skin']['female']['custom'] = custom
                with open(paths.GLOBALS_PATH, 'w') as globals:
                    dump(buffer, globals, indent=4)

    @classmethod
    def create_routine(
        cls, activity: str, start_time: str, end_time: str, waypoint: str
    ) -> dict:
        """
        Creates an NPC routine with specified activity, start time, end time, and waypoint.

        Args:
            activity (str): The activity for the NPC routine.
            start_time (str): The start time of the NPC routine.
            end_time (str): The end time of the NPC routine.
            waypoint (str): The waypoint for the NPC routine.

        Returns:
            dict: A dictionary containing the created NPC routine with keys 'activity', 'start_time', 'end_time', and 'waypoint'.
        """
        cls.routines: dict = {
            'activity': activity,
            'start_time': start_time,
            'end_time': end_time,
            'waypoint': waypoint
        }
        return cls.routines
    

class ExtractWaypoints():
    """
    A class for extracting waypoints from uncompiled ZEN files.

    Attributes:
        worlds_path (Path): The path to the directory containing the ZEN files.
        zen_files (list): The list of valid ZEN files.
        zen_filenames (list): The filenames of the valid ZEN files.
        zen_wps (dict): The extracted waypoints from the ZEN files, stored in a dictionary.
    """

    def __init__(self, path: str):
        """
        Initializes an instance of ExtractWaypoints.

        Args:
            path (str): The path to the directory containing the ZEN files.
        """
        self.worlds_path = Path(path)
        
        self.zen_files : list = self.check_files(self.worlds_path)['files']
        self.zen_filenames : list = self.check_files(self.worlds_path)['filenames']

        self.zen_wps : dict = self.extract_waypoints(
            self.zen_files, self.zen_filenames
        )

        

    def check_files(self, file_path: Path) -> dict:
        """
        Checks for valid ZEN files in the given directory and returns a
        dictionary containing the list of files and their filenames.

        Args:
            file_path (Path): The path to the directory containing
            the ZEN files.

        Returns:
            dict: A dictionary containing the list of files and their
            filenames.
        """
        file_paths = file_path.iterdir()
        uncompiled_zens : list[Path] = list()
        for file_path in file_paths:
            if file_path.is_dir():
                continue
            if file_path.suffix.lower() == '.zen':
                try:
                    with open(
                        file_path,
                        'rt',
                        encoding='windows-1252'
                    ) as file:
                        data = file.read()
                except UnicodeDecodeError:
                    continue
                else:
                    if not 'wpName=string:' in data:
                        continue
                    uncompiled_zens.append(file_path)
        return {
            'files': uncompiled_zens,
            'filenames': [
                file.stem for file in uncompiled_zens
            ]
        }
    
    def extract_waypoints(self, files: list[Path], filenames: list[str]) -> dict:
        """
        Reads the ZEN files and extracts the waypoints from them,
        storing them in a dictionary.

        Args:
            files (list[Path]): The list of valid ZEN files.
            filenames (list[str]): The filenames of the valid ZEN files.

        Returns:
            dict: A dictionary containing the extracted waypoints
            from the ZEN files.
        """
        wps = dict()
        for file, filename in zip(files, filenames):
            with open(file, 'rt', encoding='windows-1252') as zen:
                waypoints = list()

                for line in zen:
                        if 'wpName=string:' in line:
                            name = line.lstrip('\t').rstrip('\t\n').split(':')[1]
                            waypoints.append(name)
                waypoints = sorted(waypoints)
                wps[filename] = waypoints

        wps = {
            key: value for key, value
            in sorted(wps.items())
        }
        return wps
