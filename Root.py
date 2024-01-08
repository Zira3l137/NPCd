import sys
from pathlib import Path

from ttkbootstrap import Window

from ProfileManager import ProfileManager
from EditWindow import EditWindow

if hasattr(sys, 'frozen') and hasattr(sys, "_MEIPASS"):
    CURRENT_PATH = Path(sys.executable).resolve().parent
else:
    CURRENT_PATH = Path.cwd()

if (CURRENT_PATH/'NPCd.ico').is_file():
    ICON = str(CURRENT_PATH/'NPCd.ico')
else:
    ICON = ''

class Root(Window):
    def __init__(
        self,
        resolution,
        title,
        theme,
        **kwargs
    ):
        super().__init__(themename=theme, title=title, **kwargs)
        self.iconbitmap(ICON)
        pos_x = (self.winfo_screenwidth()//2) - (resolution[0]//2)
        pos_y = (self.winfo_screenheight()//2) - (resolution[1]//2)
        self.geometry(f'{resolution[0]}x{resolution[1]}+{pos_x}+{pos_y}')
        self.edit_window = EditWindow(self, self)
        self.profile_manager = ProfileManager(self, self.get_edit_menus())
        self.edit_window.show()
        self.mainloop()

    def get_edit_menus(self):
        return self.edit_window.menus

if __name__ == '__main__':
    root =  Root((768,512), 'Root', 'darkly')
