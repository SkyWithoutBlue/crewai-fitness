import os
import sys
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

models = [
    "gemini/gemini-flash-latest",
    "gemini/gemini-2.0-flash",
    "gemini/gemini-2.5-flash",
    "gemini/gemini-2.5-flash-lite",
    "gemini/gemini-3.1-flash-lite",
    "gemini/gemini-3.5-flash"
]

print("Testing models for 429 errors (plain text)...")
for model in models:
    try:
        llm = LLM(model=model, api_key=key)
        res = llm.call("Say hello in one word")
        # Strip any weird characters
        clean_res = str(res).encode('ascii', errors='ignore').decode('ascii')
        print(f"SUCCESS for {model}: {clean_res}")
    except Exception as e:
        err_msg = str(e).encode('ascii', errors='ignore').decode('ascii')
        print(f"ERROR for {model}: {err_msg[:120]}")
