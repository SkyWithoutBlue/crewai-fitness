import os
import sys

# Reconfigure stdout and stderr to handle UTF-8 and ignore encoding errors on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Загружаем переменные окружения из .env
load_dotenv()

def main():
    # 1. Проверяем наличие API ключей
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not gemini_key and not openai_key:
        print("[ОШИБКА] Не найдены ключи API!")
        print("Пожалуйста, скопируйте файл .env.example в .env и укажите ваш GEMINI_API_KEY или OPENAI_API_KEY.")
        sys.exit(1)

    # 2. Настраиваем LLM (модель ИИ)
    # По умолчанию используем Gemini, так как это наиболее доступный вариант
    if gemini_key:
        print("[ИНФО] Инициализация Google Gemini LLM (gemini-flash-latest)...")
        # Используем gemini/gemini-flash-latest для обхода суточного лимита 2.5-flash в 20 запросов
        llm = LLM(model="gemini/gemini-flash-latest", api_key=gemini_key)
    else:
        openai_model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
        print(f"[ИНФО] Инициализация OpenAI LLM ({openai_model})...")
        llm = LLM(model=openai_model, api_key=openai_key)

    # 3. Инициализируем поисковый инструмент (если есть ключ Serper)
    tools = []
    serper_key = os.getenv("SERPER_API_KEY")
    if serper_key:
        print("[ИНФО] Подключение поискового инструмента Google Search...")
        from crewai_tools import SerperDevTool
        search_tool = SerperDevTool()
        tools.append(search_tool)
    else:
        print("[ИНФО] Запуск без веб-поиска (агенты будут использовать встроенные знания).")

    print("[ИНФО] Создание команды агентов...")

    # 4. Создаем агентов

    # Агент 1: Аналитик трендов и питания
    analyst = Agent(
        role='Фитнес-Аналитик трендов и питания',
        goal='Находить самые актуальные и научно обоснованные темы в фитнесе, здоровом образе жизни и питании (особенно безглютеновом/безлактозном), которые волнуют современную аудиторию.',
        backstory='Вы опытный нутрициолог и фитнес-исследователь. Вы умеете развенчивать популярные мифы о диетах и тренировках, опираясь на научные факты. Ваша цель — найти "боль" аудитории и дать ей простое, понятное решение.',
        llm=llm,
        tools=tools,
        verbose=False,
        allow_delegation=False
    )

    # Агент 2: Копирайтер
    copywriter = Agent(
        role='Фитнес-Копирайтер и контент-менеджер',
        goal='Писать вовлекающие, мотивирующие и полезные посты для Instagram с четкими призывами к действию (CTA), ведущими на сайт chipizubova.online.',
        backstory='Вы — эксперт в фитнес-копирайтинге. Вы точно знаете, как зацепить читателя заголовок-крючком (hook), разбить текст на читаемые абзацы, добавить нужные эмодзи и естественным образом подвести читателя к покупке марафона или плана питания на chipizubova.online.',
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

    # Агент 3: Сценарист Reels и Reels-продюсер
    reels_creator = Agent(
        role='Сценарист Reels и креативный директор',
        goal='Разрабатывать вирусные идеи и сценарии для коротких видео Instagram Reels, которые привлекают новых подписчиков и удерживают внимание.',
        backstory='Вы талантливый продюсер вертикальных видео. Вы знаете все тренды Reels, понимаете психологию удержания внимания в первые 3 секунды и умеете превратить любой сложный фитнес-инсайд в динамичный, простой и вирусный видеосценарий.',
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

    # 5. Описываем задачи

    # Задача 1: Исследование темы
    research_task = Task(
        description=(
            "Исследуй тему: 'Почему не получается похудеть при регулярных тренировках, и как на это влияет питание (включая непереносимость лактозы/глютена)'. "
            "Выдели 3 ключевые научно доказанные причины и предложи простые шаги по их решению. "
            "Эта информация ляжет в основу поста для продвижения фитнес-платформы chipizubova.online."
        ),
        expected_output="Аналитический отчет с 3 причинами, научным обоснованием и простыми советами по питанию и тренировкам.",
        agent=analyst
    )

    # Задача 2: Написание поста
    writing_task = Task(
        description=(
            "На основе аналитического отчета напиши вовлекающий пост для Instagram. "
            "Требования к посту:\n"
            "1. Заголовок-крючок (цепляющий и интригующий).\n"
            "2. Структурированный текст с использованием эмодзи.\n"
            "3. Фокус на заботе о здоровье (без жестких ограничений).\n"
            "4. Четкий призыв к действию (Call to Action): 'Переходи по ссылке в шапке профиля на chipizubova.online, чтобы забрать готовое сбалансированное меню без лактозы и глютена!'.\n"
            "5. Список релевантных хэштегов (до 10 штук)."
        ),
        expected_output="Готовый текст поста для Instagram в разметке Markdown.",
        agent=copywriter
    )

    # Задача 3: Создание сценария Reels
    reels_task = Task(
        description=(
            "На основе написанного поста создай сценарий для короткого видео Reels (до 60 секунд), которое будет привлекать трафик на этот пост и сайт chipizubova.online.\n"
            "Сценарий должен содержать:\n"
            "1. Идею видео (что происходит в кадре, какая локация).\n"
            "2. Хук на первые 3 секунды (текст на экране и голос).\n"
            "3. Пошаговую раскадровку (визуальный ряд + текст на экране + закадровый голос/озвучка).\n"
            "4. Звуковое сопровождение (какой тип музыки/звука использовать).\n"
            "5. Призыв к действию в конце видео (перейти в профиль и прочитать пост)."
        ),
        expected_output="Подробный сценарий Reels с раскадровкой и текстом.",
        agent=reels_creator
    )

    # 6. Собираем команду и запускаем
    print("\n[ИНФО] Запуск рабочего процесса CrewAI...")
    crew = Crew(
        agents=[analyst, copywriter, reels_creator],
        tasks=[research_task, writing_task, reels_task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()

    # 7. Сохраняем результат в файл
    output_file = "instagram_post_result.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Результаты работы ИИ-агентов CrewAI\n\n")
        f.write(str(result))

    print(f"\n[УСПЕХ] Работа завершена!")
    print(f"Сгенерированный пост и сценарий Reels сохранены в файл: {output_file}")

if __name__ == "__main__":
    main()
