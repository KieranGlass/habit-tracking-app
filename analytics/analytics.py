from datetime import datetime, timedelta

from models.habit import Habit
from models.completion import Completion

"""
Analytics module for calculating habit streaks.

This module processes information about Habit and Completion models:

- the longest ongoing current streak per habit,
- the longest ongoing current streak overall
- the longest historical streak per habit,
- the longest historical streak overall


"""


def get_longest_current_streak(db):
    habits = Habit.fetch_all(db)
    completions = Completion.get_all_completions(db)

    longest = 0
    top_habit = None

    for habit in habits:
        streak = get_current_streak(habit, completions)
        if streak > longest:
            longest = streak
            top_habit = habit

    return top_habit, longest

def get_longest_run_streak_all(db):
    habits = Habit.fetch_all(db)
    completions = Completion.get_all_completions(db)

    longest = 0
    top_habit = None

    for habit in habits:
        streak = get_longest_streak(habit, completions)
        if streak > longest:
            longest = streak
            top_habit = habit

    return top_habit, longest

def get_longest_streaks_per_habit(db):
    habits = Habit.fetch_all(db)
    completions = Completion.get_all_completions(db)

    return [
        (habit, get_longest_streak(habit, completions))
        for habit in habits
    ]
    
    
def get_longest_streak(habit, completions):
    """Calculate the longest streak for a given habit based on its frequency."""
    
    if not completions:
        return 0
    
        # Filter completions for this habit
    dates = sorted([datetime.strptime(c.date, "%d/%m/%Y") for c in completions if c.habit_id == habit.id])

    if not dates:
        return 0 

    # Set time delta based on frequency
    freq_delta = {
        "Daily": timedelta(days=1),
        "Weekly": timedelta(weeks=1),
        "Monthly": "Monthly"
    }

    delta = freq_delta.get(habit.frequency)

    longest = 1
    current = 1

    for i in range(1, len(dates)):
        if habit.frequency in ["Monthly"]:
            prev = dates[i-1]
            curr = dates[i]
            months_diff = (curr.year - prev.year) * 12 + (curr.month - prev.month)

            expected = 1 if habit.frequency == "Monthly" else 3

            if months_diff == expected:
                current += 1
            else:
                longest = max(longest, current)
                current = 1

        else:  # Daily / Weekly
            if dates[i] - dates[i-1] == delta:
                current += 1
            else:
                longest = max(longest, current)
                current = 1

    return max(longest, current)

def get_current_streak(habit, completions):
    """Calculate the current ongoing streak for a given habit based on its frequency."""

    if not completions:
        return 0

    # Filter only completions for the given habit
    correct_completions = [c for c in completions if c.habit_id == habit.id]

    # Sort the dates in descending order (most recent first)
    dates = sorted((datetime.strptime(c.date, "%d/%m/%Y") for c in correct_completions), reverse=True)

    # Get today's date without time
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    # Define time delta for comparison
    freq_delta = {
        "Daily": timedelta(days=1),
        "Weekly": timedelta(weeks=1),
        "Monthly": "Monthly"  # Handled separately
    }

    delta = freq_delta.get(habit.frequency)
    streak = 0

    # Start checking from today or the most recent valid period
    for i in range(len(dates)):
        if i == 0:
            # First check: if the most recent completion is within the valid range from today
            if habit.frequency == "Monthly":
                months_diff = (today.year - dates[i].year) * 12 + (today.month - dates[i].month)
                if months_diff > 1:
                    break
            else:
                if today - dates[i] > delta:
                    break
            streak += 1
        else:
            prev = dates[i - 1]
            curr = dates[i]

            if habit.frequency == "Monthly":
                months_diff = (prev.year - curr.year) * 12 + (prev.month - curr.month)
                if months_diff == 1:
                    streak += 1
                else:
                    break
            else:
                if prev - curr == delta:
                    streak += 1
                else:
                    break

    return streak

