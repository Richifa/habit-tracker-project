from datetime import datetime, timedelta

class Habit:
    def __init__(self, id, name, periodicity, created_at, check_offs=None):
        self.id = id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at
        # Ensure check_offs is a list, even if None is passed
        self.check_offs = check_offs if check_offs is not None else []

    def check_off(self, timestamp):
        """Adds a check-off to the local list."""
        self.check_offs.append(timestamp)

    def get_current_streak(self):
        """Calculates the current streak based on periodicity."""
        if not self.check_offs:
            return 0

        # 1. Get unique dates from check_offs and sort them descending
        sorted_dates = sorted(list(set([dt.date() for dt in self.check_offs])), reverse=True)
        today = datetime.now().date()

        streak = 0
        
        if self.periodicity == "daily":
            # Check if the streak is active (completed today or yesterday)
            if sorted_dates[0] != today and sorted_dates[0] != (today - timedelta(days=1)):
                return 0
            
            # Start counting
            # If completed today, start from today. If yesterday, start from yesterday.
            check_date = sorted_dates[0]
            streak = 1
            
            for i in range(1, len(sorted_dates)):
                expected_prev_date = check_date - timedelta(days=1)
                if sorted_dates[i] == expected_prev_date:
                    streak += 1
                    check_date = expected_prev_date
                else:
                    break 

        elif self.periodicity == "weekly":
            # Weekly Logic: Convert all check-off dates to the Monday of their week
            # This groups any check-off in the same week to the same "Monday date"
            mondays = sorted(list(set([d - timedelta(days=d.weekday()) for d in sorted_dates])), reverse=True)
            this_monday = today - timedelta(days=today.weekday())
            last_monday = this_monday - timedelta(weeks=1)

            # Check if active (this week or last week)
            if mondays[0] != this_monday and mondays[0] != last_monday:
                return 0
            
            streak = 1
            check_monday = mondays[0]
            
            for i in range(1, len(mondays)):
                if mondays[i] == check_monday - timedelta(weeks=1):
                    streak += 1
                    check_monday = mondays[i]
                else:
                    break

        return streak

    def get_completion_rate(self, since_date):
        """Calculates completion rate since a specific date."""
        valid_checks = [c for c in self.check_offs if c >= since_date]
        days_passed = (datetime.now() - since_date).days + 1
        
        if self.periodicity == "daily":
            periods = days_passed
        else:
            periods = days_passed / 7
            
        if periods <= 0: return 0
        return len(valid_checks) / periods