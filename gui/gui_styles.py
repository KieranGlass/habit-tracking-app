from tkinter import ttk


def apply_styles():
    style = ttk.Style()
    
    style.theme_use("clam")

    style.configure("MainMenu.TButton", background="#2c4b7f", foreground="white", font=("Arial", 12, "bold"), padding=(10, 5), borderwidth=0, relief="flat")
    style.map("MainMenu.TButton", background=[("active", "#1f3559"), ("pressed", "#16263f")], foreground=[("disabled", "gray")])
    
    style.configure("Complete.TButton", background="#69d46f", foreground="white", font=("Arial", 11, "bold"), padding=(8, 4), borderwidth=0, relief="flat")
    style.map("Complete.TButton", background=[("active", "#4ebe54"), ("pressed", "#4ebe54")], foreground=[("disabled", "gray")])
    
    style.configure("Add.TButton", background="#69d46f", foreground="white", font=("Arial", 8, "bold"), padding=(8, 4), borderwidth=0, relief="flat")
    style.map("Add.TButton", background=[("active", "#4ebe54"), ("pressed", "#4ebe54")], foreground=[("disabled", "gray")])
    
    style.configure("Modify.TButton", background="#6f9cd6", foreground="white", font=("Arial", 8, "bold"), padding=(8, 4), borderwidth=0, relief="flat")
    style.map("Modify.TButton", background=[("active", "#4f7db9"), ("pressed", "#4f7db9")], foreground=[("disabled", "gray")])
    
    style.configure("Delete.TButton", background="#c0515a", foreground="white", font=("Arial", 8, "bold"), padding=(8, 4), borderwidth=0, relief="flat")
    style.map("Delete.TButton", background=[("active", "#9c2b35"), ("pressed", "#9c2b35")], foreground=[("disabled", "gray")])
    
    style.configure("DeleteCompletion.TButton", background="#c0515a", foreground="white", font=("Arial", 11, "bold"), padding=(8, 4), borderwidth=0, relief="flat")
    style.map("DeleteCompletion.TButton", background=[("active", "#9c2b35"), ("pressed", "#9c2b35")], foreground=[("disabled", "gray")])
    
    style.configure("BackHabit.TButton", background="#da7eb1", foreground="white", font=("Arial", 8, "bold"), padding=(8, 4), borderwidth=0, relief="flat")
    style.map("BackHabit.TButton", background=[("active", "#c75c97"), ("pressed", "#b85189")], foreground=[("disabled", "gray")])
    
    style.configure("Back.TButton", background="#da7eb1", foreground="white", font=("Arial", 11, "bold"), padding=(8, 4), borderwidth=0, relief="flat")
    style.map("Back.TButton", background=[("active", "#c75c97"), ("pressed", "#b85189")], foreground=[("disabled", "gray")])