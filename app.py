# Chatbot Application - Takes prompt from user, gives response, then asks for another prompt, etc.
# It will remember previous chats/coversations and continue the conversation.
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

# setup streamlit page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon=":robot_face:",
    layout="centered"
)

# this displays chatbot title & subtitle
st.title("AI Chatbot")
st.subheader("Built using LangChain, Streamlit, and GPT-4o-mini")

# initialize chat history & conversation chain if DNE
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "conversation" not in st.session_state:
    # set up language model and conversation chain
    llm = ChatOpenAI(
        model_name = "gpt-4o-mini-2024-07-18",
        temperature = 0.5,
        openai_api_key = st.secrets["OPENAI_API_KEY"]
    )

    memory = ConversationBufferMemory(return_messages=True)

    # create CoversationChain with language model and memory
    st.session_state.conversation = ConversationChain(
        llm = llm,
        memory = memory,
        verbose = False
    )

# display chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"): # display user message
            st.write(message.content)

    else: 
        # display assistant message
        with st.chat_message("assistant"):
            st.write(message.content)

user_input = st.chat_input("How can I help you today?")

if user_input:

    # this adds user inpiut to chat history
    st.session_state.chat_history.append(HumanMessage(content = user_input))

    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        response = st.session_state.conversation.predict(input = user_input)
        st.write(response)

    st.session_state.chat_history.append(AIMessage(content = response))

with st.sidebar:
    st.title("Options")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
    
        memory = ConversationBufferMemory(return_messages=True)

        llm = ChatOpenAI(
            model_name = "gpt-4o-mini-2024-07-18",
            temperature = 0.5,
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        )

        st.session_state.conversation = ConversationChain(
            llm = llm,
            memory = memory,
            verbose = False
        )

        st.rerun()
    
    st.subheader("About")

    st.markdown(
        """
        An **AI chatbot** that remembers previous conversations 
        
        Built using: 
        
        - **LangChain** for web interface
        - **Streamlit** for conversation management
        - **GPT-4o-mini** as the language model
        - **Conversation Buffer Memory** to keep track of previous conversations
        """
    )