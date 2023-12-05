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
from MiscUtils import MainPaths

class EditWindow(Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.configure(bootstyle='primary')
        self.root = root
        self.paths = MainPaths()
        self.widgets_init()
        self.widgets_pack()
        self.switch_tab(list(self.tab_names.keys())[0])
        self.pack(fill='both', padx=5, pady=5, expand=True)

    def widgets_init(self):
        self.frame_tabs = Frame(self)
        self.var_tabs = StringVar()
        self.var_current_tab = StringVar()
        self.tabs = dict()
        self.menus = dict()
        self.tab_names = {
            'Main': '768x512',
            'Visual': '768x780',
            'Stats': '784x512',
            'Inventory': '1280x800',
            'Routine': '1040x768',
            'Settings': '768x768'
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
        self.menus['Main'] = MainMenu(self.frame_menu, self.paths.SOUNDS_PATH)
        self.menus['Visual'] = VisualMenu(self.frame_menu, self.root)
        self.menus['Stats'] = StatsMenu(self.frame_menu)
        self.menus['Inventory'] = InventoryMenu(self.frame_menu)
        self.menus['Routine'] = RoutineMenu(
            self.frame_menu,
            self.menus['Main']
        )
        self.menus['Settings'] = SettingsMenu(self.frame_menu)
    
    def widgets_pack(self):
        self.frame_tabs.pack(fill='x', padx=5, pady=5, anchor='n')
        for i in self.tabs:
            self.tabs[i].pack(
                side='left', fill='x', expand=True, padx=5, pady=5
            )
        self.frame_menu.pack(
            expand=True, fill='both', padx=2, pady=2, anchor='n'
        )

    def switch_tab(self, tab, current=None):
        self.menus[tab].show()
        self.root.geometry(self.tab_names[tab])
        if current is not None and current != tab:
            self.menus[current].hide()
        self.var_current_tab.set(tab)

if __name__ == '__main__':
    root = Window(title='test', themename='darkly')
    root.geometry('512x512')
    EditWindow(root, root)
    root.mainloop()
