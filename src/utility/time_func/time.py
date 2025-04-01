import datetime
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utility import constant

# Path to the external folder
external_path = os.path.abspath("..")  # Adjust the path accordingly
sys.path.append(external_path)

def get_current_date_folder_path():
    current_folder_path = datetime.now().strftime(constant.month_year_folder_pattern)
    return current_folder_path