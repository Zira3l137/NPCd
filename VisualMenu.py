from tkinter import  Listbox, END

from ttkbootstrap import (
    Window, StringVar, IntVar,
    DoubleVar, Button, Frame,
    Label, Combobox, Radiobutton,
    Scale, Scrollbar, Canvas
)

from PIL import Image, ImageTk

from MiscUtils import NPC, PathConstants

from pathlib import Path

class VisualMenu(Frame):
    def __init__(self, parent, root, edit_window):
        super().__init__(master = parent)
        self.modules = edit_window.menus
        self.paths = PathConstants()
        self.configure(bootstyle = 'dark')
        self.widgets_init()
        self.widgets_pack()
        self.root = root

    def show(self):
        self.pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def hide(self):
        self.forget()
    
    def widgets_init(self):
        self.visual_frames = dict()
        self.visual_frame_names = [
            'gender',
            'outfit',
            'head',
            'skin',
            'walk_overlay',
            'fatness',
            'face'
        ]

        self.var_combo_head = StringVar()
        self.var_combo_skin = StringVar()
        self.var_combo_outfit = StringVar()
        self.var_combo_walk_overlay = StringVar()
        self.var_listbox_face = StringVar()
        self.listbox_face_custom_dir = None
        self.var_radio_gender = IntVar(value = 2)
        self.var_scale_fatness = DoubleVar(value = 1.0)
        self.var_scale_fatness_label = StringVar(value = '1.0 (Default)')
        self.listbox_face_list_m = StringVar(
            value = self.paths.get_globals()['NPC']['face']['male']
        )
        self.listbox_face_list_f = StringVar(
            value = self.paths.get_globals()['NPC']['face']['female']
        )
        self.combo_head_list_m = [
            i for i in
            self.paths.get_globals()['NPC']['head']['male']['default']
            +self.paths.get_globals()['NPC']['head']['male']['custom']
        ]
        self.combo_head_list_f = [
            i for i in
            self.paths.get_globals()['NPC']['head']['female']['default']
            +self.paths.get_globals()['NPC']['head']['female']['custom']
        ]
        self.combo_skin_list_m = [
            i for i in
            self.paths.get_globals()['NPC']['skin']['male']['default']
            +self.paths.get_globals()['NPC']['skin']['male']['custom']
        ]
        self.combo_skin_list_f = [
            i for i in
            self.paths.get_globals()['NPC']['skin']['female']['default']
            +self.paths.get_globals()['NPC']['skin']['female']['custom']
        ]
        self.combo_outfit_list_m = [
            self.paths.get_globals()['NPC']['outfit']['default']['male']
        ]
        self.combo_outfit_list_f = [
            self.paths.get_globals()['NPC']['outfit']['default']['female']
        ]
        self.combo_walk_overlay_list = [
            i for i in 
            self.paths.get_overlays()['overlay']['default']
            +self.paths.get_overlays()['overlay']['custom']
        ]
        empty_image = Image.open(self.paths.FACES_PATH.joinpath('Empty.png'))
        self.image_face = ImageTk.PhotoImage(empty_image)

        self.icon_reset = ImageTk.PhotoImage(
            Image.open(
                self.paths.ICONS_PATH / 'Reset.png'
            )
        )

        for i in self.visual_frame_names:
            self.visual_frames[i] = Frame(self)

        self.radio_gender_m = Radiobutton(
            self.visual_frames['gender'],
            text = 'Male',
            variable = self.var_radio_gender,
            value = 0,
            command = lambda: self.widgets_unlock(self.var_radio_gender.get()),
            bootstyle = 'info'
        )
        self.radio_gender_f = Radiobutton(
            self.visual_frames['gender'],
            text = 'Female',
            variable = self.var_radio_gender,
            value = 1,
            command = lambda: self.widgets_unlock(self.var_radio_gender.get()),
            bootstyle = 'danger'
        )

        self.label_outfit = Label(
            self.visual_frames['outfit'],
            text = 'NPC Outfit:'
        )
        self.combo_outfit = Combobox(
            self.visual_frames['outfit'],
            bootstyle = 'secondary',
            width = 30,
            textvariable = self.var_combo_outfit,
            state = 'disabled',
        )
        self.label_head = Label(
            self.visual_frames['head'],
            text = 'NPC Head Mesh:'
        )
        self.label_head_info = Label(
            self.visual_frames['head'],
            text = ''
        )
        self.button_add_head_mesh = Button(
            self.visual_frames['head'],
            text = '+',
            width = '2',
            bootstyle = 'success-outline',
            state = 'disabled',
            command = lambda: self.head_mesh_manage(
                'add',
                self.combo_head.get(),
                self.var_radio_gender.get()
            ) 
        )
        self.button_remove_head_mesh = Button(
            self.visual_frames['head'],
            text = '-',
            width = '2',
            bootstyle = 'danger-outline',
            state = 'disabled',
            command = lambda: self.head_mesh_manage(
                'remove',
                self.combo_head.get(),
                self.var_radio_gender.get()
            ) 
        )
        self.combo_head = Combobox(
            self.visual_frames['head'],
            bootstyle = 'danger',
            width = 30,
            textvariable = self.var_combo_head,
            state = 'disabled'
        )
        self.label_skin = Label(
            self.visual_frames['skin'],
            text = 'NPC Skin Texture:'
        )
        self.label_skin_info = Label(
            self.visual_frames['skin'],
            text = ''
        )
        self.button_add_skin_tex = Button(
            self.visual_frames['skin'],
            text = '+',
            width = '2',
            bootstyle = 'success-outline',
            state = 'disabled',
            command = lambda: self.skin_tex_manage(
                'add',
                self.combo_skin.get(),
                self.var_radio_gender.get()
            ) 
        )
        self.button_remove_skin_tex = Button(
            self.visual_frames['skin'],
            text = '-',
            width = '2',
            bootstyle = 'danger-outline',
            state = 'disabled',
            command = lambda: self.skin_tex_manage(
                'remove',
                self.combo_skin.get(),
                self.var_radio_gender.get()
            ) 
        )
        self.combo_skin = Combobox(
            self.visual_frames['skin'],
            bootstyle = 'success',
            width = 30,
            textvariable = self.var_combo_skin,
            state = 'disabled'
        )
        self.label_overlay_info = Label(
            self.visual_frames['walk_overlay'],
            text = ''
        )
        self.frame_overlay_manage = Frame(self.visual_frames['walk_overlay'])
        self.button_add_overlay = Button(
            self.frame_overlay_manage,
            text = '+',
            width = '2',
            bootstyle = 'success-outline',
            state = 'disabled',
            command = lambda: self.walk_overlay_manage(
                'add',
                self.var_combo_walk_overlay.get()
            )
        )
        self.button_delete_overlay = Button(
            self.frame_overlay_manage,
            text = '-',
            width = '2',
            bootstyle = 'danger-outline',
            state = 'disabled',
            command = lambda: self.walk_overlay_manage(
                'delete',
                self.var_combo_walk_overlay.get()
            )
        )
        self.label_walk_overlay = Label(
            self.visual_frames['walk_overlay'],
            text = 'NPC Walk Animation:'
        )
        self.combo_walk_overlay = Combobox(
            self.visual_frames['walk_overlay'],
            bootstyle = 'info',
            width = 30,
            values = self.combo_walk_overlay_list,
            textvariable = self.var_combo_walk_overlay,
            state = 'disabled'
        )
        self.label_fatness = Label(
            self.visual_frames['fatness'],
            text = 'NPC Model Fatness:'
        )
        self.label_fatness_value = Label(
            self.visual_frames['fatness'],
            textvariable = self.var_scale_fatness_label
        )
        self.button_fatness_reset = Button(
            self.visual_frames['fatness'],
            bootstyle = ('outline', 'info'),
            image=self.icon_reset,
            width = 2,
            command = self.reset_scale_value,
            state = 'disabled'
        )
        self.scale_fatness = Scale(
            self.visual_frames['fatness'],
            variable = self.var_scale_fatness,
            from_ = 0,
            to = 2.0,
            value = 1.0,
            length = 200,
            command = lambda value: self.update_scale_value(value),
            state = 'disabled',
            bootstyle = 'info'
        )
        self.listbox_face = Listbox(
            self.visual_frames['face'],
            listvariable = '',
            width = 30,
            height = 15,
            selectmode = 'single',
            activestyle = 'underline'
        )
        self.listbox_face.bind(
            '<ButtonRelease-1>',
            lambda *_:
                self.view_face_image()
                if self.listbox_face_custom_dir is None
                else self.view_face_image(
                    face_dir=self.listbox_face_custom_dir
                )
        )
        self.scrollbar_listbox_face = Scrollbar(
            self.visual_frames['face'],
            orient = 'vertical',
            command = self.listbox_face.yview,
            bootstyle = ('round','primary')
        )
        self.listbox_face.configure(
            yscrollcommand = self.scrollbar_listbox_face.set
        )
        self.canvas_image_face = Canvas(
            self.visual_frames['face'],
            width = '512',
            height = '256'
            )
        self.canvas_image_face.create_image(
            512//2, 256//2,
            anchor = 'center',
            image = self.image_face
        )

    def widgets_pack(self):
        for i in self.visual_frames:
            self.visual_frames[i].pack(
                fill = 'both', padx = 5, pady = 5, expand = True
            )

        self.radio_gender_m.pack(
            side = 'left', fill = 'x', expand = True, padx = 5, pady = 5
        )
        self.radio_gender_f.pack(
            side = 'left', fill = 'x', expand = True, padx = 5, pady = 5
        )
        
        self.label_outfit.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.combo_outfit.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.label_head.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.label_head_info.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'center'
        )
        self.button_add_head_mesh.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.button_remove_head_mesh.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.combo_head.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

        self.label_skin.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.label_skin_info.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'center'
        )
        self.button_add_skin_tex.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.button_remove_skin_tex.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.combo_skin.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )


        self.label_walk_overlay.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.label_overlay_info.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'center'
        )
        self.frame_overlay_manage.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.button_add_overlay.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.button_delete_overlay.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.combo_walk_overlay.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

        self.label_fatness.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', expand = True
        )
        self.label_fatness_value.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.button_fatness_reset.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )
        self.scale_fatness.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'e'
        )

        self.listbox_face.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'w', fill = 'both'
        )
        self.scrollbar_listbox_face.pack(side = 'left', fill = 'y')
        self.canvas_image_face.pack(
            side = 'left', padx = 5, pady = 5, anchor = 'center', expand = True
        )

    def widgets_unlock(self, gender):
        widget_pairs = {
            self.combo_head: (
                self.combo_head_list_m,
                self.combo_head_list_f
            ),
            self.combo_skin: (
                self.combo_skin_list_m,
                self.combo_skin_list_f
            ),
            self.combo_outfit: (
                self.combo_outfit_list_m,
                self.combo_outfit_list_f
            ),
            self.listbox_face: (
                self.listbox_face_list_m,
                self.listbox_face_list_f
            ),
            self.scale_fatness: None,
            self.button_fatness_reset: None,
            self.button_add_overlay: None,
            self.button_delete_overlay: None,
            self.button_add_head_mesh: None,
            self.button_remove_head_mesh: None,
            self.button_add_skin_tex: None,
            self.button_remove_skin_tex: None
        }
        for i in widget_pairs:
            if isinstance(i, Combobox):
                if i is self.combo_outfit:
                    i.configure(state='readonly')
                else:
                    i.configure(state = 'normal', values = widget_pairs[i][gender])
                i.delete(0,END)
            elif isinstance(i, Listbox):
                i.configure(listvariable = widget_pairs[i][gender])
            else:
                i.configure(state = 'normal')
        self.combo_walk_overlay.configure(state = 'normal')
        self.reset_scale_value()
        self.modules['Settings'].refill_data('outfit')
        self.modules['Settings'].refill_data('face')

    def update_scale_value(self, value):
        if float(value) == 1.0:
            self.var_scale_fatness_label.set('1.0 (Default)')
            return
        self.var_scale_fatness_label.set(str(round(float(value),2)))

    def reset_scale_value(self):
        self.scale_fatness.set(1.0)

    def view_face_image(self, face_dir=None):
        face_image_name = self.listbox_face.get(
            *self.listbox_face.curselection()
        )
        if face_dir is not None:
            face = Image.open(Path(face_dir) / f'{face_image_name}.png')
        else:
            face = Image.open(self.paths.FACES_PATH / f'{face_image_name}.png')
        face = face.resize((face.width*2, face.height*2))
        self.image_face = ImageTk.PhotoImage(face)
        self.canvas_image_face.delete('all')
        self.canvas_image_face.create_image(
            (512//2), (256//2),
            anchor = 'center',
            image = self.image_face
        )
        self.var_listbox_face.set(
            face_image_name.
            split('_')[2].
            replace('V', '')
        )

    def walk_overlay_manage(self, action, name):
        match action:
            case 'add':
                if name not in self.combo_walk_overlay_list:
                    NPC.add_overlay(name)
                    self.combo_walk_overlay_list = [i for i in
                        self.paths.get_overlays()['overlay']['default']+
                        self.paths.get_overlays()['overlay']['custom']
                    ]
                    self.combo_walk_overlay.configure(
                        values = self.combo_walk_overlay_list
                    )
                    self.label_overlay_info.configure(
                        text = f'{name}.mds was added',
                        foreground = 'green'
                    )
                    self.root.after(
                        3000,
                        lambda: self.label_overlay_info.configure(text = '')
                    )
                else:
                    self.label_overlay_info.configure(
                        text = f'{name}.mds already exists!',
                        foreground = 'red'
                    )
                    self.root.after(
                        3000,
                        lambda: self.label_overlay_info.configure(text = '')
                    )
            case 'delete':
                if name not in self.paths.get_overlays()['overlay']['default']:
                    NPC.delete_overlay(name)
                    self.combo_walk_overlay_list = [i for i in
                        self.paths.get_overlays()['overlay']['default']+
                        self.paths.get_overlays()['overlay']['custom']
                    ]
                    self.combo_walk_overlay.configure(
                        values = self.combo_walk_overlay_list
                    )
                    self.combo_walk_overlay.delete(0, END)
                    self.label_overlay_info.configure(
                        text = f'{name}.mds was removed',
                        foreground = 'red'
                    )
                    self.root.after(
                        3000,
                        lambda: self.label_overlay_info.configure(text = '')
                    )
                else:
                    self.label_overlay_info.configure(
                        text = f'Cannot remove default overlays!',
                        foreground = 'red'
                    )
                    self.root.after(
                        3000,
                        lambda: self.label_overlay_info.configure(text = '')
                    )

    def head_mesh_manage(self, action, name, gender):
        match gender:
            case 0:
                match action:
                    case 'add':
                        if name not in self.combo_head_list_m:
                            NPC.add_head_mesh(name=name, gender=gender)
                            self.combo_head_list_m = [
                                i for i in
                                self.paths.get_globals()['NPC']['head']['male']['default']
                                +self.paths.get_globals()['NPC']['head']['male']['custom']
                            ]
                            self.combo_head.configure(
                                values = self.combo_head_list_m
                            )
                            self.label_head_info.configure(
                                text = f'{name} was added',
                                foreground = 'green'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_head_info.configure(text = '')
                            )
                            self.combo_head.delete(0, END)
                        else:
                            self.label_head_info.configure(
                                text = f'{name} already exists',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_head_info.configure(text = '')
                            )
                            return
                    case 'remove':
                        if name in self.paths.get_globals()['NPC']['head']['male']['default']:
                            self.label_head_info.configure(
                                text = f'Cannot remove default heads!',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_head_info.configure(text = '')
                            )
                            return
                        if name in self.combo_head_list_m:
                            NPC.remove_head_mesh(name=name, gender=gender)
                            self.combo_head_list_m = [
                                i for i in
                                self.paths.get_globals()['NPC']['head']['male']['default']
                                +self.paths.get_globals()['NPC']['head']['male']['custom']
                            ]
                            self.combo_head.configure(
                                values = self.combo_head_list_m
                            )
                            self.label_head_info.configure(
                                text = f'{name} was removed',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_head_info.configure(text = '')
                            )
                            self.combo_head.delete(0, END)
            case 1:
                match action:
                    case 'add':
                        if name not in self.combo_head_list_f:
                            NPC.add_head_mesh(name=name, gender=gender)
                            self.combo_head_list_f = [
                                i for i in
                                self.paths.get_globals()['NPC']['head']['female']['default']
                                +self.paths.get_globals()['NPC']['head']['female']['custom']
                            ]
                            self.combo_head.configure(
                                values = self.combo_head_list_f
                            )
                            self.label_head_info.configure(
                                text = f'{name} was added',
                                foreground = 'green'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_head_info.configure(text = '')
                            )
                            self.combo_head.delete(0, END)
                        else:
                            self.label_head_info.configure(
                                text = f'{name} already exists',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_head_info.configure(text = '')
                            )
                            return
                    case 'remove':
                        if name in self.paths.get_globals()['NPC']['head']['female']['default']:
                            self.label_head_info.configure(
                                text = f'Cannot remove default heads!',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_head_info.configure(text = '')
                            )
                            return
                        if name in self.combo_head_list_f:
                            NPC.remove_head_mesh(name=name, gender=gender)
                            self.combo_head_list_f = [
                                i for i in
                                self.paths.get_globals()['NPC']['head']['female']['default']
                                +self.paths.get_globals()['NPC']['head']['female']['custom']
                            ]
                            self.combo_head.configure(
                                values = self.combo_head_list_f
                            )
                            self.label_head_info.configure(
                                text = f'{name} was removed',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_head_info.configure(text = '')
                            )
                            self.combo_head.delete(0, END)

    def skin_tex_manage(self, action, name, gender):
        match gender:
            case 0:
                match action:
                    case 'add':
                        if name not in self.combo_skin_list_m:
                            NPC.add_skin_tex(name=name, gender=gender)
                            self.combo_skin_list_m = [
                                i for i in
                                self.paths.get_globals()['NPC']['skin']['male']['default']
                                +self.paths.get_globals()['NPC']['skin']['male']['custom']
                            ]
                            self.combo_skin.configure(
                                values = self.combo_skin_list_m
                            )
                            self.label_skin_info.configure(
                                text = f'{name} was added',
                                foreground = 'green'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_skin_info.configure(text = '')
                            )
                            self.combo_skin.delete(0, END)
                        else:
                            self.label_skin_info.configure(
                                text = f'{name} already exists',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_skin_info.configure(text = '')
                            )
                            return
                    case 'remove':
                        if name in self.paths.get_globals()['NPC']['skin']['male']['default']:
                            self.label_skin_info.configure(
                                text = f'Cannot remove default skin texture!',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_skin_info.configure(text = '')
                            )
                            return
                        if name in self.combo_skin_list_m:
                            NPC.remove_skin_tex(name=name, gender=gender)
                            self.combo_skin_list_m = [
                                i for i in
                                self.paths.get_globals()['NPC']['skin']['male']['default']
                                +self.paths.get_globals()['NPC']['skin']['male']['custom']
                            ]
                            self.combo_skin.configure(
                                values = self.combo_skin_list_m
                            )
                            self.label_skin_info.configure(
                                text = f'{name} was removed',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_skin_info.configure(text = '')
                            )
                            self.combo_skin.delete(0, END)
            case 1:
                match action:
                    case 'add':
                        if name not in self.combo_skin_list_f:
                            NPC.add_skin_tex(name=name, gender=gender)
                            self.combo_skin_list_f = [
                                i for i in
                                self.paths.get_globals()['NPC']['skin']['female']['default']
                                +self.paths.get_globals()['NPC']['skin']['female']['custom']
                            ]
                            self.combo_skin.configure(
                                values = self.combo_skin_list_f
                            )
                            self.label_skin_info.configure(
                                text = f'{name} was added',
                                foreground = 'green'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_skin_info.configure(text = '')
                            )
                            self.combo_skin.delete(0, END)
                        else:
                            self.label_skin_info.configure(
                                text = f'{name} already exists',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_skin_info.configure(text = '')
                            )
                            return
                    case 'remove':
                        if name in self.paths.get_globals()['NPC']['skin']['female']['default']:
                            self.label_skin_info.configure(
                                text = f'Cannot remove default skin texture!',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_skin_info.configure(text = '')
                            )
                            return
                        if name in self.combo_skin_list_f:
                            NPC.remove_skin_tex(name=name, gender=gender)
                            self.combo_skin_list_f = [
                                i for i in
                                self.paths.get_globals()['NPC']['skin']['female']['default']
                                +self.paths.get_globals()['NPC']['skin']['female']['custom']
                            ]
                            self.combo_skin.configure(
                                values = self.combo_skin_list_f
                            )
                            self.label_skin_info.configure(
                                text = f'{name} was removed',
                                foreground = 'red'
                            )
                            self.root.after(
                                3000,
                                lambda: self.label_skin_info.configure(text = '')
                            )
                            self.combo_skin.delete(0, END)

if __name__ == '__main__':
    root = Window(title = 'test', themename = 'darkly')
    root.geometry('768x680')
    VisualMenu(root, root).show()
    root.mainloop()
