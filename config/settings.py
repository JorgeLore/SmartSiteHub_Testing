# Initialize enviroment variables
from dotenv import load_dotenv
import os

load_dotenv()
class Settings:
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    SMART_SITE_POS = os.getenv("SMART_SITE_POS")

settings = Settings()