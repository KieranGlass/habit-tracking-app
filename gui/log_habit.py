import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk, messagebox

from datetime import datetime

from models.habit import Habit
from models.completion import Completion

"""
    Gui Window for logging a new completion of a habit
    
    Like the habit page, contains a treeview with all habits listed, however, in this location
    the treeview also contains the date of the last completion for each habit
    
    Page contains a calendar. When a habit is selected, current completions for that habit are 
    visible in green so that users can visualize their progress.
    
    When a habit is selected, the complete button is clicked to log a new completion and persist it
    to the db. If no date has been selected when completing a habit, the completion is logged for the current
    date. Otherwise it is logged for the date selected. 
    
    Dates can be completed in the past, although this probably isnt the best practice from a user perspective, it 
    is natural that users may forget or be unable to log their completion on the day every time. Future completions 
    can not be logged as the calendar has a maxdate attribute set to today.
    
    
"""
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
                
        self.calendar = Calendar(self.calendar_frame, selectmode="day", date_pattern="y-mm-dd", maxdate=datetime.now().date(), background="#003366")
        self.calendar.grid(row=0, column=0, sticky="nsew")

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, pady=10)
        
        complete_button = ttk.Button(button_frame, text="Complete", command=self.save_interaction)
        complete_button.grid(row=0, column=0, padx=5)
        complete_button.configure(style="Complete.TButton")
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_interaction)
        delete_button.grid(row=0, column=1, padx=5)
        delete_button.configure(style="DeleteCompletion.TButton")
        
        back_button = ttk.Button(button_frame, text="Back", command=self.controller.show_main_menu)
        back_button.grid(row=0, column=2, padx=5)
        back_button.configure(style="Back.TButton")

        self.load_habits()

    def load_habits(self):
        """Clear and reload people from DB into the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)
            

        habit = Habit.fetch_all(self.controller.db)
        for p in habit:
            interactions = Completion.get_completions_by_habit(self.controller.db, p.id)
            
            if interactions:
                most_recent = max(interactions, key=lambda x: datetime.strptime(x[1], "%d/%m/%Y"))
                last_completed = most_recent[1]
            else:
                last_completed = None
            
            self.tree.insert("", "end", values=(p.id, p.description, p.frequency, last_completed))
            
    def save_interaction(self):
        
        current_date = datetime.now().strftime("%d/%m/%Y")
        selected_date_str = self.calendar.get_date()
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        print(f"{selected_date}")
        
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            values = self.tree.item(item, "values")
            habit_id = values[0]
        else:
            messagebox.showerror("Error", "Nothing Selected!")
            return
        
        if selected_date:
            interaction = Completion(None, habit_id, selected_date)
            interaction.save_to_db(self.controller.db)
        else:
            interaction = Completion(None, habit_id, current_date)
            interaction.save_to_db(self.controller.db)
            
        self.load_habits()
        
    def delete_interaction(self):
        
        selected_date_str = self.calendar.get_date()
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        print(f"{selected_date}")
        
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            values = self.tree.item(item, "values")
            habit_id = values[0]
        else:
            messagebox.showerror("Error", "Nothing Selected!")
            return
        
        if selected_date:
            interactions = Completion.get_completions_by_habit(self.controller.db, habit_id)
            
            print(interactions)
            
            for i in interactions:
                if i[1] == selected_date:
                    Completion.delete_completion(self.controller.db, i[0])
            
        else:
            messagebox.showerror("Error", "No Date Selected!")
            return
            
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
        interactions = Completion.get_completions_by_habit(self.controller.db, habit_id)

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