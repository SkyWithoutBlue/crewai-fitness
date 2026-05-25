import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

try:
    print("Listing models using google-genai client...")
    client = genai.Client(api_key=key)
    # Using the correct list method for the new SDK
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print("Error listing models:", e)
