import streamlit as st
import os

import utility.path_func.path as path_func
from utility.chroma_db_func.embedder import emails_to_vector
import utility.logger as logger
import pandas as pd
import sqlite3

logger.log_info("--- EMAILS PAGE")
#Define the directory containing the monthly data files
data_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
current_month_folder_path = os.path.join(data_directory, path_func.get_current_month_folder_path())

#Defining Streamlit objects
#Page Caption and ChatBot
st.caption("📝 Add email to the memory!")

# Create the SQL connection to pets_db as specified in your secrets file.

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()


# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
""")
conn.commit()

# Show data
st.subheader("Clienti")
query = "SELECT * FROM clients"
df = pd.read_sql(query, conn)
if not df.empty:
    st.dataframe(df) 
else:
    st.info("Nessun cliente trovato!")

@st.dialog("Aggingi")
def add():
    with st.form("add_client_form"):
        name = st.text_input("Nome")
        email = st.text_input("Email")

        submit_add_button = st.form_submit_button("Conferma")

        if submit_add_button and name:
            cursor.execute("INSERT INTO clients (name, email) VALUES (?, ?)", (name, email))
            conn.commit()

            emails_to_vector(name, email)

            st.rerun()

@st.dialog("Elimina")
def delete():
    with st.form("delete_client_form"):
        delete_id = st.number_input("Inserisci l'id del cliente che vuoi cancellare", min_value=1, step=1)
        submit_delete_button = st.form_submit_button("Conferma")
        
        if submit_delete_button and delete_id:
            cursor.execute("DELETE FROM clients WHERE id=?", (delete_id,))
            conn.commit()
            st.rerun()

if st.button("Aggiungi", key= 1, icon="➕"):
    add()
    
if st.button("Elimina", key= 2, icon="➖"):
    delete()