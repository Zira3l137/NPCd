from tkinter import Listbox
from tkinter.filedialog import askdirectory
from datetime import datetime, timedelta
from typing import Callable

from ttkbootstrap import (
    StringVar,Image,
    BooleanVar,Button,
    Frame,Label,
    Entry,Combobox,
    Spinbox,Scrollbar,
    Treeview,END,ImageTk,
    IntVar
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
        self.TIME_LIMIT = 24*60
        self.overall_time = IntVar(value=0)
        self.buffer = None
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
        self.combo_activities_list = list(
            self.paths.get_activities()['default']
        )

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
            width = 20,
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
            width = 15,
            values = self.combo_worlds_list,
            state = 'disabled'
        )
        self.var_combo_worlds.trace_add(
            'write',
            lambda *_: self.switch_worlds()
        )
        self.button_extract = Button(
            self.frame_waypoints_world,
            text = '   Extract\nWaypoints',
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
            width = 25,
            height = 6,
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
        self.treeview_schedule.column('act', width = 1, anchor = 'center')
        self.treeview_schedule.heading('start', text = 'Start Time')
        self.treeview_schedule.column('start', width = 1, anchor = 'center')
        self.treeview_schedule.heading('end', text = 'End Time')
        self.treeview_schedule.column('end', width = 1, anchor = 'center')
        self.treeview_schedule.heading('wp', text = 'Waypoint')
        self.treeview_schedule.column('wp', width = 300, anchor = 'center')

        self.treeview_schedule.bind(
            '<Button1-ButtonRelease>',
            lambda *_: self.adjust_time()
        )
        self.treeview_schedule.bind(
            '<Control-c>',
            lambda *_: self.copy_actions()
        )
        self.treeview_schedule.bind(
            '<Control-v>',
            lambda *_: self.paste_actions()
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

    def get_routine_name(self):
        """
        Returns a formatted routine name by combining the values of
        `var_entry_routine_name` and `var_entry_routine_id` with a
        prefix of "Rtn_".

        :return: Formatted routine name (string)
        """
        name = self.var_entry_routine_name.get()
        id_ = self.var_entry_routine_id.get()
        return f'Rtn_{name}{id_}'

    def manage_routine(self, condition):
        """
        Manage routines based on the given condition.

        Args:
            condition (str): The condition parameter determines whether
            to add or remove a routine. It can have two possible values:
            '+' to add a routine and '-' to remove a routine.

        Returns:
            None

        Example Usage:
            # Initialize the RoutineMenu object
            routine_menu = RoutineMenu(parent, edit_window)

            # Add a routine
            routine_menu.manage_routine('+')

            # Remove a routine
            routine_menu.manage_routine('-')
        """
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
                    for child in self.treeview_schedule.get_children(''):
                        self.treeview_schedule.delete(child)
                    self.calculate_time(update=True)

    def update_npc_id(self):
        """
        Update the NPC ID and routine ID based on the value
        entered in the Main module's entry field.

        Inputs:
        - main_id: The NPC ID entered in the Main module's entry field.
        - local_id: The current value of the routine ID.

        Flow:
        1. Get the NPC ID from the Main module's entry field.
        2. Check if the NPC ID is empty or not a digit. If it is, set
        the routine ID to _{NPC ID} and set the label color to red.
        3. If the NPC ID is valid and different from the current routine ID,
        update the routine ID to _{NPC ID}.
        4. Set the label color to green.

        Outputs:
        - The routine ID is updated based on the NPC ID entered in the Main
        module's entry field.
        - The label color is set to red if the NPC ID is invalid or green
        if it is valid.
        """
        main_id = self.modules['Main'].var_entry_id.get()
        local_id = self.var_entry_routine_id.get()
        if True in (not main_id, not main_id.isdigit()):
            self.var_entry_routine_id.set('_{NPC ID}')
            self.label_routine_id.configure(foreground='Red')
            return
        if main_id and local_id != main_id:
            self.var_entry_routine_id.set(f'_{main_id}')
        self.label_routine_id.configure(foreground='Green')

    def open_directory(self):
        """
        Opens a directory dialog box and sets the selected directory
        as the value of the var_entry_directory variable.

        Inputs: None

        Outputs: None
        """
        directory = askdirectory(
            initialdir=self.paths.WORLDS_PATH,
            mustexist=True
        )
        if directory:
            self.var_entry_directory.set(directory)

    def extract_waypoints(self):
        """
        Extracts waypoints from a directory and updates the list of available
        worlds and waypoints in the GUI.

        Inputs:
        - self: The instance of the RoutineMenu class.

        Outputs:
        - None
        """
        worlds = ExtractWaypoints(self.var_entry_directory.get())
        self.wps = worlds.zen_wps
        self.combo_worlds_list = list(self.wps)
        self.combo_worlds.configure(values=self.combo_worlds_list)
        self.combo_worlds.set(self.combo_worlds_list[0])
        self.var_listbox_waypoints.set(list(self.wps[self.var_combo_worlds.get()]))

    def switch_worlds(self):
        """
        Update the list of waypoints based on the selected world in
        the combo box.

        Inputs:
        - None

        Flow:
        1. Get the selected world from the combo box.
        2. Update the list of waypoints based on the selected world.

        Outputs:
        - None
        """
        self.var_listbox_waypoints.set(
            list(self.wps[self.var_combo_worlds.get()])
        )

    def select_waypoint(self):
        """
        Selects a waypoint from a list of waypoints and updates the value
        of a label with the selected waypoint.
    
        Inputs:
        - None
    
        Flow:
        1. Get the list of waypoints from the listbox.
        2. Check if there are any waypoints in the list.
        3. If there are waypoints, set the value of the label to the
        selected waypoint.
    
        Outputs:
        - None
        """
        waypoints = self.listbox_waypoints.get(0,END)
        if waypoints:
            self.var_label_waypoint_input.set(
                self.listbox_waypoints.selection_get()
            )

    def time_difference(self, time1: datetime, time2: datetime) -> int:
        """
        Calculates the time difference in minutes between two datetime objects.

        Args:
            time1 (datetime): The first datetime object.
            time2 (datetime): The second datetime object.

        Returns:
            int: The time difference in minutes between the two datetime
            objects.
        """
        if time1 <= time2:
            difference: timedelta = time2 - time1
            minutes = int(difference.total_seconds() / 60)
        else:
            time2 += timedelta(1)
            difference: timedelta = time2 - time1
            minutes = int(difference.total_seconds() / 60)
        return minutes

    def calculate_time(
        self,
        start_h=None, start_m=None,
        end_h=None, end_m=None,
        remove=False, update=False
    ):
        """
        Calculate the overall time span of a set of elements in a treeview.

        Args:
            start_h (str, optional): The hour value of the start time of the
            element.
            start_m (str, optional): The minute value of the start time of
            the element.
            end_h (str, optional): The hour value of the end time of the
            element.
            end_m (str, optional): The minute value of the end time of the
            element.
            remove (bool, optional): A boolean value indicating whether to
            remove an element from the treeview.
            update (bool, optional): A boolean value indicating whether to
            update the overall time after removing an element.

        Raises:
            KeyError: If the time span is 0 or exceeds the time limit of
            24 hours.

        Returns:
            None. It updates the overall_time variable, which represents the
            overall time span of the elements in the treeview.
        """
        treeview_elements = self.treeview_values()
        treeview_time_sum = 0

        if remove:
            if self.treeview_values():
                for element in treeview_elements:
                    h1, m1, h2, m2 = (
                        element[1].split()[0],
                        element[1].split()[1],
                        element[2].split()[0],
                        element[2].split()[1]
                    )
                    start = datetime.strptime(f'{h1}:{m1}', '%H:%M')
                    end = datetime.strptime(f'{h2}:{m2}', '%H:%M')
                    time_span: int = self.time_difference(start, end)
                    treeview_time_sum += time_span
                self.overall_time.set(treeview_time_sum)
                print(self.overall_time.get())
            else:
                self.overall_time.set(0)
        elif update:
            if not treeview_elements:
                self.overall_time.set(0)
                print(self.overall_time.get())
            else:
                for element in treeview_elements:
                    h1, m1, h2, m2 = (
                        element[1].split()[0],
                        element[1].split()[1],
                        element[2].split()[0],
                        element[2].split()[1]
                    )
                    start = datetime.strptime(f'{h1}:{m1}', '%H:%M')
                    end = datetime.strptime(f'{h2}:{m2}', '%H:%M')
                    time_span: int = self.time_difference(start, end)
                    treeview_time_sum += time_span
                self.overall_time.set(treeview_time_sum)
                print(treeview_time_sum)
        else:
            item_start = datetime.strptime(f'{start_h}:{start_m}', '%H:%M')
            item_end = datetime.strptime(f'{end_h}:{end_m}', '%H:%M')
            item_time_span = 0

            if self.time_difference(item_start, item_end) == 0:
                Messagebox.show_error(
                        'Cannot create element with time span 0',
                        'Time span equals zero',
                        self
                    )
                raise KeyError

            if not treeview_elements:
                time_span = self.time_difference(item_start, item_end)
                self.overall_time.set(time_span)
                print(time_span)
            else:
                for element in treeview_elements:
                    h1, m1, h2, m2 = (
                        element[1].split()[0],
                        element[1].split()[1],
                        element[2].split()[0],
                        element[2].split()[1]
                    )
                    start = datetime.strptime(f'{h1}:{m1}', '%H:%M')
                    end = datetime.strptime(f'{h2}:{m2}', '%H:%M')
                    time_span: int = self.time_difference(start, end)
                    treeview_time_sum += time_span
                item_time_span = self.time_difference(item_start, item_end)
                result = item_time_span+treeview_time_sum
                if not result > self.TIME_LIMIT:
                    self.overall_time.set(result)
                    print(result)
                else:
                    Messagebox.show_error(
                        f'''You are exceeding 24 hours. Excessive time:
                        {result - self.TIME_LIMIT}''',
                        'Time period error',
                        self
                    )
                    raise KeyError

    def adjust_time(self):
        """
        Adjusts the start and end time values based on the selected item
        in the treeview_schedule widget.

        Inputs:
        - None

        Flow:
        1. Check if there are any items in the treeview_schedule widget.
        2. If there is a selected item, retrieve its values.
        3. Split the end time value into hours and minutes.
        4. Set the start time values to the end time values.
        5. Update the end time values based on the end time hours.
        6. Set the end time minutes to '00'.

        Outputs:
        - None
        """
        if self.treeview_schedule.get_children(''):
            selection = self.treeview_schedule.selection()
            if selection:
                selected_item = self.treeview_schedule.item(selection[0])
            else:
                return
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
            elif int(end_time[0]) == 23:
                self.var_spinbox_time_end[0].set(
                    '00'
                )
            else:
                self.var_spinbox_time_end[0].set(
                    f'{int(end_time[0])+1}'
                )
            self.var_spinbox_time_end[1].set('00')

    def reset_time(self):
        """
        Resets the values of the time inputs in the RoutineMenu class.

        Inputs:
        - None

        Flow:
        1. Sets the values of the time inputs (var_spinbox_time_start and
        var_spinbox_time_end) to '00'.

        Outputs:
        - None
        """
        self.var_spinbox_time_start[0].set('00')
        self.var_spinbox_time_start[1].set('00')
        self.var_spinbox_time_end[0].set('00')
        self.var_spinbox_time_end[1].set('00')

    def convert_value(self, value, value_list):
        """
        Convert the value to the corresponding value in the
        value_list if it is not already in the list.

        Args:
            value (any type): The value to be converted.
            value_list (list): The list of values to check against.

        Returns:
            any type: The converted value.
        """
        if value not in value_list:
            value = value_list[int(value)]
        return value
    
    def spinbox_time_period(self) -> Callable[[str], dict]:
        """
        Returns a dictionary containing the values of the start
        and end time periods selected in the GUI.

        Args:
            period (str, optional): A string indicating the time period
            to retrieve. It can be 'start', 'end', or an empty string.
            If not provided, it will return both the start and end time
            periods.

        Returns:
            dict: A dictionary containing the start and/or end time values
            selected in the GUI. The keys in the dictionary are 'start_h',
            'start_m', 'end_h', and 'end_m'.
        """
        def return_time_period(period='') -> dict:
            match period:
                case 'start':
                    return {
                        'start_h': self.var_spinbox_time_start[0].get(),
                        'start_m': self.var_spinbox_time_start[1].get()
                    }
                case 'end':
                    return {
                        'end_h': self.var_spinbox_time_end[0].get(),
                        'end_m': self.var_spinbox_time_end[1].get()
                    }
                case '':
                    return {
                        'start_h': self.var_spinbox_time_start[0].get(),
                        'start_m': self.var_spinbox_time_start[1].get(),
                        'end_h': self.var_spinbox_time_end[0].get(),
                        'end_m': self.var_spinbox_time_end[1].get()
                    }
        return return_time_period

    def fetch_time_spans(self) -> tuple:
        """
        Retrieves the start and end time entries from the treeview widget
        and returns them as a tuple.

        Returns:
            tuple: A tuple containing the start and end time entries from
            the treeview widget.
        """
        if self.treeview_values():
            start_entries = [
                (
                    values[1].split()[0],
                    values[1].split()[1]
                )
                for values in self.treeview_values()
            ]
            end_entries = [
                (
                    values[2].split()[0],
                    values[2].split()[1]
                )
                for values in self.treeview_values()
            ]
        
            return (start_entries, end_entries)

    def new_time_period(self, time_period: dict) -> list[str]:
        """
        Returns a list of formatted start and end times based on
        the input time period.

        Args:
            time_period (dict): A dictionary representing a time period
            with keys 'start_h', 'start_m', 'end_h', and 'end_m'.
            The values represent the hours and minutes of the start and
            end times.

        Returns:
            list[str]: A list of two strings representing the formatted
            start and end times of the input time period.
        """
        return [
            "{s_h} {s_m}".format(
                s_h = self.convert_value(
                    time_period['start_h'], self.spinbox_values_hours
                ),
                s_m = self.convert_value(
                    time_period['start_m'], self.spinbox_values_minutes
                )
            ),
            "{e_h} {e_m}".format(
                e_h = self.convert_value(
                    time_period['end_h'], self.spinbox_values_hours
                ),
                e_m = self.convert_value(
                    time_period['end_m'], self.spinbox_values_minutes
                )
            )
        ]

    def add_routine(self, activity, start_time, end_time, waypoint):
        """
        Add a new routine to the existing routines in the RoutineMenu class.

        Args:
            activity (str): The activity for the routine.
            start_time (str): The start time for the routine.
            end_time (str): The end time for the routine.
            waypoint (str): The waypoint for the routine.

        Returns:
            None. The method modifies the existing routines and updates
            the treeview_schedule widget.
        """
        routine_name = self.combo_routines.get()
        routine = self.routines[routine_name]
        user_input = NPC.create_routine(
            activity=activity,
            start_time=start_time,
            end_time=end_time,
            waypoint=waypoint
        )
        routine.append(user_input)
        self.treeview_schedule.selection_set(
            self.treeview_schedule.insert(
                '',
                END,
                values=(
                    user_input['activity'],
                    user_input['start_time'],
                    user_input['end_time'],
                    user_input['waypoint']
                )
            )
        )
        self.treeview_schedule.see(
            self.treeview_schedule.selection()[0]
        )

    def get_waypoint(self) -> str|None:
        """
        Retrieves the chosen waypoint from the var_label_waypoint_input
        variable.

        Returns:
            str|None: The chosen waypoint as a string, or None if no
            waypoint is chosen.
        """
        waypoint_chosen = self.var_label_waypoint_input.get()
        if waypoint_chosen != 'NONE':
            return waypoint_chosen
        
    def add_to_schedule(self, internal=None):
        """
        Adds a routine to the schedule.

        Args:
            internal (tuple, optional): A tuple containing internal values
            for the activity, start time, end time, and waypoint. If provided,
            these values will be used instead of fetching them from the UI.

        Raises:
            KeyError: If the overall time in the schedule has reached the
            limit of 24 hours.

        Returns:
            None: The method adds the routine to the schedule and updates
            the overall time.
        """
        existent_time_spans: tuple = self.fetch_time_spans()
        if not internal:
            spinbox_time_period: Callable = self.spinbox_time_period()
            start_time, end_time = self.new_time_period(spinbox_time_period())
            activity: str = self.var_combo_activities.get()
            waypoint: str|None = self.get_waypoint()
        else:
            spinbox_time_period = (
                (
                    internal[1].split()[0],
                    internal[1].split()[1]
                ),
                (
                    internal[2].split()[0],
                    internal[2].split()[1]
                )
            )
            start_time = internal[1]
            end_time = internal[2]
            activity = internal[0]
            waypoint = internal[3]

        if self.overall_time.get() == self.TIME_LIMIT:
            Messagebox.show_error(
                'You reached 24 hours limit for this routine',
                'Time period error',
                parent = self
            )
            raise KeyError
        if not internal:
            if '' in tuple(spinbox_time_period().values()):
                Messagebox.show_error(
                    'Please set appropriate values for activity time period!',
                    'Time period values are unset',
                    parent = self
                )
                return
        if existent_time_spans:
            if not internal:
                if any(
                    (
                        (tuple(spinbox_time_period('start').values())
                        in existent_time_spans[0]),
                        (tuple(spinbox_time_period('end').values())
                        in existent_time_spans[1])
                    )
                ):
                    error_message ='''
    Activity with time span: {start_h}:{start_m} - {end_h}:{end_m}
    cannot be added - invalid start or end time values!
                    '''
                    Messagebox.show_error(
                        error_message.format_map(spinbox_time_period()),
                        'Invalid activity time span',
                        parent = self
                    )
                    return

        if not internal:
            try:
                self.calculate_time(*tuple(spinbox_time_period().values()))
            except KeyError:
                return
        else:
            try:
                self.calculate_time(
                    *(
                        list(spinbox_time_period[0])
                        +list(spinbox_time_period[1])
                    )
                )
            except KeyError:
                return

        if all((activity, start_time, end_time, waypoint)):
            self.add_routine(
                activity,
                start_time,
                end_time,
                waypoint
            )
            self.adjust_time()
            return
        Messagebox.show_error(
            'Waypoint name or activity are unset, ' +
            'please set them accordingly before adding a routine!',
            'Value error',
            parent = self
        )

    def remove_from_schedule(self):
        """
        Remove selected items from the schedule displayed in a treeview widget.
        Updates the 'routines' dictionary and recalculates the overall time.

        :return: None
        """
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
            self.calculate_time(remove=True)
            self.adjust_time()

    def update_treeview(self):
        """
        Updates the treeview_schedule widget based on the selected routine
        name from the combobox.
        Retrieves the routine data from a dictionary, clears the existing
        items in the treeview,
        and inserts new items with the activity, start time, end time, and
        waypoint values from the routine data.
        Finally, it calls the calculate_time method to update the overall
        time.
        """
        routine_name = self.combo_routines.get()
        if routine_name in self.routines:
            self.treeview_schedule.delete(*self.treeview_schedule.get_children())
            if self.routines[routine_name]:
                for item in self.routines[routine_name]:
                    self.treeview_schedule.insert(
                        '',
                        END,
                        values=(
                            item['activity'],
                            item['start_time'],
                            item['end_time'],
                            item['waypoint']
                        )
                    )
            self.calculate_time(update=True)

    def unlock_widgets(self):
        """
        Unlock certain widgets based on the value of the var_combo_routines
        variable.

        Inputs:
        - None

        Flow:
        1. Get the value of the var_combo_routines variable.
        2. If the value is not empty, set the state of certain widgets to
        'normal', otherwise set it to 'disabled'.
        3. Iterate over a list of widgets.
        4. If the widget is the combo_activities or combo_worlds, set the
        state to 'readonly' if the value is not empty, otherwise set it to
        'disabled'.
        5. For all other widgets, set the state to the value determined in
        step 2.

        Outputs:
        - None
        """
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

    def time_input_validation(self, var: StringVar):
        """
        Validates the input values for the time spinboxes.

        Args:
            var (StringVar): The StringVar object representing the
            value of the time spinbox.

        Returns:
            None. The method modifies the value of the var StringVar
            object if necessary.
        """
        value = var.get()
        if value:
            if not value.isdigit() or len(value) > 2:
                var.set('00')
            elif var in [self.var_spinbox_time_start[1], self.var_spinbox_time_end[1]]:
                if int(value) > 59 or ' ' in value:
                    var.set('00')
            elif int(value) > 23 or ' ' in value:
                var.set('00')

    def treeview_values(self) -> list[tuple] | None:
        """
        Retrieves the values of all the items in the Treeview widget and
        returns them as a list of tuples.

        Returns:
            list[tuple] | None: A list of tuples containing the values of
            all the items in the Treeview widget.
                Returns None if there are no items in the Treeview widget.
        """
        children = self.treeview_schedule.get_children('')
        if not children:
            return None
        values = [
            self.treeview_schedule.item(child)['values']
            for child in children
        ]
        return values

    def format_time(self, time: str, reverse=False) -> str:
        """
        Format a time string in either a forward or reverse format.

        Args:
            time (str): A time string in the format 'start end' or 'start:end'.
            reverse (bool, optional): A flag indicating whether to format
            the time string in reverse order. Defaults to False.

        Returns:
            str: A formatted time string in either 'start:end' or 'start end'
            format, depending on the value of `reverse`.

        Example Usage:
            routine_menu = RoutineMenu(parent, edit_window)
            formatted_time = routine_menu.format_time('10 20', reverse=False)
            print(formatted_time)  # Output: '10:20'

            formatted_time_reverse = routine_menu.format_time(
                '10:20',
                reverse=True
            )
            print(formatted_time_reverse)  # Output: '10 20'
        """
        if not reverse:
            digits = time.split()
            start = digits[0]
            end = digits[1]
            return f'{start}:{end}'
        else:
            digits = time.split(':')
            start = digits[0]
            end = digits[1]
            return f'{start} {end}'

    def time_to_minutes(self, time_str):
        """
        Converts a time string in the format "HH:MM" to the equivalent
        number of minutes.

        Args:
            time_str (str): A time string in the format "HH:MM".

        Returns:
            int: The total number of minutes represented by the input
            time string.
        """
        t = datetime.strptime(time_str, "%H:%M")
        return t.hour*60 + t.minute

    def minutes_to_time(self, minutes):
        """
        Convert minutes to a formatted time string.

        Args:
            minutes (int): The number of minutes.

        Returns:
            str: A formatted time string in the format "HH:MM".
        """
        hours = minutes // 60
        if hours == 24:
            hours = 0
        minutes = minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def last_action_minutes(self) -> int:
        """
        Calculate the number of minutes since the last action in a list
        of actions.

        Returns:
            int: The number of minutes since the last action.
        """
        actions: list[tuple] | None = self.treeview_values()
        if actions:
            last_item = actions[-1]
            end_time = self.format_time(last_item[2])
            return self.time_to_minutes(end_time)
        else:
            return 0

    def recalculate_time_spans(
        self,
        actions: list[list],
        base=0,
        index=0
    ) -> list[list, int]:
        """
        Recalculates the time spans for a list of actions based on a given
        base time.

        Args:
            actions (list[list]): A list of actions, where each action is a
            list containing a sublist of time values and a summand (duration).
            base (int, optional): The base time in minutes from which to
            calculate the start and end times. Defaults to 0.
            index (int, optional): The index of the current action in the
            list. Defaults to 0.

        Returns:
            list[list, int]: The updated list of actions with the start and
            end times recalculated based on the base time.
    
        Raises:
            KeyError: If the end time exceeds 23:59.

        Example Usage:
            routine_menu = RoutineMenu(parent, edit_window)
            actions = [
                [['00:00', '00:00'], 30],
                [['00:00', '00:00'], 45],
                [['00:00', '00:00'], 60]
            ]
            base_time = 0
            index = 0
            updated_actions = routine_menu.recalculate_time_spans(
                actions, base_time, index
            )
            print(updated_actions)
        """
        end_point = len(actions)-1
        index_ = index
        actions_ = actions
        action = actions_[index_]
        values: list = action[0]
        summand: int = action[1]
        values[1] = self.format_time(
            self.minutes_to_time(base),
            reverse=True
        )
        values[2] = self.format_time(
            self.minutes_to_time(base+summand),
            reverse=True
        )
        actions_[index_][0] = values
        if index_ < end_point:
            index_ += 1
            if int(values[2].split()[0]) > 23:
                raise KeyError
            formatted_base = self.format_time(values[2])
            converted_base = self.time_to_minutes(formatted_base)
            return self.recalculate_time_spans(
                actions_,
                converted_base,
                index_
            )
        else:
            return actions_

    def copy_actions(self):
        """
        Copies selected actions from a treeview and stores them in a buffer
        along with the time difference between their start and end times.
        """
        actions: list[tuple] | None = self.treeview_values()
        if actions:
            selection: list[str] = [
                self.treeview_schedule.item(child)['values']
                for child
                in self.treeview_schedule.selection()
            ]
            selection_minute_difference: list[int] = [
                self.time_difference(   
                    datetime.strptime(
                        f'{item[1].split()[0]}:{item[1].split()[1]}', '%H:%M'
                    ),
                    datetime.strptime(
                        f'{item[2].split()[0]}:{item[2].split()[1]}', '%H:%M'
                    )
                )
                for item
                in selection
            ]
            self.buffer = [
                list(pair) for pair in zip(
                    selection,
                    selection_minute_difference
                )
            ]

    def paste_actions(self):
        """
        Paste a set of actions into the schedule.

        This method recalculates the time spans of the actions based on the
        last action in the schedule and adds them to the schedule.

        :return: None
        """
        last_action_minutes: int = self.last_action_minutes()
        new_actions: list = []
        try:
            recalculated_entries = self.recalculate_time_spans(
                self.buffer,
                last_action_minutes
            )
        except KeyError:
            Messagebox.show_error(
                '''
                Failed to paste entries, because of 24 hour exceeding
                time spans.
                ''',
                'Time span error',
                self
            )
            return
        else:
            for values, _ in recalculated_entries:
                new_actions.append(values)
            for action in new_actions:
                try:
                    self.add_to_schedule(action)
                except KeyError:
                    return
