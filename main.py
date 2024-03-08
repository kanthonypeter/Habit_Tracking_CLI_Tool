# Import User interaction actions
from user_cli import user_prompt

# Welcome Screen
print('\nWelcome To Habit Tracker')


# If main.py is run as in a cli then True
# Engage user_prompt() if True
if __name__ == '__main__':
    user_prompt()
