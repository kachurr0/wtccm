import base64
from io import BytesIO
from tkinter import *
from tkinter import ttk
from typing import Optional

from PIL import ImageTk, Image
from config import ConfigManager
from archive import ArchiveManager
from pathlib import Path

from new.soundmod import SoundManager


class WTCCM(Tk):
    def __init__(self):
        super().__init__()

        self.config = ConfigManager()
        self.archive_manager = ArchiveManager(self.config)

        self.title("WTCCM")
        self.resizable(False, False)
        self.set_icon()
        self.geometry("800x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.archives_page = ArchivesPage(self.notebook, self)
        self.soundmods_page = SoundmodsPage(self.notebook, self)

        self.notebook.add(self.archives_page, text="Archives")
        self.notebook.add(self.soundmods_page, text="Sound mods")


    def set_icon(self):
        # Decoding and setting up icon
        icon_b64 = 'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL64tAD3fCAA5I5PCemFPCfqgjRB6YExTuqBMFHqgDBR6H4uUed9LVHleyxR5XorUeR5LFHkeStR5HgsUeR4LFHjeCxR4ncsUeJ2LFHidixR3nQrTt51LUHcdzIm1X5DCeNtHwC1rqUAAAAAAAAAAAAAAAAAAAAAAAAAAADmlFcA4Z1qA+yIPEjvgi6z8H4o5vB9JfbveyP773si/O56IPzteB/86nUe/OlzHfzpcxz86HId/OhxHfzncR3853Ed/OZwHvzmcB785W8d/OZwHvzkbh775G8f9uJvIObhcSWy3HMtSMl/SwPRej8AAAAAAAAAAAAAAAAA6JleANm5pALwiz5o84Mt7vSAJv/0fiX/830k//J8Iv/weyH/7Xgf/+p0HP/mcRz/5HAb/+RvGv/kbhv/424a/+NtGv/jbhr/4m0b/+JtG//ibBv/4Wwa/+JsG//ibBz/420c/+RtHf/ibiHu3XMtacGPeALTfEYAAAAAAKDRvADzjD0A8ZBHPfWHMun2gyn/9YEo//WAJ//0fyb/8n0j/+15If/kch3/3m0b/9tsG//Zahv/12ka/9doGv/WaBn/1mcZ/9ZnGf/WZxr/1Wca/9VmGf/WZxn/12cZ/9loG//caRr/4Gsa/+NrHP/ibiLp3HQxPt9xKQCPu6YA651hANu6oQL1jT2d94cv//eFLf/3hCv/9oIp//J/Jv/qeCD/2m0c/89lGf/MYxj/yGEX/8VfFv/EXhb/w10W/8JcFv/CXBb/wVwW/8BbFv/AWxb/wFsV/8FbFv/DXBb/x18Y/9BjGP/ZaBn/4Gsb/+NtHv/gcSievZR/AtR/SQDwmVgA8JlYFvaNO9T4iTL/+Ycw//iGLv/1gij/4HUi/7JeIv+dUx//mE8e/5VNHv+RTB7/jkkc/4xIHP+LSBz/ikcc/4tHHP+KRxz/iUcb/4lHG/+JRhz/iUYb/49IGv+nTxP/wVsV/9FjGP/daRv/42wd/+JwJNPbejwV2no7APSXUwD0l1Mo+I486PqLNv/6izT/+Ykx//GBKf+afWj/S3yo/0d5qf9Geaj/RXio/0R3qP9Bdqf/QXWl/0B0pf8/dKX/P3Sl/z90pP8+c6P/PnOk/z5zpP8/c6T/QHGg/2tXUf+0VBL/zWAX/9tnGv/ibB3/5HAj5t95NSbfeDUA9plUAPaaVS76kD/t+405//uNN//7izP/7IMw/3uVqv9BlNv/QpLX/0KS1/9Bkdf/P5DW/z2P1f88jtT/O4zT/zmM0/85jdP/OYzS/zmL0f86jNL/OozS/zqM0v84jNT/UW6M/6xSFf/LYBj/2Wca/+JsHf/kbyLr4XcvK+J2LwD3nVgA951ZMPuSQu78jzz/+446//uMNv/shTT/fZet/0OU2f9Dktb/Q5HW/0SS1v9xq9v/h7be/4a13f+EtNz/grPb/4Ky2/+Ds9v/ZqLV/zyM0P88jND/O4vP/zmM0v9Rbo3/qlIW/8lgGP/XaBz/4Wwd/+VvIuvjdy8r43YuAPieWwD3n1ww/JNE7vyQPv/9jz3//I05/+yGNv9+mq//RZfc/0WU1/9Ek9f/SpbY/67P6v/H2uj/wNTj/77T4v+90uL/vdLh/8XY5v+bwuH/P47S/z6N0v89jNH/O47U/1Jvjv+rUhb/yWAY/9doHP/hbR7/5XAi6+N3Lyzjdi8A+J9eAPegXzD8lUbu/ZNA//2RP//7jzv/7Ic4/4Gcsf9Hmd7/R5ba/0aW2f9MmNn/r9Dr/8bZ6P+/0+P/vdPj/7zS4v+70eH/w9jm/5zD4v9Bj9P/P47T/z+O0/88j9X/U3CP/6tTFv/JYBj/1mcb/+FtHv/lcSPr43kxLON4MQD3oF8A96FhMPyXSu78lET//ZNC//yQPf/uiTr/g52y/0ma3/9JmNv/SJfa/02Z2/+x0ez/zN7q/8XZ5//E2Of/w9fm/8LW5f/I2+n/nsXj/0CQ0/8/j9T/P4/T/z2Q1v9TcY//q1IW/8lgGP/WZxv/4W0e/+ZxJOvlejMs5XoyAPiiYQD4omIw/JlM7vyVRv/8lEX//ZNA/++KPP+En7T/S5zh/0qZ3f9Jmdz/S5nc/3ey4v+Mvub/i73m/4m75f+Hu+T/hrnk/4a5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'
        icon_data = base64.b64decode(icon_b64)
        image = Image.open(BytesIO(icon_data))
        icon = ImageTk.PhotoImage(image)
        # noinspection PyTypeChecker
        self.iconphoto(True, icon)


class ArchivesPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.config = app.config
        self.archive_manager = app.archive_manager
        self.app = app
        self.cnames = Variable()
        self.selected_dist = StringVar()
        self.sentmsg = StringVar()
        self.statusmsg = StringVar()
        self.delete_after_processing = BooleanVar()

        self.c = ttk.Frame(self, padding=(5, 5, 12, 0))
        self.c.grid(column=0, row=0, sticky='nwes')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.listBox = Listbox(self.c, listvariable=self.cnames, height=5, width=3, selectmode='multiple')

        self.lbl = ttk.Label(self.c, text="Select archives to process:")

        self.g1 = ttk.Radiobutton(self.c, text='Skins/Camouflages', variable=self.selected_dist, value='UserSkins')
        self.g2 = ttk.Radiobutton(self.c, text='Sights', variable=self.selected_dist, value='UserSights\\all_tanks')
        self.g3 = ttk.Radiobutton(self.c, text='Missions', variable=self.selected_dist, value='UserMissions')

        self.send = ttk.Button(self.c, text='Move & Unpack selected', command=self.process_archives, default='active') # как мне получить доступ к processArchives отсюда?
        self.status = ttk.Label(self.c, textvariable=self.statusmsg, anchor='w')

        self.refreshBtn = ttk.Button(self.c, text='Refresh', command=lambda: self.update_listbox(), default='active')
        self.tb1 = ttk.Checkbutton(self.c, text='Delete archive after processing?', variable=self.delete_after_processing,
                              onvalue=True, offvalue=False)

        self.selectAllBtn = ttk.Button(self.c, text='Select All',
                                  command=lambda: (self.listBox.selection_set(0, END)), default='active',
                                  width=10)
        self.unselectAllBtn = ttk.Button(self.c, text='Unselect All',
                                    command=lambda: (self.listBox.selection_clear(0, END)),
                                    default='active', width=10)

        self.refreshBtn.grid(column=0, row=6, sticky='nw', padx=160)

        self.selectAllBtn.grid(column=0, row=6, sticky='nw', ipadx=5)
        self.unselectAllBtn.grid(column=0, row=6, sticky='nw', padx=80, ipadx=5)

        self.listBox.grid(column=0, row=0, rowspan=6, sticky='nsew', ipadx=20)
        self.lbl.grid(column=1, row=0, padx=10, pady=5)
        self.g1.grid(column=1, row=1, sticky=W, padx=20)
        self.g2.grid(column=1, row=2, sticky=W, padx=20)
        self.g3.grid(column=1, row=3, sticky=W, padx=20)
        self.tb1.grid(column=1, row=4, sticky=W, padx=20, columnspan=2)
        self.send.grid(column=1, row=6, sticky='es')
        self.status.grid(column=0, row=7, columnspan=2, sticky='we')
        self.c.grid_columnconfigure(0, weight=1)
        self.c.grid_rowconfigure(5, weight=1)

        self.selected_dist.set('UserSkins')
        self.delete_after_processing.set(True)
        self.update_listbox()

    def process_archives(self):
        archives = self.get_selected_archives()
        selected_dist = self.selected_dist.get()
        destination = self.config.wt_path / selected_dist if selected_dist != 'UserSights\\all_tanks' else self.config.sights_path

        self.app.archive_manager.process_archives(
            archives=archives,
            destination=destination,
            delete_archive=self.delete_after_processing.get()
        )

        self.statusmsg.set("Done!")
        self.update_listbox()

    def get_selected_archives(self):
        selection = []
        idxs = self.listBox.curselection()
        for idx in idxs:
            selection.append(Path(self.cnames.get()[idx]))
        return selection

    def update_listbox(self):
        recent_archives = self.archive_manager.find_recent_archives(10)
        self.listBox.delete(0, 'end')
        for each_item in range(len(recent_archives)):
            self.listBox.insert(END, recent_archives[each_item])
            # coloring alternative lines of listbox
            self.listBox.itemconfig(each_item,
                               bg="white" if each_item % 2 == 0 else "lavender")


class SoundmodsPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.soundManager = SoundManager(self.app.config)

        # CHATGPT GENERATED UI, stollen from Barotrauma, but I drew it in excildraw
        # ---------------- Настройка сетки ----------------

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)

        # ---------------- Левая панель ----------------

        self.disabled_frame = ttk.LabelFrame(
            self,
            text="Disabled",
            padding=10
        )
        self.disabled_frame.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=20,
            sticky="nsew"
        )

        self.disabled_listbox = Listbox(
            self.disabled_frame,
            width=30,
            height=15
        )
        self.disabled_listbox.pack(fill="both", expand=True)

        # ---------------- Центральная панель ----------------

        self.center_frame = ttk.Frame(self)
        self.center_frame.grid(
            row=0,
            column=1,
            padx=20,
            pady=20,
            sticky="n"
        )

        ttk.Label(
            self.center_frame,
            text="Sound Mods"
        ).pack(pady=(0, 20))

        self.enable_button = ttk.Button(
            self.center_frame,
            text="→",
            width=8,
            command=self.handle_enable_button
        )
        self.enable_button.pack(pady=5)

        self.disable_button = ttk.Button(
            self.center_frame,
            text="←",
            width=8,
            command=self.handle_disable_button
        )
        self.disable_button.pack(pady=(10, 25))

        self.enable_var = BooleanVar(value=self.soundManager.soundmod_enabled)
        self.multiple_var = BooleanVar(value=False)

        self.enable_checkbox = ttk.Checkbutton(
            self.center_frame,
            text="Enable Sound-mods",
            variable=self.enable_var,
            command=self.handle_enable_checkbox
        )
        self.enable_checkbox.pack(anchor="w")

        self.multiple_checkbox = ttk.Checkbutton(
            self.center_frame,
            text="[wip] Allow multiple",
            variable=self.multiple_var,
            command=self.handle_multiple_checkbox,
            state=DISABLED #Todo
        )
        self.multiple_checkbox.pack(anchor="w")

        # ---------------- Правая панель ----------------

        self.enabled_frame = ttk.LabelFrame(
            self,
            text="Enabled",
            padding=10
        )
        self.enabled_frame.grid(
            row=0,
            column=2,
            padx=(10, 20),
            pady=20,
            sticky="nsew"
        )

        self.enabled_listbox = Listbox(
            self.enabled_frame,
            width=30,
            height=15
        )
        self.enabled_listbox.pack(fill="both", expand=True)
        self.update_disabledBox()
        self.update_enabledBox()

    def handle_multiple_checkbox(self):
        ...

    def handle_enable_checkbox(self):
        self.soundManager.toggle_soundmod()
        self.enable_var.set(self.soundManager.soundmod_enabled)

    def update_disabledBox(self):
        self.disabled_listbox.delete(0, 'end')
        disabled_mods = self.soundManager.disabled_mods
        if not disabled_mods: return
        for idx, path in enumerate(disabled_mods):
            self.disabled_listbox.insert(END, path.name)
            # coloring alternative lines of listbox
            self.disabled_listbox.itemconfig(idx,
                                    bg="white" if idx % 2 == 0 else "lavender")

    def update_enabledBox(self):
        self.enabled_listbox.delete(0, 'end')
        values = [x.name for x in self.soundManager.enabled_mods]
        if not values: return
        for idx, value in enumerate(values):
            self.enabled_listbox.insert(END, value)
            # coloring alternative lines of listbox
            self.enabled_listbox.itemconfig(idx,
                                    bg="white" if idx % 2 == 0 else "lavender")


    def handle_enable_button(self):
        selected = self.disabled_listbox.selection_get()
        mod_path = self.soundManager.stored_path / selected
        self.soundManager.enable_mod(mod=mod_path)
        self.update_enabledBox()
        self.update_disabledBox()

    def handle_disable_button(self):
        selected = self.enabled_listbox.selection_get()
        self.soundManager.disable_mod(mod=self.soundManager.stored_path / selected)
        self.update_enabledBox()
        self.update_disabledBox()