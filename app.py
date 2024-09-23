import os
from altair import themes
import streamlit as st
from PyPDF2 import PdfReader
from llama_index.llms.groq import Groq
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Fetch the Groq API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

# Check if the API key is available
if not api_key:
    logging.error("Groq API key not found in environment variables.")
    st.error("API key is missing! Please check your environment settings.")
    exit()

# Set up the Groq LLM using the fetched API key
llm = Groq(model="llama3-70b-8192", api_key=api_key)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    raw_text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content
    return raw_text

# Function to generate a summary using Groq LLM
def get_response(text):
    prompt = f"""
        You are an expert in summarizing text. You will be given a text delimited by four backquotes. 
        Make sure to capture the main points, key arguments, and any supporting evidence presented in the articles.
        Your summary should be informative and well-structured, ideally consisting of 3-5 sentences. Provide the summary
        in the form of bullet points. Give a line break between each bullet point.

        text: ````{text}````
        """
    
    try:
        response = llm.complete(prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Error during LLM call: {e}")
        return "An error occurred while processing your request."

# Main Streamlit app
def main():
    # Apply theme settings using markdown
    st.markdown("""
        <style>
        [theme]
        base="dark"
        backgroundColor="#170e17"
        </style>
    """, unsafe_allow_html=True)

  
   
    # Check if the user wants to input text or upload a PDF file
    option = st.radio("Select Input Type", ("Text", "PDF"))
    
    # Handle text input
    if option == "Text":
        user_input = st.text_area("Enter Text", "")

        # Submit button for text input
        if st.button("Submit") and user_input != "":
            response = get_response(user_input)  # Get the LLM response
            st.subheader("Summary")
            st.markdown(f">{response}")
        else:
            st.error("Please enter a text.")

    # Handle PDF input
    else:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        # Submit button for PDF input
        if st.button("Submit") and uploaded_file is not None:
            text = extract_text_from_pdf(uploaded_file)  # Extract text from PDF
            response = get_response(text=text)  # Get the LLM response
            st.subheader("Summary")
            st.markdown(f">{response}")
        else:
            st.error("Please upload a PDF file.")

if __name__ == "__main__":
    main()
