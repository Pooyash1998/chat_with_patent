from typing import Union, List
import os, requests
import shutil
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PatentDownloader:
    
    def __init__(self):
        self.patent_url = "https://patents.google.com/patent/{}"
        self.download_path = "patents"
        os.makedirs(self.download_path, exist_ok=True)
        self.patent_number = None
  
        self.driver = self._get_driver()

    def _check_browser_binary(self) -> bool:
        """ detect Chrome or Chromium binary"""
        for binary in ["google-chrome", "chromium", "chromium-browser"]:
            path = shutil.which(binary)
            if path:
                return True
        raise RuntimeError("Neither Google Chrome nor Chromium is installed!")
    def _get_driver(self):
        """Set up the WebDriver with the right binary location (Chrome/Chromium)"""
        if self._check_browser_binary() is True :
          options = Options()
          options.add_argument("--headless")
          options.add_argument("--no-sandbox")
          options.add_argument("--disable-dev-shm-usage")

          service = Service(ChromeDriverManager(
                chrome_type=ChromeType.CHROMIUM).install())
          driver = webdriver.Chrome(service=service, options=options)

          return driver
        else: return None

    def download(self, 
                 patent: Union[str, List[str]],
                 output_path: str = "./patents/",
                 waiting_time: int = 5):
      """
          Downloads a single patent or a list of patents from Google Patents.
      """
      if isinstance(patent, str):
            return self._download_single_patent(patent, output_path, waiting_time)
      elif isinstance(patent, list):
            return [self._download_single_patent(p, output_path, waiting_time) for p in patent]            
      _close(self)

    def _download_single_patent(self, patent_number: str, output_path: str, waiting_time: int):
        """
        Downloads a single patent PDF by searching on Google Patents.
        """
        print(f"Downloading patent: {patent_number}...")

        self.driver.get(self.patent_url.format(patent_number))

        try:
            Download_btn = WebDriverWait(self.driver, waiting_time).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[1]/div[2]/section/header/div/a'))
            )
            pdf_link = Download_btn.get_attribute("href")
            print(f"PDF link found: {pdf_link}")
            pdf_response = requests.get(pdf_link)
            pdf_response.raise_for_status()

            file_path = os.path.join(output_path, f"{patent_number}.pdf")
            with open(file_path, "wb") as pdf_file:
                pdf_file.write(pdf_response.content)

            print(f"Patent {patent_number} downloaded successfully: {file_path}")
            return file_path

        except Exception as e:
            print(f"Error downloading {patent_number}: {e}")
            return None

    def download_patents(self, patents):
        return [self.download(patent) for patent in patents]
    
    def _close(self):
        """Closes the WebDriver session."""
        self.driver.quit()

#"""
# test
if __name__ == "__main__":
    downloader = PatentDownloader()
    downloader.download("US20200140525A1")
#"""    