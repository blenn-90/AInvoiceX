import streamlit as st

dashboard = st.Page("1_chatbot.py", title="Dashboard", icon=":material/dashboard:", default=True)
documents = st.Page("2_documents.py", title="Documents", icon=":material/description:")

pg = st.navigation([dashboard, documents])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()