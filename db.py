import json


def read_json():
    """
    This reads the json database and returns the associated data.
    A try block is used should in case the database does not exist
    """
    try:
        # Open, load and return the data
        with open('database.json', 'r') as data_file:
            data = json.load(data_file)
            return data
    except FileNotFoundError:
        # If file does not exist return an error
        return 'Issue reading file'


def write_db(file_data):
    """
    Writes data back to the json database when called
    """
    with open('database.json', 'w+') as out_file:
        # write data to the json database and indent
        json.dump(file_data, out_file, indent=4)


def update_db(file_data, user_data):
    """
    Updates the data before passing it on to the write_db function
    """
    file_data.update(user_data)
    write_db(file_data)


def delete_entry(file_data, activity_name):
    """
    Based on the activity name entered search and deleted the associated record from the database
    """
    file_data.pop(activity_name)
    # Save the updated database
    write_db(file_data)


def create_habit(new_data):
    """
    Used to create new user habit.
    This saved the file into the database.
    Try and except and finally blocks are used to catch errors that may arise.
    """
    try:
        # Attempt to open the database file in read mode
        with open('database.json', 'r+') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # If file not found , open in reading and writing mode which creates a file if it does not exist
        with open('database.json', 'a+') as data_file:
            data = json.loads('{}')
    finally:
        # Finally update the database with the information
        update_db(data, new_data)
        read_json()
