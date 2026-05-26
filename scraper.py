import logging
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config import OUTPUT_FILE

# Configure logging
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class WebScraper:
    """Professional web scraper and automation utility."""

    def __init__(self, url):
        self.url = url

    def fetch_static_content(self):
        """Fetch static HTML content using requests."""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            logging.info("Successfully fetched static page content.")
            return response.text
        except requests.RequestException as error:
            logging.error(f"Error fetching static content: {error}")
            return None

    def parse_content(self, html):
        """Parse HTML using BeautifulSoup."""
        soup = BeautifulSoup(html, "html.parser")

        data = []

        for item in soup.find_all("a"):
            title = item.get_text(strip=True)
            link = item.get("href")

            if title and link:
                data.append({
                    "title": title,
                    "link": link
                })

        logging.info(f"Extracted {len(data)} records from page.")
        return data

    def automate_browser(self):
        """Use Selenium for browser automation."""
        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(self.url)

            page_title = driver.title
            logging.info(f"Selenium loaded page: {page_title}")

            elements = driver.find_elements(By.TAG_NAME, "a")
            logging.info(f"Selenium detected {len(elements)} links.")

        finally:
            driver.quit()

    def save_to_csv(self, data):
        """Save scraped data to CSV using Pandas."""
        df = pd.DataFrame(data)

        output_path = Path(OUTPUT_FILE)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)

        logging.info(f"Data saved to {OUTPUT_FILE}")
        print(f"Data saved successfully to {OUTPUT_FILE}")

    def run(self):
        """Run the full scraping workflow."""
        html = self.fetch_static_content()

        if not html:
            print("Failed to retrieve website content.")
            return

        parsed_data = self.parse_content(html)

        if parsed_data:
            self.save_to_csv(parsed_data)

        self.automate_browser()

        print("Web scraping and automation completed successfully.")