from ttkbootstrap import Window

from ProfileManager import ProfileManager
from EditWindow import EditWindow

class Root(Window):
    def __init__(
        self,
        resolution,
        title,
        theme,
        **kwargs
    ):
        super().__init__(themename=theme, title=title, **kwargs)
        pos_x = (self.winfo_screenwidth()//2) - (resolution[0]//2)
        pos_y = (self.winfo_screenheight()//2) - (resolution[1]//2)
        self.geometry(f'{resolution[0]}x{resolution[1]}+{pos_x}+{pos_y}')
        self.profile_manager = ProfileManager(self)
        self.edit_window = EditWindow(self, self)
        self.mainloop()   

if __name__ == '__main__':
    root =  Root((768,512), 'Root', 'darkly')
