import pytest
import os
from datetime import datetime, timedelta
from habit import Habit
import database
import analytics

# Helper to generate dates relative to today
def get_dates(days_ago_list):
    base = datetime.now()
    return [base - timedelta(days=d) for d in days_ago_list]

# --- FIXTURE: SETUP A TEMPORARY DATABASE FOR TESTING ---
@pytest.fixture
def test_conn():
    """Creates a temporary in-memory database connection for testing."""
    test_db_name = "test_habits.db"
    conn = database.get_db_connection(test_db_name)
    database.create_tables(conn)
    yield conn
    
    # Cleanup after tests run
    conn.close()
    if os.path.exists(test_db_name):
        try:
            os.remove(test_db_name)
        except PermissionError:
            pass

# --- PART A: TESTING CREATION, EDITING (CHECK-OFF), AND DELETION ---

def test_habit_creation(test_conn):
    """Test that a habit can be created and saved to the database."""
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    database.save_new_habit(test_conn, "Drink Water", "daily", created_at)
    
    habits, _ = database.fetch_all_habits_and_checkoffs(test_conn)
    assert len(habits) == 1
    assert habits[0][1] == "Drink Water"  # Index 1 is the habit name
    assert habits[0][2] == "daily"        # Index 2 is periodicity

def test_habit_editing_check_off(test_conn):
    """Test that checking off a habit updates its history in the database."""
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    habit_id = database.save_new_habit(test_conn, "Read", "daily", created_at)
    
    # Check off the habit (editing its state)
    database.save_new_checkoff(test_conn, habit_id, created_at)
    
    _, checkoffs = database.fetch_all_habits_and_checkoffs(test_conn)
    assert len(checkoffs) == 1
    assert checkoffs[0][0] == habit_id  # Index 0 is habit_id

def test_habit_deletion(test_conn):
    """Test that a habit can be successfully deleted, including cascade delete."""
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    habit_id = database.save_new_habit(test_conn, "Jogging", "weekly", created_at)
    database.save_new_checkoff(test_conn, habit_id, created_at)
    
    # Delete the habit
    database.delete_habit_by_id(test_conn, habit_id)
    
    habits, checkoffs = database.fetch_all_habits_and_checkoffs(test_conn)
    assert len(habits) == 0
    assert len(checkoffs) == 0  # Check-offs should automatically be deleted (CASCADE)

# --- PART B: TESTING ANALYTICS MODULE ---

def test_analytics_list_all():
    """Test analytics function to list all tracked habits."""
    h1 = Habit(1, "A", "daily", datetime.now())
    h2 = Habit(2, "B", "weekly", datetime.now())
    
    result = analytics.get_all_habits([h1, h2])
    assert len(result) == 2

def test_analytics_list_by_periodicity():
    """Test analytics function to filter habits by periodicity."""
    h1 = Habit(1, "Daily 1", "daily", datetime.now())
    h2 = Habit(2, "Weekly 1", "weekly", datetime.now())
    habits = [h1, h2]
    
    daily = analytics.filter_habits_by_periodicity(habits, "daily")
    assert len(daily) == 1
    assert daily[0].name == "Daily 1"
    
    weekly = analytics.filter_habits_by_periodicity(habits, "weekly")
    assert len(weekly) == 1
    assert weekly[0].name == "Weekly 1"

def test_analytics_longest_streak_all_habits():
    """Test analytics function to find the longest streak among all habits."""
    h1 = Habit(1, "Strong", "daily", datetime.now(), get_dates([0, 1, 2])) 
    h2 = Habit(2, "Weak", "daily", datetime.now(), get_dates([0]))         
    
    # Mocking the streak calculation to ensure the analytics function works correctly
    h1.get_current_streak = lambda: 3
    h2.get_current_streak = lambda: 1

    longest = analytics.get_longest_streak_all([h1, h2])
    
    assert longest[0] == "Strong"
    assert longest[1] == 3

def test_analytics_longest_streak_specific_habit():
    """Test analytics function to calculate the streak of a specific given habit."""
    h1 = Habit(1, "Gym", "weekly", datetime.now(), get_dates([0, 7, 14]))
    h1.get_current_streak = lambda: 3
    
    streak = analytics.get_longest_streak_for_habit(h1)
    assert streak == 3

def test_analytics_struggling_habits():
    """Test analytics function for struggling habits (<50% completion rate)."""
    h1 = Habit(1, "Good", "daily", datetime.now())
    h2 = Habit(2, "Bad", "daily", datetime.now())
    
    # We override the completion rate just for this test to verify the analytics filter logic
    h1.get_completion_rate = lambda d: 0.9 # 90%
    h2.get_completion_rate = lambda d: 0.2 # 20%
    
    since = datetime.now() - timedelta(days=5)
    struggling = analytics.get_struggling_habits([h1, h2], since)
    
    assert len(struggling) == 1
    assert struggling[0].name == "Bad"
