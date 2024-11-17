""" Importing the required libraries.
    I am using Google Gemini for developing this ChatBot,
    So you require a GoogleAI API key to make this code work! """

import google.generativeai as genai
import streamlit as st
import time
import os
from dotenv import load_dotenv

"""Create a .env and store your API key with the variable name API_KEY = "YOUR_API_KEY"
   Replace YOUR_API_KEY with the API key that you created! """

load_dotenv()

# Loading the API key and the system instructions required for the ChatBot
api_key = os.getenv("API_KEY")
sys_prompt = open("system_prompt.txt", 'r')

# Configuring Google Generative AI
genai.configure(api_key = api_key)

# Choosing and loading the model
model = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction=sys_prompt)

# Initialising streamlit environment
if "history" not in st.session_state:
    st.session_state.history = []

# Declaring functions to save the chat history and stream data as seen in ChatGPT
def format_history(history):
    formatted_history = []
    for entry in history:
        formatted_history.append(
            {
                "role": entry["role"],
                "parts": [{"text": entry["content"]}]
            }
        )
        return formatted_history

def get_response(message):
    formatted_history = format_history(st.session_state.history)
    chatbot = model.start_chat(history=formatted_history)
    response = chatbot.send_message(message)

    st.session_state.history.append({"role": "user", "content": message})
    st.session_state.history.append({"role": "model", "content": response.text})

    return response.text

def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

# Initialising the streamlit components
st.title("Milo - Your Coding Assistant")

st.chat_message("ai").write("""Hey Milo over here. I can review your Python script and look for potential bugs, 
                            hence provide a feedback over the same and give suggestions for fixing the bug!""")

for entry in st.session_state.history:
    if entry["role"] == "user":
        st.chat_message("human").write(entry["content"])
    else:
        st.chat_message("ai").write(entry["content"])

user_prompt = st.chat_input("Enter your Python script for review here...")

if user_prompt:
    st.chat_message("human").write(user_prompt)
    response = get_response(user_prompt)
    st.chat_message("ai").write(stream_data(response))