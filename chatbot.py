from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import shelve

gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: hsla(280, 84%, 41%, 1);

    background: linear-gradient(90deg, hsla(280, 84%, 41%, 1) 0%, hsla(218, 97%, 56%, 1) 100%);

    background: -moz-linear-gradient(90deg, hsla(280, 84%, 41%, 1) 0%, hsla(218, 97%, 56%, 1) 100%);

    background: -webkit-linear-gradient(90deg, hsla(280, 84%, 41%, 1) 0%, hsla(218, 97%, 56%, 1) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div class="gradient-text">Chatbot</div>
"""

load_dotenv()
st.markdown(gradient_text_html, unsafe_allow_html=True)
st.caption("🚀 Chatbot Demo Using Streamlit and ChatGPT")

USER_AVATAR = "💬"
BOT_AVATAR = "🤖"

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chatbot_history") as db:
        return db.get("messages", [])


# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chatbot_history") as db:
        db["messages"] = messages
        
# Sidebar settings
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[More Detail About OpenAI](https://platform.openai.com/docs/)"
    "[![Github Pages](https://img.shields.io/badge/github%20pages-121013?style=for-the-badge&logo=github&logoColor=white)](https://github.com/zbatuhan/)"

#If you have gpt-4 then you make sure change "gpt-3.5-turbo" there to "GPT-4 Turbo"
#https://platform.openai.com/docs/models/
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# chat GUI
if prompt := st.chat_input("How can I help?"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state["messages"],
            stream=True,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)