# importing necessary libraries
import streamlit as st
import google.generativeai as gemini
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

sys_prompt = open("system_instruction.txt", 'r')
# Configuring the generative ai model
gemini.configure(api_key = api_key)
model = gemini.GenerativeModel(model_name="gemini-1.5-flash-latest", system_instruction=sys_prompt)

# Initialize session state for history if it doesn't exist
if "history" not in st.session_state:
    st.session_state.history = []

# declaring required functions
def format_history_for_model(history):
    """Format history entries to match the model's expected structure."""
    formatted_history = []
    for entry in history:
        formatted_history.append({
            "role": entry["role"],
            "parts": [{"text": entry["content"]}]
        })
    return formatted_history

def get_response(message):
    # Format history for model and initialize chatbot
    formatted_history = format_history_for_model(st.session_state.history)
    chatbot = model.start_chat(history=formatted_history)
    response = chatbot.send_message(message)
    
    # Append user message and AI response to history
    st.session_state.history.append({"role": "user", "content": message})
    st.session_state.history.append({"role": "model", "content": response.text})

    return response.text

def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

# building the streamlit environment
st.title("Flash AI Assistant")

st.chat_message("assistant").write("Hey there mate, I'm Flash. Ask me anything of your wish...")

for entry in st.session_state.history:
    if entry["role"] == "user":
        st.chat_message("human").write(entry["content"])
    else:
        st.chat_message("ai").write(entry["content"])

user_prompt = st.chat_input("Flash at your assistance, ask me something...")

if user_prompt:
    st.chat_message("human").write(user_prompt)
    response = get_response(user_prompt)
    st.chat_message("ai").write(stream_data(response))

