from tkinter import Listbox
from tkinter.filedialog import askdirectory

from ttkbootstrap import (
    Window,StringVar,
    BooleanVar,Button,
    Frame,Label,
    Entry,Combobox,
    Spinbox,Scrollbar,
    Treeview,END,ImageTk,Image
)

from ttkbootstrap.dialogs.dialogs import Messagebox

from MiscUtils import (
    NPC,
    ExtractWaypoints,
    PathConstants
)

class RoutineMenu(Frame):
    def __init__(self, parent, edit_window):
        super().__init__(parent)
        self.modules = edit_window.menus
        self.paths = PathConstants()
        self.configure(bootstyle = 'dark')
        self.widgets_init()
        self.widgets_pack()
        self.update_npc_id()

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()

    def get_npc_id(self):
        id = self.modules['Main'].var_entry_id.get()
        if id:
            self.var_entry_routine_id.set(f'_{id}')
        else:
            self.var_entry_routine_id.set('_{NPC ID}')

    def widgets_init(self):
        self.var_combo_routines = StringVar()
        self.var_entry_routine_name = StringVar()
        self.var_entry_routine_id = StringVar()
        self.var_combo_activities = StringVar()
        self.var_entry_routine_appended = BooleanVar(value = False)
        self.spinbox_values_hours = list()
        self.routines = dict()
        self.wps = dict()
        self.get_npc_id()
        self.var_combo_routines.trace_add(
            'write',
            lambda *_: self.unlock_widgets()
        )
        self.modules['Main'].var_entry_id.trace_add(
            'write',
            lambda *_: self.update_npc_id()
        )
        self.combo_activities_list = [
            i for i in self.paths.get_activities()['default']
        ]

        for i in range(24):
            if i < 10:
                self.spinbox_values_hours.append(f'0{i}')
                continue
            self.spinbox_values_hours.append(str(i))

        self.spinbox_values_minutes = list()

        for i in range(60):
            if i < 10:
                self.spinbox_values_minutes.append(f'0{i}')
                continue
            self.spinbox_values_minutes.append(str(i))

        self.var_spinbox_time_start = [
            StringVar(value = '00'),
            StringVar(value = '00')
        ]
        self.var_spinbox_time_end = [
            StringVar(value = '00'),
            StringVar(value = '00')
        ]
        self.var_spinbox_time_start[0].trace_add(
            'write',
            lambda *_: 
                self.time_input_validation(self.var_spinbox_time_start[0])
        )
        self.var_spinbox_time_start[1].trace_add(
            'write',
            lambda *_:
                self.time_input_validation(self.var_spinbox_time_start[1])
        )
        self.var_spinbox_time_end[0].trace_add(
            'write',
            lambda *_:
                self.time_input_validation(self.var_spinbox_time_end[0])
        )
        self.var_spinbox_time_end[1].trace_add(
            'write',
            lambda *_:
                self.time_input_validation(self.var_spinbox_time_end[1])
        )
        self.var_label_waypoint_input = StringVar(value = 'NONE')
        self.var_entry_directory = StringVar(value = self.paths.WORLDS_PATH)
        self.var_combo_worlds = StringVar()
        self.combo_worlds_list = list()
        self.var_listbox_waypoints = StringVar()

        self.icon_reset = ImageTk.PhotoImage(
            Image.open(
                self.paths.ICONS_PATH / 'Reset.png'
            )
        )
        
        self.frame_routine = Frame(self)
        self.combo_routines = Combobox(
            self.frame_routine,
            values = list(self.routines.keys()),
            textvariable = self.var_combo_routines,
            state='readonly'
        )
        self.var_combo_routines.trace_add(
            'write',
            lambda *_: self.update_treeview()
        )
        self.label_routine = Label(
            self.frame_routine,
            text = 'Select Routine:'
        )
        self.frame_routine_entry = Frame(self.frame_routine)
        self.label_routine_rtn = Label(
            self.frame_routine_entry,
            text = 'Rtn_',
            foreground = 'green'
        )
        self.entry_routine_name = Entry(
            self.frame_routine_entry,
            width = 8,
            textvariable = self.var_entry_routine_name,
            justify = 'center'
        )
        self.label_routine_id = Label(
            self.frame_routine_entry,
            textvariable = self.var_entry_routine_id,
            foreground = 'red'
        )
        self.frame_routine_manage = Frame(self.frame_routine)
        self.btn_add_routine = Button(
            self.frame_routine_manage,
            bootstyle = 'success',
            text = '+',
            width = 2,
            command = lambda *_: self.manage_routine('+')
        )
        self.btn_remove_routine = Button(
            self.frame_routine_manage,
            bootstyle = 'danger',
            text = '-',
            width = 2,
            command = lambda *_: self.manage_routine('-')
        )

        self.frame_parameters = Frame(self)

        self.frame_parameters_params = Frame(
            self.frame_parameters,
            bootstyle = 'dark'
        )
        self.frame_waypoints_directory = Frame(self.frame_parameters_params)
        self.label_directory = Label(
            self.frame_waypoints_directory,
            text = 'Uncompiled ZEN Directory:'
        )
        self.entry_directory = Entry(
            self.frame_waypoints_directory,
            textvariable = self.var_entry_directory,
            width = 46,
            state = 'disabled'
        )
        self.button_open_directory = Button(
            self.frame_waypoints_directory,
            width = 2,
            text = '...',
            command = self.open_directory,
            state = 'disabled'
        )
        self.frame_parameters_params_activity = Frame(
            self.frame_parameters_params
        )
        self.label_activity = Label(
            self.frame_parameters_params_activity,
            text = 'Activity (Actions):'
        )
        self.combo_activities = Combobox(
            self.frame_parameters_params_activity,
            values = self.combo_activities_list,
            textvariable = self.var_combo_activities,
            width = 31,
            state = 'disabled'
        )
        self.frame_parameters_params_time = Frame(self.frame_parameters_params)
        self.label_time = Label(
            self.frame_parameters_params_time,
            text = 'Time Period:'
        )
        self.frame_start = Frame(self.frame_parameters_params_time)
        self.label_start = Label(
            self.frame_start,
            text = 'Start:',
            bootstyle = 'inverse-primary'
        )
        self.spinbox_time_start_hours = Spinbox(
            self.frame_start,
            width = 2,
            from_ = '00',
            to = '23',
            wrap = True,
            values = self.spinbox_values_hours,
            textvariable = self.var_spinbox_time_start[0],
            state = 'disabled'
        )
        self.spinbox_time_start_minutes = Spinbox(
            self.frame_start,
            width = 2,
            from_ = '00',
            to = '60',
            wrap = True,
            values = self.spinbox_values_minutes,
            textvariable = self.var_spinbox_time_start[1],
            state = 'disabled'
        )
        self.frame_end = Frame(self.frame_parameters_params_time)
        self.label_end = Label(
            self.frame_end,
            text = 'End:',
            bootstyle = 'inverse-primary'
        )
        self.spinbox_time_end_hours = Spinbox(
            self.frame_end,
            width = 2,
            from_ = '00',
            to = '23',
            wrap = True,
            values = self.spinbox_values_hours,
            textvariable = self.var_spinbox_time_end[0],
            state = 'disabled'
        )
        self.spinbox_time_end_minutes = Spinbox(
            self.frame_end,
            width = 2,
            from_ = '00',
            to = '60',
            wrap = True,
            values = self.spinbox_values_minutes,
            textvariable = self.var_spinbox_time_end[1],
            state = 'disabled'
        )
        self.button_reset_time = Button(
            self.frame_parameters_params_time,
            image=self.icon_reset,
            width=3,
            command=lambda *_: self.reset_time(),
            state='disabled'
        )
        self.frame_parameters_params_waypoint = Frame(
            self.frame_parameters_params
        )
        self.label_waypoint = Label(
            self.frame_parameters_params_waypoint,
            text = 'Waypoint (Location):'
        )
        self.label_waypoint_input = Label(
            self.frame_parameters_params_waypoint,
            textvariable = self.var_label_waypoint_input,
            bootstyle = 'inverse-primary'
        )

        self.frame_parameters_waypoints = Frame(
            self.frame_parameters, bootstyle = 'dark'
        )
        self.frame_waypoints_world = Frame(self.frame_parameters_waypoints)
        self.label_worlds = Label(self.frame_waypoints_world, text = 'Worlds:')
        self.combo_worlds = Combobox(
            self.frame_waypoints_world,
            textvariable = self.var_combo_worlds,
            width = 24,
            values = self.combo_worlds_list,
            state = 'disabled'
        )
        self.var_combo_worlds.trace_add(
            'write',
            lambda *_: self.switch_worlds()
        )
        self.button_extract = Button(
            self.frame_waypoints_world,
            text = 'Extract Waypoints',
            width = 17,
            command = lambda *_: self.extract_waypoints(),
            state = 'disabled'
        )
        self.frame_listbox_wps = Frame(self.frame_parameters_waypoints)
        self.scrollbar_listbox_waypoints = Scrollbar(
            self.frame_listbox_wps,
            orient = 'vertical',
            bootstyle = 'round-primary'
        )
        self.listbox_waypoints = Listbox(
            self.frame_listbox_wps,
            listvariable = self.var_listbox_waypoints,
            width = 30,
            height = 15,
            selectmode = 'single',
            activestyle = 'underline',
            yscrollcommand = self.scrollbar_listbox_waypoints.set,
            state = 'disabled'
        )
        self.listbox_waypoints.bind(
            '<Button1-ButtonRelease>',
            lambda *_: self.select_waypoint()
        )
        self.scrollbar_listbox_waypoints.configure(
            command = self.listbox_waypoints.yview
        )

        self.frame_schedule = Frame(self)

        self.frame_schedule_treeview = Frame(
            self.frame_schedule,
            bootstyle = 'dark'
        )
        self.treeview_schedule = Treeview(
            self.frame_schedule_treeview,
            columns = ('act', 'start', 'end', 'wp'),
            height = 6,
            show = 'headings',
            bootstyle = 'primary'
        )
        self.treeview_schedule.heading('act', text = 'Activity')
        self.treeview_schedule.column('act', width = 50, anchor = 'center')
        self.treeview_schedule.heading('start', text = 'Start Time')
        self.treeview_schedule.column('start', width = 50, anchor = 'center')
        self.treeview_schedule.heading('end', text = 'End Time')
        self.treeview_schedule.column('end', width = 50, anchor = 'center')
        self.treeview_schedule.heading('wp', text = 'Waypoint')
        self.treeview_schedule.column('wp', width = 50, anchor = 'center')

        self.treeview_schedule.bind(
            '<Button1-ButtonRelease>',
            lambda *_: self.adjust_time()
        )

        self.frame_schedule_ctrl = Frame(
            self.frame_schedule,
            bootstyle = 'dark'
        )
        self.button_add_to_schedule = Button(
            self.frame_schedule_ctrl,
            text = 'Add to Routine',
            command = lambda *_: self.add_to_schedule(),
            state = 'disabled',
            bootstyle = 'success'
        )
        self.button_remove_from_schedule = Button(
            self.frame_schedule_ctrl,
            text = 'Remove from Routine',
            command = lambda *_: self.remove_from_schedule(),
            state = 'disabled',
            bootstyle = 'danger'
        )

    def widgets_pack(self):
        self.frame_routine.pack(fill='x', padx=5, pady=5)
        self.label_routine.pack(
            side='left', padx=5, pady=5, anchor='center', expand=True
        )
        self.combo_routines.pack(
            side='left', padx=5, pady=5, anchor='w', expand=True, fill='x'
        )
        self.frame_routine_entry.pack(
            side='left', padx=5, pady=5, anchor='e', expand=True, fill='x'
        )
        self.label_routine_rtn.pack(
            side='left', pady=5, padx=1, anchor='e', fill='both'
        )
        self.entry_routine_name.pack(
            side='left', pady=5, padx=1, anchor='e', fill='both'
        )
        self.label_routine_id.pack(
            side='left', pady=5, padx=1, anchor='e', fill='both'
        )
        self.frame_routine_manage.pack(
            side='left', pady=5, padx=5, anchor='e', expand=True
        )
        self.btn_add_routine.pack(
            side='left', pady=5, padx=1, anchor='e', expand=True
        )
        self.btn_remove_routine.pack(
            side='left', pady=5, padx=1, anchor='e', expand=True
        )

        self.frame_parameters.pack(
            fill = 'both', padx = 5, pady = 5, expand = True
        )

        self.frame_parameters_params.pack(
            side='left', fill='both', padx=5, pady=5, expand=True
        )
        self.frame_waypoints_directory.pack(
            fill='both', padx=5, pady=5, expand=True
        )
        self.label_directory.pack(
            side='left', pady=5, padx=5, anchor='w', expand=True
        )
        self.entry_directory.pack(side='left', pady=5, padx=5, anchor='e')
        self.button_open_directory.pack(
            side='left', pady=5, padx=5, anchor='e'
        )
        self.frame_parameters_params_activity.pack(
            fill='both', padx=5, pady=5, expand=True
        )
        self.label_activity.pack(
            side='left', pady=5, padx=5, anchor='w', expand=True
        )
        self.combo_activities.pack(
            side='left', pady=5, padx=5, anchor='e', expand=True
        )
        self.frame_parameters_params_time.pack(
            fill='both', padx=5, pady=5, expand=True
        )
        self.label_time.pack(
            side='left', pady=5, padx=5, anchor='w', expand=True
        )
        self.frame_start.pack(
            side='left', pady=5, padx=5, anchor='w', expand=True
        )
        self.label_start.pack(
            side='left', fill='y', pady=5, padx=5, anchor='w', expand=True
        )
        self.spinbox_time_start_hours.pack(
            side='left', pady=5, padx=5, anchor='e', expand=True
        )
        self.spinbox_time_start_minutes.pack(
            side='left', pady=5, padx=5, anchor='e', expand=True
        )
        self.frame_end.pack(
            side='left', pady=5, padx=5, anchor='w', expand=True
        )
        self.label_end.pack(
            side='left', fill='y', pady=5, padx=5, anchor='w', expand=True
        )
        self.spinbox_time_end_hours.pack(
            side='left', pady=5, padx=5, anchor='e', expand=True
        )
        self.spinbox_time_end_minutes.pack(
            side='left', pady=5, padx=5, anchor='e', expand=True
        )
        self.button_reset_time.pack(
            side='left', pady=5, padx=5, anchor='e', expand=True
        )
        self.frame_parameters_params_waypoint.pack(
            fill='both', padx=5, pady=5, expand=True
        )
        self.label_waypoint.pack(
            side='left', fill='y', pady=5, padx=5, anchor='w', expand=True
        )
        self.label_waypoint_input.pack(
            side='left', fill='y', pady=5, padx=5, anchor='e', expand=True
        )

        self.frame_parameters_waypoints.pack(
            side = 'left', fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.frame_waypoints_world.pack(
            fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.label_worlds.pack(
            side = 'left', pady = 5, padx = 5, anchor = 'w', expand = True
        )
        self.combo_worlds.pack(
            side = 'left', pady = 5, padx = 5, anchor = 'e'
        )
        self.button_extract.pack(
            side = 'left', pady = 5, padx = 5, anchor = 'e'
        )
        self.frame_listbox_wps.pack(
            fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.listbox_waypoints.pack(
            side = 'left', fill = 'both', expand = True, padx = 5, pady = 5
        )
        self.scrollbar_listbox_waypoints.pack(
            side = 'left', padx = 5, pady = 5, fill = 'y'
        )

        self.frame_schedule.pack(
            fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.frame_schedule_treeview.pack(
            side = 'left', fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.treeview_schedule.pack(
            side = 'left', fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.frame_schedule_ctrl.pack(
            side = 'left', fill = 'y', padx = 5, pady = 5
        )
        self.button_add_to_schedule.pack(
            fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.button_remove_from_schedule.pack(
            fill = 'both', padx = 5, pady = 5, expand = True
        )

    def manage_routine(self, condition):
        id = self.var_entry_routine_id.get().strip('_')
        name = self.var_entry_routine_name.get()
        match condition:
            case '+':
                if id.isdigit() and name:
                    self.routines[self.get_routine_name()] = list()
                    self.combo_routines.configure(
                        values = list(self.routines.keys())
                    )
                    self.combo_routines.set(self.get_routine_name())
                    self.var_entry_routine_name.set('')
                elif not id.isdigit():
                    Messagebox.show_error(
                        'Please set a unique ID for your NPC solution!',
                        'NPC ID is unset!',
                        self
                    )
            case '-':
                selected_routine = self.combo_routines.get()
                if selected_routine:
                    del self.routines[selected_routine]
                    self.combo_routines.configure(state='normal')
                    self.combo_routines.delete(0, END)
                    self.combo_routines.configure(
                        values = list(self.routines.keys()),
                        state='readonly'
                    )

    def get_routine_name(self):
        name = self.var_entry_routine_name.get()
        id = self.var_entry_routine_id.get()
        return f'Rtn_{name}{id}'

    def update_npc_id(self):
        main_id = self.modules['Main'].var_entry_id.get()
        local_id = self.var_entry_routine_id.get()
        if True in (not main_id, not main_id.isdigit()):
            self.var_entry_routine_id.set('_{NPC ID}')
            self.label_routine_id.configure(foreground = 'Red')
            return
        if main_id and local_id != main_id:
            self.var_entry_routine_id.set(f'_{main_id}')
        self.label_routine_id.configure(foreground = 'Green')

    def open_directory(self):
        directory = askdirectory(
            initialdir = self.paths.WORLDS_PATH,
            mustexist = True
        )
        if directory:
            self.var_entry_directory.set(directory)

    def extract_waypoints(self):
        worlds = ExtractWaypoints(self.var_entry_directory.get())
        self.wps = worlds.zen_wps
        self.combo_worlds_list = [i for i in self.wps]
        self.combo_worlds.configure(values = self.combo_worlds_list)
        self.combo_worlds.set(self.combo_worlds_list[0])
        self.var_listbox_waypoints.set(
            [i for i in self.wps[self.var_combo_worlds.get()]]
        )

    def switch_worlds(self):
        self.var_listbox_waypoints.set(
            [i for i in self.wps[self.var_combo_worlds.get()]]
        )

    def select_waypoint(self):
        waypoints = self.listbox_waypoints.get(0,END)
        if waypoints:
            self.var_label_waypoint_input.set(
                self.listbox_waypoints.selection_get()
            )

    def convert_value(self, value, value_list):
        if value not in value_list:
            value = value_list[int(value)]
        return value
    
    def add_to_schedule(self):
        activity = self.var_combo_activities.get()

        start_hours = self.var_spinbox_time_start[0].get()
        start_minutes = self.var_spinbox_time_start[1].get()
        end_hours = self.var_spinbox_time_end[0].get()
        end_minutes = self.var_spinbox_time_end[1].get()

        if '' in (
            start_hours,
            start_minutes,
            end_hours,
            end_minutes
        ):
            Messagebox.show_error(
                'Please set appropriate values for activity time period!',
                'Time period values are unset'
            )
            return

        start_hours = self.convert_value(start_hours, self.spinbox_values_hours)
        start_minutes = self.convert_value(start_minutes, self.spinbox_values_minutes)
        end_hours = self.convert_value(end_hours, self.spinbox_values_hours)
        end_minutes = self.convert_value(end_minutes, self.spinbox_values_minutes)

        start_time = (
            f"{start_hours} "
            f"{start_minutes}"
        )
        end_time = (
            f"{end_hours} "
            f"{end_minutes}"
        )
        waypoint = self.var_label_waypoint_input.get()
        if all(
            (
                self.var_combo_activities.get(),
                self.var_label_waypoint_input.get()
            )
        ):
            routine_name = self.combo_routines.get()
            routine = self.routines[routine_name]
            user_input = NPC.create_routine(
                activity = activity,
                start_time = start_time,
                end_time = end_time,
                waypoint = waypoint
            )
            routine.append(user_input)
            self.treeview_schedule.selection_set(
                self.treeview_schedule.insert(
                    '',
                    END,
                    values = (
                        user_input['activity'],
                        user_input['start_time'],
                        user_input['end_time'],
                        user_input['waypoint']
                    )
                )
            )
            self.adjust_time()
            return
        Messagebox.show_error(
            'Waypoint name or activity are unset, ' +
            'please set them accordingly before adding a routine!',
            title = 'Value error',
            parent = self
        )

    def remove_from_schedule(self):
        selection = self.treeview_schedule.selection()
        routine_name = self.combo_routines.get()
        if selection:
            if len(selection) > 1:
                items = [
                    self.treeview_schedule.item(item)['values']
                    for item in selection
                ]
                for routine in self.routines[routine_name]:
                    if list(routine.values()) in items:
                        self.routines[routine_name].remove(routine)
                for selected in selection:
                    self.treeview_schedule.delete(selected)
            else:
                item = self.treeview_schedule.item(selection[0])['values']
                for routine in self.routines[routine_name]:
                    if list(routine.values()) == item:
                        self.routines[routine_name].remove(routine)
                self.treeview_schedule.delete(selection[0])

                all_items = self.treeview_schedule.get_children('')
                if all_items:
                    last_item = all_items[len(all_items)-1]
                    self.treeview_schedule.selection_set(last_item)
                self.adjust_time()

    def update_treeview(self):
        routine_name = self.combo_routines.get()
        if routine_name in self.routines:
            self.treeview_schedule.delete(*self.treeview_schedule.get_children())
            if self.routines[routine_name]:
                for item in self.routines[routine_name]:
                    self.treeview_schedule.insert(
                        '',
                        END,
                        values = (
                            item['activity'],
                            item['start_time'],
                            item['end_time'],
                            item['waypoint']
                        )
                    )
                
    def unlock_widgets(self):
        not_empty = self.var_combo_routines.get()
        state = 'normal' if not_empty else 'disabled'
        widgets = [
            self.button_reset_time,
            self.combo_activities,
            self.combo_worlds,
            self.button_extract,
            self.button_open_directory,
            self.button_add_to_schedule,
            self.button_remove_from_schedule,
            self.entry_directory,
            self.spinbox_time_end_hours,
            self.spinbox_time_end_minutes,
            self.spinbox_time_start_hours,
            self.spinbox_time_start_minutes,
            self.listbox_waypoints
        ]
        for widget in widgets:
            if True in [
                widget is self.combo_activities,
                widget is self.combo_worlds
            ]:
                state_ = 'readonly' if not_empty else 'disabled'
                widget.configure(state=state_)
                continue
            widget.configure(state=state)

    def check_spinbox_value(self):
        pass

    
    def adjust_time(self):
        if self.treeview_schedule.get_children(''):
            selection = self.treeview_schedule.selection()[0]
            selected_item = self.treeview_schedule.item(selection)
            end_time = [
                selected_item['values'][2].split()[0],
                selected_item['values'][2].split()[1]
            ]
            self.var_spinbox_time_start[0].set(end_time[0])
            self.var_spinbox_time_start[1].set(end_time[1])
            if int(end_time[0]) < 9:
                self.var_spinbox_time_end[0].set(
                    f'0{int(end_time[0])+1}'
                )
            else:
                self.var_spinbox_time_end[0].set(
                    f'{int(end_time[0])+1}'
                )
            self.var_spinbox_time_end[1].set('00')

    def reset_time(self):
        self.var_spinbox_time_start[0].set('00')
        self.var_spinbox_time_start[1].set('00')
        self.var_spinbox_time_end[0].set('00')
        self.var_spinbox_time_end[1].set('00')
            
    def time_input_validation(self, var: StringVar):
        if var.get():
            if not var.get().isdigit():
                var.set('00')
            else:
                if len(var.get()) > 2:
                    var.set('00')
                else:
                    if int(var.get()) > 23:
                        var.set('00')
                    else:
                        if ' ' in var.get():
                            var.set('00')
        
        # if not var.get().isdigit():
        #     var.set('00')
        # if int(var.get()) > 23:
        #     var.set('00')
        # if ' ' in var.get():
        #     var.set('00')
        # if len(var.get()) > 2:
        #     var.set('00')



if __name__ == '__main__':
    root = Window(title = 'Test', themename = 'darkly')
    root.geometry('980x720')
    RoutineMenu(root, root).show()
    root.mainloop()
