import sqlite3
from contextlib import closing
import os

"""Production SQLite db to be used with application


Database class will only contain connections and schema-level stuff, not individual records.
So for example, creating a new habit will be handled by the habit class.
Structured like this as it adheres to OOP best practice, promoting encapsulation and reusability

Completely separate from the test_db

Pre-populted with a handful of habits to provide the user with intuitive usage, the 
habits already in system can be easily deleted by user if not applicable to them

All id numbers for Habits and completions are autoincrementing and handled by the db

Input fields throughout the application are controlled with validations to ensure that data
in the db is of one of the correct types and formats.

For example a date will always be formatted in the code to be DD/MM/YYYY and user can only ever enter a
'Daily', 'Weekly', 'Monthly' input for frequencies.

"""

class Database:
    
    def __init__(self, db_filename='production.db'):
        '''Creates the connection to the sqlite db'''
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)
        self.conn = sqlite3.connect(self.db_path)
        
        self.conn.execute("PRAGMA foreign_keys = ON")
    
    
    def create_tables(self):
        '''
        Creates the db tables, and therefore the overall structure of the db.
        First time around it creates entire db, but when program is restarted, effectively changes nothing
        as it only creates tables if they already exist
        '''
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT UNIQUE NOT NULL,
                        date_created TEXT NOT NULL,
                        frequency TEXT NOT NULL
                    )
                ''')
                
                
                
                cursor.execute("SELECT COUNT(*) FROM habits")
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO habits (description, date_created, frequency)
                        VALUES 
                        ('Brush Teeth', '21/07/2025', 'Daily'),
                        ('Visit Grandparents', '21/07/2025', 'Monthly'),
                        ('Water Plants', '21/07/2025', 'Weekly'),
                        ('Drink 2 Litres of Water', '21/07/2025', 'Daily'),
                        ('Read a Book', '21/07/2025', 'Monthly')
                    ''')
        
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
                        UNIQUE(habit_id, date)
                    )
                ''')
                
                self.conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
            
    def close(self):
        self.conn.close()