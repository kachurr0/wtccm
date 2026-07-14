from tkinter import *

root = Tk()

class WTCCM(root):
    def __init__(self):
        super().__init__()

        self.title("WTCCM")
        self.resizable(False, False)

        self.config_data = load_config()

        self.create_widgets()
        self.create_menu()

        update_listbox(self.config_data)