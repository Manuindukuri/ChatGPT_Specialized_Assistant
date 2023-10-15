import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import PyPDF2
import io

# Define the URL of the website you want to scrape
url = "https://www.sec.gov/forms"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the links on the page
    links = soup.find_all("a")

    # Specify the base URL for relative URL resolution
    base_url = "https://www.sec.gov"

    # Iterate through the links and filter the first 20 that end with "(PDF)"
    pdf_links = []
    for link in links:
        if link.get("href") and link.get_text().strip().endswith("(PDF)"):
            pdf_url = urljoin(base_url, link.get("href"))
            link_text = link.get_text().strip()
            pdf_links.append((link_text, pdf_url))

    # Create a text file to save the content
    with open("pdf_contents.txt", "w", encoding="utf-8") as text_file:

        # Process the first 20 PDF links
        for i, (link_text, pdf_url) in enumerate(pdf_links[:20], start=1):
            print(f"Processing PDF {i}/{len(pdf_links)}: {link_text}")

            # Send an HTTP GET request to the PDF URL
            pdf_response = requests.get(pdf_url)

            if pdf_response.status_code == 200:
                # Parse the PDF content using PyPDF2
                pdf_content = pdf_response.content
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))

                # Extract the text from the PDF
                pdf_text = ""
                for page_num in range(len(pdf_reader.pages)):
                    pdf_text += pdf_reader.pages[page_num].extract_text()

                # Write the heading and extracted content to the text file
                with open("pdf_contents.txt", "a", encoding="utf-8") as text_file:
                    text_file.write(f'Heading: {link_text[:-6]}\n')  # Remove the "(PDF)" from the heading
                    text_file.write(pdf_text + "\n\n")

            else:
                with open("pdf_contents.txt", "a", encoding="utf-8") as text_file:
                    text_file.write(f"Failed to retrieve the PDF. Status code: {pdf_response.status_code}\n")

        print("PDF contents have been saved to pdf_contents.txt")