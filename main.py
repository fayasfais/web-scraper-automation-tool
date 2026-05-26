from scraper import WebScraper
from config import TARGET_URL

def main():
    scraper = WebScraper(TARGET_URL)
    scraper.run()

if __name__ == "__main__":
    main()