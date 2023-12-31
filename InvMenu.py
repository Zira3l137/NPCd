from ttkbootstrap import (
    StringVar,
    BooleanVar, Button, Frame,
    Label, Spinbox, Radiobutton,
    Treeview, Scrollbar, END,
    Checkbutton, Entry
)
from ttkbootstrap.tooltip import ToolTip
from PIL import Image, ImageTk

from MiscUtils import PathConstants

class InventoryMenu(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.paths = PathConstants()
        self.configure(bootstyle = 'dark')
        self.widgets_init()
        self.widgets_pack()

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()

    def widgets_init(self):       
        cat_names = self.paths.get_globals()['items']
        self.item_cats = {
            cat_name: cat_names[cat_name].keys() for cat_name in cat_names
        }
        self.item_cats_instances = {
            cat_name: cat_names[cat_name].values() for cat_name in cat_names
        }
        self.cat_icons = {
            file.stem: ImageTk.PhotoImage(
                Image.open(str(self.paths.ICONS_PATH.joinpath(file)))
            )
            for file in self.paths.ICONS_PATH.iterdir()
            if file.stem in cat_names
        }
        self.var_radio_item_cat = StringVar()
        self.var_label_equipped_melee = StringVar()
        self.var_label_equipped_ranged = StringVar()
        self.var_entry_search = StringVar()
        self.var_selection_empty = BooleanVar(value = True)
        self.var_spinbox_quantity = StringVar(value = 1)
        self.var_spinbox_quantity.trace_add(
            'write',
            lambda *_:
                self.quantity_validation()
        )
        self.var_check_add_amb_inv = BooleanVar(value=False)
        self.var_current_cat = StringVar()

        self.var_entry_search.trace_add(
            'write', lambda *_: self.match_to_search()
        )
        
        self.frame_items = Frame(self)
        self.frame_items_cats = Frame(self.frame_items, bootstyle = 'dark')
        self.frame_items_cats_switch = Frame(self.frame_items_cats)
        self.radio_item_cat = dict()
        for cat in self.item_cats:
            self.radio_item_cat[cat] = Radiobutton(
                self.frame_items_cats_switch,
                image = self.cat_icons[cat],
                value = cat,
                variable = self.var_radio_item_cat,
                bootstyle = 'toolbutton',
                width = 16
            )
        for cat_radio in self.radio_item_cat:
            self.radio_item_cat[cat_radio].configure(
                command = lambda var = cat_radio: self.switch_item_cat(var)
            )
            ToolTip(
                self.radio_item_cat[cat_radio],
                text=cat_radio,
                bootstyle='info-inverse'
            )

        self.frame_items_cats_treeview = Frame(self.frame_items_cats)
        self.scrollbar_treeview_items = Scrollbar(
            self.frame_items_cats_treeview,
            orient = 'vertical',
            bootstyle = 'primary-round'
        )
        self.treeview_items = Treeview(
            self.frame_items_cats_treeview,
            columns = ('des', 'inst'),
            show = 'headings',
            bootstyle = 'primary',
            yscrollcommand = self.scrollbar_treeview_items.set
        )
        self.scrollbar_treeview_items.configure(
            command = self.treeview_items.yview
        )
        self.treeview_items.bind(
            '<Button1-ButtonRelease>',
            lambda *_: self.on_click_treeview('inv')
        )
        self.treeview_items.bind(
            '<Double-Button-1>',
            lambda *_: self.set_to_inv()
        )
        self.treeview_items.heading('des', text = 'Description')
        self.treeview_items.column('des', width = 250, anchor = 'center')
        self.treeview_items.heading('inst', text = 'Instance')
        self.treeview_items.column('inst', width = 250, anchor = 'center')
        self.frame_items_manage = Frame(self.frame_items, bootstyle = 'dark')
        self.frame_items_manage_melee = Frame(self.frame_items_manage)
        self.button_equip_melee = Button(
            self.frame_items_manage_melee,
            width = 12,
            text = 'Equip Melee',
            command = self.equip_selected,
            state = 'disabled'
        )
        self.button_unequip_melee = Button(
            self.frame_items_manage_melee,
            width = 12,
            text = 'Unequip',
            state = 'disabled',
            command = lambda *_: self.var_label_equipped_melee.set('')
        )
        self.label_equipped_melee = Label(
            self.frame_items_manage_melee,
            justify = 'center',
            textvariable = self.var_label_equipped_melee,
            bootstyle = 'inverse-info'
        )
        self.frame_items_manage_ranged = Frame(self.frame_items_manage)
        self.button_equip_ranged = Button(
            self.frame_items_manage_ranged,
            width = 12,
            text = 'Equip Ranged',
            command = self.equip_selected,
            state = 'disabled'
        )
        self.button_unequip_ranged = Button(
            self.frame_items_manage_ranged,
            width = 12,
            text = 'Unequip',
            state = 'disabled',
            command = lambda *_: self.var_label_equipped_ranged.set('')
        )
        self.label_equiped_ranged = Label(
            self.frame_items_manage_ranged,
            justify = 'center',
            textvariable = self.var_label_equipped_ranged,
            bootstyle = 'inverse-info'
        )
        self.var_selection_empty.trace_add(
            'write',
            lambda *_: self.control_button_state()
        )
        self.var_label_equipped_melee.trace_add(
            'write',
            lambda *_: (
                self.button_unequip_melee.configure(state = 'normal')
                if self.var_label_equipped_melee.get()
                else self.button_unequip_melee.configure(state = 'disabled')
            )
        )
        self.var_label_equipped_ranged.trace_add(
            'write',
            lambda *_: (
                self.button_unequip_ranged.configure(state = 'normal')
                if self.var_label_equipped_ranged.get()
                else self.button_unequip_ranged.configure(state = 'disabled')
            )
        )
        self.frame_search = Frame(self.frame_items_manage)
        self.label_search = Label(
            self.frame_search,
            text='Search:'
        )
        self.entry_search = Entry(
            self.frame_search,
            textvariable=self.var_entry_search
        )
        self.frame_items_manage_inventory = Frame(self.frame_items_manage)
        self.frame_items_manage_inventory_quantity = Frame(
            self.frame_items_manage_inventory
        )
        self.label_quantity = Label(
            self.frame_items_manage_inventory_quantity,
            text = 'Quantity:'
        )
        self.spinbox_quantity = Spinbox(
            self.frame_items_manage_inventory_quantity,
            width = 4,
            from_ = 1,
            to = 1000,
            wrap = True,
            textvariable = self.var_spinbox_quantity
        )
        self.button_set_to_inv = Button(
            self.frame_items_manage_inventory_quantity,
            width = 6,
            text = 'Set',
            command = lambda *_: self.set_to_inv(),
            bootstyle = 'success'
        )
        self.button_remove_from_inv = Button(
            self.frame_items_manage_inventory_quantity,
            width = 6,
            text = 'Remove',
            command = lambda *_: self.remove_from_inv('single'),
            bootstyle = 'warning'
        )
        self.button_clear_inv = Button(
            self.frame_items_manage_inventory_quantity,
            width = 6,
            text = 'Clear',
            command = lambda *_: self.remove_from_inv('all'),
            bootstyle = 'danger'
        )
        self.check_add_amb_inv = Checkbutton(
            self.frame_items_manage_inventory,
            onvalue=True,
            offvalue=False,
            text='Add ambient inventory',
            variable=self.var_check_add_amb_inv
        )

        self.frame_inventory = Frame(self)
        self.frame_inventory_inv = Frame(
            self.frame_inventory,
            bootstyle = 'dark'
        )
        self.scrollbar_treeview_inv = Scrollbar(
            self.frame_inventory_inv,
            orient = 'vertical',
            bootstyle = 'primary-round'
        )
        self.treeview_inv = Treeview(
            self.frame_inventory_inv,
            columns = ('des','inst','qty'),
            show = 'headings',
            bootstyle = 'info',
            yscrollcommand = self.scrollbar_treeview_inv.set
        )
        self.treeview_inv.heading('des', text = 'Description')
        self.treeview_inv.column('des', width = 250, anchor = 'center')
        self.treeview_inv.heading('inst', text = 'Instance')
        self.treeview_inv.column('inst', width = 250, anchor = 'center')
        self.treeview_inv.heading('qty', text = 'Quantity')
        self.treeview_inv.column('qty', width = 100, anchor = 'center')
        self.treeview_inv.bind(
            '<Button1-ButtonRelease>',
            lambda *_: self.on_click_treeview('items')
        )
        self.treeview_inv.bind(
            '<Double-Button-1>',
            lambda *_: self.remove_from_inv('single')
        )
        self.treeview_inv.bind(
            '<Button3-ButtonRelease>',
            lambda *_: self.change_quantity('+')
        )
        self.treeview_inv.bind(
            '<Button2-ButtonRelease>',
            lambda *_: self.change_quantity('-')
        )
        self.scrollbar_treeview_inv.configure(
            command = self.treeview_inv.yview
        )

    def widgets_pack(self):
        self.frame_items.pack(
            fill = 'both', expand = True, padx = 5, pady = 5
        )
        self.frame_items_cats.pack(
            side = 'left', fill = 'both', padx = 5,
            pady = 5, expand = True, anchor = 'w'
        )
        self.frame_items_cats_switch.pack(fill = 'x', padx = 5, pady = 5)
        for item in self.radio_item_cat:
            self.radio_item_cat[item].pack(
                side = 'left', expand = True, padx = 2, pady = 2, fill = 'both'
            )
        self.frame_items_cats_treeview.pack(
            fill = 'both', expand = True, padx = 5, pady = 5
        )
        self.scrollbar_treeview_items.pack(
            side = 'right', fill = 'y', anchor = 'center'
        )
        self.treeview_items.pack(
            side = 'left', fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.frame_items_manage.pack(
            side = 'left', fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.frame_items_manage_melee.pack(fill = 'x', padx = 5, pady = 5)
        self.button_equip_melee.pack(side = 'left', padx = 5, pady = 5)
        self.button_unequip_melee.pack(side = 'left', padx = 5, pady = 5)
        self.label_equipped_melee.pack(side = 'left', pady = 5, fill = 'both')
        self.frame_items_manage_ranged.pack(fill = 'x', padx = 5, pady = 5)
        self.button_equip_ranged.pack(side = 'left', padx = 5, pady = 5)
        self.button_unequip_ranged.pack(side = 'left', padx = 5, pady = 5)
        self.label_equiped_ranged.pack(side = 'left', pady = 5, fill = 'both')
        self.frame_search.pack(fill = 'x', padx = 5, pady = 5)
        self.label_search.pack(side='left', padx=5, pady=5)
        self.entry_search.pack(side='left', padx=5, pady=5, expand=True, fill='x')
        self.frame_items_manage_inventory.pack(fill = 'x', padx = 5, pady = 5)
        self.frame_items_manage_inventory_quantity.pack(
            fill = 'x', padx = 5, pady = 5
        )
        self.label_quantity.pack(side = 'left', padx = 5, pady = 5)
        self.spinbox_quantity.pack(
            side = 'left', padx = 5, pady = 5, expand = True, anchor = 'w'
        )
        self.button_set_to_inv.pack(
            side = 'left', padx = 5, pady = 5, expand = True, anchor = 'center'
        )
        self.button_remove_from_inv.pack(
            side = 'left', padx = 5, pady = 5, expand = True, anchor = 'center'
        )
        self.button_clear_inv.pack(
            side = 'left', padx = 5, pady = 5, expand = True, anchor = 'center'
        )
        self.check_add_amb_inv.pack(
            fill = 'x', padx = 5, pady = 5, expand=True
        )

        self.frame_inventory.pack(
            fill = 'both', expand = True, padx = 5, pady = 5
        )
        self.frame_inventory_inv.pack(
            side = 'left', fill = 'both', padx = 5, pady = 5, expand = True
        )
        self.scrollbar_treeview_inv.pack(
            side = 'right', fill = 'y', anchor = 'center'
        )
        self.treeview_inv.pack(
            side = 'left', fill = 'both', padx = 5, pady = 5, expand = True
        )

    def switch_item_cat(self, cat):
        if self.treeview_items.get_children(''):
            self.treeview_items.delete(*self.treeview_items.get_children(''))
        for item, instance in zip(
            self.item_cats[cat],
        self.item_cats_instances[cat]
        ):
            self.treeview_items.insert('', END, values=(item, instance))
        self.button_equip_melee.configure(state='disabled')
        self.button_equip_ranged.configure(state='disabled')
        if not self.var_current_cat.get() == cat:
            self.var_current_cat.set(cat)

    def control_button_state(self):
        condition = self.var_selection_empty.get()
        condition_selection = self.treeview_items.selection()
        if not condition and condition_selection:
            selection = self.treeview_items.item(
                self.treeview_items.selection()[0]
            )
            wpn = selection['values'][1].split('_')[0]
            match wpn:
                case 'ItMw':
                    self.button_equip_melee.configure(state='normal')
                case 'ItRw':
                    self.button_equip_ranged.configure(state='normal')
                case _:
                    self.button_equip_melee.configure(state='disabled')
                    self.button_equip_ranged.configure(state='disabled')

    def equip_selected(self):
        selection = self.treeview_items.item(
            self.treeview_items.selection()[0]
        )
        wpn = selection['values'][1].split('_')[0]
        match wpn:
            case 'ItMw':
                self.var_label_equipped_melee.set(
                    f'Equipped: {selection["values"][1]}'
                )
            case 'ItRw':
                self.var_label_equipped_ranged.set(
                    f'Equipped: {selection["values"][1]}'
                )

    def set_to_inv(self):
        selected_items = self.treeview_items.selection()
        selected_items_inv = self.treeview_inv.selection()
        quantity = self.var_spinbox_quantity.get()
        
        if selected_items_inv:
            for item in selected_items_inv:
                self.treeview_inv.item(
                    item,
                    values = (
                    self.treeview_inv.item(item)['values'][0],
                    self.treeview_inv.item(item)['values'][1],
                    quantity
                    )
                )

        if selected_items:
            for selected_item in selected_items:
                item = self.treeview_items.item(selected_item)
                item_name = item['values'][1]
                matching_items = [
                    item for item in self.treeview_inv.get_children('')
                    if self.treeview_inv.item(item)['values'][1] == item_name
                    ]
                if matching_items:
                    self.treeview_inv.item(
                        matching_items[0],
                        values = (
                        self.treeview_inv.item(matching_items[0])['values'][0],
                        item_name, quantity
                        )
                    )
                else:
                    self.treeview_inv.insert(
                        parent='',
                        index='end',
                        values=(item['values'][0],
                        item_name, quantity)
                    )

    def on_click_treeview(self, id):
        match id:
            case 'items':
                self.treeview_items.selection_remove(
                    self.treeview_items.selection()
                )
            case 'inv':
                self.var_selection_empty.set(False)
                self.treeview_inv.selection_remove(
                    self.treeview_inv.selection()
                )

    def remove_from_inv(self, action):
        if self.treeview_inv.get_children(''):
            match action:
                case 'single':
                    selected_item = self.treeview_inv.selection()[0]
                    selected_items = self.treeview_inv.selection()
                    if len(selected_items) > 1:
                        for unit in selected_items:
                            self.treeview_inv.delete(unit)
                    else:
                        self.treeview_inv.delete(selected_item)
                case 'all':
                    all_items = self.treeview_inv.get_children('')
                    for every_item in all_items:
                        self.treeview_inv.delete(every_item)
    
    def validate_request(self, request: str) -> list[(str)]:
        search_results = list()
        names = set()
        instances = set()
        for category in self.item_cats:
            names.update(self.item_cats[category])
            instances.update(self.item_cats_instances[category])
        if '_' in request:
            if request == '_':
                return
            for instance in instances:
                if request.lower() in instance.lower():
                    search_results.append(instance)
        else:
            if not request:
                return
            for name in names:
                if request.lower() in name.lower():
                    search_results.append(name)

        return search_results
   
    def match_to_search(self):
        names = list()
        instances = list()
        for category in self.item_cats:
            names.extend(self.item_cats[category])
            instances.extend(self.item_cats_instances[category])

        category = self.var_current_cat.get()
        search_request = self.var_entry_search.get()
        search_result = self.validate_request(search_request)
        if search_result:
            self.treeview_items.delete(
                *self.treeview_items.get_children('')
            )
            for element in search_result:
                if '_' in element:
                    index = instances.index(element)
                    name = names[index]
                    self.treeview_items.insert(
                        '', END,
                        values=(
                            name, element
                        )
                    )
                else:
                    index = names.index(element)
                    instance = instances[index]
                    self.treeview_items.insert(
                        '', END,
                        values=(
                            element, instance
                        )
                    )
        else:
            if category:
                self.switch_item_cat(category)
            else:
                if self.treeview_items.get_children(''):
                    self.treeview_items.delete(
                        *self.treeview_items.get_children('')
                    )

    def quantity_validation(self):
        var = self.var_spinbox_quantity
        if var.get():
            if not var.get().isdigit():
                var.set(0)
            else:
                if ' ' in var.get():
                    var.set(0)

    def change_quantity(self, key: str):
        if self.treeview_inv.get_children(''):
            selection = self.treeview_inv.selection()
            match key:
                case '+':
                    for item_id in selection:
                        item = self.treeview_inv.item(item_id)
                        quantity = int(item['values'][2])
                        if quantity != 1000:
                            quantity += 1
                        else:
                            quantity = 1
                        self.treeview_inv.item(
                            item_id, values=(
                                self.treeview_inv.item(item_id)['values'][0],
                                self.treeview_inv.item(item_id)['values'][1],
                                quantity
                            )
                        )
                case '-':
                    for item_id in selection:
                        item = self.treeview_inv.item(item_id)
                        quantity = int(item['values'][2])
                        if quantity != 1:
                            quantity -= 1
                        else:
                            quantity = 1000
                        self.treeview_inv.item(
                            item_id, values=(
                                self.treeview_inv.item(item_id)['values'][0],
                                self.treeview_inv.item(item_id)['values'][1],
                                quantity
                            )
                        )
