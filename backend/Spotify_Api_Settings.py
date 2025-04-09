import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
env = os.path.abspath(os.path.join(current_dir, '..', '.env'))

load_dotenv(dotenv_path=env)

client_id = os.getenv("API_KEY")
client_secret = os.getenv("CLIENT_SECRET")
