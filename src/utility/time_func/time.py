import datetime
from datetime import datetime

from utility import constant

def string_date_to_folder_path(text):
    textual = datetime.strptime(text, constant.month_year_textual_pattern)
    folder = textual.strftime(constant.month_year_folder_pattern)
    return folder

def folder_path_to_string_date(text):
    folder = datetime.strptime(text, constant.month_year_folder_pattern)
    textual = folder.strftime(constant.month_year_textual_pattern)
    return textual

