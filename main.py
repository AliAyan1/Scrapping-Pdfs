from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import PyPDF2
import time
import os
import re

class SimplePDFExtractor:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        
        download_folder = os.path.abspath("downloads")
        os.makedirs(download_folder, exist_ok=True)
        
        prefs = {
            "download.default_directory": download_folder,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True
        }
        options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.download_folder = download_folder
    
    def download_pdf(self, drive_url):
        try:
            print("Opening Google Drive link...")
            self.driver.get(drive_url)
            time.sleep(3)
            
            download_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Download']")
            download_button.click()
            print("Download started")
            
            time.sleep(5)
            
            files = os.listdir(self.download_folder)
            pdf_files = [f for f in files if f.endswith('.pdf')]
            
            if pdf_files:
                latest_file = max([os.path.join(self.download_folder, f) for f in pdf_files], 
                                key=os.path.getctime)
                print(f"Downloaded: {os.path.basename(latest_file)}")
                return latest_file
            else:
                print("No PDF found")
                return None
                
        except Exception as e:
            print(f"Download error: {e}")
            return None
    
    def extract_text(self, pdf_path):
        try:
            print("Reading PDF...")
            
            with open(pdf_path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                
                all_text = ""
                for page in pdf.pages:
                    all_text += page.extract_text() + "\n"
                
                print(f"Extracted text from {len(pdf.pages)} pages")
                return all_text.strip()
                
        except Exception as e:
            print(f"Text extraction error: {e}")
            return None
    
    def find_emails(self, text):
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        print(f"Found {len(emails)} emails")
        return emails
    
    def find_phones(self, text):
        phones = re.findall(r'\b\d{3}-\d{3}-\d{4}\b|\(\d{3}\)\s*\d{3}-\d{4}', text)
        print(f"Found {len(phones)} phone numbers")
        return phones
    
    def close(self):
        self.driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    pdf_url = "https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing"
    
    extractor = SimplePDFExtractor()
    
    try:
        pdf_file = extractor.download_pdf(pdf_url)
        
        if pdf_file:
            text = extractor.extract_text(pdf_file)
            
            if text:
                emails = extractor.find_emails(text)
                phones = extractor.find_phones(text)
                
                with open("results.txt", "w", encoding="utf-8") as f:
                    f.write("EXTRACTED TEXT:\n")
                    f.write("=" * 50 + "\n")
                    f.write(text + "\n\n")
                    
                    f.write("EMAILS FOUND:\n")
                    f.write("-" * 20 + "\n")
                    for email in emails:
                        f.write(email + "\n")
                    
                    f.write("\nPHONE NUMBERS:\n")
                    f.write("-" * 20 + "\n")
                    for phone in phones:
                        f.write(phone + "\n")
                
                print("Results saved to results.txt")
                
                print(f"\nSUMMARY:")
                print(f"   Text length: {len(text)} characters")
                print(f"   Emails found: {len(emails)}")
                print(f"   Phones found: {len(phones)}")
    
    finally:
        extractor.close()