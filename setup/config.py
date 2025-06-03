import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER")
    MODEL_NAME: str = os.getenv("MODEL_NAME")