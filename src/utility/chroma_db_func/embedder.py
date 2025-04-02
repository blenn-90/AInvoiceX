from pathlib import Path
import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import utility.path_func.path as path_func
import utility.logger as logger

import chromadb
chromadb.api.client.SharedSystemClient.clear_system_cache()

#Define the directory containing the monthly data files
data_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data")
current_month_folder_path = os.path.join(data_directory, path_func.get_current_month_folder_path())
persistent_directory = os.path.join(current_month_folder_path, "chroma_db")

# create to handle different types of documents
def load_document(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(file_path)
    elif ext == ".txt":
        return TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
# create or add documents to chroma_db
def chroma_db_func(uploaded_files):
    # Ensure the books directory exists
    if not os.path.exists(current_month_folder_path):
        raise FileNotFoundError(
            f"The directory {current_month_folder_path} does not exist. Please check the path."
        )

    # Display information about the split documents
    logger.log_info("start checking for file to be added")
    logger.log_info(f"number of document: {len(uploaded_files)}")
    
    if len(uploaded_files) == 0:
        logger.log_info(f"No new files uploaded. Please add the files.")
        return

    # Read the text content from each file and store it with metadata
    documents = []
    for book_file in uploaded_files:
        file_path = os.path.join(current_month_folder_path, book_file)
        docs = load_document(file_path).load()

        for doc in docs:
            # Add metadata to each document indicating its source
            doc.metadata = {"source": book_file, "type": Path(file_path).suffix.lower()}
            documents.append(doc)

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Display information about the split documents
    logger.log_info("document chunks information")
    logger.log_info(f"Number of document chunks: {len(docs)}")

    # Create embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )  # Update to a valid embedding model if needed

    # Check if the Chroma vector store already exists
    if not os.path.exists(persistent_directory):
        # Create the vector store and persist it
        logger.log_info("creating and persisting vector store")
        db = Chroma.from_documents(
            docs, embeddings, persist_directory=persistent_directory, collection_name="local-rag")
        return

    else:
        logger.log_info("vector store already exists. No need to initialize.")
        db = Chroma(persist_directory=persistent_directory, collection_name="local-rag", embedding_function=embeddings)
        db.add_documents(docs)
        return