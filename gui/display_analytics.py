import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk, messagebox

from datetime import datetime
import analytics
from models.habit import Habit
from models.completion import Completion


class DisplayAnalytics(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Habit Analytics", font=("Arial", 16)).grid(pady=10)

        # Dropdown for analytics options
        options = [
            "All Habits",
            "Habits by Frequency",
            "Longest Streak per Habit",
            "Longest Streak (All Habits)"
        ]
        self.selected_option = tk.StringVar()
        self.selected_option.set(options[0])

        dropdown = ttk.Combobox(self, textvariable=self.selected_option, values=options, state="readonly")
        dropdown.grid(pady=5)
        dropdown.bind("<<ComboboxSelected>>", self.on_option_selected)

        self.tree = ttk.Treeview(self, columns="", show="headings", height=10)
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        tk.Button(self, text="Back", command=self.controller.show_main_menu).grid(row=5, column=0, pady=5)
        
        self.on_option_selected("All Habits")
 

    def populate_tree(self, data, columns):
        # Clear existing columns and rows
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, anchor="center", stretch=True)
        self.tree["columns"] = columns

        # Set new columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", stretch=True)

        # Clear rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data
        for row in data:
            self.tree.insert("", "end", values=row)

    def on_option_selected(self, event):
        selected = self.selected_option.get()

        if selected == "All Habits":
            habits = analytics.get_all_habits(self.controller.db)
            rows = [(h.description, h.date_created, h.frequency) for h in habits]
            self.populate_tree(rows, columns=("Description", "Date Created", "Frequency"))

        elif selected == "Habits by Frequency":
            freq = "Daily"  # Replace with user input later
            habits = analytics.get_habits_by_frequency(self.controller.db, freq)
            rows = [(h.description, h.date_created, h.frequency) for h in habits]
            self.populate_tree(rows, columns=("Description", "Date Created", "Frequency"))
            print(f"{rows}")

        elif selected == "Longest Streak per Habit":
            results = analytics.get_longest_streaks_per_habit(self.controller.db)
            rows = [(h.description, h.frequency, streak) for h, streak in results]
            self.populate_tree(rows, columns=("Description", "Frequency", "Longest Streak"))
            
        elif selected == "Longest Streak (All Habits)":
            habit, streak = analytics.get_longest_run_streak_all(self.controller.db)
            rows = [(habit.description, habit.frequency, streak)]
            self.populate_tree(rows, columns=("Description", "Frequency", "Longest Streak"))