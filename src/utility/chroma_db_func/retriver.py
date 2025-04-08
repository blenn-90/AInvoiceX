import os

from dotenv import load_dotenv
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


import utility.logger as logger

# Load environment variables from .env
load_dotenv()

# Define the persistent directory
def retrive_data_from_selected_timeframe(selected_timeframe):
    logger.log_info("generating llm answer")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persistent_directory = os.path.join(current_dir, "..", "..", "..","data", selected_timeframe, "chroma_db")
    
    # Define the embedding model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Load the existing vector store with the embedding function
    db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings, collection_name="local-rag")

    # Create a retriever for querying the vector store
    # `search_type` specifies the type of search (e.g., similarity)
    # `search_kwargs` contains additional arguments for the search (e.g., number of results to return)
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
        #filter={"type": "pdf", "date": {"$gte": one_month_ago.strftime("%Y-%m-%d")}}
    )

    # Create a ChatOpenAI model
    llm = ChatOpenAI(model="gpt-4o")
    #llama_url = "http://192.168.88.45:3000/"
    #llm = OllamaLLM(model="gemma3:12b", base_url=llama_url)
    

    # Contextualize question prompt
    # This system prompt helps the AI understand that it should reformulate the question
    # based on the chat history to make it a standalone question
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, just "
        "reformulate it if needed and otherwise return it as is."
    )

    # Create a prompt template for contextualizing questions
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # Create a history-aware retriever
    # This uses the LLM to help reformulate the question based on chat history
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # Answer question prompt
    # This system prompt helps the AI understand that it should provide concise answers
    # based on the retrieved context and indicates what to do if the answer is unknown
    qa_system_prompt = (
        "You are an assistant for question-answering tasks. Use "
        "the following pieces of retrieved context to answer the "
        "question. If you don't know the answer, just say that you "
        "don't know. Use three sentences maximum and keep the answer "
        "concise."
        "\n\n"
        "{context}"
    )

    # Create a prompt template for answering questions
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # Create a chain to combine documents for question answering
    # `create_stuff_documents_chain` feeds all retrieved context into the LLM
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Create a retrieval chain that combines the history-aware retriever and the question answering chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain