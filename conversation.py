from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from config import Config

class ConversationalAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.7,
            model_name=Config.GROQ_MODEL,
            api_key=Config.GROQ_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Be concise and helpful."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
            verbose=True
        )
        
    def chat(self, user_input):
        return self.conversation.invoke({"input": user_input})["text"]