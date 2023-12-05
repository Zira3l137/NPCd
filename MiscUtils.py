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
    - WAYPOINTS_PATH: Represents the path to the 'Waypoints.json' file.
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
        self.WAYPOINTS_PATH: Path = self.STRINGS_PATH / 'Waypoints.json'

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
    #TODO: implement data dumping into NPC solution file. 
    def create_profile(cls, name: str):
        '''
        Create a new NPC solution file and dump all the available data into it.

        name : str - NPC solution name.
        '''
        with open(paths.SOLUTIONS_PATH / f'{name}.json', 'w') as profile:
            dump('Data', profile)

    @classmethod
    def delete_profile(cls, name: str):
        '''
        Delete specified NPC solution file.

        name : str - NPC solution name.
        '''
        remove(paths.SOLUTIONS_PATH / f'{name}.json')  

class NPC():
    '''
    A class containing all the necessary methods for script parsing and NPC
    data fetching.
    '''
    def __init__(self):
        pass       
    
    @classmethod
    def get_guilds(cls, constants_path: str) -> dict:
        '''
        Parse Constants.d and dump fetched data into Globals.json.

        constants_path : str - A path to a directory containing Constants.d
        
        Returns dict type object with fetched and default data.
        '''
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
    def get_voices(self, svm_path: str) -> dict:
        '''
        Parse SVM.d and dump fetched data into Globals.json.

        svm_path : str - A path to a directory containing SVM.d
        
        Returns dict type object with fetched and default data.
        '''
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
    def get_outfits(self, items_path: str):
        '''
        Parse IT_Armor.d and IT_Addon_Armor.d and dump
        fetched data into Globals.json.

        items_path : str - A path to a directory containing
        IT_Armor.d and IT_Addon_Armor.d.
        '''
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
    '''
    Parse uncompiled ZEN files from a specified directory,
    fetch all waypoints from them and store them into dictionaries.

    path : str - Path to a directory containing ZEN files
    '''

    def __init__(self, path: str):
        self._zen_files : dict = dict()
        self._zen_wps : dict = dict()
        self._worlds_path : Path = Path(path)

    def load(self) -> dict:
        '''
        Load waypoints from Waypoints.json.

        Returns: dict type object with ZEN filenames as keys and waypoint lists
        as values.
        '''
        if not paths.STRINGS_PATH / 'Waypoints.json':
            self._write()
        return load(open(paths.STRINGS_PATH / 'Waypoints.json'))

    def _write(self):
        if not self._worlds_path:
            if not paths.WORLDS_PATH.iterdir():
                raise FileNotFoundError
            for i in paths.WORLDS_PATH.iterdir():
                if '.zen' or '.ZEN' in i:
                    self._zen_files[i.stem] = paths.WORLDS_PATH / i
        else:
            if not self._worlds_path.iterdir():
                raise FileNotFoundError
            for i in self._worlds_path.iterdir():
                if '.zen' or '.ZEN' in i:
                    self._zen_files[i.stem] = self._worlds_path / i
        self.__extract(self._zen_files, paths.STRINGS_PATH)

    def __extract(self, zen_dir, save_dir):
        for file in zen_dir:
            if False in (
                Path(zen_dir[file]).is_file(),
                Path(save_dir).is_dir()
            ):
                raise FileNotFoundError
            with open(zen_dir[file], 'rt', encoding='Windows-1252') as zen:
                waypoints = list()
                for line in zen.readlines():
                    if 'MeshAndBsp' in line:
                        raise KeyError
                    if 'wpName=string:' in line:
                        name = line.lstrip('\t').rstrip('\t\n').split(':')[1]
                        waypoints.append(name)
            self._zen_wps[file] = waypoints
        with open(paths.STRINGS_PATH / 'Waypoints.json', 'w') as file:
            dump(self._zen_wps, file, indent=4)
