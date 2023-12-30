from ttkbootstrap import (
    Window, Frame,
    Label, Entry,
    Button, StringVar,
    BooleanVar, Combobox, END,
    ImageTk, Image
)
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox

from MiscUtils import Profile, PathConstants

class ProfileManager(Frame):
    def __init__(self, parent, menus):
        super().__init__(master = parent)
        self.configure(bootstyle = 'primary')
        self.paths = PathConstants()
        self.modules = menus
        self.widgets_init()
        self.widgets_pack()
        self.pack(fill = 'both', padx = 5, pady = 5)

    def widgets_init(self):
        self.icon_reset = ImageTk.PhotoImage(
            Image.open(
                self.paths.ICONS_PATH / 'Reset.png'
            )
        )
        
        self.profiles = Profile.load_profiles()

        self.var_entry_profile = StringVar()
        self.var_combo_profile = StringVar()
        self.var_entry_profile_appended = BooleanVar(value=False)
        
        self.frame_profile = Frame(self)
        self.combo_profiles = Combobox(
            self.frame_profile,
            values=self.profiles,
            textvariable=self.var_combo_profile
        )
        self.label_profile = Label(
            self.frame_profile,
            text = 'Select NPC Solution:',
            justify = 'center'
        )
        self.entry_profile = Entry(
            self.frame_profile,
            width = 30,
            textvariable = self.var_entry_profile,
            justify = 'center'
        )
        self.frame_profile_prof_manage = Frame(self.frame_profile)
        self.btn_add_profile = Button(
            self.frame_profile_prof_manage,
            bootstyle = 'success',
            text = '+',
            width = 2,
            command = lambda: self.profile_manage(
                self.profiles,
                self.var_entry_profile,
                self.combo_profiles,
                'add'
            )
        )
        self.btn_remove_profile = Button(
            self.frame_profile_prof_manage,
            bootstyle = 'danger',
            text = '-',
            width = 2,
            command = lambda: self.profile_manage(
                self.profiles,
                self.var_entry_profile,
                self.combo_profiles,
                'remove'
            )
        )
        self.btn_refresh_list = Button(
            self.frame_profile_prof_manage,
            bootstyle = 'primary',
            image=self.icon_reset,
            width = 2,
            command = lambda: self.refresh_profile_list()
        )
        self.tooltip_refresh = ToolTip(
            self.btn_refresh_list,
            'Reload NPC solution list',
            bootstyle='info-inverse'
        )

        self.entry_profile.insert(END, '<New NPC Solution>')
        self.entry_profile.bind(
            '<Button-1>',
            lambda *_: self.clear_entry_profile(
                self.var_entry_profile_appended
            )
        )

        self.frame_profile_manage = Frame(self)
        self.button_extract_info = Button(
            self.frame_profile_manage,
            text='Write Script',
            command=lambda *_: self.write_script(),
            state='disabled'
        )
        self.button_view_info = Button(
            self.frame_profile_manage,
            text='Preview Script',
            state='disabled'
        )
        self.button_save_file = Button(
            self.frame_profile_manage,
            text='Save File',
            state='disabled'
        )
        self.button_open_file = Button(
            self.frame_profile_manage,
            text='Open File',
            state='disabled'
        )

        self.var_combo_profile.trace_add(
            'write',
            lambda *_:
                self.button_extract_info.configure(state='normal')
                if self.var_combo_profile.get()
                else self.button_extract_info.configure(state='disabled')
        )

    def widgets_pack(self):
        self.frame_profile.pack(
            fill = 'x', padx = 5, pady = 5, anchor = 'n', expand = True
        )
        self.label_profile.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'center', expand = True
        )
        self.combo_profiles.pack(
            side = 'left', padx = 5, pady = 5,
            anchor = 'center', expand = True, fill = 'x'
        )
        self.entry_profile.pack(
            side = 'left', padx = 5, pady = 5,
            anchor = 'center', expand = True, fill = 'x')
        self.frame_profile_prof_manage.pack(
            side = 'left', pady = 5, padx = 5, anchor = 'center', expand = True
        )
        self.btn_add_profile.pack(
            side = 'left', pady = 5, padx = 1, anchor = 'e', expand = True
        )
        self.btn_remove_profile.pack(
            side = 'left', pady = 5, padx = 1, anchor = 'e', expand = True
        )
        self.btn_refresh_list.pack(
            side = 'left', pady = 5, padx = 1, anchor = 'e', expand = True
        )

        self.frame_profile_manage.pack(
            fill = 'x', padx = 5, pady = 5, anchor = 'n', expand = True
        )
        self.button_extract_info.pack(
            side = 'left',
            pady = 5,
            padx = 5,
            anchor = 'center',
            fill='x',
            expand = True
        )
        self.button_view_info.pack(
            side = 'left',
            pady = 5,
            padx = 5,
            anchor = 'center',
            fill='x',
            expand = True
        )
        self.button_save_file.pack(
            side = 'left',
            pady = 5,
            padx = 5,
            anchor = 'center',
            fill='x',
            expand = True
        )
        self.button_open_file.pack(
            side = 'left',
            pady = 5,
            padx = 5,
            anchor = 'center',
            fill='x',
            expand = True
        )

    def profile_manage(self, profiles, entry, widget, action):
        if action == 'add' and self.var_entry_profile_appended.get():
            Profile.create_profile(entry.get())
            profiles = Profile.load_profiles()
            widget.configure(values = profiles)
            widget.set(entry.get())
        if action == 'remove' and widget.get != '':
            Profile.delete_profile(widget.get())
            profiles = Profile.load_profiles()
            widget.configure(values = profiles)
            widget.set(profiles[0]) if profiles else widget.set('')

    def missing_data(self, data: tuple[dict,dict]) -> dict:
        data_ = data[0]
        empty_keys = list()
        empty_data = dict()
        
        for key in data_:
            if not data_[key]:
                empty_keys.append(key)

        if empty_keys:
            for key in empty_keys:
                empty_data[empty_keys.index(key)] = key
        
        return empty_data
    
    def rtn_start_exists(self) -> bool:
        routine_menu = self.modules['Routine']
        for routine in routine_menu.routines:
            if '_start' in routine.lower():
                return True

    def write_script(self):
        data = Profile.extract_data(self.modules)
        missing_data: dict = self.missing_data(data)
        if missing_data:
            data_list = ', '.join(list(missing_data.values()))
            Messagebox.show_warning(
                f'Following data was not assigned upon writing script:\n{data_list}',
                'Warning!',
                self,
                True
            )
        if not self.rtn_start_exists():
            Messagebox.show_warning(
                f'Starting routine block for this solution was not created!',
                'Warning!',
                self,
                True
            )
        Profile.construct_script(data)

    def refresh_profile_list(self):
        self.profiles = Profile.load_profiles()
        self.combo_profiles.configure(values = self.profiles)


    def clear_entry_profile(self, condition):
        if not condition.get():
            self.entry_profile.delete(0, END)
            self.entry_profile.configure(justify = 'left')
            condition.set(True)
            

if __name__ == '__main__':
    root = Window(title='test',themename='darkly')
    root.geometry('640x512')
    ProfileManager(root)
    root.mainloop()
