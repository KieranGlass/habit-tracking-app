from databases.create_db import Database
import sqlite3
from contextlib import closing

"""
    Model for a Completion
    
    Comprised of three attributes
    
    id - autoincrementing and handled by db
    habit_id - foreign key linked to Habit
    date - the date of the habit completion
    
    Contains methods for;
    
    - Saving new completions to the db
    - Getting all completions
    - Getting completions based on habit id
    - Deleting completions

"""
class Completion:
    
    def __init__(self, id, habit_id, date):
        self.id = id
        self.habit_id = habit_id
        self.date = date
    
    
    def save_to_db(self, db: Database):
        try:
            with closing(db.conn.cursor()) as cursor:
                cursor.execute('''
                    INSERT INTO interactions (habit_id, date)
                    VALUES (?, ?)
                ''', (self.habit_id, self.date))
                db.conn.commit()
        except sqlite3.Error as e:
            print(f"Failed to insert interaction: {e}")
            
    
    def get_all_completions(db):
        try:
            with closing(db.conn.cursor()) as cursor:
                cursor.execute("SELECT id, habit_id, date FROM interactions")
                rows = cursor.fetchall()
                return [Completion(*row) for row in rows]
        except sqlite3.Error as e:
            print(f"Failed to get completions: {e}")
              
    
    def get_completions_by_habit(db, habit_id):
        try:
            with closing(db.conn.cursor()) as cursor:
                cursor.execute("SELECT id, date FROM interactions WHERE habit_id=?", (habit_id,))
                interactions = cursor.fetchall()
                return interactions
        except sqlite3.Error as e:
            print(f"Failed to insert habit: {e}")
                               
                               