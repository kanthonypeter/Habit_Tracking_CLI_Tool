# Import HabitTracker Class
from user_habit import HabitTracker

# Initialize the Class
habit_tracker = HabitTracker()


# Create a create delete function. Perform operation based on user input from 'user_q1' variable
def create_delete():
    # Get user input into variable user_q1
    user_q1 = input('   Enter the name of a Habit you want to track: ')

    # Get user input and compare against string '1' and string '2'.
    # NB : Input received has the type string
    user_q2 = input(f'  Would you like to \n 1. Create {user_q1} \n 2. Delete {user_q1}\n ')
    if user_q2 == '1':
        habit_tracker.get_habit_type_from_user(user_q1)
    elif user_q2 == '2':
        habit_tracker.delete_activity(user_q1)
    else:
        print('Invalid Entry try again')


# Sort Menu function. Help user sort out habits based on tracking type.
# Options Currently available Daily & Weekly
def sort_menu():
    # Get User Input.
    # NB : Input received has the type string
    sort_user_q = input('\n\nSorted habits either by Daily / Weekly'
                        '\nEnter 1 for Daily'
                        '\nEnter 2 for Weekly\n')

    if sort_user_q == '1':
        tracking_type = 'daily'
        # Call the sort_by_type method from the class against the tracking type
        habit_tracker.sort_by_type(tracking_type)

    elif sort_user_q == '2':
        tracking_type = 'weekly'
        # Call the sort_by_type method from the class against the tracking type
        habit_tracker.sort_by_type(tracking_type)

    else:
        print('Please Enter a valid option 1 or 2: ')


# Analyze function. Perform analytical operation based on information available in database.
# Query read and perfrom calculations based on data available
def analyze():
    print('_______________________________________________________')
    print('Current Habits that can be analyzed..')
    habit_tracker.activities_to_analyze()

    print('################################################################')
    # Get User Input.
    # NB : Input received has the type string
    user_analyze_q = input('Select an Option'
                           '\n 1. Sort list of Daily/Weekly Habits & Current Habit Streak'
                           '\n 2. Historical Longest Streak of a Habit\n')

    if user_analyze_q == '1':
        print('Sort list of Daily/Weekly Habits & Current Habit Streak')
        sort_menu()

    elif user_analyze_q == '2':
        print('\nHistorical Longest Streak of a Habit\n')
        habit_tracker.historical_streak()

    else:
        print('Please select a valid option')


# Complete function. Mark Tasks as complete, open and write information to database.
def complete():
    # Using a list comprehension, loop through and store available user habits
    available_habits = [f'{name}' for name in habit_tracker.json_contents()]

    # Adding +1 to the index, to get the numbers to start from One instead of Zero
    # Print out the available User Habits using enumerate to help with pairing of index & habit name
    [print(f"{index + 1}. {name}") for index, name in enumerate(available_habits)]

    try:
        # Get user input based on information displayed
        user_complete_q = input('Enter the number associated with the habit to complete: ')

        # To get the user choice selected
        # Convert the user input into an integer and subtract 1 to get the actual index of the habit
        # If user enters a value that cannot be converted into an integer.
        # The try block fails and the except block takes effect.
        user_habit_choice = available_habits[int(user_complete_q) - 1]

        # Display the information back to the user for confirmation.
        # Get user input and covert it to lower case
        user_complete_answer = input(f'Would you like to mark {user_habit_choice} '
                                     f'as completed?: \n Answer Yes or No \n').lower()
        if user_complete_answer == 'yes':
            # write the activity to the database by calling the required method
            habit_tracker.complete_activity(user_habit_choice)
        else:
            print("Invalid Entry Detected - Select Yes or No\n")
    except ValueError:
        print("Invalid Entry Detected - Select a corresponding Habit Number\n")


# Options available to the user that can be called from the "user prompt" function
user_options = {
    '1': ['Create or Delete', create_delete],
    '2': ['Analyze', analyze],
    '3': ['Complete', complete]
}


# User_Prompt functions that runs a true while loop until a false (exit) command is entered
def user_prompt():
    app_on = True

    while app_on:
        print('\n*************************************')
        # Get user input.
        # Input type received is str.

        get_user = input(
            'What would you like to do today: '
            '\n Available Options '
            '\n Enter 1 or 2 or 3 or exit '
            '\n   1.Create/Delete '
            '\n   2.Analyze '
            '\n   3.Complete \n')
        print('*************************************\n')

        # If the "text" entered by the user is present in the options listed
        # Select the option and run the function associated
        if get_user in user_options:
            user_options[get_user][1]()

        # Else If option entered is "exit" set the app_on from True to False and Close the program
        elif get_user == 'exit':
            app_on = False
            print('Exiting....')

        # No match found based on user input prompt the user to try again
        else:
            print('Invalid Option entered try again')
