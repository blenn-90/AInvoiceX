import streamlit as st
import os
from uuid import uuid4
from  chroma_db_func.embedder import chroma_db_func

import datetime
from datetime import datetime
 
month = datetime.now().month
year = datetime.now().year
current_folder_path = str(month) + "_" + str(year)

#Define the directory containing the text files and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "..", "data", current_folder_path)
os.makedirs(db_dir, exist_ok=True)

st.title("📝 Add documents to the memory!")

uploaded_files = st.file_uploader(
    "Choose a file", accept_multiple_files=True
)

if len(uploaded_files) == 0:
    st.error("No file were uploaded")

uploaded_files_name_list = []
for i in range(len(uploaded_files)):
    bytes_data = uploaded_files[i].read()  # read the content of the file in binary
    
    with open(os.path.join(db_dir, uploaded_files[i].name), "wb") as f:
        f.write(bytes_data)  # write this content elsewhere

        uploaded_files_name_list.append(uploaded_files[i].name)
            
chroma_db_func(uploaded_files_name_list)


