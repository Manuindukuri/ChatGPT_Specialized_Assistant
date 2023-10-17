import streamlit as st
import subprocess
import time
import requests
from io import BytesIO
from PyPDF2 import PdfReader
import base64

# Function to extract text from a PDF using PyPDF2
def extract_text_pypdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def ngrok_nougat(pdf_url,ngrok_url):
    try:
        # Download the PDF file from the URL
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Create a file-like object from the response content
        file_data = response.content

        # Prepare the file for uploading
        files = {'file': ('uploaded_file.pdf', file_data, 'application/pdf')}

        # Replace with the ngrok URL provided by ngrok
        ng_url = ngrok_url 

        # Send the POST request to the Nougat API via ngrok
        response = requests.post(f'{ng_url}/predict/', files=files, timeout=300)

        # Check if the request to the Nougat API was successful (status code 200)
        if response.status_code == 200:
            # Get the response content (Markdown text)
            markdown_text = response.text
            return markdown_text
        else:
            return f"Failed to make the request! Status Code: {response.status_code}"

    except Exception as e:
        return f"An error occurred: {e}"
    
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

            # Call the conversion function and display the result for Nougat API              
            result = ngrok_nougat(pdf_link,ngrok_url)
            progress_message.empty()

            if result:
                st.subheader("Nougat Extration:")
                st.write(result)
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

            try:
                # Download the PDF file
                response = requests.get(pdf_link)
                pdf_content = response.content

                # Extract text using PyPDF2
                text = extract_text_pypdf(BytesIO(pdf_content))
                progress_message.empty()
                st.subheader("PyPdf Extraction:")
                st.write(text)  # Display the extracted text
                
                # Calculate and display the length of the PDF and summary
                st.subheader("Length of PDF:")
                st.write(len(pdf_content))
                st.subheader("Length of Summary:")
                st.write(len(text))

            except Exception as e:
                st.error(f"An error occurred: {e}")

        else:
            st.warning("Please enter a valid PDF link.")