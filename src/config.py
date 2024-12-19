from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 21600))  # 6 hours default
    LOCATIONS = os.getenv('LOCATIONS', 'Remote,New York NY,San Francisco CA').split(',')