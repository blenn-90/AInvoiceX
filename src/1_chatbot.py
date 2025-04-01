import streamlit as st

import chroma_db_func.retriver as retriver  

with st.sidebar:
    add_radio = st.radio(
        "Time frame over which data is analyzed",
        ("Current month", "Last Month")
    )

st.title("💬 Chatbot")
st.caption("An assistant chatbot powered by OpenAI")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    rag_chain = retriver.retrive_data_from_selected_timeframe("4_2025")
    print(rag_chain)
    result = rag_chain.invoke({"input": prompt, "chat_history": st.session_state.chat_history})
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = result['answer']
    st.session_state.chat_history.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)