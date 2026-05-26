import os
from dotenv import load_dotenv

load_dotenv()

TARGET_URL = os.getenv("TARGET_URL", "https://example.com")
OUTPUT_FILE = "data/output/scraped_data.csv"