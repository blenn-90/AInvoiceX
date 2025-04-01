import streamlit as st
import os
from uuid import uuid4
from utility.chroma_db_func.embedder import chroma_db_func
import sys

import datetime
from datetime import datetime

import pandas as pd

import utility.time_func.time as time_func
 
current_folder_path_v1 = time_func.get_current_date_folder_path()

#Define the directory containing the text files and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "..", "data")
get_month_db_dir = os.path.join(db_dir, current_folder_path_v1)


st.title("📝 Add documents to the memory!")

uploaded_files = st.file_uploader(
    "Choose a file", accept_multiple_files=True
)

uploaded_files_name_list = []
for i in range(len(uploaded_files)):
    bytes_data = uploaded_files[i].read()  # read the content of the file in binary
    
    with open(os.path.join(get_month_db_dir, uploaded_files[i].name), "wb") as f:
        f.write(bytes_data)  # write this content elsewhere

        uploaded_files_name_list.append(uploaded_files[i].name)
            
chroma_db_func(uploaded_files_name_list)

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
    
# Streamlit UI
st.title("Uploaded files")

if os.path.exists(db_dir):
    subdir_dfs = list_files_in_subdirs(db_dir)

    if subdir_dfs:
        for subdir, df in subdir_dfs.items():
            # Convert it to a datetime object
            month_year = datetime.strptime(subdir, '%m_%Y')
            # Convert it to a textual month and year format
            textual_month_year = month_year.strftime('%B %Y')
            print(textual_month_year)  # Output: April 2025
            st.subheader(f"{textual_month_year}")  # Show subdirectory name
            st.dataframe(df)  # Display the corresponding DataFrame
    else:
        st.warning("No files found")
else:
    st.error(f"Directory '{db_dir}' not found!")