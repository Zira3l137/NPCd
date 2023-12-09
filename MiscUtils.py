'''
The MainPaths class is responsible for defining the paths to various
directories and files used in the program.

The Profile class contains methods for handling NPC solution files.

The NPC class contains methods for script parsing and NPC data fetching.

The ExtractWaypoints class is used to parse uncompiled ZEN files and
extract waypoints from them.
'''
import sys
from pathlib import Path
from os import remove
from json import dump, load

class MainPaths():
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
        '''
        return load(open(paths.GLOBALS_PATH))


    def get_overlays(self) -> dict:
        '''
        Return Walk_Overlays.json as a dictionary.
        '''
        return load(open(paths.OVERLAYS_PATH))


    def get_activities(self) -> dict:
        '''
        Return Activities.json as a dictionary.
        '''
        return load(open(paths.ACTIVITIES_PATH))
        
paths = MainPaths()

class Profile():
    '''
    A class containing all the necessary methods for NPC solution handling.
    '''
    def __init__(self):
        pass

    @classmethod
    def load_profiles(cls) -> list:
        '''
        Load NPC solutions from paths.SOLUTIONS_PATH as a list of filenames
        without extensions.
        '''
        return [i.stem for i in paths.SOLUTIONS_PATH.iterdir() if '.json' in str(i)]

    @classmethod 
    def create_profile(cls, name: str):
        '''
        Create a new NPC solution file.

        name : str - NPC solution name.
        '''
        with open(paths.SOLUTIONS_PATH / f'{name}.json', 'w') as profile:
            dump('', profile)

    @classmethod
    def delete_profile(cls, name: str):
        '''
        Delete specified NPC solution file.

        name : str - NPC solution name.
        '''
        remove(paths.SOLUTIONS_PATH / f'{name}.json')  

    @classmethod
    def extract_data(cls, widget: dict) -> dict:
        '''
        '''
        solution_info = dict()

        solution_info['id'] = widget['Main'].var_entry_id.get()
        solution_info['name'] = widget['Main'].var_entry_name.get()
        solution_info['guild'] = widget['Main'].var_combo_guild.get()
        solution_info['voice'] = widget['Main'].var_combo_voice.get().replace('SVM_','')
        solution_info['flags'] = widget['Main'].var_radio_flag.get()
        solution_info['npctype'] = widget['Main'].var_combo_type.get()
        
        visual_params = list()
        visual_params.append(widget['Visual'].var_radio_gender.get())
        visual_params.append(widget['Visual'].var_combo_head.get())
        visual_params.append(widget['Visual'].var_listbox_face.get())
        visual_params.append(widget['Visual'].var_combo_skin.get())
        visual = ', '.join(map(str, visual_params))

        solution_info['B_SetNpcVisual'] = visual

        solution_info['Mdl_SetModelFatness'] = round(widget['Visual'].var_scale_fatness.get(), 2)
        solution_info['Mdl_ApplyOverlayMds'] = widget['Visual'].var_combo_walk_overlay.get()

        solution_info['fight_tactic'] = widget['Stats'].var_combo_fight_tactic.get() 
        solution_info['B_GiveNpcTalents'] = widget['Stats'].var_check_talents.get()
        solution_info['B_SetFightSkills'] = widget['Stats'].var_entry_fightskill.get()


        solution_info['ATR_HITPOINTS_MAX'] = widget['Stats'].var_current_stat[4].get()
        solution_info['ATR_MANA_MAX'] = widget['Stats'].var_current_stat[5].get()
        solution_info['ATR_STRENGTH'] = widget['Stats'].var_current_stat[6].get()
        solution_info['ATR_DEXTERITY'] = widget['Stats'].var_current_stat[7].get()

        melee = widget['Inventory'].var_label_equipped_melee.get()
        ranged = widget['Inventory'].var_label_equipped_ranged.get().split()[1]
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

        for item in solution_info.items():
            print(item)

class NPC():
    """
    The `NPC` class provides methods for parsing and manipulating NPC data, such as guilds, voices, types, outfits, overlays, head meshes, and skin textures.

    Example Usage:
        npc = NPC()
        npc.get_guilds(constants_path)  # Returns a dictionary with default and custom guilds\n
        npc.get_voices(svm_path)  # Returns a dictionary with default and custom voices\n
        npc.get_types(ai_constants_path)  # Returns a dictionary with default and custom types\n
        npc.get_outfits(items_path)  # Updates Globals.json with custom outfits\n
        npc.add_overlay(name)  # Adds an overlay to Walk_Overlays.json\n
        npc.delete_overlay(name)  # Removes an overlay from Walk_Overlays.json\n
        npc.add_head_mesh(name, gender)  # Adds a head mesh to Globals.json\n
        npc.remove_head_mesh(name, gender)  # Removes a head mesh from Globals.json\n
        npc.add_skin_tex(name, gender)  # Adds a skin texture to Globals.json\n
        npc.remove_skin_tex(name, gender)  # Removes a skin texture from Globals.json\n
        npc.create_routine(activity, start_time, end_time, waypoint)  # Returns a dictionary representing an NPC routine solution

    Main functionalities:
    - Parsing and dumping NPC data into Globals.json
    - Updating Globals.json with custom NPC data
    - Creating NPC routine solutions

    Methods:
    - get_guilds(constants_path: str) -> dict: Parses Constants.d and updates Globals.json with fetched guild data
    - get_voices(svm_path: str) -> dict: Parses SVM.d and updates Globals.json with fetched voice data
    - get_types(ai_constants_path: str) -> dict: Parses AI_Constants.d and updates Globals.json with fetched type data
    - get_outfits(items_path: str): Parses IT_Armor.d and IT_Addon_Armor.d and updates Globals.json with fetched outfit data
    - add_overlay(name: str): Adds an overlay with a specified name to Walk_Overlays.json
    - delete_overlay(name: str): Removes an overlay with a specified name from Walk_Overlays.json
    - add_head_mesh(name: str, gender: int): Adds a head mesh with a specified name to Globals.json
    - remove_head_mesh(name: str, gender: int): Removes a head mesh with a specified name from Globals.json
    - add_skin_tex(name: str, gender: int): Adds a skin texture with a specified name to Globals.json
    - remove_skin_tex(name: str, gender: int): Removes a skin texture with a specified name from Globals.json
    - create_routine(activity: str, start_time: str, end_time: str, waypoint: str) -> dict: Constructs an NPC routine solution as a dictionary with specified parameters

    Fields:
    - No significant fields in the `NPC` class
    """
    def __init__(self):
        pass       
    
    @classmethod
    def get_guilds(cls, constants_path: str) -> dict:
        '''
        Parse Constants.d and dump fetched data into Globals.json.

        constants_path : str - A path to a directory containing Constants.d
        
        Returns dict type object with fetched and default data.
        '''
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
        '''
        Parse SVM.d and dump fetched data into Globals.json.

        svm_path : str - A path to a directory containing SVM.d
        
        Returns dict type object with fetched and default data.
        '''
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
        '''
        Parse AI_Constants.d and dump fetched data into Globals.json.

        ai_constants_path : str - A path to a directory containing
        AI_Constants.d
        
        Returns dict type object with fetched and default data.
        '''
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
        '''
        Parse IT_Armor.d and IT_Addon_Armor.d and dump
        fetched data into Globals.json.

        items_path : str - A path to a directory containing
        IT_Armor.d and IT_Addon_Armor.d.

        Returns default and custom outfits as a dictionary.
        '''
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
                if True in [
                    'INSTANCE' in line,
                    'instance' in line
                ] and True in [
                    '(C_ITEM)' in line,
                    '(C_Item)' in line
                ] and False in [
                    'ITAR_DJG_BABE' in line
                ]:
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
                if True in [
                    'INSTANCE' in line,
                    'instance' in line
                ] and True in [
                    '(C_ITEM)' in line,
                    '(C_Item)' in line
                ]:
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
        '''
        Parse AI_Constants.d and dump fetched data into Globals.json.

        ai_constants_path : str - A path to a directory containing
        AI_Constants.d
        
        Returns dict type object with fetched and default data.
        '''
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
    def add_overlay(cls, name: str):
        '''
        Add an overlay with a specified name to Walk_Overlays.json.

        name : str - Overlay name.
        '''
        result : dict = dict()
        buffer : dict = load(
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
        '''
        Remove an overlay with a specified name from Walk_Overlays.json.

        name : str - Overlay name.
        '''
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
        '''
        Add specified head mesh name into a specified gender section in
        Globals.json.

        name : str - Head mesh name.
        gender : int - Gender (0 - Male, 1 - Female)
        '''
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
        '''
        Remove specified head mesh name from a specified gender section in
        Globals.json.

        name : str - Head mesh name.
        gender : int - Gender (0 - Male, 1 - Female)
        '''
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
        '''
        Add specified skin texture name into a specified gender section in
        Globals.json.

        name : str - Skin texture name.
        gender : int - Gender (0 - Male, 1 - Female)
        '''
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
        '''
        Remove specified skin texture name from a specified gender section in
        Globals.json.

        name : str - Skin texture name.
        gender : int - Gender (0 - Male, 1 - Female)
        '''
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
        cls,
        activity: str,
        start_time: str,
        end_time: str,
        waypoint: str
    ) -> dict:
        '''
        Construct an NPC routine solution as a dictionary
        with specified parameters.

        activity   : str - Activity name.
        start_time : str - A string representing activity starting time.
        end_time   : str - A string representing activity ending time.
        waypoint   : str - Waypoint name.
        
        Returns: dict type NPC solution object.
        '''
        cls.routines : dict = {
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
                        file.readlines()
                except UnicodeDecodeError:
                    continue
                else:
                    with open(
                        file_path,
                        'rt',
                        encoding='windows-1252'
                    ) as file:
                        data = file.read()
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
                lines = zen.readlines()

                for line in lines:
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
