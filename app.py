import os
from altair import themes
import openai
import streamlit as st

from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPEN_API_KEY")

def load_files():
    text= ""
    data_dir= os.path.join(os.getcwd(), "data")
    for filename in os.listdir(data_dir): 
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir, filename), "r") as f:
                text += f.read()
    return text

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    raw_text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content
    return raw_text

def get_response(text):
    prompt = f"""
        You are an expert in summarizing text. You will be given a text delimited by four backquotes, 
        Make sure to capture the main points, key arguments, and any supporting evidence presented in the articles.
        Your summary should be informative and well-structed, ideally consisitng of 3-5 sentences. Provide the Summary
        in the form of bullet points. Give a line break between each bullet points.

        text: ````{text}````
        """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
        ],
    )
    return response["choices"][0]["message"]["content"]


def main():
    # Apply theme settings using markdown
    st.markdown("""
        <style>
        [theme]
        base="dark"
        backgroundColor="#170e17"
        </style>
    """, unsafe_allow_html=True)

    #Header
   
    #Check if the user wants to write a text or upload pdf file
    option = st.radio("Select Input Type", ("Text", "PDF"))
    #Create area for the user to write the text
    if option == "Text":
        user_input = st.text_area("Enter Text", "")

        #Submit Button
        if st.button("Submit") and user_input != "":
            #call the get_response function to display the response
            response = get_response(user_input)
            #display the summary
            st.subheader("Summary")
            st.markdown(f">{response}")
        else:
            st.error("Please enter a text.")
    else:
        #create a file uploader for the user to upload the pdf file
        uploaded_file = st.file_uploader("Choose a PDF file", type = "pdf")

        #creating a submit button for pdf file
        if st.button("Submit") and uploaded_file is not None:
            #Extract text from a pdf file
            text = extract_text_from_pdf(uploaded_file)
            
            #calling the get_response function to display the response
            response = get_response(text=text)
            st.subheader("Summary")
            st.markdown(f">{response}")

        else:
            st.error("Please upload a PDF file.")

if __name__ == "__main__":
    main()