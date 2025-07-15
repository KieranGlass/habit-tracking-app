from datetime import datetime, timedelta
from itertools import groupby


from models.habit import Habit
from models.completion import Completion

def get_all_habits(db):
    return Habit.fetch_all(db)

def get_habits_by_frequency(db, frequency):
    habits = Habit.fetch_all(db)
    return list(filter(lambda habit: habit.frequency == frequency, habits))

'''def get_longest_current_streak(db):'''

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
    
    correct_completions = []
    
    for c in completions:
        if c.habit_id == habit.id:
            correct_completions.append(c)

    # Sort dates ascending
    dates = sorted(datetime.strptime(c.date, "%d/%m/%Y") for c in correct_completions)

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

