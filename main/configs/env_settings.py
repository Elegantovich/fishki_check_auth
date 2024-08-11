import os

from dotenv import load_dotenv

load_dotenv()


ENV = os.getenv("ENVIROMENT") if os.getenv("ENVIROMENT") else "PROD"
