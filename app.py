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

import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Настройка страницы
st.set_page_config(
    page_title="Chipizubova Fitness AI SaaS",
    page_icon="🏋️‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Загружаем п# Функция проверки авторизации (Логин + Пароль)
def check_login():
    """Возвращает True, если пользователь ввел правильный логин и пароль."""
    
    def login_clicked():
        """Проверяет правильность введенных логина и пароля."""
        # Логин и Пароль по умолчанию "nikitaludmila", но можно переопределить через Secrets или .env
        correct_username = st.secrets.get("APP_USERNAME", os.getenv("APP_USERNAME", "nikitaludmila"))
        correct_password = st.secrets.get("APP_PASSWORD", os.getenv("APP_PASSWORD", "nikitaludmila"))
        
        if (st.session_state["login_username"] == correct_username and 
            st.session_state["login_password"] == correct_password):
            st.session_state["logged_in"] = True
            # Очищаем пароль и логин из состояния для безопасности
            del st.session_state["login_username"]
            del st.session_state["login_password"]
        else:
            st.session_state["logged_in"] = False

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        # Выводим премиальный экран авторизации строго в стиле бренда (Outfit шрифт, песочно-графитовые тона)
        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 30px; text-align: center; max-width: 500px; margin: 100px auto 25px auto; background: #FFFFFF; border-radius: 16px; border: 1px solid #E5E5E5; box-shadow: 0 10px 30px rgba(0,0,0,0.03);">
            <div style="font-size: 56px; margin-bottom: 25px; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.05));">🔐</div>
            <h2 style="font-family: 'Outfit', sans-serif; font-weight: 700; color: #2C2C2C; margin: 0 0 10px 0; letter-spacing: -0.5px; font-size: 26px;">Авторизация</h2>
            <p style="font-family: 'Outfit', sans-serif; color: #7A6D6B; font-size: 14px; margin: 0 0 20px 0; line-height: 1.5; font-weight: 400;">Введите ваши учетные данные для доступа к ИИ-продюсерам Людмилы Чипизубовой.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Инпуты ввода логина и пароля по центру страницы
        col1, col2, col3 = st.columns([1, 1.8, 1])
        with col2:
            st.text_input(
                "Имя пользователя (Логин)",
                key="login_username",
                placeholder="Логин..."
            )
            st.text_input(
                "Пароль",
                type="password",
                key="login_password",
                placeholder="Пароль..."
            )
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.button("Войти в систему 🚀", use_container_width=True, on_click=login_clicked)
            
            if "logged_in" in st.session_state and not st.session_state["logged_in"]:
                st.error("😕 Неверный логин или пароль. Попробуйте еще раз.")
        return False
        
    return True

# Останавливаем выполнение приложения, если пользователь не авторизован
if not check_login():
    st.stop()  


def clean_html(text):
    if not text:
        return ""
    # Заменяем HTML-теги переноса строк на стандартные переносы строк для Markdown
    return text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")

# Имена временных файлов для сохранения результатов по отдельным задачам
analyst_file = "temp_analyst_report.md"
writer_file = "temp_writer_post.md"
reels_file = "temp_reels_script.md"
funnel_file = "temp_funnel.md"
telegram_file = "temp_telegram.md"
hooks_file = "temp_hooks.md"
brainstorm_file = "temp_brainstorm_reels.md"

# Инициализация session_state для управления полями ввода
if "app_mode" not in st.session_state:
    st.session_state["app_mode"] = "📝 Полный контент-пак (Пост + Сценарий + Воронка в Директ + А/Б Хуки + Telegram)"
if "app_model_name" not in st.session_state:
    st.session_state["app_model_name"] = "gemini/gemini-flash-latest"
if "app_tone" not in st.session_state:
    st.session_state["app_tone"] = "Дружелюбный, мягкий и поддерживающий 🥰"
if "app_topic_full" not in st.session_state:
    st.session_state["app_topic_full"] = "Как регулярные тренировки и сбалансированное питание помогают вернуть упругость ягодиц и плоский живот без жестких диет"
if "app_topic_brainstorm" not in st.session_state:
    st.session_state["app_topic_brainstorm"] = "Правильное сбалансированное питание и домашние функциональные тренировки для женщин"
if "app_topic_ab" not in st.session_state:
    st.session_state["app_topic_ab"] = "Как перестать срываться на сладкое по вечерам и заменить его полезным сбалансированным перекусом"
if "app_website" not in st.session_state:
    st.session_state["app_website"] = "https://chipizubova.online"
if "app_keyword" not in st.session_state:
    st.session_state["app_keyword"] = "УВЕРЕННОСТЬ"
if "app_extra_instructions" not in st.session_state:
    st.session_state["app_extra_instructions"] = ""
if "app_workout_type" not in st.session_state:
    st.session_state["app_workout_type"] = "Динамичный Кросс-тренинг (Жиросжигание и выносливость) ⚡"
if "app_meal_type" not in st.session_state:
    st.session_state["app_meal_type"] = "Быстрый завтрак для заряда энергией 🍳"
if "app_diet_pref" not in st.session_state:
    st.session_state["app_diet_pref"] = "Сбалансированное ПП (Без ограничений) 🥗"
if "app_tg_token" not in st.session_state:
    st.session_state["app_tg_token"] = os.getenv("TELEGRAM_BOT_TOKEN", "8817369132:AAFrkbYONxDQpmtxlnRVra1WBpieBZPsfFY")
if "app_tg_chat_id" not in st.session_state:
    st.session_state["app_tg_chat_id"] = os.getenv("TELEGRAM_CHAT_ID", "-5199231431")

import re
import io
import requests
import json

def extract_speech(text):
    if not text:
        return ""
    cleaned = re.sub(r'[*_`#]', '', text)
    lines = cleaned.split("\n")
    speech_lines = []
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        if any(word in line_strip.lower() for word in ["визуальный", "ракурс", "тайминг", "звуки", "сценарий", "схема", "триггер", "нарезка", "slow-mo"]):
            continue
        if re.search(r'\d+-\d+\s*(сек|sec)', line_strip):
            continue
        speech_lines.append(line_strip)
    return "\n".join(speech_lines)[:500]

def extract_hooks(text):
    if not text:
        return ["Ваш идеальный силуэт за 15 минут в день"]
    lines = text.split("\n")
    hooks = []
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        if any(line_strip.startswith(p) for p in ["Вариант А:", "Вариант Б:", "Вариант В:", "Вариант Г:", "Вариант Д:", "1.", "2.", "3.", "4.", "5."]):
            hooks.append(line_strip)
        elif line_strip.startswith("- ") and len(line_strip) > 15 and len(hooks) < 5:
            hooks.append(line_strip[2:])
            
    if not hooks:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip() and not p.strip().startswith("#")]
        hooks = paragraphs[:5]
        
    return [h[:100] for h in hooks]

def generate_scripter_code(hooks, tone, website):
    hooks_js_array = json.dumps(hooks, ensure_ascii=False)
    code = f"""// Figma Scripter: Автоматическое создание слайдов-историй для Людмилы
const slides = {hooks_js_array};

const font = {{ family: "Arial", style: "Bold" }};
figma.loadFontAsync(font).then(() => {{
  slides.forEach((text, index) => {{
    // Создаем фрейм под Stories (1080x1920)
    const frame = figma.createFrame();
    frame.name = `Слайд ${{index + 1}}`;
    frame.resize(1080, 1920);
    frame.x = index * 1200;
    frame.y = 0;
    
    // Фирменный бежевый фон #F5F1EE
    frame.fills = [{{ type: 'SOLID', color: {{ r: 0.96, g: 0.94, b: 0.93 }} }}];
    
    // Текстовый блок с хуком
    const textNode = figma.createText();
    textNode.fontName = font;
    textNode.characters = text;
    textNode.fontSize = 64;
    textNode.lineHeight = {{ value: 80, unit: 'PIXELS' }};
    
    // Фирменный графитовый цвет #2C2C2C
    textNode.fills = [{{ type: 'SOLID', color: {{ r: 0.17, g: 0.17, b: 0.17 }} }}];
    
    textNode.resize(900, 1000);
    textNode.x = 90;
    textNode.y = 450;
    
    frame.appendChild(textNode);
    figma.currentPage.appendChild(frame);
  }});
  figma.viewport.scrollAndZoomIntoView(figma.currentPage.children);
  console.log("Фирменные фреймы успешно созданы в Figma!");
}});
"""
    return code

def send_to_telegram(token, chat_id, text, file_path=None):
    if not token or not chat_id:
        return False, "Отсутствуют Bot Token или Chat ID в настройках."
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        r = requests.post(url, json=payload, timeout=10)
        
        if file_path and os.path.exists(file_path):
            doc_url = f"https://api.telegram.org/bot{token}/sendDocument"
            with open(file_path, "rb") as doc:
                files = {"document": doc}
                doc_payload = {
                    "caption": "🏋️‍♀️ Ваш сгенерированный брендированный PDF-гайд",
                    "chat_id": chat_id
                }
                requests.post(doc_url, data=doc_payload, files=files, timeout=15)
                
        if r.status_code == 200:
            return True, "Успешно отправлено в Telegram! ✈️"
        else:
            res_json = r.json()
            return False, f"Ошибка Telegram API: {res_json.get('description', 'Неизвестная ошибка')}"
    except Exception as e:
        return False, f"Ошибка сети при отправке в Telegram: {str(e)}"

def improve_content_via_crew(content_text, instruction, model_name, api_key):
    llm = LLM(model=model_name, api_key=api_key)
    improver = Agent(
        role="ИИ-Редактор контента",
        goal="Дорабатывать тексты по точным указаниям пользователя, сохраняя структуру и стиль.",
        backstory="Вы профессиональный копирайтер и редактор. Вы получаете текст и инструкцию, и выдаете обновленный текст.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
    edit_task = Task(
        description=f"Исходный текст:\n---\n{content_text}\n---\nИнструкция по доработке: '{instruction}'. Перепиши исходный текст, применив инструкцию. Сохрани исходный формат и разметку Markdown. Выдай ТОЛЬКО обновленный текст.",
        expected_output="Полностью обновленный текст без вводных фраз.",
        agent=improver
    )
    crew = Crew(agents=[improver], tasks=[edit_task], verbose=False)
    return str(crew.kickoff())

def analyze_virality_via_crew(post_text, reels_text, model_name, api_key):
    llm = LLM(model=model_name, api_key=api_key)
    analyzer = Agent(
        role="ИИ-Аналитик виральности",
        goal="Оценивать тексты на вовлечение, вирусный потенциал и триггеры, рассчитывая точный балл.",
        backstory="Вы опытный маркетолог социальных сетей. Вы оцениваете контент на воображаемой шкале от 1 до 100.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
    analysis_task = Task(
        description=(
            f"Instagram Пост:\n---\n{post_text}\n---\nReels Сценарий:\n---\n{reels_text}\n---\n"
            f"Проанализируй этот контент на виральность (удержание внимания, эмоциональные триггеры, четкость призыва к действию).\n"
            f"Требования к ответу:\n"
            f"1. Первая строчка должна содержать числовой балл от 1 до 100 в формате: 'Балл: [Число]' (например, 'Балл: 87'). Никакого другого текста на первой строке!\n"
            f"2. Далее дай подробный разбор:\n"
            f"   - 🎯 Сила Хука (Hook Strength)\n"
            f"   - ⚡ Эмоциональные триггеры\n"
            f"   - 📢 Четкость призыва к действию (CTA Clarity)\n"
            f"3. Напиши 3 конкретные рекомендации по улучшению на русском языке."
        ),
        expected_output="Числовой балл на первой строчке и подробный структурированный разбор.",
        agent=analyzer
    )
    crew = Crew(agents=[analyzer], tasks=[analysis_task], verbose=False)
    return str(crew.kickoff())

def load_calendar():
    calendar_file = "content_calendar.json"
    if os.path.exists(calendar_file):
        try:
            with open(calendar_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_calendar(events):
    calendar_file = "content_calendar.json"
    try:
        with open(calendar_file, "w", encoding="utf-8") as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

# Кастомные стили CSS для премиального SaaS внешнего вида
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
    /* Глобальный премиальный шрифт (исключая служебные иконки) */
    html, body, p, label, .stMarkdown, .stButton>button, .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        font-family: 'Outfit', sans-serif !important;
        color: #2C2C2C !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #1A1A1A !important;
    }
    
    /* Сохраняем иконки Streamlit в целости */
    [class*="Icon"], [id*="Icon"], [data-testid="stIcon"], svg, i {
        font-family: inherit !important;
    }
    
    /* Силовой БЕЛЫЙ фон для всего приложения Streamlit */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #FFFFFF !important;
        color: #2C2C2C !important;
    }
    
    /* Красивый светлый сайдбар в теплом бежевом стиле бренда */
    [data-testid="stSidebar"] {
        background-color: #F5F1EE !important;
        border-right: 1px solid #E5E5E5 !important;
    }
    
    /* Заголовки с темным градиентом высокой контрастности */
    h1 {
        background: linear-gradient(135deg, #1A1A1A 30%, #4D4D4D 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 700 !important;
    }
    
    /* Кнопки с премиальным кораллово-розовым градиентом бренда */
    .stButton>button {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff8533 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-size: 13px !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.35) !important;
        filter: brightness(1.05) !important;
    }
    .stButton>button:active {
        transform: translateY(0px) !important;
    }
    
    /* Светлые вкладки в виде скругленных пилюль */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F5F1EE !important;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #E5E5E5 !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: pre-wrap;
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        color: #7A6D6B !important;
        font-weight: 600 !important;
        border: none !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2C2C2C 0%, #4D4D4D 100%) !important;
        box-shadow: 0 4px 12px rgba(44, 44, 44, 0.15) !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="false"] * {
        color: #7A6D6B !important;
    }
    
    /* Изящные карточки результатов и экспандеры */
    .report-box, div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #F8F8F8 !important;
        border: 1px solid #E5E5E5 !important;
        padding: 22px !important;
        border-radius: 12px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.03) !important;
    }
    
    /* Текстовые поля ввода и селекторы в светлой гамме */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #2C2C2C !important;
        border: 1px solid #D1D1D1 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox [data-baseweb="select"]:focus {
        border-color: #ff8533 !important;
        box-shadow: 0 0 8px rgba(255, 133, 51, 0.1) !important;
    }
    
    /* Текст разметки */
    .stMarkdown p {
        line-height: 1.6 !important;
        color: #404040 !important;
    }
    
    /* Скрываем стандартные футеры Streamlit */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Заголовок приложения
st.title("🏋️‍♀️ Chipizubova Fitness AI Content Engine")
st.markdown("Добро пожаловать в интеллектуальный маркетинговый SaaS-центр. Здесь ваши ИИ-агенты разрабатывают премиальный, вирусный и продающий контент для привлечения клиентов на [chipizubova.online](http://chipizubova.online).")

# Боковая панель с настройками
st.sidebar.image("https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=400&q=80", use_container_width=True)
st.sidebar.title("⚙️ Настройки ИИ-продюсера")

# Кнопка безопасного выхода из системы
if st.sidebar.button("🔒 Выйти из системы", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()

# Управление API-ключом
env_key = os.getenv("GEMINI_API_KEY", "")
api_key = st.sidebar.text_input("Google Gemini API Ключ", value=env_key, type="password", help="Получите бесплатный ключ в Google AI Studio")

if api_key:
    st.sidebar.success("API-ключ успешно подключен! ✅")
else:
    st.sidebar.warning("Пожалуйста, введите ваш API-ключ Gemini.")

st.sidebar.markdown("---")

# Дополнительные настройки генерации
model_options = [
    "gemini/gemini-flash-latest",
    "gemini/gemini-3.5-flash",
    "gemini/gemini-3.1-flash-lite",
    "gemini/gemini-2.5-flash-lite",
    "gemini/gemini-2.5-flash"
]
model_name = st.sidebar.selectbox(
    "Модель ИИ",
    model_options,
    index=model_options.index(st.session_state["app_model_name"]) if st.session_state["app_model_name"] in model_options else 0,
    key="app_model_name",
    help="Выберите модель Google Gemini. 'gemini-flash-latest' и 'gemini-3.5-flash' поддерживают до 1500 запросов в день и рекомендуются во избежание ошибок лимита (429)."
)

tone_options = [
    "Дружелюбный, мягкий и поддерживающий 🥰",
    "Вдохновляющий и энергичный ⚡",
    "Экспертный и научно-обоснованный 🔬"
]
tone = st.sidebar.selectbox(
    "Тон публикации (Tone of Voice)",
    tone_options,
    index=tone_options.index(st.session_state["app_tone"]) if st.session_state["app_tone"] in tone_options else 0,
    key="app_tone"
)

# ✈️ Настройки Telegram Интеграции
with st.sidebar.expander("✈️ Настройки Telegram"):
    tg_token = st.text_input(
        "Telegram Bot Token", 
        value=st.session_state["app_tg_token"], 
        type="password", 
        key="app_tg_token_input", 
        help="Токен бота от @BotFather"
    )
    st.session_state["app_tg_token"] = tg_token
    
    tg_chat_id = st.text_input(
        "Telegram Chat ID", 
        value=st.session_state["app_tg_chat_id"], 
        key="app_tg_chat_id_input", 
        help="Ваш Chat ID (узнайте у бота @userinfobot)"
    )
    st.session_state["app_tg_chat_id"] = tg_chat_id

st.sidebar.markdown("---")

# 📂 История прошлых генераций
st.sidebar.subheader("📂 История прошлых генераций")
history_file = "generation_history.json"
history_list = []
if os.path.exists(history_file):
    try:
        import json
        with open(history_file, "r", encoding="utf-8") as hf:
            history_list = json.load(hf)
    except:
        pass

if history_list:
    history_options = []
    for idx, entry in enumerate(history_list):
        timestamp = entry.get("timestamp", "Неизвестно")
        mode_label = entry.get("mode", "").split(" ")[0]  # Первый смайлик/слово
        topic_preview = entry.get("topic", "")[:30] + "..." if len(entry.get("topic", "")) > 30 else entry.get("topic", "")
        history_options.append(f"{timestamp} | {mode_label} | {topic_preview}")
    
    selected_history_str = st.sidebar.selectbox(
        "Выберите прошлую генерацию:",
        options=history_options,
        index=0,
        key="selected_history_item"
    )
    
    selected_idx = history_options.index(selected_history_str)
    selected_entry = history_list[selected_idx]
    
    col_load, col_del = st.sidebar.columns(2)
    with col_load:
        if st.button("📂 Загрузить", use_container_width=True):
            st.session_state["app_mode"] = selected_entry.get("mode", mode_options[0])
            
            loaded_topic = selected_entry.get("topic", "")
            st.session_state["app_topic_full"] = loaded_topic
            st.session_state["app_topic_full_input"] = loaded_topic
            st.session_state["app_topic_brainstorm"] = loaded_topic
            st.session_state["app_topic_brainstorm_input"] = loaded_topic
            st.session_state["app_topic_ab"] = loaded_topic
            st.session_state["app_topic_ab_input"] = loaded_topic
            
            inputs = selected_entry.get("inputs", {})
            if inputs:
                st.session_state["app_tone"] = inputs.get("tone", tone_options[0])
                st.session_state["app_model_name"] = inputs.get("model_name", model_options[0])
                st.session_state["app_website"] = inputs.get("website", "https://chipizubova.online")
                st.session_state["app_keyword"] = inputs.get("keyword", "УВЕРЕННОСТЬ")
                st.session_state["app_extra_instructions"] = inputs.get("extra_instructions", "")
                
                if "workout_type" in inputs:
                    st.session_state["app_workout_type"] = inputs["workout_type"]
                if "meal_type" in inputs:
                    st.session_state["app_meal_type"] = inputs["meal_type"]
                if "diet_pref" in inputs:
                    st.session_state["app_diet_pref"] = inputs["diet_pref"]
                if "tg_token" in inputs:
                    st.session_state["app_tg_token"] = inputs["tg_token"]
                    st.session_state["app_tg_token_input"] = inputs["tg_token"]
                if "tg_chat_id" in inputs:
                    st.session_state["app_tg_chat_id"] = inputs["tg_chat_id"]
                    st.session_state["app_tg_chat_id_input"] = inputs["tg_chat_id"]
            
            # Перезаписываем временные файлы историческими результатами
            results = selected_entry.get("results", {})
            file_mapping = {
                "report_data": analyst_file,
                "post_data": writer_file,
                "reels_data": reels_file,
                "funnel_data": funnel_file,
                "telegram_data": telegram_file,
                "hooks_data": hooks_file,
                "brainstorm_data": brainstorm_file
            }
            
            for key, filename in file_mapping.items():
                content = results.get(key, "")
                if content:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(content)
                else:
                    if os.path.exists(filename):
                        try:
                            os.remove(filename)
                        except:
                            pass
            
            st.toast("Генерация успешно загружена! 🔄")
            st.rerun()
            
    with col_del:
        if st.button("🗑 Удалить", use_container_width=True):
            history_list.pop(selected_idx)
            with open(history_file, "w", encoding="utf-8") as hf:
                json.dump(history_list, hf, ensure_ascii=False, indent=2)
            st.toast("Запись удалена! 🗑")
            st.rerun()
            
    if st.sidebar.button("🧹 Очистить всю историю", use_container_width=True):
        if os.path.exists(history_file):
            try:
                os.remove(history_file)
            except:
                pass
        for filename in [analyst_file, writer_file, reels_file, funnel_file, telegram_file, hooks_file, brainstorm_file]:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except:
                    pass
        st.toast("История и результаты полностью очищены! 🧹")
        st.rerun()
else:
    st.sidebar.info("История генераций пока пуста. После первой генерации здесь появится список сохраненных записей! ✍️")

st.sidebar.markdown("---")
st.sidebar.markdown("🙋‍♂️ **Инструкция продюсера:**\n1. Выберите режим работы ниже.\n2. Укажите тему или настройки.\n3. Нажмите «Сгенерировать контент».\n4. Заберите готовые посты, раскадровки, воронки в Директ и Telegram-версии во вкладках!")

# Главные вкладки приложения: Генератор и Планировщик
generator_tab, planner_tab = st.tabs(["✍️ Генератор контента", "📅 Планировщик контента"])

with generator_tab:
    # Главная форма ввода
    st.subheader("📝 Задание для ИИ-агентов")

    mode_options = [
        "📝 Полный контент-пак (Пост + Сценарий + Воронка в Директ + А/Б Хуки + Telegram)", 
        "🔥 Психологический прогрев для Stories (Запуск фитнес-курса)",
        "🗣️ Сценарий Продающего Прямого Эфира / Вебинара",
        "💡 Брейншторм 10 вирусных идей для Reels",
        "🥗 Фитнес-Рецепт + Reels-Сценарий (ПП под тренировку)",
        "⚡ Быстрый А/Б Тест Хуков"
    ]
    mode = st.selectbox(
        "Режим работы ИИ-агентов",
        mode_options,
        index=mode_options.index(st.session_state["app_mode"]) if st.session_state["app_mode"] in mode_options else 0,
        key="app_mode",
        help="Выберите формат работы контент-машины."
    )

    col1, col2 = st.columns([3, 1])

    # Определение динамических полей ввода в зависимости от режима
    with col1:
        if mode == "📝 Полный контент-пак (Пост + Сценарий + Воронка в Директ + А/Б Хуки + Telegram)":
            topic = st.text_area(
                "Направление или тема (чем подробнее, тем лучше):",
                value=st.session_state["app_topic_full"],
                height=100,
                key="app_topic_full_input",
                help="Напишите тему как можно подробнее. Агенты проведут исследование и составят весь контент-пак."
            )
            st.session_state["app_topic_full"] = topic
        elif mode == "🔥 Психологический прогрев для Stories (Запуск фитнес-курса)":
            topic = st.text_area(
                "Тема запуска или продукт для прогрева в Stories:",
                value=st.session_state["app_topic_full"],
                height=100,
                key="app_topic_stories_warmup_input",
                help="Например: запуск курса по упругим ягодицам или марафона стройности."
            )
            st.session_state["app_topic_full"] = topic
        elif mode == "🗣️ Сценарий Продающего Прямого Эфира / Вебинара":
            topic = st.text_area(
                "Тема вебинара или фокус эфира:",
                value=st.session_state["app_topic_full"],
                height=100,
                key="app_topic_live_stream_input",
                help="Например: как похудеть за 3 шага без жестких ограничений."
            )
            st.session_state["app_topic_full"] = topic

        elif mode == "💡 Брейншторм 10 вирусных идей для Reels":
            topic = st.text_area(
                "Ниша или основное направление для брейншторма:",
                value=st.session_state["app_topic_brainstorm"],
                height=100,
                key="app_topic_brainstorm_input"
            )
            st.session_state["app_topic_brainstorm"] = topic
        elif mode == "🥗 Фитнес-Рецепт + Reels-Сценарий (ПП под тренировку)":
            workout_options = [
                "Динамичный Кросс-тренинг (Жиросжигание и выносливость) ⚡",
                "Акцентированная тренировка Ноги + Пресс (Подтянутые ягодицы и плоский живот) 🍑",
                "Интенсивное домашнее Кардио (Укрепление кора и тонус) 🏃‍♀️",
                "Функциональный силовой тренинг (Мышечный рельеф) 💪"
            ]
            workout_type = st.selectbox(
                "Тип тренировки, под которую адаптируем рецепт:",
                workout_options,
                index=workout_options.index(st.session_state["app_workout_type"]) if st.session_state["app_workout_type"] in workout_options else 0,
                key="app_workout_type"
            )

            meal_options = [
                "Быстрый завтрак для заряда энергией 🍳",
                "Сытный восстанавливающий обед 🥗",
                "Легкий ужин без тяжести и вздутия 🍲",
                "Энергетический перекус / Посттренировочный протеиновый шейк 🥤"
            ]
            meal_type = st.selectbox(
                "Прием пищи / Формат блюда:",
                meal_options,
                index=meal_options.index(st.session_state["app_meal_type"]) if st.session_state["app_meal_type"] in meal_options else 0,
                key="app_meal_type"
            )

            diet_options = [
                "Сбалансированное ПП (Без ограничений) 🥗",
                "Без лактозы 🥛",
                "Без глютена 🌾",
                "Вегетарианское 🥦",
                "Без лактозы и без глютена 🌾🥛"
            ]
            diet_pref = st.selectbox(
                "Особенности питания / Диета (Опционально):",
                diet_options,
                index=diet_options.index(st.session_state["app_diet_pref"]) if st.session_state["app_diet_pref"] in diet_options else 0,
                key="app_diet_pref"
            )

            topic = f"Разработай полезный фитнес-рецепт для категории '{meal_type}', тип питания '{diet_pref}', идеально подходящий для восстановления после тренировки '{workout_type}'."
            st.info(f"🥗 ИИ-нутрициолог разработает рецепт под запрос: **{meal_type}** ({diet_pref}) для восстановления после **{workout_type}**.")
        elif mode == "⚡ Быстрый А/Б Тест Хуков":
            topic = st.text_area(
                "Сырая идея видео или тема для разработки хуков:",
                value=st.session_state["app_topic_ab"],
                height=100,
                key="app_topic_ab_input"
            )
            st.session_state["app_topic_ab"] = topic

    with col2:
        if mode in ["📝 Полный контент-пак (Пост + Сценарий + Воронка в Директ + А/Б Хуки + Telegram)", "🥗 Фитнес-Рецепт + Reels-Сценарий (ПП под тренировку)"]:
            website = st.text_input(
                "Ссылка для призыва к действию (CTA)",
                value=st.session_state["app_website"],
                key="app_website",
                help="Ссылка на ваш сайт, которую копирайтер вставит в призывы к действию."
            )
            keyword = st.text_input(
                "Триггер-слово для воронки в Директ",
                value=st.session_state["app_keyword"],
                placeholder="например: МЕНЮ, ПРЕСС, КУРС",
                key="app_keyword",
                help="Слово, которое зритель должен написать в комментариях к Reels, чтобы автоворонка ManyChat/n8n отправила ему лид-магнит в Директ."
            )
        else:
            website = "https://chipizubova.online"
            keyword = "МЕНЮ"

        extra_instructions = st.text_input(
            "Дополнительные пожелания (опционально)",
            value=st.session_state["app_extra_instructions"],
            placeholder="например: 'добавь юмора', 'сделай упор на боли'",
            key="app_extra_instructions",
            help="Сюда можно вписать любые микро-требования к стилю или деталям."
        )

    # Кнопка запуска
    if st.button("Сгенерировать контент ✨", use_container_width=True):
        if not api_key:
            st.error("❌ Невозможно запустить генерацию: отсутствует API-ключ Google Gemini. Пожалуйста, укажите его в боковой панели.")
        else:
            # Временные файлы для сохранения результатов по отдельным задачам
            analyst_file = "temp_analyst_report.md"
            writer_file = "temp_writer_post.md"
            reels_file = "temp_reels_script.md"
            funnel_file = "temp_funnel.md"
            telegram_file = "temp_telegram.md"
            hooks_file = "temp_hooks.md"
            brainstorm_file = "temp_brainstorm_reels.md"

            # Удаляем старые временные файлы, если они есть
            for f in [analyst_file, writer_file, reels_file, funnel_file, telegram_file, hooks_file, brainstorm_file]:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except:
                        pass

            # Контейнер для отображения процесса
            with st.status("🕵️‍♂️ Запуск ИИ-команды продюсеров...", expanded=True) as status:
                try:
                    # 1. Инициализация ИИ модели
                    llm = LLM(model=model_name, api_key=api_key)

                    # 2. Создание агентов
                    status.write("🤝 Инициализация агентов (Аналитик, Копирайтер, Сценарист)...")

                    analyst = Agent(
                        role='Фитнес-Аналитик трендов и питания',
                        goal='Находить научно обоснованные факты и глубокие инсайты в фитнесе и сбалансированном правильном питании (ПП), помогающие решить проблемы аудитории.',
                        backstory='Вы опытный нутрициолог и исследователь. Вы развенчиваете мифы о диетах и даете научно обоснованные советы простым языком.',
                        llm=llm,
                        verbose=False,
                        allow_delegation=False
                    )

                    copywriter = Agent(
                        role='Фитнес-Копирайтер и контент-менеджер',
                        goal=f'Писать вовлекающие посты для Instagram и Telegram с тоном "{tone}" и призывом к действию на сайт {website}.',
                        backstory='Вы — эксперт в фитнес-копирайтинге. Вы умеете цеплять внимание ярким заголовком, делить текст на удобные абзацы и ненавязчиво продавать услуги.',
                        llm=llm,
                        verbose=False,
                        allow_delegation=False
                    )

                    reels_creator = Agent(
                        role='Сценарист Reels и креативный директор',
                        goal='Разрабатывать вирусные идеи и сценарии Reels (до 60 секунд) с визуальной режиссурой, ракурсами и звуками, удерживающие внимание зрителя с первых секунд.',
                        backstory='Вы талантливый продюсер вертикальных видео. Вы знаете все тренды Reels, понимаете психологию удержания внимания и умеете превратить фитнес-совет в зрелищный сценарий.',
                        llm=llm,
                        verbose=False,
                        allow_delegation=False
                    )

                    # 3. Описание задач с указанием выходных файлов в зависимости от режима
                    status.write("📋 Распределение маркетинговых задач...")

                    tasks_list = []

                    if mode == "📝 Полный контент-пак (Пост + Сценарий + Воронка в Директ + А/Б Хуки + Telegram)":
                        # Задача 1: Глубокий анализ темы
                        research_task = Task(
                            description=f"Проведи глубокое научное исследование на тему: '{topic}'. Найди 3 научно подтвержденные проблемы и простые пути их решения. {extra_instructions}",
                            expected_output="Аналитический отчет с 3 ключевыми выводами и практическими рекомендациями.",
                            agent=analyst,
                            output_file=analyst_file
                        )

                        # Задача 2: Пост в Instagram
                        writing_task = Task(
                            description=(
                                f"На основе аналитического отчета напиши вовлекающий, бьющий в боль пост для Instagram.\n"
                                f"Требования к тексту:\n"
                                f"- Тон общения: {tone}\n"
                                f"- Яркий, интригующий заголовок.\n"
                                f"- Структурированная подача с эмодзи и абзацами.\n"
                                f"- В конце поста упомяни возможность написать слово '{keyword}' в комментариях, чтобы бесплатно забрать ценный гайд по теме в Директ."
                            ),
                            expected_output="Готовый текст поста для Instagram с эмодзи.",
                            agent=copywriter,
                            output_file=writer_file
                        )

                        # Задача 3: Сценарий Reels с режиссурой и ракурсами
                        reels_task = Task(
                            description=(
                                f"Создай детальный сценарий Reels (до 60 сек) для привлечения людей на этот пост и сайт {website}.\n"
                                f"Обязательно добавь Режиссерскую раскадровку (Director's Visual Cut):\n"
                                f"- Точные тайминги (например, 0-3 сек, 3-7 сек).\n"
                                f"- Ракурсы съемки (крупный план, съемка снизу, следящий кадр в движении, детализация работы мышц).\n"
                                f"- Инструкции для тренера (что показывать, эмоции, жесты).\n"
                                f"- Рекомендации по музыке и звуковым эффектам (саунд-дизайн, дроп баса, шумы движения).\n"
                                f"- Сильный призыв написать кодовое слово '{keyword}' в комментариях."
                            ),
                            expected_output="Детализированный сценарий Reels с таймингами, ракурсами и звуками.",
                            agent=reels_creator,
                            output_file=reels_file
                        )

                        # Задача 4: Воронка в Директ + Лид-магнит (ManyChat/n8n)
                        funnel_task = Task(
                            description=(
                                f"Для темы '{topic}' разработай полноценную воронку автоответов в Директ по ключевому слову '{keyword}'.\n"
                                f"Эта задача должна включать:\n"
                                f"1. Пошаговую схему чат-бота ManyChat/n8n (Триггер -> Сообщение 1 -> Кнопка -> Сообщение 2 -> Линк на {website}).\n"
                                f"2. Точные тексты сообщений для Директа (сверх-дружелюбные, быстрые, дающие пользу).\n"
                                f"3. ПОЛНЫЙ готовый текст лид-магнита (гайда, чек-листа или PDF-инструкции), который бот будет отдавать. Напиши этот гайд качественно, без общих фраз, чтобы пользователь захотел купить основную программу на {website}!"
                            ),
                            expected_output="Сценарий воронки автоответов и готовый текст лид-магнита для Директа.",
                            agent=copywriter,
                            output_file=funnel_file
                        )

                        # Задача 5: А/Б Тестировщик 5 вирусных хуков для экрана
                        hooks_task = Task(
                            description=(
                                f"Разработай 5 альтернативных вариантов хуков (текста на экране в первые 3 секунды Reels) и интригующих заголовков для темы: '{topic}'.\n"
                                f"Каждый хук должен бить в разные психологические триггеры:\n"
                                f"- Вариант А: Триггер боли и страха\n"
                                f"- Вариант Б: Триггер любопытства / тайны\n"
                                f"- Вариант В: Триггер мгновенной пользы\n"
                                f"- Вариант Г: Разрушение популярного мифа\n"
                                f"- Вариант Д: Эмоциональное сочувствие / эмпатия\n"
                                f"Для каждого хука напиши, почему он сработает."
                            ),
                            expected_output="5 психологических хуков для Reels с анализом эффективности.",
                            agent=copywriter,
                            output_file=hooks_file
                        )

                        # Задача 6: Адаптация контента для Telegram
                        telegram_task = Task(
                            description=(
                                f"Адаптируй тему '{topic}' для публикации в Telegram-канале Людмилы.\n"
                                f"Напиши:\n"
                                f"1. Глубокий, структурированный Telegram-пост (Telegram лонгрид) с жирным шрифтом, списками, без лишней воды.\n"
                                f"2. Короткий сценарий (скрипт) для записи 30-секундного видеосообщения («кружочка») или голосового сообщения от Людмилы, предваряющего этот пост.\n"
                                f"3. Текст вовлекающего интерактивного опроса (Telegram Poll) по теме для поднятия активности подписчиков."
                            ),
                            expected_output="Telegram контент-план: лонгрид, сценарий кружочка и опрос.",
                            agent=copywriter,
                            output_file=telegram_file
                        )

                        tasks_list = [research_task, writing_task, reels_task, funnel_task, hooks_task, telegram_task]

                    elif mode == "🔥 Психологический прогрев для Stories (Запуск фитнес-курса)":
                        research_task = Task(
                            description=f"Проанализируй психологические барьеры, возражения и боли аудитории, мешающие им купить фитнес-программу по теме: '{topic}'. Выдели 5 ключевых возражений (например, нет времени, боюсь сорваться, пробовала и не вышло) и предложи пути их снятия через экспертность.",
                            expected_output="Психологический анализ с 5 ключевыми барьерами ЦА и стратегией их преодоления.",
                            agent=analyst,
                            output_file=analyst_file
                        )
                        
                        writing_task = Task(
                            description=(
                                f"На основе психологического анализа разработай пошаговый 5-дневный прогрев в Stories для запуска курса.\n"
                                f"Каждый день должен содержать от 3 до 5 слайдов со сценарным описанием (что показать: фото, видео, говорящая голова, интерактив) и текстом на экране.\n"
                                f"Дни должны идти по следующей схеме:\n"
                                f"- День 1: Актуализация боли и сочувствие аудитории.\n"
                                f"- День 2: Разрушение ложного пути (почему жесткие диеты/изнурительный бег не работают).\n"
                                f"- День 3: Презентация простого и бережного решения (метод Людмилы).\n"
                                f"- День 4: Демонстрация социальных доказательств (кейсы до/после, отзывы).\n"
                                f"- День 5: Открытие продаж и призыв написать ключевое слово '{keyword}' в комментариях для получения PDF-гайда и ссылки {website}."
                            ),
                            expected_output="5-дневный сценарный план Stories для Instagram с описанием визуалов и текстами.",
                            agent=copywriter,
                            output_file=writer_file
                        )
                        
                        reels_task = Task(
                            description=(
                                f"Создай сценарий Reels (до 60 сек), который идеально предваряет или поддерживает этот Stories-прогрев.\n"
                                f"Цель видео: вызвать бурный интерес к теме и заставить зрителя перейти в Stories или написать ключевое слово '{keyword}'.\n"
                                f"Обязательно пропиши ракурсы съемки, динамичный темпоритм и призыв к действию."
                            ),
                            expected_output="Сценарий Reels с ракурсами и музыкой для поддержки Stories-запуска.",
                            agent=reels_creator,
                            output_file=reels_file
                        )
                        
                        tasks_list = [research_task, writing_task, reels_task]

                    elif mode == "🗣️ Сценарий Продающего Прямого Эфира / Вебинара":
                        research_task = Task(
                            description=f"Составь подробную структуру выступления и 3 главных смысловых тезиса для прямого эфира по теме: '{topic}'. Выдели основные боли, которые нужно затронуть в первые 10 минут, чтобы зрители не расходились.",
                            expected_output="Структура эфира и 3 ключевых тезиса с триггерами удержания внимания.",
                            agent=analyst,
                            output_file=analyst_file
                        )
                        
                        writing_task = Task(
                            description=(
                                f"На основе тезисов составь детальный, поминутный сценарий прямого эфира (вебинара) на 45 минут.\n"
                                f"Сценарий должен состоять из разделов:\n"
                                f"1. Вступление (0-5 мин) — правила, создание интриги, самопрезентация Людмилы.\n"
                                f"2. Контентная часть (5-25 мин) — разбор 3-х главных фитнес-ошибок аудитории, простые лайфхаки.\n"
                                f"3. Блок продаж (25-35 мин) — презентация фитнес-программы на {website}, разбор ценности, отработка страхов.\n"
                                f"4. Блок ответов на вопросы (35-45 мин) — интерактив со зрителями.\n"
                                f"Для каждого блока пропиши конкретные фразы Людмилы, интонации и подсказки, что выводить на экран."
                            ),
                            expected_output="Поминутный сценарий прямого эфира на 45 минут с текстовыми репликами.",
                            agent=copywriter,
                            output_file=writer_file
                        )
                        
                        reels_task = Task(
                            description=(
                                f"Создай сценарий короткого промо-Reels (до 30 сек) для приглашения подписчиков на этот прямой эфир.\n"
                                f"Используй интригующий хук, расскажи о ценности эфира и призови написать кодовое слово '{keyword}' в комментариях, чтобы бот выслал ссылку-приглашение на эфир."
                            ),
                            expected_output="Промо-сценарий Reels с ракурсами и призывом зарегистрироваться на эфир.",
                            agent=reels_creator,
                            output_file=reels_file
                        )
                        
                        tasks_list = [research_task, writing_task, reels_task]

                    elif mode == "💡 Брейншторм 10 вирусных идей для Reels":
                        # Режим Брейншторма!
                        research_task = Task(
                            description=(
                                f"Проведи брейншторминг и найди 10 самых вирусных, актуальных и цепляющих тем для коротких видео Reels в нише: '{topic}'. "
                                f"Темы должны бить в боль целевой аудитории (активные женщины, заботящиеся о здоровье, ищущие баланс в питании, тренировках, похудении без насилия над собой). {extra_instructions}"
                            ),
                            expected_output="Список из 10 детально проработанных тем.",
                            agent=analyst,
                            output_file=analyst_file
                        )

                        writing_task = Task(
                            description=(
                                "На основе 10 тем от Аналитика разработай для каждой темы по 2 варианта цепляющих текстовых хуков (текст на экране в первые 3 секунды) и 1 интригующий заголовок."
                            ),
                            expected_output="Список тем с разработанными хуками и заголовками.",
                            agent=copywriter,
                            output_file=writer_file
                        )

                        reels_task = Task(
                            description=(
                                "Для каждой из 10 тем разработай подробный визуальный сценарий для съемки (что показывать в кадре, действия тренера), "
                                "указав точные ракурсы (крупный план, ракурс снизу, динамическое ведение) и порекомендуй тип звука (музыка, тренд, голос).\n"
                                "Каждую идею оформи в виде красивого, хорошо читаемого структурированного блока с четким разделением по строкам и отступами (НЕ используй таблицы, используй списки, абзацы и жирный шрифт):\n"
                                "### 🎥 Идея №[Номер]: [Название идеи]\n"
                                "- **🎯 Тема и Суть:** [Описание сути]\n"
                                "- **⚡ Текстовый Хук на экране:** [Хук на первые 3 секунды]\n"
                                "- **🎬 Визуальный ряд и Ракурс (что снимать):**\n"
                                "  - **0-3 сек:** [Кадр, ракурс, действия]\n"
                                "  - **3-10 сек:** [Кадр, ракурс, действия]\n"
                                "  - **10-15 сек:** [Кадр, ракурс, действия]\n"
                                "- **🎵 Звук / Музыка:** [Описание звука и музыки]\n\n"
                                "Добавь разделительную горизонтальную черту '---' между идеями."
                            ),
                            expected_output="10 детально прописанных идей Reels с четкой структурой в виде списков и заголовков.",
                            agent=reels_creator,
                            output_file=brainstorm_file
                        )

                        tasks_list = [research_task, writing_task, reels_task]

                    elif mode == "🥗 Фитнес-Рецепт + Reels-Сценарий (ПП под тренировку)":
                        # Режим кулинарного Reels
                        research_task = Task(
                            description=(
                                f"Разработай эксклюзивный, быстрый, вкусный и полезный фитнес-рецепт (ПП) под запрос: '{topic}'.\n"
                                f"Рецепт должен содержать доступные ингредиенты и готовиться не более 15-20 минут.\n"
                                f"Обязательно добавь научное нутрициологическое обоснование: как именно компоненты этого блюда помогают организму восстановиться, "
                                f"запустить метаболизм или дать энергию именно для выбранной тренировки."
                            ),
                            expected_output="Рецепт с граммовками, шагами и научным разбором пользы.",
                            agent=analyst,
                            output_file=analyst_file
                        )

                        writing_task = Task(
                            description=(
                                f"На основе рецепта напиши цепляющий, безумно аппетитный и продающий пост для Instagram.\n"
                                f"Требования:\n"
                                f"- Эстетичное описание вкуса блюда.\n"
                                f"- Список ингредиентов и пошаговая схема.\n"
                                f"- Интегрированный призыв к действию (CTA): пригласи на {website} забрать готовую сбалансированную программу питания и тренировок для идеального тела."
                            ),
                            expected_output="Аппетитный продающий рецепт-пост для Instagram.",
                            agent=copywriter,
                            output_file=writer_file
                        )

                        reels_task = Task(
                            description=(
                                "Разработай вирусный, эстетичный сценарий кулинарного Reels (до 40 сек) для приготовления этого блюда.\n"
                                "Сценарий должен включать:\n"
                                "- Невероятно аппетитный хук на 1-3 секунды.\n"
                                "- Пошаговую раскадровку видеоряда: макро-съемка ингредиентов, замедленная съемка (slow-mo), эстетичный пар, сочные текстуры.\n"
                                "- Текст на экране (короткий, динамичный, накладываемый в такт музыке).\n"
                                "- Звуковое сопровождение (ритмичный трек, ASMR-звуки нарезки, шипения сковороды, бурления воды)."
                            ),
                            expected_output="Кулинарный сценарий Reels с ASMR и раскадровкой.",
                            agent=reels_creator,
                            output_file=reels_file
                        )

                        tasks_list = [research_task, writing_task, reels_task]

                    elif mode == "⚡ Быстрый А/Б Тест Хуков":
                        # Режим А/Б тестов
                        research_task = Task(
                            description=f"Проанализируй психологические барьеры, боли и страхи аудитории касательно темы: '{topic}'. Выдели 3 триггерные точки.",
                            expected_output="Психологический анализ темы с 3 болевыми точками ЦА.",
                            agent=analyst,
                            output_file=analyst_file
                        )

                        writing_task = Task(
                            description=(
                                f"На основе анализа разработай 5 принципиально разных цепляющих хуков (оверлеев на экран) для начала видео Reels по теме '{topic}'.\n"
                                f"Хуки должны быть следующими:\n"
                                f"1. Боль / Эмоциональный срыв\n"
                                f"2. Жесткая правда / Миф\n"
                                f"3. Выгода за 10 секунд\n"
                                f"4. Противоречие / Разрыв шаблона\n"
                                f"5. Поддерживающий / Эмпатичный\n"
                                f"Для каждого хука дай 2 варианта интригующего заголовка для текста описания видео."
                            ),
                            expected_output="5 А/Б вариантов хуков и текстовых заголовков.",
                            agent=copywriter,
                            output_file=writer_file
                        )

                        reels_task = Task(
                            description=(
                                f"Для каждого из 5 разработанных хуков придумай конкретную идею видеоряда: где снимать, что делать Людмиле в кадре (действие тренера), "
                                f"какой ракурс камеры использовать (сбоку, в движении, сверху) и как выстроить визуальный ритм."
                            ),
                            expected_output="5 сценариев видеоряда под А/Б хуки.",
                            agent=reels_creator,
                            output_file=reels_file
                        )

                        tasks_list = [research_task, writing_task, reels_task]

                    # 4. Запуск процесса
                    status.write("🚀 Запуск симуляции ИИ-агентов (может занять около 1-1.5 минут)...")
                    crew = Crew(
                        agents=[analyst, copywriter, reels_creator],
                        tasks=tasks_list,
                        process=Process.sequential,
                        verbose=False
                    )

                    result = crew.kickoff()
                    status.update(label="✅ Контент-пак успешно сгенерирован!", state="complete", expanded=False)
                    st.balloons()

                    # Сохраняем в локальную JSON историю
                    try:
                        import json
                        from datetime import datetime
                        history_file = "generation_history.json"

                        # Читаем существующую историю
                        history_list = []
                        if os.path.exists(history_file):
                            with open(history_file, "r", encoding="utf-8") as hf:
                                try:
                                    history_list = json.load(hf)
                                except:
                                    pass

                        # Собираем текстовые результаты генерации
                        entry_results = {}
                        for name, fpath in [
                            ("report_data", analyst_file),
                            ("post_data", writer_file),
                            ("reels_data", reels_file),
                            ("funnel_data", funnel_file),
                            ("telegram_data", telegram_file),
                            ("hooks_data", hooks_file),
                            ("brainstorm_data", brainstorm_file)
                        ]:
                            if os.path.exists(fpath):
                                with open(fpath, "r", encoding="utf-8") as f:
                                    entry_results[name] = clean_html(f.read())
                            else:
                                entry_results[name] = ""

                        # Создаем запись
                        new_entry = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "mode": mode,
                            "topic": topic,
                            "inputs": {
                                "tone": tone,
                                "model_name": model_name,
                                "website": website if 'website' in locals() else "https://chipizubova.online",
                                "keyword": keyword if 'keyword' in locals() else "УВЕРЕННОСТЬ",
                                "extra_instructions": extra_instructions,
                                "workout_type": workout_type if 'workout_type' in locals() else "",
                                "meal_type": meal_type if 'meal_type' in locals() else "",
                                "diet_pref": diet_pref if 'diet_pref' in locals() else "",
                                "tg_token": st.session_state["app_tg_token"],
                                "tg_chat_id": st.session_state["app_tg_chat_id"]
                            },
                            "results": entry_results
                        }

                        # Добавляем в начало списка и ограничиваем до 20 записей
                        history_list.insert(0, new_entry)
                        history_list = history_list[:20]

                        with open(history_file, "w", encoding="utf-8") as hf:
                            json.dump(history_list, hf, ensure_ascii=False, indent=2)
                    except Exception as ex:
                        pass

                except Exception as e:
                    status.update(label="❌ Произошла ошибка!", state="error", expanded=True)
                    st.error(f"Ошибка при работе ИИ-агентов: {str(e)}")

    # Отображение результатов (вынесено за пределы кнопки запуска для персистентности)
    has_results = False
    for fpath in [analyst_file, writer_file, reels_file, funnel_file, telegram_file, hooks_file, brainstorm_file]:
        if os.path.exists(fpath):
            has_results = True
            break

    if has_results:
        st.subheader("🎉 Результаты работы ИИ-продюсеров")

        # Читаем данные из файлов
        report_data = ""
        post_data = ""
        reels_data = ""
        funnel_data = ""
        telegram_data = ""
        hooks_data = ""
        brainstorm_data = ""

        if os.path.exists(analyst_file):
            with open(analyst_file, "r", encoding="utf-8") as f:
                report_data = clean_html(f.read())

        if os.path.exists(writer_file):
            with open(writer_file, "r", encoding="utf-8") as f:
                post_data = clean_html(f.read())

        if os.path.exists(reels_file):
            with open(reels_file, "r", encoding="utf-8") as f:
                reels_data = clean_html(f.read())

        if os.path.exists(funnel_file):
            with open(funnel_file, "r", encoding="utf-8") as f:
                funnel_data = clean_html(f.read())

        if os.path.exists(telegram_file):
            with open(telegram_file, "r", encoding="utf-8") as f:
                telegram_data = clean_html(f.read())

        if os.path.exists(hooks_file):
            with open(hooks_file, "r", encoding="utf-8") as f:
                hooks_data = clean_html(f.read())

        if os.path.exists(brainstorm_file):
            with open(brainstorm_file, "r", encoding="utf-8") as f:
                brainstorm_data = clean_html(f.read())

        # Отрисовка вкладок в зависимости от режима
        if mode == "📝 Полный контент-пак (Пост + Сценарий + Воронка в Директ + А/Б Хуки + Telegram)":
            tabs = st.tabs([
                "📝 Instagram Пост", 
                "🎬 Режиссерский Reels", 
                "💬 Воронка в Директ", 
                "⚡ А/Б Хуки (Экран)", 
                "✈️ Пост для Telegram", 
                "🔬 Исследование",
                "📈 Анализ виральности"
            ])

            with tabs[0]:
                st.markdown("### 📝 Сгенерированный текст поста для Instagram")
                edited_post = st.text_area("Редактор поста", value=post_data, height=400)

                col_post_dl, col_post_tg = st.columns(2)
                with col_post_dl:
                    st.download_button("📥 Скачать текст поста (.txt)", data=edited_post, file_name="instagram_post.txt", use_container_width=True)
                with col_post_tg:
                    if st.button("✈️ Отправить пост в Telegram", use_container_width=True):
                        if st.session_state["app_tg_token"] and st.session_state["app_tg_chat_id"]:
                            with st.spinner("Отправляем в Telegram..."):
                                success, msg = send_to_telegram(
                                    st.session_state["app_tg_token"],
                                    st.session_state["app_tg_chat_id"],
                                    f"<b>📝 INSTAGRAM ПОСТ ДЛЯ ЛЮДМИЛЫ:</b>\n\n{edited_post}"
                                )
                                if success:
                                    st.toast(msg)
                                else:
                                    st.error(msg)
                        else:
                            st.warning("⚠️ Пожалуйста, укажите Telegram Bot Token и Chat ID в сайдбаре.")

                st.markdown("---")
                with st.expander("📅 Запланировать этот пост в Календарь"):
                    col_c1, col_c2 = st.columns(2)
                    with col_c1:
                        c_day = st.selectbox("День публикации:", ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"], key="cal_post_day")
                    with col_c2:
                        c_time = st.text_input("Время публикации (ЧЧ:ММ):", value="12:00", key="cal_post_time")
                    if st.button("📅 Сохранить пост в календарь", use_container_width=True):
                        import uuid
                        events = load_calendar()
                        new_event = {
                            "id": str(uuid.uuid4()),
                            "title": f"Instagram Пост: {topic[:30]}...",
                            "day": c_day,
                            "time": c_time,
                            "type": "📝 Instagram Пост",
                            "content": edited_post
                        }
                        events.append(new_event)
                        save_calendar(events)
                        st.success("Пост успешно запланирован в контент-календарь! 📅")

            with tabs[1]:
                st.markdown("### 🎬 Сценарий Reels с режиссерской раскойровкой")
                st.markdown(reels_data if reels_data else "Сценарий Reels отсутствует")

                col_reels_dl, col_reels_tg = st.columns(2)

                if reels_data:
                    st.markdown("---")
                    with st.expander("📅 Запланировать этот Reels в Календарь"):
                        col_cr1, col_cr2 = st.columns(2)
                        with col_cr1:
                            cr_day = st.selectbox("День публикации:", ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"], key="cal_reels_day")
                        with col_cr2:
                            cr_time = st.text_input("Время публикации (ЧЧ:ММ):", value="12:00", key="cal_reels_time")
                        if st.button("📅 Сохранить Reels в календарь", use_container_width=True):
                            import uuid
                            events = load_calendar()
                            new_event = {
                                "id": str(uuid.uuid4()),
                                "title": f"Reels Сценарий: {topic[:30]}...",
                                "day": cr_day,
                                "time": cr_time,
                                "type": "🎬 Reels Сценарий",
                                "content": reels_data
                            }
                            events.append(new_event)
                            save_calendar(events)
                            st.success("Reels успешно запланирован в контент-календарь! 📅")

                    st.markdown("---")
                    st.markdown("### 🖼️ ИИ-Генератор обложки Reels")
                    st.markdown("Сгенерируйте привлекательную, брендированную обложку для вашего Reels, адаптированную под тему!")

                    cover_prompt = st.text_input(
                        "Промпт для генерации изображения (по умолчанию адаптирован под тему):", 
                        value=f"Stunning dynamic fitness coach female active, warm sunset ambient, minimalist clean typography, hyperrealistic, 8k resolution, color palette gray #2c2c2c and warm sand #9a8a88, chipizubova style",
                        key="cover_prompt_input"
                    )

                    col_cov1, col_cov2 = st.columns(2)

                    with col_cov1:
                        if st.button("🖼️ Сгенерировать обложку мгновенно", use_container_width=True):
                            import urllib.parse
                            encoded_prompt = urllib.parse.quote(cover_prompt)
                            pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true"

                            with st.spinner("Создаем стильную обложку с помощью ИИ..."):
                                try:
                                    response = requests.get(pollinations_url, timeout=20)
                                    if response.status_code == 200:
                                        with open("reels_cover_image.png", "wb") as f:
                                            f.write(response.content)
                                        st.success("Обложка успешно создана! 🎉")
                                        st.rerun()
                                    else:
                                        st.error("Не удалось сгенерировать обложку. Попробуйте еще раз.")
                                except Exception as ex:
                                    st.error(f"Ошибка сети: {str(ex)}")

                    with col_cov2:
                        st.info("💡 Нужна обложка премиального качества? Вы также можете попросить ИИ-ассистента в чате запустить профессиональный 8k-рендер!")

                    if os.path.exists("reels_cover_image.png"):
                        st.image("reels_cover_image.png", caption="✨ Сгенерированная ИИ Обложка Reels", width=400)
                        with open("reels_cover_image.png", "rb") as img_file:
                            st.download_button(
                                "📥 Скачать обложку (.png)",
                                data=img_file.read(),
                                file_name="reels_cover_image.png",
                                mime="image/png",
                                use_container_width=True
                            )
                with col_reels_dl:
                    if reels_data:
                        st.download_button("📥 Скачать сценарий Reels (.md)", data=reels_data, file_name="reels_director_script.md", use_container_width=True)
                with col_reels_tg:
                    if reels_data:
                        if st.button("✈️ Отправить сценарий Reels в Telegram", use_container_width=True):
                            if st.session_state["app_tg_token"] and st.session_state["app_tg_chat_id"]:
                                with st.spinner("Отправляем в Telegram..."):
                                    success, msg = send_to_telegram(
                                        st.session_state["app_tg_token"],
                                        st.session_state["app_tg_chat_id"],
                                        f"<b>🎬 СЦЕНАРИЙ REELS ДЛЯ ЛЮДМИЛЫ:</b>\n\n{reels_data}"
                                    )
                                    if success:
                                        st.toast(msg)
                                    else:
                                        st.error(msg)
                            else:
                                st.warning("⚠️ Пожалуйста, укажите Telegram Bot Token и Chat ID в сайдбаре.")

                if reels_data:
                    with st.expander("🗣 Голосовой суфлер (Аудио-репетиция Reels)"):
                        speech_val = extract_speech(reels_data)
                        edited_speech = st.text_area("Текст для озвучки (до 500 символов):", value=speech_val, height=120)
                        if st.button("🔊 Озвучить реплики Reels", use_container_width=True):
                            with st.spinner("Синтезируем русскую озвучку..."):
                                try:
                                    from gtts import gTTS
                                    tts = gTTS(text=edited_speech, lang='ru')
                                    audio_fp = io.BytesIO()
                                    tts.write_to_fp(audio_fp)
                                    audio_fp.seek(0)
                                    st.audio(audio_fp.read(), format='audio/mp3')
                                    st.success("Озвучка успешно сгенерирована! Прослушайте в плеере выше ☝️")
                                except Exception as ex:
                                    st.error(f"Ошибка TTS: {str(ex)}")

            with tabs[2]:
                st.markdown("### 💬 Автоворонка ответов в Директ ManyChat/n8n + Лид-магнит")
                
                if funnel_data:
                    # ⚡ Интерактивная блок-схема автоворонки
                    st.markdown("### ⚡ Интерактивная блок-схема автоворонки")
                    flowchart_html = f"""
                    <style>
                        @keyframes pulse {{
                            0% {{ transform: scale(1); box-shadow: 0 4px 10px rgba(255,75,75,0.05); }}
                            50% {{ transform: scale(1.02); box-shadow: 0 4px 20px rgba(255,75,75,0.15); }}
                            100% {{ transform: scale(1); box-shadow: 0 4px 10px rgba(255,75,75,0.05); }}
                        }}
                        .flow-container {{
                            background-color: #F8F8F8; 
                            border: 1px solid #E5E5E5; 
                            border-radius: 12px; 
                            padding: 25px; 
                            margin-bottom: 25px;
                            font-family: 'Arial', sans-serif;
                        }}
                        .flow-node {{
                            transition: all 0.3s ease;
                        }}
                        .flow-node:hover {{
                            transform: translateY(-2px);
                            box-shadow: 0 6px 15px rgba(0,0,0,0.05) !important;
                        }}
                        .trigger-node {{
                            animation: pulse 3s infinite;
                        }}
                    </style>
                    <div class="flow-container">
                      <div style="display: flex; flex-direction: column; align-items: center; gap: 15px;">
                        
                        <!-- NODE 1: TRIGGER -->
                        <div class="flow-node trigger-node" style="background: linear-gradient(135deg, #FFFFFF 0%, #ff4b4b11 100%); border: 2px solid #ff4b4b; border-radius: 10px; padding: 15px 20px; width: 320px; text-align: center;">
                          <span style="font-size: 10px; color: #ff4b4b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">🚀 1. ТРИГГЕР (Запуск воронки)</span>
                          <p style="margin: 8px 0 0 0; font-weight: bold; color: #2C2C2C; font-size: 15px;">💬 Зритель оставляет комментарий к Reels</p>
                          <span style="font-size: 12px; color: #ff8533; background: rgba(255,133,51,0.1); padding: 4px 12px; border-radius: 6px; display: inline-block; margin-top: 8px; font-weight: bold; border: 1px solid #ff853333;">Кодовое слово: "{keyword}"</span>
                        </div>
                        
                        <!-- ARROW -->
                        <div style="color: #ff4b4b; font-size: 24px; font-weight: bold; margin: -5px 0;">⬇️</div>
                        
                        <!-- NODE 2: AUTO-REPLY -->
                        <div class="flow-node" style="background: #FFFFFF; border: 1px solid #D1D1D1; border-radius: 10px; padding: 15px 20px; width: 320px; text-align: center;">
                          <span style="font-size: 10px; color: #7A6D6B; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">🤖 2. МГНОВЕННЫЙ АВТООТВЕТ В ДИРЕКТ</span>
                          <p style="margin: 8px 0 0 0; font-weight: bold; color: #2C2C2C; font-size: 14px;">✉️ Сообщение 1: Знакомство и триггер</p>
                          <p style="margin: 8px 0 0 0; font-size: 11px; color: #404040; font-style: italic; background-color: #F5F1EE; padding: 6px; border-radius: 5px; text-align: left; line-height: 1.3;">
                            "Привет! Рада твоему интересу к плоскому животу и упругим ягодицам! Жми кнопку ниже, чтобы забрать брендированный PDF-гайд..."
                          </p>
                        </div>
                        
                        <!-- ARROW -->
                        <div style="color: #ff4b4b; font-size: 24px; font-weight: bold; margin: -5px 0;">⬇️</div>
                        
                        <!-- NODE 3: INTERACTION BUTTON -->
                        <div class="flow-node" style="background: linear-gradient(135deg, #ff8533 0%, #ff4b4b 100%); border-radius: 25px; padding: 10px 30px; width: 260px; text-align: center; box-shadow: 0 4px 15px rgba(255,75,75,0.2); cursor: pointer;">
                          <span style="font-size: 13px; font-weight: bold; color: white; text-transform: uppercase; letter-spacing: 1px;">👉 Нажатие кнопки в Директ</span>
                        </div>
                        
                        <!-- ARROW -->
                        <div style="color: #ff8533; font-size: 24px; font-weight: bold; margin: -5px 0;">⬇️</div>
                        
                        <!-- NODE 4: FILE DELIVERY -->
                        <div class="flow-node" style="background: #FFFFFF; border: 1px solid #ff853344; border-radius: 10px; padding: 15px 20px; width: 320px; text-align: center;">
                          <span style="font-size: 10px; color: #ff8533; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">🎁 3. ВЫДАЧА ЛИД-МАГНИТА</span>
                          <p style="margin: 8px 0 0 0; font-weight: bold; color: #2C2C2C; font-size: 14px;">📕 Отправка брендированного PDF-гайда</p>
                          <p style="margin: 5px 0 0 0; font-size: 11px; color: #7A6D6B; font-style: italic;">
                            Пользователь получает PDF, сверстанный строго по бренд-буку Людмилы с CTA-ссылкой
                          </p>
                        </div>
                        
                        <!-- ARROW -->
                        <div style="color: #2e7d32; font-size: 24px; font-weight: bold; margin: -5px 0;">⬇️</div>
                        
                        <!-- NODE 5: GOAL / REDIRECT -->
                        <div class="flow-node" style="background: linear-gradient(135deg, #FFFFFF 0%, #e8f5e9 100%); border: 2px solid #2e7d32; border-radius: 10px; padding: 15px 20px; width: 320px; text-align: center; box-shadow: 0 4px 15px rgba(46,125,50,0.05);">
                          <span style="font-size: 10px; color: #2e7d32; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">🎯 4. ЦЕЛЬ ВОРОНКИ (Конверсия)</span>
                          <p style="margin: 8px 0 0 0; font-weight: bold; color: #2C2C2C; font-size: 15px;">🔥 Переход на сайт и запись на курс</p>
                          <a href="{website}" target="_blank" style="font-size: 12px; color: #2e7d32; display: inline-block; margin-top: 8px; font-weight: bold; text-decoration: underline;">{website} 🔗</a>
                        </div>
                        
                      </div>
                    </div>
                    """
                    st.components.v1.html(flowchart_html, height=670)
                    st.markdown("---")
                
                st.markdown(funnel_data if funnel_data else "Сценарий воронки отсутствует")

                if funnel_data:
                    st.markdown("---")
                    st.markdown("### 🎨 Брендированный PDF Лид-магнит")
                    col_pdf_gen, col_pdf_tg = st.columns(2)

                    pdf_path = "lead_magnet_guide.pdf"

                    with col_pdf_gen:
                        if st.button("🎨 Сгенерировать брендированный PDF-гайд", use_container_width=True):
                            with st.spinner("Верстаем премиальный PDF-гайд по бренд-буку..."):
                                try:
                                    from create_pdf import generate_dynamic_pdf
                                    pdf_title = "Бережное Преображение"
                                    pdf_subtitle = topic[:120] + "..." if len(topic) > 120 else topic
                                    generate_dynamic_pdf(
                                        title=pdf_title,
                                        subtitle=pdf_subtitle,
                                        markdown_content=funnel_data,
                                        website=website,
                                        keyword=keyword,
                                        output_filename=pdf_path
                                    )
                                    st.success("PDF-гайд успешно сгенерирован и оформлен по бренд-буку! 🎉")
                                except Exception as ex:
                                    st.error(f"Не удалось сгенерировать PDF: {str(ex)}")

                        if os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    "📥 Скачать сгенерированный PDF-гайд",
                                    data=f.read(),
                                    file_name="lead_magnet_guide.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )

                    with col_pdf_tg:
                        if st.button("✈️ Отправить воронку + PDF в Telegram", use_container_width=True):
                            if st.session_state["app_tg_token"] and st.session_state["app_tg_chat_id"]:
                                with st.spinner("Отправляем воронку и PDF в Telegram..."):
                                    text_payload = f"<b>💬 ВОРОНКА + ГАЙД ДЛЯ ЛЮДМИЛЫ:</b>\n\nТриггер-слово: <b>{keyword}</b>\nСсылка: {website}\n\nСценарий отправлен во вложении."
                                    has_pdf = os.path.exists(pdf_path)
                                    success, msg = send_to_telegram(
                                        st.session_state["app_tg_token"],
                                        st.session_state["app_tg_chat_id"],
                                        text_payload,
                                        file_path=pdf_path if has_pdf else None
                                    )
                                    if success:
                                        st.toast(msg + (" (PDF-файл прикреплен)" if has_pdf else " (сгенерируйте PDF слева, чтобы отправить и файл)"))
                                    else:
                                        st.error(msg)
                            else:
                                st.warning("⚠️ Пожалуйста, укажите Telegram Bot Token и Chat ID в сайдбаре.")

                    st.download_button("📥 Скачать сырой сценарий воронки (.md)", data=funnel_data, file_name="direct_funnel.md", use_container_width=True)

            with tabs[3]:
                st.markdown("### ⚡ 5 А/Б вариантов хуков для наложения на экран")
                st.markdown(hooks_data if hooks_data else "Хуки отсутствуют")

                col_hooks_dl, col_hooks_tg = st.columns(2)
                with col_hooks_dl:
                    if hooks_data:
                        st.download_button("📥 Скачать варианты хуков (.md)", data=hooks_data, file_name="reels_ab_hooks.md", use_container_width=True)
                with col_hooks_tg:
                    if hooks_data:
                        if st.button("✈️ Отправить хуки в Telegram", use_container_width=True):
                            if st.session_state["app_tg_token"] and st.session_state["app_tg_chat_id"]:
                                with st.spinner("Отправляем в Telegram..."):
                                    success, msg = send_to_telegram(
                                        st.session_state["app_tg_token"],
                                        st.session_state["app_tg_chat_id"],
                                        f"<b>⚡ А/Б ХУКИ ДЛЯ ЛЮДМИЛЫ:</b>\n\n{hooks_data}"
                                    )
                                    if success:
                                        st.toast(msg)
                                    else:
                                        st.error(msg)
                            else:
                                st.warning("⚠️ Пожалуйста, укажите Telegram Bot Token и Chat ID в сайдбаре.")

                if hooks_data:
                    with st.expander("❖ Figma Scripter: Генератор дизайн-кода слайдов"):
                        parsed_hooks = extract_hooks(hooks_data)
                        scripter_payload = generate_scripter_code(parsed_hooks, tone, website)
                        st.markdown("Скопируйте этот JS-код и запустите его в Figma Scripter. Он нарисует Stories-фреймы в фирменных цветах с вашими хуками! 🚀")
                        st.code(scripter_payload, language="javascript")

            with tabs[4]:
                st.markdown("### ✈️ Адаптация поста под Telegram (Пост + Скрипт кружка + Опрос)")
                st.markdown(telegram_data if telegram_data else "Telegram-адаптация отсутствует")

                if telegram_data:
                    st.markdown("---")
                    with st.expander("📅 Запланировать этот Telegram-пост в Календарь"):
                        col_ct1, col_ct2 = st.columns(2)
                        with col_ct1:
                            ct_day = st.selectbox("День публикации:", ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"], key="cal_tg_day")
                        with col_ct2:
                            ct_time = st.text_input("Время публикации (ЧЧ:ММ):", value="12:00", key="cal_tg_time")
                        if st.button("📅 Сохранить Telegram-пост в календарь", use_container_width=True):
                            import uuid
                            events = load_calendar()
                            new_event = {
                                "id": str(uuid.uuid4()),
                                "title": f"Telegram Пост: {topic[:30]}...",
                                "day": ct_day,
                                "time": ct_time,
                                "type": "✈️ Telegram Пост",
                                "content": telegram_data
                            }
                            events.append(new_event)
                            save_calendar(events)
                            st.success("Telegram-пост успешно запланирован в контент-календарь! 📅")

                col_tg_dl, col_tg_send = st.columns(2)
                with col_tg_dl:
                    if telegram_data:
                        st.download_button("📥 Скачать контент для Telegram (.md)", data=telegram_data, file_name="telegram_content.md", use_container_width=True)
                with col_tg_send:
                    if telegram_data:
                        if st.button("✈️ Переслать лонгрид в Telegram", use_container_width=True):
                            if st.session_state["app_tg_token"] and st.session_state["app_tg_chat_id"]:
                                with st.spinner("Отправляем в Telegram..."):
                                    success, msg = send_to_telegram(
                                        st.session_state["app_tg_token"],
                                        st.session_state["app_tg_chat_id"],
                                        f"<b>✈️ TELEGRAM КОНТЕНТ ДЛЯ ЛЮДМИЛЫ:</b>\n\n{telegram_data}"
                                    )
                                    if success:
                                        st.toast(msg)
                                    else:
                                        st.error(msg)
                            else:
                                st.warning("⚠️ Пожалуйста, укажите Telegram Bot Token и Chat ID в сайдбаре.")

                if telegram_data:
                    with st.expander("🗣 Голосовой суфлер (Аудио-репетиция кружка в Telegram)"):
                        circle_val = extract_speech(telegram_data)
                        edited_circle = st.text_area("Текст кружка для озвучки (до 500 символов):", value=circle_val, height=120, key="circle_speech_area")
                        if st.button("🔊 Озвучить кружок", use_container_width=True):
                            with st.spinner("Синтезируем русскую озвучку..."):
                                try:
                                    from gtts import gTTS
                                    tts = gTTS(text=edited_circle, lang='ru')
                                    audio_fp = io.BytesIO()
                                    tts.write_to_fp(audio_fp)
                                    audio_fp.seek(0)
                                    st.audio(audio_fp.read(), format='audio/mp3')
                                    st.success("Озвучка кружка сгенерирована! 🎧")
                                except Exception as ex:
                                    st.error(f"Ошибка TTS: {str(ex)}")

            with tabs[5]:
                st.markdown("### 🔬 Научный разбор темы от Аналитика")
                st.markdown(report_data if report_data else "Аналитический отчет отсутствует")
                if report_data:
                    st.download_button("📥 Скачать отчет аналитика (.md)", data=report_data, file_name="analyst_report.md", use_container_width=True)

            with tabs[6]:
                st.markdown("### 📈 ИИ-Анализатор виральности контента")
                st.markdown("Нажмите кнопку ниже, чтобы запустить глубокий нейросетевой анализ вашего Instagram-поста и сценария Reels на виральность, силу зацепки (хука) и вовлечение.")

                analysis_result_file = "temp_virality_analysis.md"

                if st.button("📊 Запустить анализ виральности", use_container_width=True):
                    if not api_key:
                        st.error("Пожалуйста, введите API-ключ Gemini!")
                    else:
                        with st.spinner("Анализируем эмоциональные триггеры и CTA..."):
                            try:
                                analysis_text = analyze_virality_via_crew(post_data, reels_data, model_name, api_key)
                                with open(analysis_result_file, "w", encoding="utf-8") as f:
                                    f.write(analysis_text)
                                st.success("Анализ виральности успешно завершен!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Ошибка при анализе: {str(e)}")

                if os.path.exists(analysis_result_file):
                    with open(analysis_result_file, "r", encoding="utf-8") as f:
                        analysis_content = f.read()

                    score = 80
                    try:
                        first_line = analysis_content.split("\n")[0]
                        match = re.search(r'Балл:\s*(\d+)', first_line)
                        if match:
                            score = int(match.group(1))
                    except:
                        pass

                    st.markdown(f"#### 🏆 Итоговый индекс виральности: **{score} / 100**")
                    st.progress(score / 100.0)

                    if score >= 90:
                        st.success("🚀 **Исключительный вирусный потенциал!** Этот пост имеет огромный шанс завируситься.")
                    elif score >= 75:
                        st.info("⭐ **Сильный контент.** Отличное удержание внимания и призывы.")
                    else:
                        st.warning("⚠️ **Средний потенциал.** Рекомендуется улучшить хуки.")

                    st.markdown("---")
                    lines = analysis_content.split("\n")
                    if "Балл:" in lines[0]:
                        st.markdown("\n".join(lines[1:]))
                    else:
                        st.markdown(analysis_content)

            # Сохраняем полный контент-пак
            full_result = (
                f"# Полный контент-пак для темы: {topic}\n\n"
                f"## 1. Аналитическое исследование\n{report_data}\n\n"
                f"## 2. Текст поста в Instagram\n{post_data}\n\n"
                f"## 3. Сценарий Reels с раскадровкой\n{reels_data}\n\n"
                f"## 4. Воронка в Директ и Лид-магнит\n{funnel_data}\n\n"
                f"## 5. Варианты А/Б хуков\n{hooks_data}\n\n"
                f"## 6. Telegram контент\n{telegram_data}"
            )
            with open("instagram_post_result.md", "w", encoding="utf-8") as f:
                f.write(full_result)

        elif mode == "🔥 Психологический прогрев для Stories (Запуск фитнес-курса)":
            tabs = st.tabs([
                "🔥 5-дневный Stories Прогрев", 
                "🎬 Поддерживающий Reels", 
                "🔬 Анализ возражений ЦА"
            ])
            
            with tabs[0]:
                st.markdown("### 🔥 Пошаговый 5-дневный Stories-прогрев")
                st.markdown(post_data if post_data else "Сценарий прогрева отсутствует")
                
                st.markdown("---")
                with st.expander("📅 Запланировать этот Stories-прогрев в Календарь"):
                    col_cs1, col_cs2 = st.columns(2)
                    with col_cs1:
                        cs_day = st.selectbox("День публикации:", ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"], key="cal_stories_day")
                    with col_cs2:
                        cs_time = st.text_input("Время публикации (ЧЧ:ММ):", value="12:00", key="cal_stories_time")
                    if st.button("📅 Сохранить Stories в календарь", use_container_width=True):
                        import uuid
                        events = load_calendar()
                        new_event = {
                            "id": str(uuid.uuid4()),
                            "title": f"Stories Прогрев: {topic[:30]}...",
                            "day": cs_day,
                            "time": cs_time,
                            "type": "📝 Stories Прогрев",
                            "content": post_data
                        }
                        events.append(new_event)
                        save_calendar(events)
                        st.success("Прогрев успешно запланирован в контент-календарь! 📅")
                
                if post_data:
                    st.download_button("📥 Скачать Stories-прогрев (.md)", data=post_data, file_name="stories_warmup.md", use_container_width=True)
                
            with tabs[1]:
                st.markdown("### 🎬 Поддерживающий Reels сценарий")
                st.markdown(reels_data if reels_data else "Сценарий Reels отсутствует")
                if reels_data:
                    st.download_button("📥 Скачать Reels (.md)", data=reels_data, file_name="stories_promo_reels.md", use_container_width=True)
                    
            with tabs[2]:
                st.markdown("### 🔬 Анализ возражений и барьеров ЦА")
                st.markdown(report_data if report_data else "Анализ возражений отсутствует")
                if report_data:
                    st.download_button("📥 Скачать анализ ЦА (.md)", data=report_data, file_name="psychological_analysis.md", use_container_width=True)
                    
            full_result = f"# Психологический прогрев Stories\n\n## 1. Stories Прогрев\n{post_data}\n\n## 2. Поддерживающий Reels\n{reels_data}\n\n## 3. Анализ возражений ЦА\n{report_data}"
            with open("stories_warmup_result.md", "w", encoding="utf-8") as f:
                f.write(full_result)

        elif mode == "🗣️ Сценарий Продающего Прямого Эфира / Вебинара":
            tabs = st.tabs([
                "🗣️ Сценарий Эфира (45 мин)", 
                "🎬 Промо-Reels эфира", 
                "🔬 Тезисы и удержание внимания"
            ])
            
            with tabs[0]:
                st.markdown("### 🗣️ Поминутный сценарий прямого эфира")
                st.markdown(post_data if post_data else "Сценарий эфира отсутствует")
                
                st.markdown("---")
                with st.expander("📅 Запланировать эфир в Календарь"):
                    col_cl1, col_cl2 = st.columns(2)
                    with col_cl1:
                        cl_day = st.selectbox("День трансляции:", ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"], key="cal_live_day")
                    with col_cl2:
                        cl_time = st.text_input("Время эфира (ЧЧ:ММ):", value="12:00", key="cal_live_time")
                    if st.button("📅 Сохранить эфир в календарь", use_container_width=True):
                        import uuid
                        events = load_calendar()
                        new_event = {
                            "id": str(uuid.uuid4()),
                            "title": f"Живой Эфир: {topic[:30]}...",
                            "day": cl_day,
                            "time": cl_time,
                            "type": "🎙️ Прямой эфир",
                            "content": post_data
                        }
                        events.append(new_event)
                        save_calendar(events)
                        st.success("Эфир успешно запланирован в контент-календарь! 📅")
                
                if post_data:
                    st.download_button("📥 Скачать сценарий эфира (.md)", data=post_data, file_name="live_stream_script.md", use_container_width=True)
                
            with tabs[1]:
                st.markdown("### 🎬 Промо-Reels сценарий")
                st.markdown(reels_data if reels_data else "Сценарий Reels отсутствует")
                if reels_data:
                    st.download_button("📥 Скачать Reels (.md)", data=reels_data, file_name="live_promo_reels.md", use_container_width=True)
                    
            with tabs[2]:
                st.markdown("### 🔬 Тезисы и триггеры удержания внимания")
                st.markdown(report_data if report_data else "Анализ удержания отсутствует")
                if report_data:
                    st.download_button("📥 Скачать анализ удержания (.md)", data=report_data, file_name="live_thesis_analysis.md", use_container_width=True)
                    
            full_result = f"# Сценарий Продающего Эфира\n\n## 1. Сценарий Эфира\n{post_data}\n\n## 2. Промо-Reels\n{reels_data}\n\n## 3. Тезисы и удержание\n{report_data}"
            with open("live_stream_result.md", "w", encoding="utf-8") as f:
                f.write(full_result)

        elif mode == "💡 Брейншторм 10 вирусных идей для Reels":
            tabs = st.tabs([
                "💡 10 вирусных идей Reels", 
                "🔬 Полный отчет исследований"
            ])

            with tabs[0]:
                st.markdown("### 💡 10 вирусных идей для съемки Reels с ракурсами и звуками")
                st.markdown(brainstorm_data if brainstorm_data else "Идеи Reels отсутствуют")
                if brainstorm_data:
                    st.download_button("📥 Скачать идеи Reels (.md)", data=brainstorm_data, file_name="reels_brainstorm_ideas.md")

            with tabs[1]:
                st.markdown("### 🔬 Дополнительные материалы исследования")
                st.markdown("#### 1. Темы от Аналитика:")
                st.markdown(report_data if report_data else "Отчет отсутствует")
                st.markdown("---")
                st.markdown("#### 2. Разработанные хуки и заголовки от Копирайтера:")
                st.markdown(post_data if post_data else "Отчет отсутствует")

            full_result = f"# Брейншторм 10 идей Reels для темы: {topic}\n\n## Таблица сценариев\n{brainstorm_data}\n\n## 1. Анализ тем от Аналитика\n{report_data}\n\n## 2. Хуки от Копирайтера\n{post_data}"
            with open("reels_brainstorm_result.md", "w", encoding="utf-8") as f:
                f.write(full_result)

        elif mode == "🥗 Фитнес-Рецепт + Reels-Сценарий (ПП под тренировку)":
            tabs = st.tabs([
                "🍳 Сценарий Reels", 
                "📖 Фитнес-Рецепт", 
                "🔬 Польза нутрициолога"
            ])

            with tabs[0]:
                st.markdown("### 🍳 Сценарий Reels для кулинарного процесса (ASMR / Slow-mo)")
                st.markdown(reels_data if reels_data else "Сценарий кулинарного Reels отсутствует")
                if reels_data:
                    st.download_button("📥 Скачать кулинарный сценарий Reels (.md)", data=reels_data, file_name="culinary_reels_script.md")

            with tabs[1]:
                st.markdown("### 📖 Пошаговый рецепт и Instagram-пост")
                st.markdown(post_data if post_data else "Рецепт отсутствует")
                if post_data:
                    st.download_button("📥 Скачать рецепт-пост (.md)", data=post_data, file_name="culinary_post.md")

            with tabs[2]:
                st.markdown("### 🔬 Нутрициологическая польза для восстановления тела")
                st.markdown(report_data if report_data else "Анализ пользы отсутствует")
                if report_data:
                    st.download_button("📥 Скачать отчет аналитика (.md)", data=report_data, file_name="culinary_analyst_report.md")

            full_result = f"# Вирусный рецепт под тренировку\n\n## 1. Сценарий кулинарного Reels\n{reels_data}\n\n## 2. Пост с рецептом\n{post_data}\n\n## 3. Польза нутрициолога\n{report_data}"
            with open("reels_recipe_result.md", "w", encoding="utf-8") as f:
                f.write(full_result)

        elif mode == "⚡ Быстрый А/Б Тест Хуков":
            tabs = st.tabs([
                "⚡ А/Б Хуки и заголовки", 
                "🎥 Идеи видеоряда", 
                "🔬 Анализ темы"
            ])

            with tabs[0]:
                st.markdown("### ⚡ 5 А/Б вариантов хуков для наложения на экран и 2 варианта заголовков")
                st.markdown(post_data if post_data else "Хуки отсутствуют")
                if post_data:
                    st.download_button("📥 Скачать А/Б хуки (.md)", data=post_data, file_name="ab_hooks_fast.md")

            with tabs[1]:
                st.markdown("### 🎥 Концепты съемок и ракурсы под каждый хук")
                st.markdown(reels_data if reels_data else "Идеи съемок отсутствуют")
                if reels_data:
                    st.download_button("📥 Скачать концепты съемок (.md)", data=reels_data, file_name="reels_concepts.md")

            with tabs[2]:
                st.markdown("### 🔬 Психологический анализ темы")
                st.markdown(report_data if report_data else "Анализ отсутствует")
                if report_data:
                    st.download_button("📥 Скачать анализ темы (.md)", data=report_data, file_name="topic_analysis.md")

            full_result = f"# Быстрый А/Б Тест Хуков\n\n## 1. Варианты хуков и заголовков\n{post_data}\n\n## 2. Идеи видеоряда\n{reels_data}\n\n## 3. Анализ темы\n{report_data}"
            with open("hooks_test_result.md", "w", encoding="utf-8") as f:
                f.write(full_result)

        # 🤖 Интерактивная доработка ИИ
        st.markdown("---")
        st.markdown("### 🤖 Интерактивная доработка ИИ")
        st.markdown("Хотите доработать сгенерированный текст? Выберите целевой раздел, введите инструкцию (например, *'добавь больше юмора'*, *'сократи в два раза'*), и ИИ мгновенно обновит контент!")

        col_ed1, col_ed2 = st.columns([1, 2])
        with col_ed1:
            edit_target = st.selectbox(
                "Что редактируем:", 
                ["Instagram Пост", "Сценарий Reels", "Воронка в Директ", "Telegram Пост"],
                key="ai_edit_target"
            )
        with col_ed2:
            edit_instruction = st.text_input(
                "Инструкция для ИИ:", 
                placeholder="например: сделай более дерзким, добавь призыв к действию, сократи...",
                key="ai_edit_instruction"
            )

        if st.button("🪄 Улучшить с помощью ИИ", use_container_width=True):
            if not api_key:
                st.error("Пожалуйста, введите API-ключ Gemini!")
            elif not edit_instruction:
                st.error("Введите инструкцию для доработки!")
            else:
                file_map = {
                    "Instagram Пост": writer_file,
                    "Сценарий Reels": reels_file,
                    "Воронка в Директ": funnel_file,
                    "Telegram Пост": telegram_file
                }
                target_file = file_map[edit_target]
                if os.path.exists(target_file):
                    with open(target_file, "r", encoding="utf-8") as f:
                        current_text = f.read()

                    with st.spinner(f"ИИ редактирует {edit_target}..."):
                        try:
                            improved_text = improve_content_via_crew(
                                current_text, 
                                edit_instruction, 
                                model_name, 
                                api_key
                            )
                            with open(target_file, "w", encoding="utf-8") as f:
                                f.write(improved_text)
                            st.success(f"✨ {edit_target} успешно обновлен!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Ошибка при редактировании: {str(e)}")
                else:
                    st.error("Файл с исходным текстом не найден! Пожалуйста, сгенерируйте контент сначала.")


# --- TAB 1: WEEKLY CONTENT CALENDAR ---
with planner_tab:
    st.subheader("📅 Еженедельный контент-планировщик")
    st.markdown("Здесь вы можете визуализировать свой контент-план на неделю, добавлять публикации вручную или переносить сгенерированный контент в календарь.")
    
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    events = load_calendar()
    
    # Группировка событий по дням
    events_by_day = {day: [] for day in days}
    for event in events:
        day = event.get("day", "Понедельник")
        if day in events_by_day:
            events_by_day[day].append(event)
            
    # Отображение сетки календаря (7 колонок)
    cols = st.columns(7)
    for idx, col in enumerate(cols):
        day_name = days[idx]
        with col:
            # Премиальный заголовок дня
            st.markdown(f"""
            <div style="background-color: #1a1c2a; border-radius: 8px 8px 0 0; padding: 8px 5px; text-align: center; border-bottom: 2px solid #ff8533;">
                <span style="font-weight: bold; color: #ff8533; font-size: 13px;">{day_name}</span>
            </div>
            """, unsafe_allow_html=True)
            
            day_events = events_by_day[day_name]
            # Сортировка по времени
            day_events = sorted(day_events, key=lambda x: x.get("time", "00:00"))
            
            if not day_events:
                st.markdown("""
                <div style="background-color: #121420; border: 1px dashed #232533; border-radius: 0 0 8px 8px; padding: 15px 5px; text-align: center; min-height: 100px;">
                    <span style="color: #64748b; font-size: 11px;">Нет публикаций</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                for event in day_events:
                    card_title = event.get("title", "Без названия")
                    card_time = event.get("time", "12:00")
                    card_type = event.get("type", "Публикация")
                    card_content = event.get("content", "")
                    event_id = event.get("id", "")
                    
                    st.markdown(f"""
                    <div style="background-color: #161823; border: 1px solid #ff4b4b33; border-radius: 8px; padding: 10px; margin-top: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-size: 10px; color: #ff8533; font-weight: bold;">⏰ {card_time}</span>
                            <span style="font-size: 9px; background-color: #232533; color: #94a3b8; padding: 1px 4px; border-radius: 3px;">{card_type.split(" ")[-1]}</span>
                        </div>
                        <p style="font-size: 12px; font-weight: bold; margin: 0; color: #e2e8f0; line-height: 1.2;">{card_title[:25] + '...' if len(card_title) > 25 else card_title}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Кнопки взаимодействия через всплывающее окно
                    with st.popover("🔎 Управление", use_container_width=True):
                        st.markdown(f"**Тип публикации:** {card_type}")
                        st.markdown(f"**Время публикации:** {card_time}")
                        st.markdown(f"**Тема:** {card_title}")
                        st.markdown("---")
                        st.text_area("Текст поста:", value=card_content, height=200, disabled=True, key=f"view_txt_{event_id}")
                        
                        if st.button("🗑 Удалить", key=f"del_{event_id}", use_container_width=True):
                            events = [e for e in events if e.get("id") != event_id]
                            save_calendar(events)
                            st.toast("Публикация удалена из календаря! 🗑")
                            st.rerun()
                            
    st.markdown("---")
    st.markdown("### ➕ Добавить публикацию вручную")
    col_add1, col_add2, col_add3, col_add4 = st.columns([2, 1, 1, 2])
    with col_add1:
        new_title = st.text_input("Заголовок публикации:", key="cal_new_title")
    with col_add2:
        new_day = st.selectbox("День недели:", days, key="cal_new_day")
    with col_add3:
        new_time = st.text_input("Время публикации (ЧЧ:ММ):", value="12:00", key="cal_new_time")
    with col_add4:
        new_type = st.selectbox("Тип контента:", ["📝 Instagram Пост", "🎬 Reels Сценарий", "✈️ Telegram Пост", "💬 Сценарий автоворонки", "Другое"], key="cal_new_type")

    new_content = st.text_area("Текст или описание публикации:", key="cal_new_content")

    if st.button("📅 Запланировать в календарь", use_container_width=True):
        if not new_title:
            st.error("Укажите заголовок публикации!")
        else:
            import uuid
            events = load_calendar()
            new_event = {
                "id": str(uuid.uuid4()),
                "title": new_title,
                "day": new_day,
                "time": new_time,
                "type": new_type,
                "content": new_content
            }
            events.append(new_event)
            save_calendar(events)
            st.success("Публикация успешно добавлена в календарь! 🎉")
            st.rerun()
