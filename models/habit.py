from database import Database
import sqlite3
from contextlib import closing

class Habit:
    def __init__(self, id, description, date_created, frequency):
        self.id = id
        self.description = description
        self.date_created = date_created
        self.frequency = frequency
        
    def save_to_db(self, db: Database):
        try:
            with closing(db.conn.cursor()) as cursor:
                cursor.execute('''
                    INSERT INTO habits (description, date_created, frequency)
                    VALUES (?, ?, ?)
                ''', (self.description, self.date_created, self.frequency))
                db.conn.commit()
        except sqlite3.Error as e:
            print(f"Failed to insert habit: {e}")
            
    def save_changes_to_db(self, db: Database):
        try:
            with closing(db.conn.cursor()) as cursor:
                cursor.execute('''
                    UPDATE habits
                    SET description = ?, date_created = ?, frequency = ?
                    WHERE id = ?
                ''', (self.description, self.date_created, self.frequency, self.id))
                db.conn.commit()
        except sqlite3.Error as e:
            print(f"Failed to insert habit: {e}")
            
    def fetch_all(db):
        with closing(db.conn.cursor()) as cursor:
            cursor.execute("SELECT id, description, date_created, frequency FROM habits")
            rows = cursor.fetchall()
            return [Habit(*row) for row in rows]
        
    def fetch_habit(db, id):
        with closing(db.conn.cursor()) as cursor:
            cursor.execute("SELECT id, description, date_created, frequency FROM habits WHERE id=?", (id,))
            habit = cursor.fetchall()
            return habit

    def delete(db, id):
        try:
            with closing(db.conn.cursor()) as cursor:
                cursor.execute("DELETE FROM habits WHERE id=?", (id,))
                db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Delete error: {e}")
            return False
    