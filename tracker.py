from datetime import datetime
import database
from habit import Habit
import analytics

class HabitTracker:
    def __init__(self, db_path='habits.db'):
        """Initialize the tracker and load data."""
        self.db_path = db_path
        self.conn = database.get_db_connection(db_path)
        database.create_tables(self.conn)
        self.habits = []
        self.load_all_habits()

    def load_all_habits(self):
        """Loads habits and check-offs from DB and creates Habit objects."""
        habit_rows, checkoff_rows = database.fetch_all_habits_and_checkoffs(self.conn)
        
        habit_map = {}
        for row in habit_rows:
            try:
                created_at_dt = datetime.fromisoformat(row[3])
            except ValueError:
                created_at_dt = datetime.now()

            h = Habit(id=row[0], name=row[1], periodicity=row[2], created_at=created_at_dt)
            habit_map[h.id] = h

        for row in checkoff_rows:
            habit_id = row[0]
            ts_str = row[1]
            if habit_id in habit_map:
                try:
                    ts_dt = datetime.fromisoformat(ts_str)
                    habit_map[habit_id].check_off(ts_dt)
                except ValueError:
                    pass

        self.habits = list(habit_map.values())

    def add_habit(self, name, periodicity):
        """Creates a new habit and saves it."""
        created_at = datetime.now()
        new_id = database.save_new_habit(self.conn, name, periodicity, created_at.isoformat())
        new_habit = Habit(new_id, name, periodicity, created_at)
        self.habits.append(new_habit)
        print(f"Habit '{name}' created successfully!")

    def delete_habit(self, habit_id):
        """Deletes a habit."""
        database.delete_habit_by_id(self.conn, habit_id)
        self.load_all_habits()
        print("Habit deleted.")

    def check_off_habit(self, name, date_str=None):
        """Finds a habit by name and checks it off."""
        found_habit = next((h for h in self.habits if h.name.lower() == name.lower()), None)
        
        if not found_habit:
            print(f"Error: Habit '{name}' not found.")
            return

        if date_str:
            try:
                dt = datetime.fromisoformat(date_str)
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                return
        else:
            dt = datetime.now()

        database.save_new_checkoff(self.conn, found_habit.id, dt.isoformat())
        found_habit.check_off(dt)
        print(f"Checked off '{name}' for {dt.date()}!")