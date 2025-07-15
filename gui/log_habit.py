import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk, messagebox

from datetime import datetime

from models.habit import Habit
from models.completion import Completion


class LogHabit(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Title
        tk.Label(self, text="Complete a Habit", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        # Treeview to show list of people
        self.tree = ttk.Treeview(self, columns=("id", "Description", "Frequency", "Last Completed"), show="headings")
        self.tree.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        for col in ("id", "Description", "Frequency", "Last Completed"):
            self.tree.heading(col, text=col.title())
            if col == "id":
                self.tree.column(col, width=0, stretch=False)
            else:
                self.tree.column(col, stretch=True, anchor="center", width=80)
                
        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.grid(row=2, column=0, padx=5, sticky="nsew")
        
        self.calendar_frame.grid_columnconfigure(0, weight=1)
        self.calendar_frame.grid_rowconfigure(0, weight=1)
                
        self.calendar = Calendar(self.calendar_frame, selectmode="day", date_pattern="y-mm-dd", background="#003366")
        self.calendar.grid(row=0, column=0, sticky="nsew")

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, pady=10)
        
        
        tk.Button(button_frame, text="Complete", command=self.save_interaction).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Back", command=self.controller.show_main_menu).grid(row=0, column=1, padx=5)

        self.load_habits()

    def load_habits(self):
        """Clear and reload people from DB into the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)
            

        habit = Habit.fetch_all(self.controller.db)
        for p in habit:
            interactions = Completion.get_interactions_by_habit(self.controller.db, p.id)
            
            if interactions:
                most_recent = max(interactions, key=lambda x: datetime.strptime(x[1], "%d/%m/%Y"))
                last_completed = most_recent[1]
            else:
                last_completed = None
            
            self.tree.insert("", "end", values=(p.id, p.description, p.frequency, last_completed))
            
    def save_interaction(self):
        
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            values = self.tree.item(item, "values")
            habit_id = values[0]
        else:
            messagebox.showerror("Error", "Nothing Selected!")
            return
        
        interaction = Completion(None, habit_id, current_date)
        interaction.save_to_db(self.controller.db)
        
        self.load_habits()
        
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Get the habit ID from the hidden first column
        item = selected_item[0]
        values = self.tree.item(item, "values")
        habit_id = values[0] 
        
        # Clear previous calendar highlights
        self.calendar.calevent_remove("all")

        # Get all interactions for this habit
        interactions = Completion.get_interactions_by_habit(self.controller.db, habit_id)

        # Highlight the dates on the calendar
        for _, date_str in interactions:
            try:
                # Convert string to datetime object
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()

                # Add calendar event
                self.calendar.calevent_create(date_obj, "", "completed")
            except Exception as e:
                print(f"Skipping invalid date '{date_str}': {e}")

        self.calendar.tag_config("completed", background="green", foreground="white")