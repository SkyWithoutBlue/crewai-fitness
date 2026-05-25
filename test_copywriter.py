import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

print("Initializing LLM...")
llm = LLM(model="gemini/gemini-2.5-flash", api_key=key)

prompt = """
You are Фитнес-Копирайтер и контент-менеджер.
Your goal is: Писать вовлекающие посты для Instagram с тоном "Вдохновляющий и энергичный ⚡" и призывом к действию на сайт https://chipizubova.online.
Backstory: Вы — эксперт в фитнес-копирайтинге. Вы умеете цеплять внимание ярким заголовком, делить текст на удобные абзацы и ненавязчиво продавать услуги.

Please write a post based on this research:
---
Хроническая усталость у одиноких мам...
Короткие тренировки ноги+пресс...
Волшебной таблетки нет, но есть 15-20 минут функционального кросс-тренинга.
---

Requirements:
- Тон общения: Вдохновляющий и энергичный ⚡
- Яркий, бьющий в цель заголовок.
- Структура с эмодзи и абзацами.
- Четкий призыв к действию.
"""

try:
    print("Making call...")
    res = llm.call(prompt)
    print("SUCCESS!")
    print(res)
except Exception as e:
    print("ERROR:")
    import traceback
    traceback.print_exc()
