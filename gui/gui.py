import tkinter as tk
from tkinter import messagebox

from gui.main_menu import MainMenu

from gui.log_habit import LogHabit

from gui.habits import HabitView
from gui.add_habit import AddHabitForm
from gui.modify_habit import ModifyHabitForm
from gui.display_analytics import DisplayAnalytics



class Gui(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Small Steps")
        self.geometry("400x400")
        self.current_frame = None

        # Set grid config so frames can expand
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.show_main_menu()
        self.mainloop()

    def switch_frame(self, new_frame_class):
        # Remove current frame if it exists
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Create and display new frame
        self.current_frame = new_frame_class(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def show_main_menu(self):
        self.switch_frame(MainMenu)
        
    def show_log_interaction(self):
        self.switch_frame(LogHabit)
        
    def show_habits(self):
        self.switch_frame(HabitView)
        
    def show_add_habit(self):
        self.switch_frame(AddHabitForm)
        
    def show_modify_habit(self):
        self.switch_frame(ModifyHabitForm)
        
    def show_analytics(self):
        self.switch_frame(DisplayAnalytics)