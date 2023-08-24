"""HTML Templates zum Styling des Streamlit ChatBot-Frontends."""
import os
from dotenv import load_dotenv
load_dotenv()

CSS = '''<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''
BOT_TEMPLATE = ('<div class="chat-message bot">'
                '<div class="avatar">'
                f'<img src="{os.getenv("APPLICATION_BOT_AVATAR")}" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">'
                '</div>'
                '<div class="message">{{MSG}}</div>'
                '</div>'
                )

USER_TEMPLATE = ('<div class="chat-message user">'
                 '<div class="avatar">'
                 f'<img src="{os.getenv("APPLICATION_USER_AVATAR")}">'
                 '</div>'
                 '<div class="message">{{MSG}}</div>'
                 '</div>'
                 )
