from subprocess import run
from json import load

from ttkbootstrap import (
    Frame,
    Label, Entry,
    Button, StringVar,
    BooleanVar, Combobox, END,
    ImageTk, Image, ScrolledText,
    Toplevel
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

        self.top_script_preview = Toplevel(
            'Script Preview',
            topmost=True,
            size=(560, 512),
            position=(
                self.winfo_screenwidth()//2-(560//2),
                self.winfo_screenheight()//2-(512//2)
            )
        )
        self.top_script_preview.protocol('WM_DELETE_WINDOW', self.preview_script)
        self.top_script_preview.withdraw()

        self.text_script = ScrolledText(
            self.top_script_preview,
            state='disabled'
        )
        
        self.frame_profile = Frame(self)
        self.label_profile = Label(
            self.frame_profile,
            text = 'Select NPC Solution:',
            justify = 'center'
        )
        self.combo_profiles = Combobox(
            self.frame_profile,
            values=self.profiles,
            textvariable=self.var_combo_profile,
            state='readonly'
        )
        self.button_save_solution = Button(
            self.frame_profile,
            bootstyle = 'info',
            text = 'Save',
            width = 5,
            state='disabled',
            command=lambda *_: self.save_solution()
        )
        self.button_load_solution = Button(
            self.frame_profile,
            bootstyle = 'info',
            text = 'Load',
            width = 5,
            state='disabled',
            command=lambda *_: self.load_solution()
        )
        self.button_reset_solution = Button(
            self.frame_profile,
            bootstyle = 'info',
            text = 'Reset',
            width = 5,
            state='disabled',
            command=lambda *_: self.reset_data_entry()
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
            state='disabled',
            command=lambda *_: self.preview_script()
        )
        self.button_save_file = Button(
            self.frame_profile_manage,
            text='Save File',
            state='disabled',
            command=lambda *_: self.save_script()
        )
        self.button_open_file = Button(
            self.frame_profile_manage,
            text='Open File',
            state='disabled',
            command=lambda *_: self.open_script()
        )

        self.var_combo_profile.trace_add(
            'write',
            lambda *_: self.unlock_buttons()
        )

    def widgets_pack(self):
        self.text_script.pack(
            fill='both', padx=5, pady=5, expand=True
        )
        
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
        self.button_save_solution.pack(
            side = 'left', pady = 5, padx = 1, anchor = 'e', expand = True
        )
        self.button_load_solution.pack(
            side = 'left', pady = 5, padx = 1, anchor = 'e', expand = True
        )
        self.button_reset_solution.pack(
            side = 'left', pady = 5, padx = 1, anchor = 'e', expand = True
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
            side = 'left', pady = 5, padx = 1, anchor = 'e', expand = True,
            fill='y'
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

    def insert_text(self, entry: str):
        self.text_script.configure(state='normal')
        self.text_script.delete(1.0,END)
        self.text_script.insert(END,entry)
        self.text_script.configure(state='disabled')
    
    def write_script(self):
        self.solution = Profile(self.modules)
        data: tuple[dict, dict] = self.solution.extracted_data
        self.script: str = self.solution.construct_script()

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
        self.insert_text(self.script)

    def preview_script(self):
        window_state = self.top_script_preview.state()
        match window_state:
            case 'normal':
                self.top_script_preview.withdraw()
            case 'withdrawn':
                self.top_script_preview.deiconify()

    def save_solution(self):
        self.solution.dump_data(self.var_combo_profile.get())

    def save_script(self):
        self.solution.dump_script(
            self.script,
            self.var_combo_profile.get(),
            'Windows-1251'
        )

    def open_script(self):
        profile = self.var_combo_profile.get()
        name = profile + '.d'
        path = self.paths.OUTPUT_PATH / profile / name
        run(['notepad', path])

    def refresh_profile_list(self):
        self.profiles = Profile.load_profiles()
        self.combo_profiles.configure(values = self.profiles)

    def clear_entry_profile(self, condition):
        if not condition.get():
            self.entry_profile.delete(0, END)
            self.entry_profile.configure(justify = 'left')
            condition.set(True)
    
    def unlock_buttons(self):
        state = str()
        if self.var_combo_profile.get():
            state = 'normal'
            self.button_extract_info.configure(state=state)
            self.button_view_info.configure(state=state)
            self.button_save_file.configure(state=state)
            self.button_open_file.configure(state=state)
            self.button_load_solution.configure(state=state)
            self.button_save_solution.configure(state=state)
            self.button_reset_solution.configure(state=state)
        else:
            state = 'disabled'
            self.button_extract_info.configure(state=state)
            self.button_view_info.configure(state=state)
            self.button_save_file.configure(state=state)
            self.button_open_file.configure(state=state)
            self.button_load_solution.configure(state=state)
            self.button_save_solution.configure(state=state)
            self.button_reset_solution.configure(state=state)

    def reset_data_entry(self):
        main: object = self.modules['Main']
        visual: object = self.modules['Visual']
        stats: object = self.modules['Stats']
        inv: object = self.modules['Inventory']
        routine: object = self.modules['Routine']
        data_mapping = {
            #Main
            'level': main.var_entry_level,
            'id': main.var_entry_id,
            'name': main.var_entry_name,
            'guild': main.var_combo_guild,
            'voice': main.var_combo_voice,
            'flags': main.var_combo_flag,
            'npctype': main.var_combo_type,
            #Visual
            'gender': visual.var_radio_gender,
            'head': visual.var_combo_head,
            'face': visual.listbox_face,
            'skin': visual.var_combo_skin,
            'outfit': visual.var_combo_outfit,
            'fatness': visual.var_scale_fatness,
            'walk_overlay': visual.var_combo_walk_overlay,
            #Stats
            'atr_mode': stats.var_radio_option,
            'fight_tactic': stats.var_combo_fight_tactic,
            'give_talents': stats.var_check_talents,
            'fight_skill': stats.var_entry_fightskill,
            'atr_hp': stats.var_current_stat[4],
            'atr_mp': stats.var_current_stat[5],
            'atr_str': stats.var_current_stat[6],
            'atr_dex': stats.var_current_stat[4],
            'atr_chapter': stats.var_spinbox_chapter,
            #Inventory
            'melee': inv.var_label_equipped_melee,
            'ranged': inv.var_label_equipped_ranged,
            'items': inv.treeview_inv,
            'ambient_inv': inv.var_check_add_amb_inv,
        }
        for key in data_mapping:
            if data_mapping[key]:
                if key == 'gender':
                    data_mapping[key].set(2)
                    continue
                if key == 'give_talents':
                    data_mapping[key].set(False)
                    continue
                if key == 'fight_skill':
                    if data_mapping[key].get():
                        stats.check_fightskill.invoke()
                    continue
                if key == 'fatness':
                    visual.update_scale_value(1.0)
                    continue
                if key == 'atr_mode':
                    stats.radio_auto.invoke()
                    continue
                if key == 'face':
                    continue
                if key == 'items':
                    items: list[list] = [
                        item
                        for item
                        in data_mapping[key].get_children('')
                    ]
                    if items:
                        inv.remove_from_inv('all')
                    continue
                if key == 'ambient_inv':
                    data_mapping[key].set(False)
                    continue
                data_mapping[key].set('')
        for item in routine.treeview_schedule.get_children(''):
            routine.treeview_schedule.delete(item)
        routine.combo_routines.configure(
            values=''
        )
        routine.combo_routines.set('')

    def load_solution(self):
        name = self.var_combo_profile.get() + '.json'
        path = self.paths.SOLUTIONS_PATH / name

        main: object = self.modules['Main']
        visual: object = self.modules['Visual']
        stats: object = self.modules['Stats']
        inv: object = self.modules['Inventory']
        routine: object = self.modules['Routine']
        data_mapping = {
            #Main
            'level': main.var_entry_level,
            'id': main.var_entry_id,
            'name': main.var_entry_name,
            'guild': main.var_combo_guild,
            'voice': main.var_combo_voice,
            'flags': main.var_combo_flag,
            'npctype': main.var_combo_type,
            #Visual
            'gender': visual.var_radio_gender,
            'head': visual.var_combo_head,
            'face': visual.listbox_face,
            'skin': visual.var_combo_skin,
            'outfit': visual.var_combo_outfit,
            'fatness': visual.var_scale_fatness,
            'walk_overlay': visual.var_combo_walk_overlay,
            #Stats
            'atr_mode': stats.var_radio_option,
            'fight_tactic': stats.var_combo_fight_tactic,
            'give_talents': stats.var_check_talents,
            'fight_skill': stats.var_entry_fightskill,
            'atr_hp': stats.var_current_stat[4],
            'atr_mp': stats.var_current_stat[5],
            'atr_str': stats.var_current_stat[6],
            'atr_dex': stats.var_current_stat[4],
            'atr_chapter': stats.var_spinbox_chapter,
            #Inventory
            'melee': inv.var_label_equipped_melee,
            'ranged': inv.var_label_equipped_ranged,
            'items': inv.treeview_inv,
            'ambient_inv': inv.var_check_add_amb_inv,
        }

        solution: dict = (
            load(open(path))
            if isinstance(load(open(path)), dict)
            else None
        )
        if not solution: return
        self.reset_data_entry()
        routine.routines = solution['routines']

        for key in solution:
            if solution[key]:
                if key == 'gender':
                    match solution[key]:
                        case '0':
                            visual.radio_gender_m.invoke()
                        case '1':
                            visual.radio_gender_f.invoke()
                    continue
                if key == 'fight_skill':
                    if not stats.var_check_fightskill.get():
                        stats.check_fightskill.invoke()
                if key == 'fatness':
                    visual.update_scale_value(solution[key])
                if key == 'atr_mode':
                    match solution[key]:
                        case 'manual':
                            stats.radio_manual.invoke()
                            continue
                        case 'auto':
                            stats.radio_auto.invoke()
                            continue
                if key == 'face':
                    faces: list = [
                        face.lower()
                        for face in
                        data_mapping[key].get(0,END)
                    ]
                    face = f'hum_head_v{solution[key]}_c0'
                    if face in faces:
                        cur_value: int = faces.index(face)
                        data_mapping[key].selection_set(cur_value)
                    else:
                        print(f'Face texture: {face} was not found!')
                        continue
                    if not visual.listbox_face_custom_dir:
                        visual.view_face_image()
                        continue
                    else:
                        visual.view_face_image(visual.listbox_face_custom_dir)
                        continue
                if 'atr_' in key:
                    if key != 'atr_mode:':
                        if key != 'atr_chapter':
                            if solution['atr_mode'] == 'manual':
                                data_mapping[key].set(solution[key])
                                continue
                            else:
                                continue
                        else:
                            if solution['atr_mode'] == 'manual':
                                continue
                            else:
                                data_mapping[key].set(solution[key])
                                continue
                if key == 'items':
                    items: list[list] = solution[key]
                    inv.remove_from_inv('all')
                    for item in items:
                        data_mapping[key].insert(
                        parent='',
                        index='end',
                        values=(item[0], item[1], item[2])
                    )
                    continue
                if key == 'routines':
                    routine_list = list(routine.routines.keys())
                    routine.combo_routines.configure(
                        values=routine_list
                    )
                    routine.combo_routines.set(routine_list[0])
                    continue
                data_mapping[key].set(solution[key])
        self.write_script()
