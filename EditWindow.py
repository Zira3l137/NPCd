from ttkbootstrap import (
    Frame,
    Radiobutton,
    StringVar,
    Window
)

from MainMenu import MainMenu
from VisualMenu import VisualMenu
from StatsMenu import StatsMenu
from InvMenu import InventoryMenu
from RoutineMenu import RoutineMenu
from SettingsMenu import SettingsMenu
from MiscUtils import PathConstants

class EditWindow(Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.configure(bootstyle='primary')
        self.root: Window = root
        self.paths = PathConstants()
        self.widgets_init()
        self.widgets_pack()
        self.switch_tab(list(self.tab_names.keys())[0])

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()
    
    def widgets_init(self):
        self.frame_tabs = Frame(self)
        self.var_tabs = StringVar()
        self.var_current_tab = StringVar()
        self.tabs = dict()
        self.menus = dict()
        self.tab_names = {
            'Main': (50,60),
            'Visual': (50,74),
            'Stats': (50,56),
            'Inventory': (55,74),
            'Routine': (50,65),
            'Settings': (50,60)
        }
        for n, i in enumerate(list(self.tab_names.keys())):
            self.tabs[n] = Radiobutton(
                master=self.frame_tabs,
                text=i,
                value=i,
                variable=self.var_tabs,
                bootstyle='toolbutton-info'
            )
        self.var_tabs.set(list(self.tab_names.keys())[0])
        self.frame_menu = Frame(self)
        for i in self.tabs:
            self.tabs[i].configure(
                command=lambda: self.switch_tab(
                    self.var_tabs.get(),
                    self.var_current_tab.get()
                )
            )
        self.menus['Main'] = MainMenu(
            self.frame_menu,
            self.paths.SOUNDS_PATH,
        )
        self.menus['Visual'] = VisualMenu(self.frame_menu, self.root, self)
        self.menus['Stats'] = StatsMenu(self.frame_menu)
        self.menus['Inventory'] = InventoryMenu(self.frame_menu)
        self.menus['Routine'] = RoutineMenu(self.frame_menu, self)
        self.menus['Settings'] = SettingsMenu(self.frame_menu, self)
    
    def widgets_pack(self):
        self.frame_tabs.pack(fill='x', padx=5, pady=5)
        for i in self.tabs:
            self.tabs[i].pack(
                side='left', fill='x', expand=True, padx=5, pady=5
            )
        self.frame_menu.pack(
            expand=True, fill='both', padx=5, pady=5, anchor='n'
        )

    def switch_tab(self, tab, current=None):
        self.menus[tab].show()
        self.root.geometry(self.get_tab_res(tab))
        if current is not None and current != tab:
            self.menus[current].hide()
        self.var_current_tab.set(tab)

    def get_screen_res(self) -> tuple[int,int]:
        return (
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight()
        )
    
    def get_tab_res(self, tab: str) -> str:
        screen_res = self.get_screen_res()
        return '{w}x{h}'.format(
            w=(screen_res[0]*self.tab_names[tab][0])//100,
            h=(screen_res[1]*self.tab_names[tab][1])//100
        )

