import json
import os
import datetime
import math

def group_files_by_month(list_of_json_files):
    """Assumes files are named with YYYY-MM-DD.json format."""
    # get all dates for convenience
    dates = [os.path.basename(os.path.splitext(f)[0]) for f in list_of_json_files]

    # Get all unique combinations of year/month
    year_months = {
        (datetime.date.fromisoformat(d).year, datetime.date.fromisoformat(d).month)
        for d in dates
    }

    # Create a list of lists, where each sub-list contains all JSON filepaths for a 
    # given year+month
    return [
        [
            f
            for f in list_of_json_files
            if datetime.date.fromisoformat(
                os.path.basename(os.path.splitext(f)[0])
            ).month
            == m
            and datetime.date.fromisoformat(
                os.path.basename(os.path.splitext(f)[0])
            ).year
            == y
        ]
        for y, m in year_months
    ]


def group_files_by_n_days(list_of_json_files, n_days):
    """Group list of filepaths into subgroups containing no more than n_days"""

    # Find number of groups to be used
    n_groups = math.ceil(len(list_of_json_files) / n_days)

    # Return list of lists containing filenames
    return [list_of_json_files[n * n_days : (n + 1) * n_days] for n in range(n_groups)]


def open_json_files_list(list_of_json_files):
    """Read each JSON file from list of filepaths into a dict"""
    list_of_json = []
    for f in list_of_json_files:
        with open(f, "r") as file:
            list_of_json.append(json.load(file))

    return list_of_json


def concatenate_json(list_of_json):
    """Combine all JSON/dict values into a single list
    
    assumes each JSON body is an array at the top-level
    """
    output_json = []
    for f in list_of_json:
        output_json.extend(f)

    return output_json