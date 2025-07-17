import sqlite3
from contextlib import closing
import os

'''Notes for reader, 
Database class will only contain connections and schema-level stuff, not individual records.
So for example, creating a new person will be handled by the person class.
Structured like this as it adheres to OOP best practice, promoting encapsulation and reusability'''

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
                
                cursor.execute('''
                INSERT OR IGNORE INTO habits (description, date_created, frequency)
                    VALUES 
                    ('Brush Teeth', '06/05/2025', 'Daily'),
                    ('Visit Grandparents', '04/06/2025', 'Monthly'),
                    ('Water Plants', '06/06/2025', 'Weekly'),
                    ('Drink 2 Litres of Water', '04/04/2025', 'Daily'),
                    ('Read a Book', '06/05/2025', 'Monthly')
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
                
                cursor.execute('''
                INSERT OR IGNORE INTO interactions (habit_id, date)
                    VALUES 
                    (1, '02/05/2025'),
                    (1, '04/07/2025'),
                    (1, '06/07/2025'),
                    (1, '07/07/2025'),
                    (1, '08/07/2025'),
                    (1, '09/07/2025'),
                    (2, '04/06/2025'),
                    (3, '06/06/2025'),
                    (4, '04/04/2025'),
                    (5, '06/05/2025')
                ''')
                
                
                self.conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
            
    def close(self):
        self.conn.close()