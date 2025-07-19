import pytest
from analytics.analytics import get_longest_streak
from datetime import datetime
from collections import namedtuple

Habit = namedtuple("Habit", ["id", "description", "date_created", "frequency"])
Completion = namedtuple("Completion", ["habit_id", "date"])


'''
Tests for the Analytics Module

Following tests are unit tests, testing the get_longest streak method 
in the analytics module to ensure it handles daily, weekly and monthly cases
properly as well as when there are no completions at all

'''

# Daily
def test_daily_longest_streak():
    habit = Habit(id=1, description="Test Daily", date_created="01/01/2025", frequency="Daily")
    completions = [
        Completion(1, "01/01/2025"),
        Completion(1, "02/01/2025"),
        Completion(1, "03/01/2025"),
        Completion(1, "04/01/2025"),
    ]
    assert get_longest_streak(habit, completions) == 4

# Daily With a gap
def test_daily_longest_streak_with_gap():
    habit = Habit(1, "Test Daily", "01/01/2025", "Daily")
    completions = [
        Completion(1, "01/01/2025"),
        Completion(1, "02/01/2025"),
        Completion(1, "04/01/2025"), 
        Completion(1, "05/01/2025"),
    ]
    assert get_longest_streak(habit, completions) == 2

# Weekly
def test_weekly_longest_streak():
    habit = Habit(2, "Test Weekly", "01/01/2025", "Weekly")
    completions = [
        Completion(2, "01/01/2025"),
        Completion(2, "08/01/2025"),
        Completion(2, "15/01/2025"),
        Completion(2, "29/01/2025"),  # skip a week
    ]
    assert get_longest_streak(habit, completions) == 3

# Monthly
def test_monthly_longest_streak():
    habit = Habit(3, "Test Monthly", "01/01/2025", "Monthly")
    completions = [
        Completion(3, "01/01/2025"),
        Completion(3, "01/02/2025"),
        Completion(3, "01/03/2025"),
        Completion(3, "01/05/2025"),  # skip April
    ]
    assert get_longest_streak(habit, completions) == 3
    
# When there are no completions present
def test_no_completions():
    habit = Habit(4, "Empty Habit", "01/01/2025", "Daily")
    completions = []
    assert get_longest_streak(habit, completions) == 0
    
# Ensure method isnt thrown by multiple habits
def test_different_habit_ids():
    habit = Habit(5, "Test Daily", "01/01/2025", "Daily")
    completions = [
        Completion(9, "01/01/2025"),
        Completion(5, "01/01/2025"),
        Completion(2, "02/01/2025"),
        Completion(6, "02/01/2025"),
        Completion(16, "02/01/2025"),
        Completion(5, "02/01/2025")
    ]
    assert get_longest_streak(habit, completions) == 2