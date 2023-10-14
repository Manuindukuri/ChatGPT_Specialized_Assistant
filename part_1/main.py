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

def run_colab_notebook():
    # Replace 'YOUR_COLAB_NOTEBOOK_URL' with the actual Colab notebook URL
    colab_notebook_url = 'https://colab.research.google.com/drive/1m6HVtjNsZv_ru3n7ykfRDCmd73zhYAdA#scrollTo=JLXCdVCNULDm'

    link_text = "Click here to open the link in Google Colab"

    # Create a hyperlink using Markdown
    st.markdown(f"[{link_text}]({colab_notebook_url})")

st.title("PDF Analysis")

# Add a radio button to select the PDF processing library
pdf_library = st.radio("Select PDF processing library:", ["PyPDF2", "Nougat"])

# If "Nougat" is selected, hide the text box
if pdf_library == "Nougat":
    st.write("Nougat library selected. No need to enter a link here instead please press the button below")
else:
    # If "PyPDF2" or any other option is selected, show the text box
    pdf_link = st.text_input("Enter the link to the PDF file:")

if pdf_library == "Nougat":
    if st.button("Run Colab Notebook"):
        run_colab_notebook()
        st.success("Colab notebook execution triggered successfully.")

if pdf_library != "Nougat":
    if st.button("Generate Summary"):
        if pdf_link:
            # Create an empty text element for progress updates
            progress_text = st.empty()

            # Simulate progress and update the progress text
            for percent_complete in range(101):
                progress_text.text(f"Generating summary progress {percent_complete}% complete.")
                if percent_complete == 100:
                    time.sleep(2)  # Wait for 2 seconds at 100% progress
                time.sleep(0.1)  # Simulate processing time

            # Display a loading message while generating the report
            progress_message = st.info("Generating the summary. Please wait...")

            # Remove the "Pandas Profiling Report is 100% complete." message
            progress_text.empty()

            try:
                # Download the PDF file
                response = requests.get(pdf_link)
                pdf_content = response.content

                if pdf_library == "PyPDF2":
                    # Extract text using PyPDF2
                    text = extract_text_pypdf(BytesIO(pdf_content))
                    progress_message.empty()
                    st.subheader("Summary:")
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