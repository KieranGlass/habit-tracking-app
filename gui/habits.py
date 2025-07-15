import tkinter as tk
from tkinter import ttk, messagebox
from models.habit import Habit
from gui.add_habit import AddHabitForm
from gui.modify_habit import ModifyHabitForm


class HabitView(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Title
        tk.Label(self, text="Habits", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        # Treeview to show list of people
        self.tree = ttk.Treeview(self, columns=("id", "description", "date created", "frequency"), show="headings")
        self.tree.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Hide 'id' column from view
        self.tree.column("id", width=0, stretch=False)
        
        self.tree.heading("id", text="")  
        # Make Treeview columns expand to fill the available space
        column_widths = [1, 1, 1, 1, 1]  

        for col, width in zip(("description", "date created", "frequency"), column_widths):
            self.tree.heading(col, text=col.title())
            self.tree.column(col, stretch=True, anchor="center", width=80)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, pady=10)

        tk.Button(button_frame, text="Add Habit", command=self.open_add_habit).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Modify Habit", command=self.modify_habit).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Habit", command=self.delete_habit).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Back", command=self.controller.show_main_menu).grid(row=0, column=3, padx=5)

        self.load_habits()

    def load_habits(self):
        """Clear and reload habits from DB into the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        people = Habit.fetch_all(self.controller.db)
        for p in people:
            self.tree.insert("", "end", values=(p.id, p.description, p.date_created, p.frequency))

    def open_add_habit(self):
        """Replace frame with AddHabitForm and reload on return."""
        form = AddHabitForm(self.controller)
        form.grid(row=0, column=0, sticky="nsew")
        self.destroy()

    def modify_habit(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Habit", "Please select a habit to modify.")
            return
        
        habit_data = self.tree.item(selected)["values"]
        id = habit_data[0]
        
        form = ModifyHabitForm(self.controller, id)
        form.grid(row=0, column=0, sticky="nsew")
        self.destroy()

    def delete_habit(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Habit", "Please select a habit to delete.")
            return

        habit_data = self.tree.item(selected)["values"]
        id, description = habit_data[0], habit_data[1]
        confirm = messagebox.askyesno("Confirm", f"Delete {description}?")
        if confirm:
            success = Habit.delete(self.controller.db, id)
            if success:
                messagebox.showinfo("Deleted", "Habit deleted successfully.")
                self.load_habits()
            else:
                messagebox.showerror("Error", "Failed to delete habit.")