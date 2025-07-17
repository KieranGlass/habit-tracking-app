from databases.create_db import Database
from gui.gui import Gui

import subprocess
import sys


def run_tests():
    
    ''' Automatic Testing Method
    
    When application is run is development environment, all tests within the 
    tests folder are run automatically
    
    Serves as an aide to me as developer to continually check tests pass after changes are made
    '''
    
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Tests failed! Exiting.")
        sys.exit(1)  # Stop running the program if tests fail

run_tests()

class App:
    
    '''   Main application class, run from main.py.

    When instantiated, the App class:
    - Creates a Database object, which opens a connection to the SQLite database file located
      in the same directory as create_db.py.
    - Calls create_tables() to ensure the database schema is set up; if the database and tables
      already exist, this has no effect.
    - Creates a Gui object, passing the Database instance to it.

    The run() method starts the Gui's main event loop.

    when the program is exited, the database connection is closed.'''
    
    
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