from pathlib import Path
from winsound import PlaySound, SND_ALIAS
from random import choice

from ttkbootstrap import (
    StringVar,
    Frame, Label,
    Entry, Combobox,
    Button, ImageTk, Image
)
from ttkbootstrap.dialogs.dialogs import Messagebox

from MiscUtils import PathConstants

class MainMenu(Frame):
    def __init__(self, parent, snd_path):
        super().__init__(parent)
        self.snd_path : Path = snd_path
        self.paths = PathConstants()
        self.configure(bootstyle = 'dark')
        self.widgets_init()
        self.widgets_pack()
        self.fill_id()

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()

    def widgets_init(self):
        self.main_frames = dict()
        self.main_frame_names = [
            'lvl',
            'id', 'name',
            'guild', 'voice',
            'type', 'flag'
        ]
        self.var_entry_level = StringVar()
        self.var_entry_level.trace_add(
            'write',
            lambda *_:
                self.digit_validation(self.var_entry_level)
        )
        self.var_entry_id = StringVar()
        self.var_entry_name = StringVar()
        self.var_combo_guild = StringVar()
        self.var_combo_voice = StringVar()
        self.var_combo_flag = StringVar()
        self.var_combo_type = StringVar()
        self.radio_flag = dict()
        self.combo_guild_list = [i for i in
            self.paths.get_globals()['NPC']['guild']['default']
        ]
        self.combo_voice_list = self.paths.get_globals()['NPC']['voice']['default']
        self.combo_flags_list = self.paths.get_globals()['NPC']['flag']
        self.combo_type_list = self.paths.get_globals()['NPC']['type']['default']
        self.names_database = [
            i.lower() for i in self.paths.get_globals()['NPC']['name']
        ]
        self.ids_database = self.paths.get_globals()['NPC']['id']

        self.sound_icon = ImageTk.PhotoImage(
            Image.open(
                self.paths.ICONS_PATH / 'Sound.png'
            )
        )

        for i in self.main_frame_names:
            self.main_frames[i] = Frame(self)

        self.label_level = Label(
            self.main_frames['lvl'],
            text='NPC Level:'
        )
        self.entry_level = Entry(
            self.main_frames['lvl'],
            bootstyle = 'danger',
            width = 10,
            justify='center',
            textvariable = self.var_entry_level
        )

        self.label_id = Label(self.main_frames['id'], text = 'Unique NPC ID:')
        self.frame_label_warning_id = Frame(self.main_frames['id'])
        self.label_warning_id = Label(
            self.frame_label_warning_id,
            text = 'This ID already exists!',
            foreground = 'Red'
        )
        self.entry_id = Entry(
            self.main_frames['id'],
            bootstyle = 'danger',
            width = 10,
            justify='center',
            textvariable = self.var_entry_id
        )
        self.var_entry_id.trace_add(
            'write',
            lambda *_: self.check_if_exists('id', self.var_entry_id.get())
        )
        self.var_entry_id.trace_add(
            'write',
            lambda *_: self.digit_validation(self.var_entry_id)
        )

        self.label_name = Label(
            self.main_frames['name'],
            text = 'Unique NPC Name:'
        )
        self.frame_label_warning_name = Frame(self.main_frames['name'])
        self.label_warning_name = Label(
            self.frame_label_warning_name,
            text = 'This name already exists!',
            foreground = 'Red'
        )
        self.entry_name = Entry(
            self.main_frames['name'],
            bootstyle = 'success',
            width = 10,
            justify='center',
            textvariable = self.var_entry_name
        )
        self.var_entry_name.trace_add(
            'write',
            lambda *args: self.check_if_exists(
                'name',
                self.var_entry_name.get()
            )
        )

        self.label_guild = Label(
            self.main_frames['guild'],
            text = 'NPC Guild:'
        )
        self.combo_guild = Combobox(
            self.main_frames['guild'],
            bootstyle = 'info',
            width = 31,
            values = self.combo_guild_list,
            textvariable = self.var_combo_guild,
            state='readonly'
        )
        self.label_voice = Label(
            self.main_frames['voice'],
            text = 'NPC Voice:'
        )
        self.button_voice = Button(
            self.main_frames['voice'],
            image= self.sound_icon,
            width = 2,
            bootstyle = 'primary-outline',
            command = lambda: self.play_voice_sample(
                self.var_combo_voice.get()
            )
        )
        self.combo_voice = Combobox(
            self.main_frames['voice'],
            bootstyle = 'warning',
            width = 31,
            values = self.combo_voice_list,
            textvariable = self.var_combo_voice,
            state='readonly'
        )
        self.label_type = Label(self.main_frames['type'], text = 'NPC Type:')
        self.combo_type = Combobox(
            self.main_frames['type'],
            bootstyle = 'light',
            width = 31,
            values = self.combo_type_list,
            textvariable = self.var_combo_type,
            state='readonly'
        )
        self.label_flags = Label(
            self.main_frames['flag'],
            text='Flags:'
        )
        self.combo_flags = Combobox(
            self.main_frames['flag'],
            textvariable=self.var_combo_flag,
            values=self.combo_flags_list,
            width= 31,
            bootstyle = 'light',
            state='readonly'
        )

    def widgets_pack(self):
        for i in self.main_frames:
            self.main_frames[i].pack(
                fill = 'both', padx = 5, pady = 5, expand = True
            )

        self.label_level.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.entry_level.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        
        self.label_id.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.frame_label_warning_id.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.entry_id.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

        self.label_name.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.frame_label_warning_name.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.entry_name.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

        self.label_guild.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.combo_guild.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

        self.label_voice.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.button_voice.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.combo_voice.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        
        self.label_type.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.combo_type.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

        self.label_flags.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.combo_flags.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

    def play_voice_sample(self, voice):
        if not voice:
            Messagebox.show_error(
                'Nothing to play: Select a voice type!',
                'Error'
            )
            return
        if voice in self.paths.get_globals()['NPC']['voice']['default']:
            voice_index = voice.split('_')[1]
        if voice_index:
            sound_file = str(self.paths.SOUNDS_PATH.joinpath(f'{voice_index}.wav'))
        else:
            sound_file = str(self.snd_path.joinpath(f'{voice}.wav'))
        if Path(sound_file).is_file():
            PlaySound(sound_file, SND_ALIAS)
        else:
            Messagebox.show_error(
                'Specified voice type was not found.'
                + 'Make sure to choose correct path for custom sound files.',
                'Error'
            )

    def check_if_exists(self, cat, input):
        match cat:
            case 'name':
                if input.lower() in self.names_database:
                    self.label_warning_name.pack()
                else:
                    self.label_warning_name.forget()
            case 'id':
                if input in self.ids_database:
                    self.label_warning_id.pack()
                else:
                    self.label_warning_id.forget()

    def fill_id(self):
        taken_ids = set(self.paths.get_globals()['NPC']['id'])
        available_ids = (
            str(id) for id in range(100,99999)
            if str(id) not in taken_ids
        )
        self.var_entry_id.set(choice(list(available_ids)))

    def digit_validation(self, var):
        if var.get():
            if not var.get().isdigit():
                var.set(0)
            else:
                if ' ' in var.get():
                    var.set(0)
