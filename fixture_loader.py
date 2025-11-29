import database
from datetime import datetime, timedelta

def seed_db():
    print(" Loading sample habits and test data...")

    # Connect to database using our existing database.py module
    conn = database.get_db_connection()
    database.create_tables(conn)

    # ---------------------------------------------------------
    # 1. Predefined habits (Matches your Concept Document)
    # ---------------------------------------------------------
    habits = [
        ("Morning Meditation", "daily"),
        ("Go for a run", "daily"),
        ("Weekly Review", "weekly"),
        ("Read 20 pages", "daily"),
        ("Meal Prep", "weekly")
    ]

    habit_ids = {}
    # Backdate start by 4 weeks
    start_date = datetime.now() - timedelta(weeks=4)

    for name, period in habits:
        # We use isoformat() to ensure the date saves as a string string
        habit_id = database.save_new_habit(conn, name, period, start_date.isoformat())
        habit_ids[name] = habit_id

    print("✔ Added 5 predefined habits.")

    # ---------------------------------------------------------
    # 2. Generate 4 weeks of check-off data
    # ---------------------------------------------------------
    checkoffs = []

    # Habit 1: Morning Meditation (Daily - Perfect)
    h_id = habit_ids["Morning Meditation"]
    for i in range(28):
        date = start_date + timedelta(days=i)
        checkoffs.append((h_id, date.isoformat()))

    # Habit 2: Go for a run (Daily - Every 3 days)
    h_id = habit_ids["Go for a run"]
    for i in range(28):
        if i % 3 == 0:
            date = start_date + timedelta(days=i)
            checkoffs.append((h_id, date.isoformat()))

    # Habit 3: Weekly Review (Weekly - Perfect)
    h_id = habit_ids["Weekly Review"]
    for i in range(4):
        date = start_date + timedelta(weeks=i)
        checkoffs.append((h_id, date.isoformat()))

    # Habit 4: Read 20 pages (Daily - Broken streak)
    h_id = habit_ids["Read 20 pages"]
    for i in range(10): # First 10 days
        date = start_date + timedelta(days=i)
        checkoffs.append((h_id, date.isoformat()))
    for i in range(15, 28): # Resume after gap
        date = start_date + timedelta(days=i)
        checkoffs.append((h_id, date.isoformat()))

    # Habit 5: Meal Prep (Weekly - Missed last week)
    h_id = habit_ids["Meal Prep"]
    for i in range(3): # Only 3 weeks
        date = start_date + timedelta(weeks=i)
        checkoffs.append((h_id, date.isoformat()))

    # Save all check-offs to database
    for h_id, ts in checkoffs:
        database.save_new_checkoff(conn, h_id, ts)

    print("✔ Added 4 weeks of sample check-offs.")
    print("🎉 Database seeded successfully!")

# This is the missing part that makes the script actually run!
if __name__ == "__main__":
    seed_db()