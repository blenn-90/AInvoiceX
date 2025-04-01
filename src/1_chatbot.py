import streamlit as st
import os
import utility.chroma_db_func.retriver as retriver  
import datetime
from datetime import datetime
import utility.time_func.time as time_func
 
current_folder_path_v1 = time_func.get_current_date_folder_path()

#Define the directory containing the text files and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "..", "data")
get_month_db_dir = os.path.join(db_dir, current_folder_path_v1)
os.makedirs(get_month_db_dir, exist_ok=True)

def list_subdirs(directory):
    subdir_data = []
    # Get all subdirectories (only first-level)
    subdirs = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    for subdir in subdirs:
        # Convert it to a datetime object
        month_year = datetime.strptime(os.path.basename(subdir), '%m_%Y')

        # Convert it to a textual month and year format
        textual_month_year = month_year.strftime('%B %Y')
        subdir_data.append(textual_month_year)

    return subdir_data


with st.sidebar:
    add_radio = st.radio(
        "Time frame over which data is analyzed",
        list_subdirs(db_dir)
    )

st.title("💬 Chatbot")
st.caption("An assistant chatbot")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # Convert it to a datetime object
    month_year = datetime.strptime(add_radio,'%B %Y')
    textual_month_year = month_year.strftime('%m_%Y')
    rag_chain = retriver.retrive_data_from_selected_timeframe(textual_month_year)
    result = rag_chain.invoke({"input": prompt, "chat_history": st.session_state.chat_history})
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = result['answer']
    st.session_state.chat_history.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)