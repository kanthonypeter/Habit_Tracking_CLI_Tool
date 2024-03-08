from datetime import datetime, timedelta
from db import create_habit, read_json, delete_entry, write_db


# Create the HabitTracker Class and initialize the dates
class HabitTracker:
    def __init__(self):
        self.date_format = '%Y-%m-%d'
        self.current_day = datetime.now()
        self.date_today = datetime.now().strftime(self.date_format)

    # From the imported "db" library call the "json_contents" to read files from the database
    @staticmethod
    def json_contents():
        return read_json()

    def current_week(self):
        # Current_monday gets the current day minus the numerical value obtained from timedelta function
        # This gives us the first Monday of the week from the target date
        current_monday = self.current_day - timedelta(self.current_day.weekday())
        # Use the Current Monday to then generate a week list by adding 7 days from the start of the week
        week_list = [datetime.strftime(current_monday + timedelta(x), '%Y-%m-%d') for x in range(7)]
        return week_list

    def get_habit_type_from_user(self, name):
        habit_type = input("Would you like to track this habit on a \n 1. Daily basis \n 2. Weekly basis \n")
        self.create_activity(name, habit_type)

    def create_activity(self, name, habit_type):
        # Directly use habit_type parameter instead of asking for user input
        if habit_type == '1':
            # If habit_type is of value one set to daily
            habit_type = 'daily'
            # Create and save the data
            habit_data = {
                name: {
                    'type': habit_type,
                    'creation_date': self.date_today,
                    'days_completed': []
                }
            }
            self.save_habit(habit_data)
            print(f'Created {name} to be tracked on a {habit_type} basis')

        elif habit_type == '2':
            # If habit_type is of value two set to weekly
            habit_type = 'weekly'
            # Create and save the data
            habit_data = {
                name: {
                    'type': habit_type,
                    'creation_date': self.date_today,
                    'days_completed': []
                }
            }
            self.save_habit(habit_data)
            print(f'Created {name} to be tracked on a {habit_type} basis')

    @staticmethod
    def save_habit(habit_data):
        create_habit(habit_data)

    def delete_activity(self, name):
        # Read the database and remove activity based on input provided by user
        # Read current Database
        json_data = self.json_contents()
        if json_data:
            # If input presented is found in the database, delete the entry
            if name in json_data:
                delete_entry(json_data, name)
                print("Activity Deleted")
            # Else return activity not found
            else:
                print(f'{name} activity not found')

    def get_dates(self, name):
        # Retrieve dates from database based on activity name
        # Read current Database
        json_data = self.json_contents()
        if name in json_data:
            # Use try method to validate data is present to avoid error
            try:
                if json_data[name]['type'] == 'daily':
                    # Using a list comprehension convert the activity dates pulled from the json_data
                    # This then returns ordinals (easy to use numerical values to later use to determine streaks)
                    daily_user_dates = [datetime.strptime(date, self.date_format).toordinal() for date in
                                        json_data[name]['days_completed']]
                    return daily_user_dates

                elif json_data[name]['type'] == 'weekly':
                    # Using a list comprehension convert the activity dates pulled from the json_data
                    # Since this returns an array this then converts them into datetime ordinal
                    # for later use in streak calculation
                    weekly_user_dates = [datetime.toordinal(datetime.strptime(val, self.date_format)) for date in
                                         json_data[name]['days_completed'] for val in date]
                    return weekly_user_dates

            except IndexError:
                return "No dates available for this completed activity"
        else:
            return f"Activity {name} not found"

    def activities_to_analyze(self):
        # Analysing the date available to give the user informational updates when requested
        # Read database contents
        json_data = self.json_contents()
        for habit_name in json_data:
            # Get and return the habit names from the database. Providing the user with available habits being tracked
            print(f"{habit_name.capitalize()} is a {json_data[habit_name]['type']} activity")
        print('_______________________________________________________\n')

    def split_dates(self, name):
        """
           Based on the name of the activity, it splits a list of dates into groups of consecutive dates.
            And then returns a list of each group of dates if the separation is greater than 1.
            """
        data = self.get_dates(name)
        if isinstance(data, list):
            group_dates = [[data[0]]]
            for i, new_dates in enumerate(data[1:]):
                last_list_item = group_dates[-1][-1]
                if new_dates - last_list_item > 1:
                    # If difference between current date and last date is greater than 1 add to new list
                    group_dates.append([new_dates])
                else:
                    # Else add to the end of list
                    group_dates[-1].append(new_dates)
            return group_dates

    def habit_current_streak(self, name):
        current_streak = 0
        json_data = self.json_contents()
        dates_data = self.split_dates(name)
        if json_data[name]['type'] == 'daily':
            # Set current streak to the length of the last dates.
            current_streak = len(dates_data[-1])
            return current_streak

        elif json_data[name]['type'] == 'weekly':
            # Calculate the weekly streak by dividing the length of the last dates and divide by 7.
            current_streak = len(dates_data[-1]) // 7
            return current_streak

    def historical_streak(self):
        # Load the json data
        json_data = self.json_contents()
        highest_daily_historical_streak = 0
        highest_weekly_historical_streak = 0
        for habit_name in json_data:
            # Split the dates associated with each habit
            dates_data = self.split_dates(habit_name)
            # Check if the habit type is daily
            if json_data[habit_name]['type'] == 'daily':
                # Find the highest number of consecutive days
                highest_daily_historical_streak = max(dates_data, key=len)
                print(
                    f"{habit_name.capitalize()} has a historical streak of {len(highest_daily_historical_streak)} days")

            # Check if the habit type is weekly
            elif json_data[habit_name]['type'] == 'weekly':
                # Find the longest sequence of dates for weekly habits and update the highest streak
                highest_weekly_historical_streak = max(dates_data, key=len)
                # The highest streak is determined by dividing the length of the highest number by 7
                highest_weekly_historical_streak = len(highest_weekly_historical_streak) // 7
                print(f"{habit_name.capitalize()} has a historical streak of {highest_weekly_historical_streak} weeks")

    def sort_by_type(self, track_type):
        # Load json data
        json_data = self.json_contents()
        for habit_name in json_data:
            # Match habits to the tracking type
            if json_data[habit_name]["type"] == track_type:
                # Use a try statement and catch indexerrors where possible in instances where no streak is found
                try:
                    # Get the habit data and update the current streak count
                    streak_count = self.habit_current_streak(habit_name)
                    print('______________________________________________')
                    print(f'{habit_name.capitalize()} has a streak of {streak_count}')
                except IndexError:
                    # If habit has no streak data, indicate no data available
                    print(f"{habit_name.capitalize()} currently has no data to analyze")

    def complete_activity(self, name):
        # Load json content
        json_data = self.json_contents()
        # If habit name is prent in json data match the habit type
        if name in json_data:
            if json_data[name]['type'] == 'daily':
                # If today's date is not present in "days completed" add today's date to the list
                if self.date_today not in json_data[name]['days_completed']:
                    json_data[name]['days_completed'].append(self.date_today)
                    # Save the data
                    write_db(json_data)
                    print(f'Daily activity {name.capitalize()} completed for the day.\n')
                else:
                    # If today's date is already present indicate activity already completed
                    print(f"\n{name.capitalize()} already completed today\n")

            elif json_data[name]['type'] == "weekly":
                # If the current week is not present in the "days_completed" weekly list append the current week
                if self.date_today not in json_data[name]['days_completed']:
                    json_data[name]['days_completed'].append(self.current_week())
                    # Save the data
                    write_db(json_data)
                    print(f'Weekly activity {name.capitalize()} completed for the week.\n')
                else:
                    # if week already exists indicated activity completed for the week
                    print(f"\n{name.capitalize()} already completed this week\n")
        else:
            # If activity name entered does not exist in database return activity not found
            print('{name} not found')
