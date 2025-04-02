import streamlit as st
import os

from utility.chroma_db_func.embedder import chroma_db_func
import utility.path_func.path as path_func
import utility.time_func.time as time_func
import utility.logger as logger

logger.log_info("--- DOCUMENTS PAGE")
#Define the directory containing the monthly data files
data_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
current_month_folder_path = os.path.join(data_directory, path_func.get_current_month_folder_path())

#Defining Streamlit objects
#Page Caption and ChatBot
st.caption("📝 Add documents to the memory!")

#Upload input
uploaded_files = st.file_uploader(
    "Choose a file", accept_multiple_files=True
)

uploaded_files_name_list = []
for i in range(len(uploaded_files)):
    bytes_data = uploaded_files[i].read()  # read the content of the file in binary
    
    with open(os.path.join(current_month_folder_path, uploaded_files[i].name), "wb") as f:
        f.write(bytes_data)  # write this content elsewhere

        uploaded_files_name_list.append(uploaded_files[i].name)
            
chroma_db_func(uploaded_files_name_list)

#Uploaded file in the system
st.title("Uploaded files")
#list of all the files grouped by month
if os.path.exists(data_directory):
    subdir_dfs = path_func.list_files_in_subdirs(data_directory)

    if subdir_dfs:
        for subdir, df in subdir_dfs.items():
            st.subheader(f"{time_func.folder_path_to_string_date(subdir)}") 
            st.dataframe(df)  
    else:
        st.warning("No files found")
else:
    st.error(f"Directory '{data_directory}' not found!")