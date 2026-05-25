import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

models_to_test = [
    "gemini/gemini-2.0-flash-lite",
    "gemini/gemini-2.5-flash",
    "gemini/gemini-flash-latest",
    "gemini/gemini-pro-latest",
    "gemini/gemini-1.5-flash",
]

for model in models_to_test:
    print(f"\n[Тест] Проверка модели '{model}'...")
    try:
        llm = LLM(model=model, api_key=key)
        res = llm.call("Say hello in one word")
        print(f"👉 УСПЕХ для {model}: {res}")
    except Exception as e:
        print(f"❌ Ошибка для {model}: {str(e)[:300]}")
