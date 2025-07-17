import sqlite3
from contextlib import closing

class TestDatabase:
    
    def __init__(self):
        """Creates a fresh in-memory test database with test-specific data."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self):
        """Creates tables and seeds them with test-specific data."""
        with closing(self.conn.cursor()) as cursor:
            # Create habits table
            cursor.execute('''
                CREATE TABLE habits (
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
    
            
    def close(self):
        self.conn.close()