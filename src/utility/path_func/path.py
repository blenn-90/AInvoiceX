import datetime
from datetime import datetime
import pandas as pd

from utility import constant

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Path to the external folder
external_path = os.path.abspath("..")  # Adjust the path accordingly
sys.path.append(external_path)

def get_current_month_folder_path():
    current_folder_path = datetime.now().strftime(constant.month_year_folder_pattern)
    return current_folder_path

def list_subdirs(directory):
    subdir_data = []
    # Get all subdirectories (only first-level)
    subdirs = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    for subdir in subdirs:
        # Convert it to a datetime object
        month_year = datetime.strptime(os.path.basename(subdir), constant.month_year_folder_pattern)

        # Convert it to a textual month and year format
        textual_month_year = month_year.strftime(constant.month_year_textual_pattern)
        subdir_data.append(textual_month_year)

    return subdir_data

# Function to list only files (not subdirectories)
def list_files_in_subdirs(directory):
    subdir_data = {}
    # Get all subdirectories (only first-level)
    subdirs = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
    for subdir in subdirs:
        files = [f for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))]
        
        # If there are files in the subdir, add them to the list
        if files:
            file_list = []
            for file in files:
               
                file_path = os.path.join(subdir, file)
                file_size = os.path.getsize(file_path)  # Get file size in bytes
                file_list.append({"File Name": file, "Size (KB)": round(file_size / 1024, 2)})

            subdir_data[os.path.basename(subdir)] = pd.DataFrame(file_list)  # Store DataFrame with subdir name
    return subdir_data
    