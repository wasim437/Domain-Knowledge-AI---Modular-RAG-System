import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.resolve()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL =    "llama-3.3-70b-versatile"
    
    # Document processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Vector store
    VECTOR_STORE_PATH = str(BASE_DIR / "data/vector_store")
    UPLOAD_FOLDER = str(BASE_DIR / "data/uploads")
    
    # System prompts
    SUMMARIZATION_PROMPT = """Please provide a concise summary of the following document. 
    Focus on key points, findings, and conclusions. Keep it under 300 words.
    
    Document: {text}
    
    Summary:"""
    
    QA_PROMPT = """Answer the question based only on the following context. 
    If you don't know the answer, say you don't know. Be precise and factual.
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    @classmethod
    def create_directories(cls):
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(cls.VECTOR_STORE_PATH), exist_ok=True)