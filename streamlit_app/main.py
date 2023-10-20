import streamlit as st
import subprocess
import time
import requests
from io import BytesIO
from PyPDF2 import PdfReader
import base64
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv 

load_dotenv()

ip_address = os.getenv("IP_ADDRESS")

app=FastAPI()
generated_summary = ""
st.title("PDF Extraction App")

# Add a radio button to select the PDF processing library
pdf_library = st.radio("Select PDF processing library:", ["PyPDF", "Nougat"])
pdf_link = st.text_input("Enter the PDF link here:")


if pdf_library == "Nougat":
    ngrok_url = st.text_input('Enter the ngrok url here:')
    st.markdown("[Create your Local Tunnel here: ](https://colab.research.google.com/drive/1ahln8HZ9bMICruZy1esLK4iZKkagI-Z1#scrollTo=lTCb9OAOPDxA)")

    if st.button("Extract contents"):
        if pdf_link and ngrok_url:

            # Create an empty text element for progress updates
            progress_text = st.empty()

            # Simulate progress and update the progress text
            for percent_complete in range(101):
                progress_text.text(f"Generating summary progress {percent_complete}% complete.")
                if percent_complete == 100:
                    time.sleep(2)  # Wait for 2 seconds at 100% progress
                time.sleep(0.05)  # Simulate processing time

            # Display a loading message while generating the report
            progress_message = st.info("Generating the summary. Please wait...")
            # Remove the message
            progress_text.empty()

            response = requests.post('http://127.0.0.1:8000/extract-nougat-text?pdf_link={}&ngrok_url={}'.format(pdf_link, ngrok_url))
            if response.status_code == 200:
                data = response.json()
                extracted_text = data.get("text", "")

                if extracted_text:
                    st.subheader("Nougat Extraction:")
                    st.write(extracted_text)          
                    progress_message.empty()
                else:
                    st.error("Failed to analyze the PDF using Nougat API.")
        else:
            st.warning("Please enter both PDF URL and Ngrok URL.")


if pdf_library == "PyPDF":
    if st.button("Extract contents"):
        if pdf_link:
            # Create an empty text element for progress updates
            progress_text = st.empty()

            # Simulate progress and update the progress text
            for percent_complete in range(101):
                progress_text.text(f"Generating summary progress {percent_complete}% complete.")
                if percent_complete == 100:
                    time.sleep(2)  # Wait for 2 seconds at 100% progress
                time.sleep(0.05)  # Simulate processing time

            # Display a loading message while generating the report
            progress_message = st.info("Generating the summary. Please wait...")
            # Remove the message
            progress_text.empty()

            response = requests.post('http://127.0.0.1:8000/extract-pypdf-text?pdf_link={}'.format(pdf_link))
            if response.status_code == 200:
                data = response.json()
                extracted_text = data.get("text", "")

                if extracted_text:
                    st.subheader("PyPDF Extraction:")
                    st.write(extracted_text)
                    progress_message.empty()

                    # Saving extracted file to a .txt file
                    json_filename = "extracted_text.json"

                    # Step 2: Create a Python Dictionary
                    data = {
                        "pdf_content": extracted_text
                    }

                    # Step 3: Convert the Dictionary to JSON
                    json_data = json.dumps(data)

                    # Step 4: Save the JSON to a File
                    with open(json_filename, 'w') as f:
                        f.write(json_data)

                else:
                    st.error("No text extracted from the PDF.")
            else:
                st.error(f"Failed to make the request! Status Code: {response.status_code}")
        else:
            st.warning("Please enter a valid PDF link.")

st.markdown('---')
st.subheader("Ask Me")
user_question = st.text_input("Enter your question:")

if st.button("Ask Question"):
    if user_question:
        # Create a JSON object with the question
        file = "extracted_text.json"
        with open(file, 'r') as f:
            data = json.load(f)

        extracted_text = data.get('pdf_content', None)   
        question_data = {"question": user_question, "pdf_content": extracted_text}
        generated_summary = extracted_text 
        if generated_summary:
            st.subheader("Generated Summary:")
            st.write(generated_summary)
            
        # Send the question to the FastAPI endpoint
        response = requests.post('http://127.0.0.1:8000/ask-question', json=question_data)
        
        if response.status_code == 200:
            data = response.json()
            extracted_answer = data.get("answer", "")
            st.subheader("Answer:")
            st.write(extracted_answer)
        else:
            st.error("Failed to get an answer from the OpenAI API.")
    else:
        st.warning("Please enter a question before asking.")
