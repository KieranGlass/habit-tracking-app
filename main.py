from databases.create_db import Database
from gui.gui import Gui

class App:
    def __init__(self):
        self.db = Database()
        self.db.create_tables()
        self.gui = Gui(self.db)

    def run(self):
        self.gui.mainloop()

    def close(self):
        self.db.close()

if __name__ == "__main__":
    app = App()
    try:
        app.run()
    finally:
        app.close()