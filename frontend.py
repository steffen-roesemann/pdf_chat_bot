""" 
Die Klasse Frontend dient der Bereitstellung eines webbasierten Frontends 
für den Zugriff auf das Backend des Chat-Bots. 
"""
import os
from dotenv import load_dotenv
import streamlit
from chatbackend import ChatBackend
from pdfingester import PDFIngester
from htmltemplates import CSS, USER_TEMPLATE, BOT_TEMPLATE
load_dotenv()

class Frontend():
    """
    Die Klasse Frontend() dient der Bereitstellung eines webbasierten 
    Frontends mit streamlit.
    """
    def __init__(self):
        self.chatbackend = ChatBackend()
        self.pdfingester = PDFIngester()
        self.st = streamlit
        self.st.set_page_config(page_title=os.getenv("APPLICATION_HEADER"))
        self.st.write(CSS, unsafe_allow_html=True)

    def show_sidebar(self):
        """
        Die Methode show_sidebar() dient der Darstellung der Seitenleiste im
        webbasierten Frontend.
        """
        with self.st.sidebar:
            if not os.path.isdir(os.getenv("FAISS_LOCAL_VECTORSTORE")):
                self.st.error("Der lokale FAISS Vector Store ist noch leer. " +
                              "Befülle ihn mit Dokumenten, um den ChatBot mit Wissen anzureichern.", icon="⚠️")

            self.st.subheader(
                "Ergänze das Wissen des ChatBots mit weiteren PDF-Dokumenten:")
            pdf_docs = self.st.file_uploader(
                "Lade weitere PDF Dokumente hoch, die in den Vector Store eingebettet werden" +
                " sollen und klicke auf 'Verarbeiten'.", type="pdf", accept_multiple_files=True)
            if self.st.button("Verarbeiten"):
                with self.st.spinner("Verarbeite Dokumente"):
                    text = self.pdfingester.get_text_from_pdf(pdf_docs)
                    chunks = self.pdfingester.get_text_chunks(text)
                    EMBEDDED = self.pdfingester.embed_text_chunks_in_vectorstore(
                        chunks)
                    if EMBEDDED:
                        self.st.write(
                            "Die Dokumente wurde erfolgreich importiert.")
                    else:
                        self.st.write(
                            "Beim Importieren der Dokumente ist ein Fehler aufgetreten.")

    def show_main_window(self):
        """
        Die Methode show_main_window() dient der Darstellung des Hauptfensters im
        webbasierten Frontend.
        """
        self.st.header(os.getenv("APPLICATION_HEADER"))
        if os.path.isdir(os.getenv("FAISS_LOCAL_VECTORSTORE")):
            prompt = self.st.text_input(
                "Prompt:", placeholder="Prompt hier eingeben...", disabled=False)

            if "user_prompt_history" not in self.st.session_state:
                self.st.session_state["user_prompt_history"] = []

            if "chat_answers_history" not in self.st.session_state:
                self.st.session_state["chat_answers_history"] = []

            if "chat_history" not in self.st.session_state:
                self.st.session_state["chat_history"] = []

            if prompt:
                with self.st.spinner("Generiere Antwort..."):
                    generated_answer = self.chatbackend.chat(
                        prompt, chat_history=self.st.session_state["chat_history"])
                    formatted_response = f"{generated_answer['answer']}"

                    self.st.session_state["user_prompt_history"].append(prompt)
                    self.st.session_state["chat_answers_history"].append(
                        formatted_response)
                    self.st.session_state["chat_history"].append(
                        (prompt, generated_answer["answer"]))

            if self.st.session_state["chat_answers_history"]:
                for generated_answer, user_query in zip(self.st.session_state["chat_answers_history"],
                                                        self.st.session_state["user_prompt_history"]):
                    self.st.write(USER_TEMPLATE.replace(
                        "{{MSG}}", user_query), unsafe_allow_html=True)
                    self.st.write(BOT_TEMPLATE.replace(
                        "{{MSG}}", generated_answer), unsafe_allow_html=True)
        else:
            self.st.text_input(
                "Prompt:", placeholder="Prompt hier eingeben...", disabled=True)
