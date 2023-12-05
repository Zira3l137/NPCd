from ttkbootstrap import (
    StringVar, Window,
    Frame, Label,
    Entry, Combobox,
    Radiobutton, Button
)

#from MiscUtils import 

class SettingsMenu(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bootstyle = 'dark')
        self.widgets_init()
        self.widgets_pack() 

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()

    def widgets_init(self):
        self.frame_settings = Frame(self, bootstyle = 'dark')

    def widgets_pack(self):
        pass