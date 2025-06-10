# Chatbot Application - Takes prompt from user, gives response, then asks for another prompt, etc.
# It will remember previous chats/coversations and continue the conversation.
import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schemas import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(
    page_title="AI Chatbot",
    page_icon=":robot_face:",
    layout="centered"
)

st.title("AI Chatbot")
st.subheader("Built using LangChain, Streamlit, and GPT-4o-mini")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "conversation" not in st.session_state:
    