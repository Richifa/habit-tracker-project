import pytest
from datetime import datetime, timedelta
from habit import Habit
import analytics

# Helper to generate dates relative to today
def get_dates(days_ago_list):
    base = datetime.now()
    return [base - timedelta(days=d) for d in days_ago_list]

class TestHabit:
    
    def test_daily_streak_calculation_perfect(self):
        """Test a perfect 3-day daily streak."""
        # Check-offs: Today (0), Yesterday (1), Day before (2)
        check_offs = get_dates([0, 1, 2])
        h = Habit(1, "Test", "daily", datetime.now(), check_offs)
        assert h.get_current_streak() == 3

    def test_daily_streak_broken(self):
        """Test a broken streak."""
        # Check-offs: Today (0), 2 days ago (2) -> Missed yesterday (1)
        check_offs = get_dates([0, 2])
        h = Habit(1, "Test", "daily", datetime.now(), check_offs)
        # Streak is 1 (just today)
        assert h.get_current_streak() == 1

    def test_daily_streak_zero(self):
        """Test zero streak if not done today or yesterday."""
        # Check-offs: 5 days ago
        check_offs = get_dates([5])
        h = Habit(1, "Test", "daily", datetime.now(), check_offs)
        assert h.get_current_streak() == 0

class TestAnalytics:

    def test_filter_by_periodicity(self):
        h1 = Habit(1, "A", "daily", datetime.now())
        h2 = Habit(2, "B", "weekly", datetime.now())
        habits = [h1, h2]
        
        daily = analytics.filter_habits_by_periodicity(habits, "daily")
        assert len(daily) == 1
        assert daily[0].name == "A"

    def test_longest_streak_all(self):
        # Mock habits with checkoffs
        h1 = Habit(1, "Strong", "daily", datetime.now(), get_dates([0, 1, 2, 3, 4])) # Streak 5
        h2 = Habit(2, "Weak", "daily", datetime.now(), get_dates([0]))             # Streak 1
        
        name, length = analytics.get_longest_streak_all([h1, h2])
        assert name == "Strong"
        assert length == 5
