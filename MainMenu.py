from pathlib import Path
from winsound import PlaySound, SND_ALIAS

from ttkbootstrap import (
    StringVar, Window,
    Frame, Label,
    Entry, Combobox,
    Radiobutton, Button
)
from ttkbootstrap.dialogs.dialogs import Messagebox

from MiscUtils import MainPaths

class MainMenu(Frame):
    def __init__(self, parent, snd_path):
        super().__init__(parent)
        self.snd_path : Path = snd_path
        self.paths = MainPaths()
        self.configure(bootstyle = 'dark')
        self.widgets_init()
        self.widgets_pack() 

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()

    def widgets_init(self):
        self.main_frames = dict()
        self.main_frame_names = [
            'id', 'name',
            'guild', 'voice',
            'type', 'flag'
        ]
        self.var_entry_id = StringVar()
        self.var_entry_name = StringVar()
        self.var_combo_guild = StringVar()
        self.var_combo_voice = StringVar()
        self.var_radio_flag = StringVar()
        self.var_combo_type = StringVar()
        self.radio_flag = dict()
        self.combo_guild_list = [i for i in
            self.paths.get_globals()['NPC']['guild']['default']
        ]
        self.combo_voice_list = self.paths.get_globals()['NPC']['voice']['default']
        self.flag_names_list = [
            i for i in self.paths.get_globals()['NPC']['flag']
        ]
        self.combo_type_list = self.paths.get_globals()['NPC']['type']['default']
        self.names_database = [
            i.lower() for i in self.paths.get_globals()['NPC']['name']
        ]
        self.ids_database = self.paths.get_globals()['NPC']['id']

        for i in self.main_frame_names:
            self.main_frames[i] = Frame(self)
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
            width = 33,
            textvariable = self.var_entry_id
        )
        self.var_entry_id.trace_add(
            'write',
            lambda *args: self.check_if_exists('id', self.var_entry_id.get())
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
            width = 33,
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
            textvariable = self.var_combo_guild
        )
        self.label_voice = Label(
            self.main_frames['voice'],
            text = 'NPC Voice:'
        )
        self.button_voice = Button(
            self.main_frames['voice'],
            text = '>',
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
            textvariable = self.var_combo_voice
        )
        self.label_type = Label(self.main_frames['type'], text = 'NPC Type:')
        self.combo_type = Combobox(
            self.main_frames['type'],
            bootstyle = 'light',
            width = 31,
            values = self.combo_type_list,
            textvariable = self.var_combo_type
        )
        for i in self.flag_names_list:
            self.radio_flag[i] = Radiobutton(
                master = self.main_frames['flag'],
                variable = self.var_radio_flag,
                value = i,
                text = i,
                bootstyle = 'info'
            )

    def widgets_pack(self):
        for i in self.main_frames:
            self.main_frames[i].pack(
                fill = 'both', padx = 5, pady = 5, expand = True
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

        for i in self.radio_flag:
            self.radio_flag[i].pack(
                side = 'left', fill = 'x', expand = True, padx = 5, pady = 5
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
                '''Specified voice type was not found. Make sure
to choose correct path for custom sound files.''',
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


if __name__ == '__main__':
    root = Window(title='test', themename='darkly')
    root.geometry('536x512')
    MainMenu(root, MainPaths().SOUNDS_PATH).show()
    root.mainloop()
