import pytest
from analytics.analytics import get_longest_streak, get_success_percentage
from datetime import datetime
from collections import namedtuple

from models.habit import Habit
from models.completion import Completion

Habit_tuple = namedtuple("Habit", ["id", "description", "date_created", "frequency"])
Completion_tuple = namedtuple("Completion", ["habit_id", "date"])


'''
Tests for the Analytics Module

Following tests are unit tests, testing the get_longest streak method 
in the analytics module to ensure it handles daily, weekly and monthly cases
properly as well as when there are no completions at all. These functions
do not use the test_db and test purely the functionality

'''

# Daily
def test_daily_longest_streak():
    habit = Habit_tuple(id=1, description="Test Daily", date_created="01/01/2025", frequency="Daily")
    completions = [
        Completion_tuple(1, "01/01/2025"),
        Completion_tuple(1, "02/01/2025"),
        Completion_tuple(1, "03/01/2025"),
        Completion_tuple(1, "04/01/2025"),
    ]
    assert get_longest_streak(habit, completions) == 4

# Daily With a gap
def test_daily_longest_streak_with_gap():
    habit = Habit_tuple(1, "Test Daily", "01/01/2025", "Daily")
    completions = [
        Completion_tuple(1, "01/01/2025"),
        Completion_tuple(1, "02/01/2025"),
        Completion_tuple(1, "04/01/2025"), 
        Completion_tuple(1, "05/01/2025"),
    ]
    assert get_longest_streak(habit, completions) == 2

# Weekly
def test_weekly_longest_streak():
    habit = Habit_tuple(2, "Test Weekly", "01/01/2025", "Weekly")
    completions = [
        Completion_tuple(2, "01/01/2025"),
        Completion_tuple(2, "08/01/2025"),
        Completion_tuple(2, "15/01/2025"),
        Completion_tuple(2, "29/01/2025"),  # skip a week
    ]
    assert get_longest_streak(habit, completions) == 3

# Monthly
def test_monthly_longest_streak():
    habit = Habit_tuple(3, "Test Monthly", "01/01/2025", "Monthly")
    completions = [
        Completion_tuple(3, "01/01/2025"),
        Completion_tuple(3, "01/02/2025"),
        Completion_tuple(3, "01/03/2025"),
        Completion_tuple(3, "01/05/2025"),  # skip April
    ]
    assert get_longest_streak(habit, completions) == 3
    
# When there are no completions present
def test_no_completions():
    habit = Habit_tuple(4, "Empty Habit", "01/01/2025", "Daily")
    completions = []
    assert get_longest_streak(habit, completions) == 0
    
# Ensure method isnt thrown by multiple habits
def test_different_habit_ids():
    habit = Habit_tuple(5, "Test Daily", "01/01/2025", "Daily")
    completions = [
        Completion_tuple(9, "01/01/2025"),
        Completion_tuple(5, "01/01/2025"),
        Completion_tuple(2, "02/01/2025"),
        Completion_tuple(6, "02/01/2025"),
        Completion_tuple(16, "02/01/2025"),
        Completion_tuple(5, "02/01/2025")
    ]
    assert get_longest_streak(habit, completions) == 2
    
    
"""
Following tests will test the get_current streak method
in the same manner as the tests above but will do so while 
using the test_db.
"""

# Daily
def test_daily_longest_streak_db(test_db):
    
    # brush teeth habit from test_db (1)
    habit = Habit.fetch_habit(test_db, 1)
    completions = Completion.get_completions_by_habit(test_db, 1)
    
    print(completions) 
    
    assert get_longest_streak(habit, completions) == 4
    
def test_weekly_longest_streak_db(test_db):
    
    habit = Habit.fetch_habit(test_db, 3)
    completions = Completion.get_completions_by_habit(test_db, 3)
    
    print(completions) 
    
    assert get_longest_streak(habit, completions) == 3