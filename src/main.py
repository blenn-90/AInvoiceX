import streamlit as st

import utility.constant as constant
import utility.logger as logger

logger.log_info("------ AINVOICEX IS STARTING ------")
logger.log_info("loading navigation bar")
#defining nagivation bar pages
dashboard = st.Page("1_chatbot.py", title="Dashboard", icon=":material/dashboard:", default=True)
documents = st.Page("2_documents.py", title="Documenti", icon=":material/description:")
emails = st.Page("3_emails.py", title="Emails", icon=":material/email:")
pg = st.navigation([dashboard, documents, emails])

#defining basic streamlit page config
logger.log_info("loading streamlit config")
st.set_page_config(page_title=constant.project_name, page_icon=":material/edit:")
st.title(constant.project_name)

pg.run()