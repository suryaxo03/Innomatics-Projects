# importing the libraries

import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

sys_prompt = open("system_prompt.txt", "r")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction=sys_prompt)

if "current_input" not in st.session_state:
    st.session_state.current_input = None

if "current_output" not in st.session_state:
    st.session_state.current_output = None

def get_response(script):
    chatbot = model.start_chat(history=[])
    response = chatbot.send_message(script)
    return response.text

st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom right, #4CAF50, #81C784);
        color: white; /* Optional: Change text color for better contrast */
    }
    .title {
        text-align: center;
        color: #ec2c76;
        font-size: 40px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #333;
        font-size: 18px;
        margin-bottom: 20px;
    }
    .input-box, .output-box {
        background-color: #f9f9f9;
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        font-size: 16px;
        color: #220d0d;
        font-family: monospace;
        white-space: pre-wrap;
        overflow-x: auto;
        margin-bottom: 20px;
    }
    .output-box {
        background-color: #f0fff4;
        border-color: #4CAF50;
        color: #333;
    }
    div[data-baseweb="radio"] > div {
        padding: 10px;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        background-color: #f9f9f9;
        margin-bottom: 10px;
        transition: background-color 0.3s, transform 0.3s;
    }
    div[data-baseweb="radio"] > div:hover {
        background-color: #e8f5e9;
        transform: scale(1.02);
    }
    div[data-baseweb="radio"] > div > input:checked + label {
        color: #ffffff;
        background-color: #4CAF50;
        padding: 5px 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Milo - Coding Assistant")
page = st.sidebar.radio("Navigate", ["Input", "Review"])

if page == "Input":
    st.markdown('<div class="title">Milo - Coding Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Enter your Python script below for review</div>', unsafe_allow_html=True)

    script = st.text_area("Your Python script:", "", placeholder="Paste your Python code here...", height=300)

    if st.button("Submit for Review"):
        if script.strip():
            st.session_state.current_input = script
            st.session_state.current_output = get_response(script)
            st.success("Your script has been submitted for review. Check the 'Review' tab for feedback!")
        else:
            st.warning("Please enter a Python script before submitting.")

elif page == "Review":
    st.markdown('<div class="title">Review Feedback</div>', unsafe_allow_html=True)

    if st.session_state.current_input and st.session_state.current_output:
        st.markdown(
            f'<div class="input-box"><b>User Script:</b><pre>{st.session_state.current_input}</pre></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="output-box"><b>Milo\'s Feedback:</b><pre>{st.session_state.current_output}</pre></div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No feedback to display. Submit your script in the 'Input' tab.")