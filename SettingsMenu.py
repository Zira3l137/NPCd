from ttkbootstrap import (
    StringVar, Window,
    Frame, Entry,
    Checkbutton, Button,
    BooleanVar, END
)

from MiscUtils import NPC, MainPaths

from tkinter.filedialog import askdirectory

class SettingsMenu(Frame):
    def __init__(self, parent, edit_window):
        super().__init__(parent)
        self.modules = edit_window.menus
        self.paths = MainPaths()
        self.configure(bootstyle = 'dark')
        self.widgets_init()
        self.widgets_pack() 

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()

    def widgets_init(self):
        KEYS = ['guild', 'voice', 'type']
        self.vars_checks_main : dict = {
            key: BooleanVar(value=False) for key in KEYS
        }
        self.vars_entries_main : dict = {
            key: StringVar(value=f'path/to/{self.get_source_name(key, dir=True)}')
            for key in KEYS
        }
        self.frame_settings = Frame(self, bootstyle = 'dark')
        self.frames_main : dict = {
            key: Frame(self.frame_settings) for key in KEYS
        }
        self.buttons_main : dict = {
            key: Button(
                self.frames_main[key],
                width=3,
                text='...',
                command=lambda caller=key: self.load_custom_dir(caller),
                state='disabled'
            ) for key in KEYS
        }
        self.checks_main : dict = {
            key: Checkbutton(
                self.frames_main[key],
                text=f'Custom directory for {key}s',
                variable=self.vars_checks_main[key],
                offvalue=False,
                onvalue=True,
                command=lambda caller = key: self.toggle_custom_dir(caller)
            ) for key in KEYS
        }
        self.entries_main : dict = {
            key: Entry(
                self.frames_main[key],
                textvariable=self.vars_entries_main[key],
                width=50,
                state='disabled'
            ) for key in KEYS
        }

        for key in KEYS:
            self.vars_entries_main[key].trace_add(
                'write',
                lambda *_, key=key: self.refill_data(key)
            )

    def widgets_pack(self):
        self.frame_settings.pack(
            padx=5, pady=5, fill='both', expand=True
        )

        for key in self.frames_main:
            self.frames_main[key].pack(
                padx=5, pady=5, fill='both', expand=True
            )
            self.checks_main[key].pack(
                padx=5, pady=5, side='left', anchor='w'
            )
            self.buttons_main[key].pack(
                padx=5, pady=5, side='right', anchor='e'
            )
            self.entries_main[key].pack(
                padx=5, pady=5, side='right', anchor='e'
            )

    def get_source_name(self, caller: str, stem = False, dir = False) -> str:
        match caller:
            case 'guild':
                if stem:
                    return 'Constants.d'
                if dir:
                    return 'Scripts/Content/_intern/'
                return '_intern/Constants.d'
            case 'voice':
                if stem:
                    return 'SVM.d'
                if dir:
                    return 'Scripts/Content/Story/'
                return 'Story/SVM.d'
            case 'type':
                if stem:
                    return 'AI_Constants.d'
                if dir:
                    return 'Scripts/Content/AI/AI_Intern/'
                return 'AI_Intern/AI_Constants.d'
    
    def toggle_custom_dir(self, caller: str):
        condition = self.vars_checks_main[caller].get()
        state = 'normal' if condition else 'disabled'
        source_file = self.get_source_name(caller=caller, dir=True)

        self.entries_main[caller].configure(state=state)
        self.vars_entries_main[caller].set(f'path/to/{source_file}')
        
        self.buttons_main[caller].configure(state=state)

    def load_custom_dir(self, caller: str):
        specified_dir = askdirectory(mustexist=True)
        if specified_dir:
            self.vars_entries_main[caller].set(specified_dir)

    def refill_data(self, caller):
        if self.vars_checks_main[caller].get():
            directory = self.vars_entries_main[caller].get()
            match caller:
                case 'guild':
                    if NPC.get_guilds(directory):
                        self.modules['Main'].combo_guild_list = [i for i in
                            self.paths.get_globals()['NPC']['guild']['default']
                            +self.paths.get_globals()['NPC']['guild']['custom']
                        ]
                        self.modules['Main'].combo_guild.configure(
                            values = self.modules['Main'].combo_guild_list
                        )
                case 'voice':
                    if NPC.get_guilds(directory):
                        self.modules['Main'].combo_voice_list = [i for i in
                            self.paths.get_globals()['NPC']['voice']['default']
                            +self.paths.get_globals()['NPC']['voice']['custom']
                        ]
                    self.modules['Main'].combo_voice.configure(
                        values = self.modules['Main'].combo_voice_list
                    )
                case 'type':
                    if NPC.get_guilds(directory):
                        self.modules['Main'].combo_type_list = [i for i in
                            self.paths.get_globals()['NPC']['type']['default']
                            +self.paths.get_globals()['NPC']['type']['custom']
                        ]
                        self.modules['Main'].combo_type.configure(
                            values = self.modules['Main'].combo_type_list
                        )
        else:
            match caller:
                case 'guild':
                    self.modules['Main'].combo_guild_list = [i for i in
                        self.paths.get_globals()['NPC']['guild']['default']
                    ]
                    self.modules['Main'].combo_guild.configure(
                        values = self.modules['Main'].combo_guild_list
                    )
                case 'voice':
                    self.modules['Main'].combo_voice_list = [i for i in
                        self.paths.get_globals()['NPC']['voice']['default']
                    ]
                    self.modules['Main'].combo_voice.configure(
                        values = self.modules['Main'].combo_voice_list
                    )
                case 'type':
                    self.modules['Main'].combo_type_list = [i for i in
                        self.paths.get_globals()['NPC']['type']['default']
                    ]
                    self.modules['Main'].combo_type.configure(
                        values = self.modules['Main'].combo_type_list
                    )

if __name__ == '__main__':
    root = Window(title='Settings Menu', themename='darkly')
    root.geometry('512x512')
    SettingsMenu(root).show()
    root.mainloop()
