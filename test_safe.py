import os
import sys
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

# Safe log using simple ASCII
log_file = "model_test_results.txt"

with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"Testing Gemini Models. Key: {key[:10]}...\n\n")

    models_to_test = [
        "gemini/gemini-2.0-flash-lite",
        "gemini/gemini-2.5-flash",
        "gemini/gemini-flash-latest",
        "gemini/gemini-pro-latest",
        "gemini/gemini-1.5-flash",
    ]

    for model in models_to_test:
        f.write(f"Testing model: {model}\n")
        print(f"Testing model: {model}")
        try:
            llm = LLM(model=model, api_key=key)
            res = llm.call("Say hello")
            f.write(f"SUCCESS: {res}\n\n")
            print(f"SUCCESS: {res}")
        except Exception as e:
            f.write(f"ERROR: {str(e)}\n\n")
            print(f"ERROR: {str(e)[:100]}")

print("Done! Results written to model_test_results.txt")
