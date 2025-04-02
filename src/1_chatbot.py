import streamlit as st
import os

import utility.chroma_db_func.retriver as retriver  
import utility.path_func.path as path_func
import utility.time_func.time as time_func
 
import utility.logger as logger

logger.log_info("--- CHATBOT PAGE")

#Define the directory containing the monthly data files
data_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
current_month_folder_path = os.path.join(data_directory, path_func.get_current_month_folder_path())

#Create the directory containing the monthly data files if it doesnt exist
os.makedirs(current_month_folder_path, exist_ok=True)

#Defining Streamlit objects
#Sidebar
with st.sidebar:
    radio_monthly = st.radio(
        "Time frame over which data is analyzed",
        path_func.list_subdirs(data_directory)
    )

#Page Title and ChatBot
st.caption("💬 An assistant chatbot")

#Session values
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "How can I help you?"}]
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

#User excute a query to the chatbot
if prompt := st.chat_input():
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    #invoke llm chain
    rag_chain = retriver.retrive_data_from_selected_timeframe(time_func.string_date_to_folder_path(radio_monthly))
    result = rag_chain.invoke({"input": prompt, "chat_history": st.session_state.chat_history})
    msg = result['answer']
    st.session_state.chat_history.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)