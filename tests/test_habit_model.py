import pytest
from models.habit import Habit

"""
    Tests for the Habit Model
    
    Tests written for all methods within the Habit Model
    
    Tests use a specific test database as these tests are only interested in
    testing the functionality of the methods.
    
"""

def test_fetch_all_habits(test_db):
    
    habits = Habit.fetch_all(test_db)
    assert len(habits) == 14
    
def test_fetch_habit(test_db):
    
    first_habit = Habit.fetch_habit(test_db, 1)
    third_habit = Habit.fetch_habit(test_db, 3)
    seventh_habit = Habit.fetch_habit(test_db, 7)
    twelfth_habit = Habit.fetch_habit(test_db, 12)
    no_habit = Habit.fetch_habit(test_db, 9999)  # ID that doesn't exist
    
    assert first_habit.description == "Brush Teeth"
    assert third_habit.date_created == "06/06/2025"
    assert seventh_habit.description == "Shower"
    assert twelfth_habit.frequency == "Daily"
    assert no_habit == None
    
def test_save_to_db(test_db):
    
    new_habit = Habit(15, "Moisturise", "01/06/2025", "Daily")
    
    new_habit.save_to_db(test_db)
    
    check_habit = Habit.fetch_habit(test_db, 15)
    
    assert check_habit.id == 15
    assert check_habit.description == "Moisturise"
    
    
def test_delete_habit(test_db):
    
    pre_deleted_habit = Habit.fetch_habit(test_db, 14)
    
    assert pre_deleted_habit.description == "Make the bed"
    
    Habit.delete(test_db, 14)
    
    habits = Habit.fetch_all(test_db)
    
    assert len(habits) == 13
    
    Habit.delete(test_db, 3)
    
    habits_two = Habit.fetch_all(test_db)
    
    assert len(habits_two) == 12
    
    ids = [habit.id for habit in habits]
    assert 14 not in ids