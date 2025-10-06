📄 Scraping PDFs Data using Python & Selenium

This project demonstrates how to automate the process of downloading and extracting data from PDFs using Python with the help of Selenium and PDF parsing libraries.

🚀 Features

Automates web navigation with Selenium

Downloads PDFs from dynamic websites

Extracts text/data from PDFs using libraries like PyPDF2 or pdfminer

Saves extracted data into structured formats (CSV/JSON)

🛠️ Requirements

Make sure you have the following installed:

Python 3.8+

Google Chrome / Firefox

WebDriver (ChromeDriver/GeckoDriver)

📦 Installation

Clone the repository and install the dependencies:

git clone https://github.com/your-username/scraping-pdfs-selenium.git
cd scraping-pdfs-selenium
pip install -r requirements.txt

📚 Libraries Used

selenium – For browser automation

PyPDF2 / pdfminer.six – For PDF text extraction

requests – For handling direct PDF downloads

pandas – For saving structured data

▶️ Usage

Run the script to start scraping:

python scraper.py


Example flow:

Open target website with Selenium

Locate and download PDF files

Extract data from PDFs

Save results into CSV/JSON

📂 Output

Extracted data will be stored in:

output/data.csv

output/data.json
