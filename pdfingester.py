"""PDFIngester class is for ingesting PDF files and saving the content to a local vector store."""
import os
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

class PDFIngester():
    """
    DOCSTRING
    """

    def __init__(self):
        self.vector_store = os.getenv("FAISS_LOCAL_VECTORSTORE")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separator="\n")

    def get_text_from_pdf(self, pdf_docs: bytes) -> str:
        """
        Die Methode get_text_from_pdf() extrahiert aus PDF-Dokumenten die Textrohdaten, fügt
        sie aneinander und gibt sie als String zurück.

        pdf_docs: bytes
            Ein Byte-Array von PDF-Dokumenten (z.B. UploadedFiles des Streamlit file_uploader 
            Dialogs)
        """
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def get_text_chunks(self, text: str) -> list:
        """
        Die Methode get_text_chunks() dient dazu, einen Text-String in kleinere Einheiten
        zu zerlegen, damit diese Einheiten besser in ein Large Language Model (LLM) eingebettet
        und in einem Vector Store abgelegt werden können.

        text: str
            Der Text, der in kleinere Einheiten zerlegt werden soll.
        """
        textsplitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len)
        chunks = textsplitter.split_text(text)
        return chunks

    def embed_text_chunks_in_vectorstore(self, chunks: list) -> bool:
        """
        DOCSTRING
        """
        embedded = False
        embeddings = OpenAIEmbeddings(
            openai_api_key=self.openai_api_key, chunk_size=10)
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

        if os.path.exists(self.vector_store):
            local_vector_store = FAISS.load_local(
                self.vector_store, embeddings)
            local_vector_store.merge_from(vectorstore)
            local_vector_store.save_local(self.vector_store)
            embedded = True
        else:
            vectorstore.save_local(self.vector_store)
            embedded = True
        return embedded
