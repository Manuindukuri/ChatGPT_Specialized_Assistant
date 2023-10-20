from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PyPDF2 import PdfReader
from io import BytesIO
import requests
import openai

app = FastAPI()

# Pydantic model for the response data
class TextResponse(BaseModel):
    text: str

class QuestionRequest(BaseModel):
    question: str
    pdf_content: str
    #extracted_text: str 

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

@app.post("/extract-pypdf-text")
async def extract_pypdf_text(pdf_link:str):
    try:
        
        # Download the PDF file
        response = requests.get(pdf_link)
        pdf_content = response.content

        # Extract text using PyPDF
        text = extract_text_pypdf(BytesIO(pdf_content))
        return JSONResponse(content={"text": text})
    except Exception as e:
        print("Error:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/extract-nougat-text")
async def extract_nougat_text(pdf_link:str, ngrok_url:str):
    try:
        # Download the PDF file
        response = requests.get(pdf_link)
        pdf_content = response.content

        # Extract text using PyPDF
        result = ngrok_nougat(pdf_link, ngrok_url)
        return JSONResponse(content={"text": result})
    except Exception as e:
        print("Error:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/ask-question")
async def ask_question(request: QuestionRequest):
    try:
        # Get the question from the request
        # extracted_text = request.extracted_text

        # Send the question to the OpenAI API (you'll need to configure your OpenAI API key)
        openai.api_key = "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"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Content: {request.pdf_content}\nQuestion: {request.question}\nAnswer:",
            max_tokens=100
        )
        print("Before generating answer")
        # Extract and return the answer
        answer = response.choices[0].text
        print("After generating answer")
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
