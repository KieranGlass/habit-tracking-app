import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from models.habit import Habit

class ModifyHabitForm(tk.Frame):
    def __init__(self, controller, id):
        super().__init__(controller)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        habit = Habit.fetch_habit(self.controller.db, id)
        if habit and isinstance(habit, list) and len(habit) > 0:
            habit = habit[0]  
        else:
            print("Person not found!")
            return

        habit_id, description, date_created, frequency = habit
    
        print(f"{habit}")

        tk.Label(self, text="Modify details", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Entry fields
        self.description_label = tk.Label(self, text="Description").grid(row=1, column=0, columnspan=2, sticky="n", pady=2)
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=2, column=0, columnspan=2, sticky="n", pady=(0, 8))
        self.description_entry.insert(0, description)

        # Frequency dropdown
        tk.Label(self, text="Habit Frequency").grid(row=9, column=0,  columnspan=2, sticky="n", pady=2)
        self.freq_var = tk.StringVar(value=frequency)
        frequencies = ["Daily", "Weekly", "Monthly"]
        tk.OptionMenu(self, self.freq_var, *frequencies).grid(row=10, column=0,  columnspan=2, pady=(0, 8))

        tk.Button(self, text="Submit", command=lambda : self.save_habit(habit_id, date_created)).grid(row=13, column=1, pady=5)
        tk.Button(self, text="Back", command=self.controller.show_habits).grid(row=14, column=0, pady=5)

    def save_habit(self, id, date_created):
        
        description = self.description_entry.get()
        freq = self.freq_var.get()
        
        habit_id = id

        if not all([description, freq]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
    
        habit = Habit(habit_id, description, date_created, freq)
        habit.save_changes_to_db(self.controller.db)
        messagebox.showinfo("Success", "Habit updated successfully.")
        self.controller.show_habits()