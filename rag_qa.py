from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import Config

class RAGQA:
    def __init__(self, retriever):
        self.llm = ChatGroq(
            temperature=0,
            model_name=Config.GROQ_MODEL,
            api_key=Config.GROQ_API_KEY
        )
        self.retriever = retriever
        self.prompt = ChatPromptTemplate.from_template(Config.QA_PROMPT)
        
    def answer_question(self, question):
        chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        return chain.invoke(question)