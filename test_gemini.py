import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print(f"API Key found (first 10 chars): {key[:10] if key else 'None'}")

# Тест 1: gemini/gemini-1.5-flash
try:
    print("\n[Тест 1] Проверка 'gemini/gemini-1.5-flash'...")
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=key)
    res = llm.call("Say hello in one word")
    print("👉 УСПЕХ:", res)
except Exception as e:
    print("❌ Ошибка:", e)

# Тест 2: gemini/gemini-1.5-flash-latest
try:
    print("\n[Тест 2] Проверка 'gemini/gemini-1.5-flash-latest'...")
    llm = LLM(model="gemini/gemini-1.5-flash-latest", api_key=key)
    res = llm.call("Say hello in one word")
    print("👉 УСПЕХ:", res)
except Exception as e:
    print("❌ Ошибка:", e)

# Тест 3: gemini/gemini-2.0-flash
try:
    print("\n[Тест 3] Проверка 'gemini/gemini-2.0-flash'...")
    llm = LLM(model="gemini/gemini-2.0-flash", api_key=key)
    res = llm.call("Say hello in one word")
    print("👉 УСПЕХ:", res)
except Exception as e:
    print("❌ Ошибка:", e)

# Тест 4: Нативный вызов через google-genai
try:
    print("\n[Тест 4] Проверка нативного google-genai...")
    from google import genai
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='Say hello in one word',
    )
    print("👉 УСПЕХ нативного вызова:", response.text)
except Exception as e:
    print("❌ Ошибка нативного вызова:", e)
