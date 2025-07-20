import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from models.habit import Habit

"""
    Gui Window for creating/adding a new habit
    
    Provides inputs to the user for assigning values to the new habits attributes
    
    when submit is clicked the new habit is added to the db, but only if the inputs fields 
    are not empty. The input validations here ensure there is no bad information in the db
    
"""

class AddHabitForm(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        tk.Label(self, text="Add a New Habit", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Description").grid(row=1, column=0, columnspan=2, sticky="n", pady=2)
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=2, column=0, columnspan=2, sticky="n", pady=(0, 8))
        

        # Frequency dropdown
        tk.Label(self, text="Habit Frequency").grid(row=3, column=0, columnspan=2, sticky="n", pady=2)
        self.freq_var = tk.StringVar(value="Weekly")
        frequencies = ["Daily", "Weekly", "Monthly"]
        tk.OptionMenu(self, self.freq_var, *frequencies).grid(row=4, column=0, columnspan=2, pady=(0, 8))

        submit_button = ttk.Button(self, text="Submit", command=self.save_habit)
        submit_button.grid(row=5, column=1, pady=5)
        submit_button.configure(style="Complete.TButton")
        
        back_button = ttk.Button(self, text="Back", command=self.controller.show_habits)
        back_button.grid(row=5, column=0, pady=5)
        back_button.configure(style="Back.TButton")

    def save_habit(self):
        description = self.description_entry.get()
        freq = self.freq_var.get()

        if not all([description, freq]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        current_date = datetime.now().strftime("%d/%m/%Y")

        habit = Habit(None, description, current_date, freq)
        habit.save_to_db(self.controller.db)
        messagebox.showinfo("Success", "Habit added successfully.")
        self.controller.show_habits()