# Importing Libraries
import streamlit as st
import google.generativeai as genai
import pytesseract
from gtts import gTTS
from PIL import Image
import tempfile
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import base64

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\surya\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_AI_API_KEY") 
genai.configure(api_key=api_key)

# Defining system instructions
scene_understanding_instruction = """Analyze the content of the provided image and generate a thorough and vivid description of the scene. 
Your response should include all observable details such as objects, actions, surroundings, colors, and any relevant contextual information. 
The description should be clear, detailed, and structured to provide maximum insight for visually impaired individuals, ensuring no key aspect of the scene is omitted."""

text_to_speech_instruction = """You are a model designed to assist visually impaired individuals by processing text extracted from images via OCR. 
Your task is to analyze the input text, determine its context, and ensure it is well-structured and easy to understand. 
If the text consists of multiple sentences, punctuate them appropriately to enhance clarity. 
If the text lacks complete sentences, transform the content into coherent, grammatically correct sentences that accurately convey the intended meaning and context."""

# Setting up LangChain for text processing
chat_model = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-flash-latest")
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", text_to_speech_instruction),
    ("human", "{text_input}"),
])
output_parser = StrOutputParser()
chain = chat_prompt_template | chat_model | output_parser

# Function to extract text using Pytesseract
def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)
    return temp.name

# Streamlit app UI
st.set_page_config(page_title="Third-Eye AI", page_icon="🌟", layout="wide")

st.sidebar.title("Third-Eye AI Tasks")
task = st.sidebar.radio("Choose a Task", ["Scene Understanding", "Text-to-Speech Conversion"])

# Apply custom styles
st.markdown("""
    <style>
        .main { background-color: #f4f9fd; }
        .stButton>button { background-color: #FF5722; color: white; border-radius: 10px; }
        .stButton>button:hover { background-color: #FF3D00; color: #ffffee}
        .css-145kmo2 { background-color: #ffffff; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

if task == "Scene Understanding":
    st.title("🌟 Scene Understanding Powered by Third-Eye AI")
    st.write("Upload an image, and the AI will describe its scene in detail.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width =True)

        if st.button("Generate Scene Description"):
            try:
                model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", system_instruction=scene_understanding_instruction)
                response = model.generate_content([image, "Follow the system instruction"])
                st.subheader("AI-Generated Scene Description")
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")

elif task == "Text-to-Speech Conversion":
    st.title("🎙️ Text-to-Speech Conversion")
    st.write("Upload an image, and the AI will extract text, organize it, and read it aloud.")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        with st.spinner("Processing..."):
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.write(uploaded_file.read())
            image_path = temp.name

            text = extract_text(image_path)
            user_input = {"text_input": text}
            organised_text = chain.invoke(user_input)

            st.subheader("Organized Text")
            st.write(organised_text)

            if st.button("Convert to Speech"):
                audio_path = text_to_speech(organised_text)
                audio_html = f"""
                <audio controls style="width: 100%;">
                    <source src="data:audio/mp3;base64,{base64.b64encode(open(audio_path, "rb").read()).decode()}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
