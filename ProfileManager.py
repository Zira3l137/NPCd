from ttkbootstrap import (
    Window, Frame,
    Label, Entry,
    Button, StringVar,
    BooleanVar, END
)
from ttkwidgets.autocomplete.autocompletecombobox import AutocompleteCombobox

from MiscUtils import Profile

class ProfileManager(Frame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.configure(bootstyle = 'primary')
        self.widgets_init()
        self.widgets_pack()
        self.pack(fill = 'both', padx = 5, pady = 5)

    def widgets_init(self):
        self.profiles = Profile.load_profiles()

        self.var_entry_profile = StringVar()
        self.var_entry_profile_appended = BooleanVar(value=False)
        
        self.frame_profile = Frame(self)
        self.combo_profiles = AutocompleteCombobox(
            self.frame_profile, self.profiles
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
        self.frame_profile_manage = Frame(self.frame_profile)
        self.btn_add_profile = Button(
            self.frame_profile_manage,
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
            self.frame_profile_manage,
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
            self.frame_profile_manage,
            bootstyle = 'primary',
            text = 'R',
            width = 2,
            command = lambda: self.refresh_profile_list()
        )

        self.entry_profile.insert(END, '<New NPC Solution>')
        self.entry_profile.bind(
            '<Button-1>',
            lambda *_: self.clear_entry_profile(
                self.var_entry_profile_appended
            )
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
        self.frame_profile_manage.pack(
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

    def profile_manage(self, profiles, entry, widget, action):
        if action == 'add' and self.var_entry_profile_appended.get():
            Profile.create_profile(entry.get())
            profiles = Profile.load_profiles()
            widget.configure(completevalues = profiles)
            widget.set(entry.get())
        if action == 'remove' and widget.get != '':
            Profile.delete_profile(widget.get())
            profiles = Profile.load_profiles()
            widget.configure(completevalues = profiles)
            widget.set(profiles[0]) if profiles else widget.set('')

    def refresh_profile_list(self):
        self.profiles = Profile.load_profiles()
        self.combo_profiles.configure(completevalues = self.profiles)


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
