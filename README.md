AInvoiceX
📌 Project Overview
AInvoiceX is a demo application that uses AI-powered document retrieval to compare client requests with invoices. The system applies RAG (Retrieval-Augmented Generation) to extract relevant information from stored documents and provides insights using a local or cloud-based LLM.

🛠️ Technologies Used
Python – Core programming language

LangChain – Manages AI interactions and document retrieval

Streamlit – Web interface for interacting with the AI

OpenAI – Default LLM for processing text queries

ChromaDB – Vector database for embedding and retrieving documents

SQLite – Stores metadata and client details

🔍 How It Works
Document Upload & Embedding:

Users upload invoices and client request documents (PDF, TXT, etc.).

The system embeds the documents into a vector database (ChromaDB).

Retrieval-Augmented Generation (RAG):

When a query is made, the system retrieves relevant documents based on semantic similarity.

The extracted documents are passed to an LLM (OpenAI or a local model via Ollama) for processing.

AI Response & Comparison:

The AI analyzes the retrieved documents to verify if invoices match client requests.

Results are displayed in Streamlit with a clear comparison.

🚀 Installation & Setup

🔧 Build the Application
To install the dependencies, navigate to the folder containing pyproject.toml and run:

poetry install --no-root

▶ Run the Application
To launch the application, execute each .py file individually from the /src directory:

python src/main.py

⚠ Python Version Requirement
For dependency compatibility, it is recommended to use Python 3.11.8 to avoid issues.

📌 Future Enhancements
Integration with Gmail API to analyze client emails.

Support for additional LLMs (e.g., local Gemma via Ollama).

Advanced filtering (e.g., retrieving documents by date range).

