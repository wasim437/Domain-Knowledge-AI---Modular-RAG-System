# 🧠 Domain Knowledge AI - Modular RAG System

A modular AI system designed for domain-specific document ingestion, summarization, and Retrieval-Augmented Generation (RAG) based Q&A, wrapped in a professional Streamlit interface.

## 🚀 Features

- 📄 **Document Summarization**  
- ❓ **RAG-based Question Answering**  
- 💬 **Conversational Agent with Memory**  
- ⚙️ **Modular and Extensible Architecture**  
- 🌗 **Dark-themed Streamlit UI**

---

## 🧱 Modular Architecture

| Component              | Responsibility |
|------------------------|----------------|
| `document_processor.py` | Load, chunk, embed documents; manage FAISS vector store |
| `summarizer.py`         | Summarize raw text or documents using Llama 3 |
| `rag_qa.py`             | Perform Q&A via retrieval + generation |
| `conversation.py`       | Stateful chat interface with memory |
| `config.py`             | Centralized configuration and environment loading |
| `app.py`                | Streamlit UI with three functional tabs |

Each module is **independent**, allowing for easy integration, testing, or replacement.

---

## 🛠️ Tech Stack

- **LLM**: GROQ's LLaMA 3 70B via API
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2`
- **Vector Store**: FAISS (CPU-based)
- **Chunking**: Recursive character text splitter
- **UI Framework**: Streamlit
- **Configuration**: `python-dotenv`

---

## 📦 Setup Instructions

1. **Clone the repository**
   https://github.com/wasim437/-Domain-Knowledge-AI---Modular-RAG-Sy 


```bash  


## 🧪 Usage Guide

### 📤 Upload Documents
- **Supported formats**: PDF, DOCX, TXT, PPTX, MD  
- Documents are automatically chunked and embedded into a FAISS index.

### 🧾 Summarization
- Paste text or select a processed document.  
- Summarization is handled by LLaMA 3 with a customizable prompt.

### ❓ Q&A Interface
- Ask questions related to uploaded documents.  
- The system retrieves relevant chunks and synthesizes answers via the LLM.

### 💬 Conversational Agent
- Chat with memory retained across turns.  
- Ideal for multi-turn interactions with domain-specific content.

---

## 🌟 Key Advantages

| Feature             | Normal RAG | This Project         |
|---------------------|------------|----------------------|
| Architecture        | Monolithic | Modular              |
| Extensibility       | Low        | High                 |
| Summarization       | ❌         | ✅                    |
| Memory              | Stateless  | Stateful             |
| Config Management   | Hardcoded  | `.env` + centralized |
| Error Handling      | Basic      | Component-level      |

---

## 🔮 Future Enhancements

- [ ] More file format support  
- [ ] Cloud storage integration  
- [ ] Authentication & session management  
- [ ] Admin dashboard for analytics  
- [ ] Multi-modal input (images, tables)  
- [ ] Fine-tuning and adapter support  

---

## 📁 Project Structure

📦 domain-knowledge-ai
├── app.py # Streamlit UI
├── config.py # Central configuration
├── document_processor.py # File loader, chunker, vector store
├── summarizer.py # Summarization logic
├── rag_qa.py # Retrieval-Augmented QA
├── conversation.py # Conversational agent with memory
├── requirements.txt # Dependencies
├── .env.example # Example env file
└── README.md # You're here!

## 🙌 Acknowledgments

- [HuggingFace Transformers](https://huggingface.co)
- [FAISS by Facebook AI](https://github.com/facebookresearch/faiss)
- [Streamlit](https://streamlit.io/)
- [GROQ](https://groq.com/)

---

## 🔗 GitHub Repository
https://github.com/wasim437/-Domain-Knowledge-AI---Modular-RAG-Sy




