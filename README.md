# Open AI Chatbot

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-navy?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/product)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)](https://scipy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)


This project is a tool for analysts to load pdf documents and get a summary using either Nougat or PyPdf library. The project can also answer default & custom question asked by the user using the GPT-3.5 Turbo model based on the extracted pdf files.

### Overview:

This application is designed to load PDF documents and automatically generate summaries using the two libraries Nougat & PyPdf, then answer questions about the extracted text using GPT-3.5 Turbo. The application is built using Streamlit and deployed on a Streamlit Cloud Platform. The project utilizes Fast API to get the extracted data from the pdf and send it back to streamlit.

### Pages and features:

**Main :** This page sets up a web interface for extracting text from PDF documents using two different libraries (PyPDF and Nougat), and it allows users to ask questions based on the extracted text and receive answers from the application which are obtained by using GPT -3.5 Turbo Model. It uses FastAPI to handle API endpoints and Streamlit for the user interface.

Documentation - https://codelabs-preview.appspot.com/?file_id=1dTgG3eOt01K-niwv8QjoJc1m-HczTReqxmTclldGFU8

# Project Tree
```
📦 
├─ .DS_Store
├─ .gitignore
├─ LICENSE
├─ README.md
├─ fastapi
│  └─ fast.py
├─ openai_notebooks
│  ├─ embeddings
│  │  ├─ data_1.csv
│  │  ├─ filtered_data.csv
│  │  ├─ new_data.csv
│  │  ├─ preprocessed_data.csv
│  │  ├─ processed_data.csv
│  │  └─ search.ipynb
│  ├─ summary.jsonl
│  ├─ summary1.csv
│  └─ test_creation.ipynb
├─ requirements.txt
└─ streamlit_app
   ├─ extracted_text.json
   ├─ main.py
   ├─ pdf_contents.txt
   ├─ requirements.txt
   ├─ summary.csv
   └─ webscrape.py
```

# Prerequisites

To run this project, you will need:

- Google Cloud Platform account
- Fast API
- OpenAI API key
- Streamlit
- .env file containing the OpenAI keys

# Installation

- Clone the repository.
- Install the required packages by running pip install -r requirements.txt.
- Pass the GCP and OpenAI keys as environment variables
- Create a new directory named streamlit in part_1 folder and a virtual environment named .streamlit.
- Activate the environment
- Run fast api server using the uvicorn command.
- Run the main file using streamlit command to start the streamlit app.

# Create virtual environments

### Install virtualenv if you haven't already
```
pip install virtualenv
```

### Create a virtual environment
```
virtualenv myenv
```

### Create python environment for the directory
```
python -m venv myenv
```

### Activate the virtual environment
```
source myenv/bin/activate
```

### Pip install requirements
```
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License.

