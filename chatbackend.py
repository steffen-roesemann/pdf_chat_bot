""" 
Die Klasse ChatBackend stellt die Verbindung zwischen den Eingaben und Ausgaben
im webbasierten Frontend und der ChatGPT-API von OpenAI her.
"""
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
load_dotenv()


class ChatBackend():
    """
    Die Klasse ChatBackend() stellt die Verbindung zwischen Fragen eines Benutzers oder
    einer Benutzerin und einem Vector Store und Antworten durch ein Large Language Model
    her.
    """

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=self.openai_api_key)
        #self.vector_store = FAISS.load_local(
        #    os.getenv("FAISS_LOCAL_VECTORSTORE"), self.embeddings)

    def chat(self, prompt: str, chat_history: list) -> ConversationalRetrievalChain:
        """
        Die Methode chat() nimmt einen Prompt und die Chat-Historie einer Konversation
        entgegen und befragt unter Einbeziehen eines Vector Stores ChatGPT zu Antworten 
        über das API von OpenAI.

        prompt: str
            Ein Prompt, der an den Vector Store und die ChatGPT API gesendet wird, um 
            eine Antwort zu erzeugen.

        chat_history: list
            Die Chat Historie einer Unterhaltung mit dem ChatBot aus dem Frontend der
            Anwendung. Sie beinhaltet vergangene Prompts des / der Benutzer/-in und 
            die darauf abgegebenen Antworten des Large Language Models.
        """
        vector_store = FAISS.load_local(os.getenv("FAISS_LOCAL_VECTORSTORE"), self.embeddings)
        chat = ChatOpenAI(verbose=True, temperature=0,
                          model_name=os.getenv("OPENAI_MODEL"))
        answer = ConversationalRetrievalChain.from_llm(
            llm=chat,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            return_source_documents=True)

        return answer({"question": prompt, "chat_history": chat_history})
