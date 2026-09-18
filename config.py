import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BE_BASE_URL = os.getenv("BE_BASE_URL", "http://localhost:8000/api/v1")
    SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "")
    TAXONOMY_REFRESH_SECONDS = int(os.getenv("TAXONOMY_REFRESH_SECONDS", 86400))
    PORT = int(os.getenv("PORT", 8001))