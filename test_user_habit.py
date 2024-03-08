import unittest
from unittest.mock import patch, MagicMock, call
from user_habit import HabitTracker

class TestHabitTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = HabitTracker()

    @patch('user_habit.create_habit')
    def test_create_daily_activity(self, mock_create_habit):
        self.tracker.create_activity("Yoga", '1')
        mock_create_habit.assert_called_once_with({
            'Yoga': {
                'type': 'daily',
                'creation_date': self.tracker.date_today,
                'days_completed': []
            }
        })

    @patch('user_habit.create_habit')
    def test_create_weekly_activity(self, mock_create_habit):
        self.tracker.create_activity("Meal Prep", '2')
        mock_create_habit.assert_called_once_with({
            'Meal Prep': {
                'type': 'weekly',
                'creation_date': self.tracker.date_today,
                'days_completed': []
            }
        })

    @patch('user_habit.read_json')
    @patch('user_habit.write_db')
    def test_complete_daily_activity(self, mock_write_db, mock_read_json):
        mock_read_json.return_value = {"Yoga": {"type": "daily", "days_completed": []}}
        self.tracker.date_today = "2024-03-08"
        self.tracker.complete_activity("Yoga")
        mock_write_db.assert_called_once()

    @patch('user_habit.read_json')
    @patch('user_habit.write_db')
    def test_complete_weekly_activity(self, mock_write_db, mock_read_json):
        mock_read_json.return_value = {"Meal Prep": {"type": "weekly", "days_completed": []}}
        self.tracker.date_today = "2024-03-08"
        self.tracker.complete_activity("Meal Prep")
        mock_write_db.assert_called_once()

    @patch('user_habit.read_json')
    def test_sort_activities_by_type(self, mock_read_json):
        mock_read_json.return_value = {
            "Yoga": {"type": "daily", "days_completed": []},
            "Meal Prep": {"type": "weekly", "days_completed": []}
        }
        with patch('builtins.print') as mock_print:
            self.tracker.sort_by_type("daily")
            # Ensure the correct messages are printed
            mock_print.assert_any_call('Yoga currently has no data to analyze')

    @patch('user_habit.read_json')
    def test_historical_streak(self, mock_read_json):
        mock_read_json.return_value = {
            "Yoga": {"type": "daily", "creation_date": "2024-03-08", "days_completed": ["2024-01-01", "2024-01-02"]},
            "Meal Prep": {"type": "weekly", "creation_date": "2024-03-08", "days_completed": [
                ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06", "2024-01-07"]]}
        }
        with patch('builtins.print') as mock_print:
            self.tracker.historical_streak()
            mock_print.assert_any_call("Yoga has a historical streak of 2 days")
            mock_print.assert_any_call("Meal prep has a historical streak of 1 weeks")

    @patch('user_habit.read_json')
    @patch('user_habit.delete_entry')
    def test_delete_activity(self, mock_delete_entry, mock_read_json):
        mock_read_json.return_value = {"Yoga": {"type": "daily"}}
        self.tracker.delete_activity("Yoga")
        mock_delete_entry.assert_called_once()



if __name__ == '__main__':
    unittest.main(verbosity=1)