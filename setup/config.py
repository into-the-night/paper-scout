import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")