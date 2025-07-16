import tkinter as tk
from tkinter import ttk

import analytics
from models.completion import Completion


class DisplayAnalytics(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        tk.Label(self, text="Habit Analytics", font=("Arial", 16)).grid(pady=10)

        # Dropdown for analytics options
        options = [
            "All Habits",
            "Habits by Frequency",
            "Streaks per Habit"
        ]
        
        frequency_options = [
            "Daily",
            "Weekly",
            "Monthly"
        ]
        self.selected_option = tk.StringVar()
        self.selected_option.set(options[0])
        
        self.selected_frequency = tk.StringVar()
        self.selected_frequency.set(frequency_options[0])
        
        current_habit, current_streak = analytics.get_longest_current_streak(self.controller.db)
        
        current_streak_label = tk.Label(self, text="Longest Current Streak:\n" +  current_habit.description + " - " + str(current_streak))
        current_streak_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        longest_habit, longest_streak = analytics.get_longest_run_streak_all(self.controller.db)
        
        longest_streak_label = tk.Label(self, text="Longest Ever Streak:\n" + longest_habit.description + " - " + str(longest_streak))
        longest_streak_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        
        dropdown_frame = tk.Frame(self)
        dropdown_frame.grid(row=3, column=0, padx=5, pady=5)

        dropdown = ttk.Combobox(dropdown_frame, textvariable=self.selected_option, values=options, state="readonly")
        dropdown.grid(row=0, column=0, pady=5, padx=5)
        dropdown.bind("<<ComboboxSelected>>", self.on_option_selected)
        
        self.frequency_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.selected_frequency, values=frequency_options, state="readonly")
        self.frequency_dropdown.grid(row=0, column=1, pady=5, padx=5)
        self.frequency_dropdown.grid_remove()
        self.frequency_dropdown.bind("<<ComboboxSelected>>", self.on_option_selected)

        self.tree = ttk.Treeview(self, columns="", show="headings", height=6)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
        scrollbar.grid(row=4, column=1, sticky="ns", pady=10)
        
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
        
         # Toggle frequency dropdown visibility
        if selected == "Habits by Frequency":
            self.frequency_dropdown.grid()  # Show it
        else:
            self.frequency_dropdown.grid_remove()  # Hide it

        if selected == "All Habits":
            habits = analytics.get_all_habits(self.controller.db)
            rows = [(h.description, h.date_created, h.frequency) for h in habits]
            self.populate_tree(rows, columns=("Description", "Date Created", "Frequency"))

        elif selected == "Habits by Frequency":
            freq = self.selected_frequency.get()
            habits = analytics.get_habits_by_frequency(self.controller.db, freq)
            rows = [(h.description, h.date_created, h.frequency) for h in habits]
            self.populate_tree(rows, columns=("Description", "Date Created", "Frequency"))
            print(f"{rows}")

        elif selected == "Streaks per Habit":
            results = analytics.get_longest_streaks_per_habit(self.controller.db)

            rows = []
            for habit, longest_streak in results:
                current_streak = analytics.get_current_streak(habit, Completion.get_all_completions(self.controller.db))
                rows.append((habit.description, habit.frequency, longest_streak, current_streak))

            self.populate_tree(rows, columns=("Description", "Frequency", "Longest Streak", "Current Streak"))