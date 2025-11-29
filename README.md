# Python Habit Tracker CLI

A robust, command-line-based Habit Tracking application built with Python 3. This project demonstrates Object-Oriented Programming (OOP) for state management and Functional Programming (FP) for data analytics.

## Features
- **Habit Management:** Create daily and weekly habits.
- **Streak Tracking:** Algorithms automatically calculate current streaks based on periodicity.
- **Analytics:** View longest streaks and filter habits using functional programming paradigms.
- **Data Persistence:** Uses SQLite3 for robust data storage.
- **Test Suite:** Fully tested using `pytest`.

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/Richifa/habit-tracker-project.git
   cd habit-tracker-project

2. Install dependencies:

 ```bash
pip install -r requirements.txt
 ```
##### Usage
Initialize Database & Test Data:
 ```bash
python main.py seed-db
 ```
##### List Habits:
 ```
python main.py list
```
Add a Habit:
 ```
python main.py add --name "Reading" --period daily
```
Check-off a Habit:
```
python main.py check-off --name "Reading"
```
Run Analytics:
```
python main.py analyze --mode longest
```
Running Tests
Run the unit test suite to verify logic:
```
python -m pytest
```
4.  Click **Commit changes**.

---

