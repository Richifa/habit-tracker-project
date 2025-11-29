from functools import reduce

def get_all_habits(habits):
    """Returns the list of habits."""
    return habits

def filter_habits_by_periodicity(habits, periodicity):
    """Returns habits matching the periodicity (daily/weekly)."""
    # Functional: Uses filter() and lambda
    return list(filter(lambda h: h.periodicity == periodicity, habits))

def get_longest_streak_all(habits):
    """Returns the single longest streak among ALL habits."""
    if not habits:
        return ("None", 0)
    
    # Functional: Uses map() to create (name, streak) tuples
    streaks = list(map(lambda h: (h.name, h.get_current_streak()), habits))
    
    # Functional: Uses max() to find the highest tuple
    return max(streaks, key=lambda item: item[1])

def get_longest_streak_for_habit(habit):
    """Returns the longest streak for a specific habit."""
    return habit.get_current_streak()

def get_struggling_habits(habits, since_date):
    """Returns habits with < 50% completion rate."""
    # Functional: filter based on completion rate
    return list(filter(lambda h: h.get_completion_rate(since_date) < 0.5, habits))