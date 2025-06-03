import os
import shutil
from typing import List
from langchain_community.document_loaders import PyPDFLoader, UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import Config

class DocumentProcessor:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        Config.create_directories()
        
    def load_document(self, file_path: str) -> List:
        try:
            if file_path.lower().endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            else:
                loader = UnstructuredFileLoader(file_path)
            return loader.load()
        except Exception as e:
            raise Exception(f"Error loading document {file_path}: {str(e)}")
    
    def process_document(self, file_path: str) -> List:
        try:
            docs = self.load_document(file_path)
            chunks = self.text_splitter.split_documents(docs)
            
            if os.path.exists(Config.VECTOR_STORE_PATH):
                db = FAISS.load_local(
                    Config.VECTOR_STORE_PATH,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                db.add_documents(chunks)
            else:
                db = FAISS.from_documents(chunks, self.embeddings)
                
            db.save_local(Config.VECTOR_STORE_PATH)
            return chunks
        except Exception as e:
            raise Exception(f"Error processing document {file_path}: {str(e)}")
    
    def get_vector_store(self):
        if os.path.exists(Config.VECTOR_STORE_PATH):
            return FAISS.load_local(
                Config.VECTOR_STORE_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        return None
    
    @staticmethod
    def clear_data():
        try:
            if os.path.exists(Config.UPLOAD_FOLDER):
                shutil.rmtree(Config.UPLOAD_FOLDER)
            if os.path.exists(Config.VECTOR_STORE_PATH):
                os.remove(Config.VECTOR_STORE_PATH + ".index")
                os.remove(Config.VECTOR_STORE_PATH + ".pkl")
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False