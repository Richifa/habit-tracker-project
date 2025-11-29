import click
from tracker import HabitTracker
import analytics
import fixture_loader

tracker = HabitTracker()

@click.group()
def cli():
    """Habit Tracker CLI - Track your daily and weekly habits."""
    pass

@cli.command()
@click.option('--name', prompt='Habit Name', help='The name of the habit')
@click.option('--period', type=click.Choice(['daily', 'weekly'], case_sensitive=False), prompt='Periodicity', help='daily or weekly')
def add(name, period):
    """Create a new habit."""
    tracker.add_habit(name, period)

@cli.command()
def list():
    """List all current habits."""
    tracker.load_all_habits() # Refresh data
    habits = tracker.habits
    if not habits:
        click.echo("No habits found.")
        return
    
    click.echo(f"{'ID':<5} {'Name':<20} {'Period':<10} {'Streak':<10}")
    click.echo("-" * 50)
    for h in habits:
        streak = h.get_current_streak()
        click.echo(f"{h.id:<5} {h.name:<20} {h.periodicity:<10} {streak:<10}")

@cli.command()
@click.option('--name', prompt='Habit Name', help='The name of the habit to check off')
@click.option('--date', help='Date in YYYY-MM-DD format (optional)', default=None)
def check_off(name, date):
    """Mark a habit as completed."""
    tracker.check_off_habit(name, date)

@cli.command()
@click.option('--name', prompt='Habit Name', help='The name of the habit to delete')
def delete(name):
    """Delete a habit."""
    found_habit = next((h for h in tracker.habits if h.name.lower() == name.lower()), None)
    if found_habit:
        if click.confirm(f"Are you sure you want to delete '{name}'?"):
            tracker.delete_habit(found_habit.id)
    else:
        click.echo("Habit not found.")

@cli.command()
@click.option('--mode', type=click.Choice(['all', 'daily', 'weekly', 'longest'], case_sensitive=False), default='all')
def analyze(mode):
    """Analyze your habits."""
    tracker.load_all_habits()
    habits = tracker.habits
    
    if mode == 'all':
        click.echo(f"Total habits tracked: {len(habits)}")
        for h in habits: click.echo(f"- {h.name} ({h.periodicity})")
    elif mode == 'daily':
        daily = analytics.filter_habits_by_periodicity(habits, 'daily')
        click.echo("Daily Habits:")
        for h in daily: click.echo(f"- {h.name}")
    elif mode == 'weekly':
        weekly = analytics.filter_habits_by_periodicity(habits, 'weekly')
        click.echo("Weekly Habits:")
        for h in weekly: click.echo(f"- {h.name}")
    elif mode == 'longest':
        name, length = analytics.get_longest_streak_all(habits)
        click.echo(f"Longest streak is {length} days/weeks by '{name}'")

@cli.command(name="seed-db")
def seed_db():
    """Load test fixtures (5 habits + 4 weeks data)."""
    if click.confirm("This will Add sample data. Continue?"):
        fixture_loader.seed_db()
        tracker.load_all_habits() # Reload tracker
        click.echo("Test data loaded.")

if __name__ == '__main__':
    cli()