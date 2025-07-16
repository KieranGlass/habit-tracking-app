import tkinter as tk


class MainMenu(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        for i in range(10):
            self.rowconfigure(i, weight=1)

        tk.Label(self, text="Habit Tracker", font=("Arial", 14)).grid(row=0, column=0, pady=5, sticky="n")

        menu_options = [
            ("1. Complete Habit", controller.show_log_interaction),
            ("2. Habits", controller.show_habits),
            ("3. Analytics", controller.show_analytics)
        ]

        for i, (text, command) in enumerate(menu_options):
            btn = tk.Button(self, text=text, command=command, width=30)
            btn.grid(row=i + 2, column=0, pady=2, sticky="n")