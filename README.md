# Habit Tracking Application

An application developed using Python and the TKinter interface

## Technology Stack

- Python
- Python TKinter
- Pytest
- Sqlite 3

## Application Features for Users

- Create and manage habits using the Tkinter interface
- Users can add habit completions immediately or after the fact
- Users can delete incorrect completions or unwanted habits
- Habit frequency and description can be modified if necesarry
- Users can view analytics based on their progress
- Sqlite database persists data across sessions

## Database

- Lightweight SQLite database
- Stores information about Habits and Completions in two separate tables
- Database setup pre-populates application with 5 habits
- Pre-populated habits can be easily deleted if not necessary by the user

## Installing the Application

### Step 1: Clone the repository

```

git clone https://github.com/KieranGlass/habit-tracking-app.git
cd habit-tracking-app

```
### Step 2: Install Dependencies

- Dependencies only needed at this point in time for running
  the applications tests. (Pytest)
- Both SQLite and TKinter are built in Python modules
- Requires Python 3.7 or newer

```

pip install -r requirements.txt

```

## Running the Application

```

python main.py

```

- Starts the GUI Mainloop and opens the main menu
- 1 - Logging Habit Completions
- 2 - Creating, Altering + Modifying Habits
- 3 - Analytics Module



