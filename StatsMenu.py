from ttkbootstrap import (
    Window, IntVar, Button,
    Frame, BooleanVar, Label,
    Checkbutton, Entry, Combobox,
    StringVar, Radiobutton, Spinbox
)

from MiscUtils import PathConstants

class StatsMenu(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.paths = PathConstants()
        self.configure(bootstyle = 'dark')
        self.widgets_init()
        self.widgets_pack()
        self._option_trace()

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()
    
    def widgets_init(self):
        self.var_combo_fight_tactic = StringVar()
        self.var_check_talents = BooleanVar(value = False)
        self.var_check_fightskill = BooleanVar(value = False)
        self.var_entry_fightskill = StringVar(value = 10)
        self.var_entry_fightskill.trace_add(
            'write',
            lambda*_:
                self.input_validation(self.var_entry_fightskill)
        )
        self.frame_stats_stat = dict()
        self.label_stats_stat = dict()
        self.var_entry_stats_stat = dict()
        self.entry_stats_stat = dict()
        self.var_current_stat = dict()
        self.label_stats_value = dict()
        self.button_stats_stat = dict()
        self.combo_fight_tactic_list = [
            i for i in self.paths.get_globals()['NPC']['fight_tactic']['default']
        ]
        self.label_stats_stat_text = {
            'Set Max HP:': 'danger',
            'Set Max MP:': 'info',
            'Set Strength:': 'warning',
            'Set Dexterity:': 'success',
            'Current Max HP:': 'danger', 
            'Current Max MP:': 'info',
            'Current Strength:': 'warning',
            'Current Dexterity:': 'success'
        }
        labels = list(self.label_stats_stat_text.keys())
        self.colors = list(self.label_stats_stat_text.values())
        self.var_radio_option = StringVar(value='auto')
        self.var_spinbox_chapter = StringVar(value=1)
        self.var_spinbox_chapter.trace_add(
            'write',
            lambda*_:
                self.input_validation(self.var_spinbox_chapter)
        )
        
        self.frame_checks = Frame(self)
        self.label_fight_tactic = Label(
            self.frame_checks, text = 'Fight Tactic:'
        )
        self.combo_fight_tactic = Combobox(
            self.frame_checks,
            textvariable = self.var_combo_fight_tactic,
            values = self.combo_fight_tactic_list,
            state='readonly'
        )
        self.check_talents = Checkbutton(
            self.frame_checks,
            text = 'Toggle NPC talents',
            variable = self.var_check_talents,
            bootstyle = 'info-round-toggle'
        )
        self.frame_checks_fightskill = Frame(self.frame_checks)
        self.check_fightskill = Checkbutton(
            self.frame_checks_fightskill,
            text = 'Set NPC fightskill',
            variable = self.var_check_fightskill,
            bootstyle = 'info-round-toggle'
        )
        self.entry_fightskill = Entry(
            self.frame_checks_fightskill,
            textvariable = self.var_entry_fightskill,
            justify = 'center',
            width = 4,
            state = 'disabled',
            bootstyle = 'info'
        )
        self.var_check_fightskill.trace_add(
            'write',
            lambda *_: self._entry_fightskill_reset()
        )
        self.entry_fightskill.bind(
            '<Button1-ButtonRelease>',
            lambda *_: self._entry_fightskill_onclick()
        )

        self.frame_options = Frame(self)
        self.radio_manual = Radiobutton(
            self.frame_options,
            value='manual',
            text='Edit character attributes manually',
            variable=self.var_radio_option,
            command=lambda *_: self._option_trace()
        )
        self.radio_auto = Radiobutton(
            self.frame_options,
            value='auto',
            text='Set attributes to chapter',
            variable=self.var_radio_option,
            command=lambda *_: self._option_trace()
        )
        self.spinbox_chapter = Spinbox(
            self.frame_options,
            from_=1,
            to=6,
            width=3,
            wrap=True,
            textvariable=self.var_spinbox_chapter
        )

        self.frame_stats = Frame(self)
        self.frame_stats_set = Frame(self.frame_stats)
        self.frame_stats_display = Frame(self.frame_stats, bootstyle = 'dark')
        for i in range(8):
            if i > 3:
                self.frame_stats_stat[i] = Frame(self.frame_stats_display)
                continue
            self.frame_stats_stat[i] = Frame(
                self.frame_stats_set,
                bootstyle = 'dark'
            )
        for i in range(8):
            if i > 3:
                self.label_stats_stat[i] = Label(
                    self.frame_stats_stat[i],
                    text = labels[i],
                    width = 20,
                    justify = 'center',
                    bootstyle = f'inverse-{self.colors[i]}'
                )
                self.var_current_stat[i] = IntVar(value = 10)
                self.label_stats_value[i] = Label(
                    self.frame_stats_stat[i],
                    textvariable = self.var_current_stat[i],
                    bootstyle = f'{self.colors[i]}'
                )
                continue
            self.label_stats_stat[i] = Label(
                self.frame_stats_stat[i],
                text = labels[i],
                width = 13,
                bootstyle = f'{self.colors[i]}'
            )
            self.var_entry_stats_stat[i] = IntVar(value = 10)
            self.entry_stats_stat[i] = Entry(
                self.frame_stats_stat[i],
                textvariable = self.var_entry_stats_stat[i],
                bootstyle = f'{self.colors[i]}',
                justify = 'center',
                width = 4
            )
            self.button_stats_stat[i] = Button(
                self.frame_stats_stat[i],
                text = 'Set',
                width = 4,
                bootstyle = f'{self.colors[i]}'
            )
        for i in range(2):
            self.entry_stats_stat[i].configure(width = 6)
            self.var_entry_stats_stat[i].set(100)
        for i in range(4):
            self.button_stats_stat[i].configure(
                command = lambda i = i: self._label_set_stat(
                    i + 4,
                    self.var_entry_stats_stat[i].get()
                )
            )

    def widgets_pack(self):
        self.frame_checks.pack(fill = 'both', padx = 5, pady = 5)
        self.label_fight_tactic.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w'
        )
        self.combo_fight_tactic.pack(
            side = 'left', fill = 'x', expand = True,
            padx = 5, pady = 5, anchor = 'w'
        )
        self.check_talents.pack(
            side = 'left', fill = 'x', expand = True,
            padx = 5, pady = 5, anchor = 'w'
        )
        self.frame_checks_fightskill.pack(
            side = 'left', fill = 'x', expand = True,
            padx = 5, pady = 5, anchor = 'w'
        )
        self.check_fightskill.pack(
            side = 'left', fill = 'x', expand = True,
            padx = 5, pady = 5, anchor = 'e'
        )
        self.entry_fightskill.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

        self.frame_options.pack(
            fill = 'both', expand = True, padx = 5, pady = 5, anchor = 'n'
        )
        self.radio_manual.pack(
            side = 'left', fill = 'both', expand = True,
            padx = 5, pady = 5, anchor = 'w'
        )
        self.radio_auto.pack(
            side = 'left', fill = 'both',
            padx = 5, pady = 5, anchor = 'e'
        )
        self.spinbox_chapter.pack(
            side = 'left',
            padx = 5, pady = 5, anchor = 'e'
        )

        self.frame_stats.pack(
            fill = 'both', expand = True, padx = 5, pady = 5, anchor = 'n'
        )
        self.frame_stats_set.pack(
            side = 'left', fill = 'both', expand = True,
            padx = 5, pady = 5, anchor = 'w'
        )
        self.frame_stats_display.pack(
            side = 'left', fill = 'both', expand = True,
            padx = 5, pady = 5, anchor = 'e'
        )
        for i in self.frame_stats_stat:
            self.frame_stats_stat[i].pack(
                fill = 'both', padx = 5, pady = 5, expand = True
            )
        for i in self.label_stats_stat:
            self.label_stats_stat[i].pack(
                side = 'left', expand = True, padx = 5, pady = 5, anchor = 'w'
            )
        for i in self.entry_stats_stat:
            self.entry_stats_stat[i].pack(
                side = 'left', expand = True, padx = 5, pady = 5, anchor = 'e'
            )
        for i in self.button_stats_stat:
            self.button_stats_stat[i].pack(
                side = 'left', padx = 5, pady = 5, anchor = 'e'
            )
        for i in self.label_stats_value:
            self.label_stats_value[i].pack(
                side = 'left', padx = 5, pady = 5, anchor = 'e'
            )

    def _entry_fightskill_reset(self):
        if self.var_check_fightskill.get():
            self.entry_fightskill.configure(state = 'normal')
        else:
            self.var_entry_fightskill.set(10)
            self.entry_fightskill.configure(state = 'disabled')

    def _entry_fightskill_onclick(self):
        if self.var_check_fightskill.get():
            self.entry_fightskill.select_range(0, 'end')

    def _label_set_stat(self, stat, value):
        self.var_current_stat[stat].set(value)

    def _option_trace(self):
        option = self.var_radio_option.get()
        match option:
            case 'auto':
                for button in self.button_stats_stat:
                    self.button_stats_stat[button].configure(
                        state='disabled'
                    )
                for entry in self.entry_stats_stat:
                    self.entry_stats_stat[entry].configure(
                        state='disabled'
                    )
                for i in range(8):
                    if i < 4:
                        self.label_stats_stat[i].configure(
                            bootstyle = 'secondary'
                        )
                        continue
                    self.label_stats_stat[i].configure(
                        bootstyle = 'secondary-inverse'
                    )
            case 'manual':
                for button in self.button_stats_stat:
                    self.button_stats_stat[button].configure(
                        state='normal'
                    )
                for entry in self.entry_stats_stat:
                    self.entry_stats_stat[entry].configure(
                        state='normal'
                    )
                for i in range(8):
                    if i < 4:
                        self.label_stats_stat[i].configure(
                            bootstyle = self.colors[i]
                        )
                        continue
                    self.label_stats_stat[i].configure(
                        bootstyle = f'{self.colors[i]}-inverse'
                    )

    def input_validation(self, var: StringVar|IntVar):
        if var.get():
            if not var.get().isdigit():
                var.set('')
            else:
                if var is self.var_spinbox_chapter:
                    if int(var.get()) > 6:
                        var.set(1)
                if ' ' in var.get():
                    var.set('')

if __name__ == '__main__':
    root = Window(title = 'test', themename = 'darkly')
    root.geometry('768x300')
    StatsMenu(root).show()
    root.mainloop()
