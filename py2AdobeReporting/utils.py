"""This module is for all support functions or utility functions"""
import time
import datetime
from datetime import datetime as dt
from datetime import timezone as tz
import random
import string
from itertools import chain
import os
import sys
import importlib.util
import pandas as pd
import pytz

def get_start_date(date_string):
    """For converting to a YYYY-MM-DD date from adobe timestamp"""
    ## date_string = 2019-12-01T00:00:00.000/2019-12-05T00:00:00.000
    start_date = date_string.rsplit('T', -1)
    start_date = start_date[0]
    return start_date

def get_end_date(date_string):
    """For converting to a YYYY-MM-DD date from adobe timestamp"""
    ## date_string = 2019-12-01T00:00:00.000/2019-12-05T00:00:00.000
    end_date = date_string.rsplit('/', 1)
    end_date = end_date[1]
    end_date = end_date.rsplit('T', -1)
    end_date = end_date[0]
    return end_date

def adobe_timestamp():
    """
    Generates an Adobe-compatible timestamp in ISO 8601 format
    with milliseconds precision and a 'Z' suffix for UTC.
    """
    utc = dt.now(tz.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def generate_tracing_id():
    """Generates a random 32-character alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def get_timezone_time(timezone):
    """Get the time for a requested timezone"""
    datetime_now = dt.now()
    zone = pytz.timezone(timezone)
    current_datetime = datetime_now.astimezone(zone)
    print("Current Datetime in " + timezone + ":", current_datetime)
    return current_datetime

def merge_dicts(dict1, dict2):
    """merge two dictionaries"""
    result = {}
    for key in dict1:
        if key in dict2:
            result[key] = dict1[key] + dict2[key]
    return result

## check execution time in ms
def execution_time(input_func):
    """This is for checking the execution time values without explicitedly spamming the API"""
    start = time.time()
    input_func
    end = time.time()
    exe_time = (end - start) * 10**3
    return exe_time
## convert ms to minutes
def minutes(ms_input):
    """Converting milliseconds to minutes"""
    minutes_value = ms_input / 60000
    return minutes_value

## check if a string is in a list
def check_if_a_string_in_list(input_list, string_to_search):
    """Check a list for a string value"""
    if string_to_search in input_list:
        print(string_to_search + " is present in list")
    else:
        print(string_to_search + " is not currently present in list.")

## Find a string input in a list's location to reference it
def return_index_of_string_in_list(input_list, string_to_search):
    """Find out where in a list a specific string is"""
    try:
        # check if string is present in list
        index = input_list.index(string_to_search)
        print(f'{string_to_search} is present in the list at index {index}')
    except ValueError:
        print(f'{string_to_search} is not present in the list')
    return index

## Remove a nested list from a list, example [[]]
def make_nested_list_a_list(list_input):
    """Change a nested list to just a regular list [[]] to []"""
    a = list(chain.from_iterable(list_input))
    return a

## Creates a dictionary with empty lists for column names created by a column names list
def dict_creation(column_names):
    """Create a dictionary of keys to be filled with values"""
    df_dict = {key: [] for key in column_names}
    return df_dict

## Create a variable list of the variables created for append into the dictionary based lists
def append_function_loop(df_dict, var_list, column_names):
    """Appending a list of lists by column name or key value"""
    i = 0
    while i < len(var_list):
        df_dict[column_names[i]].append(var_list[i])
        i += 1
    return df_dict

def search_dict_keys_for_a_string(search_key, dict_to_search):
    """Look through all dictionary keys for a key value"""
    result = [val for key, val in dict_to_search.items() if search_key in key]
    return result

def list_of_months(start_date, end_date):
    """Create a list of months in the YYYY-MM-DD format"""
    months = pd.date_range(start_date, end_date,
                          freq='MS').strftime("%Y-%m-%d").tolist()
    return months

def timestamp_to_date(input_timestamp):
    """Convert a timestamp to a YYYY-MM-DD format date
    timestamp is assumed to be in milliseconds, in UTC"""
    date = datetime.datetime.fromtimestamp(input_timestamp / 1000.0, tz=datetime.timezone.utc)
    date = date.strftime("%Y-%m-%d")
    return date

def timestamp_to_month(input_timestamp):
    """Convert a timestamp to a month value
    timestamp is assumed to be in milliseconds, in UTC"""
    date = datetime.datetime.fromtimestamp(input_timestamp / 1000.0, tz=datetime.timezone.utc)
    month = date.strftime("%m")
    return month

def timestamp_to_year(input_timestamp):
    """Convert a timestamp to a year value
    timestamp is assumed to be in milliseconds, in UTC"""
    date = datetime.datetime.fromtimestamp(input_timestamp / 1000.0, tz=datetime.timezone.utc)
    year = date.strftime("%Y")
    return year

def timestamp_to_year_month(input_timestamp):
    """Convert a timestamp to a YYYY-MM value
    timestamp is assumed to be in milliseconds, in UTC"""
    date = datetime.datetime.fromtimestamp(input_timestamp / 1000.0, tz=datetime.timezone.utc)
    year_month = date.strftime("%Y-%m")
    return year_month

def filter_dataset_by_string_value(column_name, column_value, df):
    """Filter a dataframe by a string value by checking in a column"""
    df_f = df[df[column_name].str.contains(column_value)]
    return df_f

def list_of_days(start_date, end_date):
    """Create a list of YYYY-MM-DD string values"""
    days = pd.date_range(start_date, end_date,
                        freq='D').strftime("%Y-%m-%d").tolist()
    return days

def day_date_delta(start_date, end_date):
    """Input two dates and get a delta value of the number of days"""
    date_format = "%Y-%m-%d"
    a = dt.strptime(start_date, date_format)
    b = dt.strptime(end_date, date_format)
    delta = b - a
    return delta.days

def check_all_paths():
    """Check the system path values"""
    for path in sys.path:
        print(path)

def create_directory_path(name_of_path):
## create a directory in your path
    """Create a path directory"""
    custom_directory = os.path.abspath(name_of_path)
    print(custom_directory)
    sys.path.insert(0, custom_directory)
    check_all_paths()

def check_module_path(module_name):
    """Check the py2Adobe module path"""
    module_name = 'py2Adobe'  # Replace with the module you're checking
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"Module {module_name} not found")
    else:
        print(f"Module {module_name} found at: {spec.origin}")


def remove_directory_from_path(dir_to_remove):
    # Check if the directory is in the path
    """Remove a directory from your system path"""
    if dir_to_remove in sys.path:
        sys.path.remove(dir_to_remove)
        print(sys.path)
    else:
        print("Not in path")


def list_of_integers_with_anomalies(low_bound, high_bound, total_periods, perc_anomaly):
    """For creating integer list with a specified amount of anomalous numbers"""
    # Generate a list of integers (e.g., generate total_periods between low_bound and high_bound)
    data = [random.randint(low_bound, high_bound) for x in range(total_periods)]
    # Calculate the number of anomalies in decimal format
    num_anomalies = int(len(data) * perc_anomaly)
    print(num_anomalies)
    # Introduce anomalies by modifying random positions in the list
    for x in range(num_anomalies):
        random_index = random.randint(0, len(data) - 1)
        data[random_index] = random.randint(low_bound, high_bound)  # Assign an anomalous value
    return data
