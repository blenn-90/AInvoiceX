import streamlit as st
import os
from uuid import uuid4
from pathlib import Path
import datetime


from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import chromadb
chromadb.api.client.SharedSystemClient.clear_system_cache()


#Define the directory containing the text files and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "..", "data")
persistent_directory = os.path.join(db_dir, "db", "chroma_db_with_metadata")

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

# create to handle different types of documents
def load_document(file_path):
    """Detects file type and loads it using the appropriate LangChain loader."""
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
    if not os.path.exists(db_dir):
        raise FileNotFoundError(
            f"The directory {db_dir} does not exist. Please check the path."
        )

    # Display information about the split documents
    print("\n--- Document Information ---")
    print(f"Number of document: {len(uploaded_files)}")
    print(f"New files uploaded. Starting the process to embeddings.")
    
    if len(uploaded_files) == 0:
        print(f"No new files uploaded. Please add the files.")
        return

    # Read the text content from each file and store it with metadata
    documents = []
    for book_file in uploaded_files:
        file_path = os.path.join(db_dir, book_file)
        docs = load_document(file_path).load()

        for doc in docs:
            print(f"Found file : {book_file}")
            # Add metadata to each document indicating its source

            doc.metadata = {"source": book_file, "type": Path(file_path).suffix.lower(), "date": datetime.datetime.now().strftime("%Y/%m/%d") }
            documents.append(doc)

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Display information about the split documents
    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(docs)}")

    # Create embeddings
    print("\n--- Creating embeddings ---")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )  # Update to a valid embedding model if needed
    print(embeddings)
    print("\n--- Finished creating embeddings ---")
    # Check if the Chroma vector store already exists
    if not os.path.exists(persistent_directory):
        # Create the vector store and persist it
        print("\n--- Creating and persisting vector store ---")
        db = Chroma.from_documents(
            docs, embeddings, persist_directory=persistent_directory, collection_name="local-rag")
        print(db)
        print("\n--- Finished creating and persisting vector store ---")
        return

    else:
        print("Vector store already exists. No need to initialize.")
        db = Chroma(persist_directory=persistent_directory, collection_name="local-rag", embedding_function=embeddings)
        db.add_documents(docs)
        print("\n--- Finished adding the documents to the vector store ---")
        return
            
chroma_db_func(uploaded_files_name_list)


