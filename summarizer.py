from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config import Config

class Summarizer:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            model_name=Config.GROQ_MODEL,
            api_key=Config.GROQ_API_KEY
        )
        self.prompt = ChatPromptTemplate.from_template(Config.SUMMARIZATION_PROMPT)
        
    def summarize(self, text):
        chain = self.prompt | self.llm
        return chain.invoke({"text": text}).content