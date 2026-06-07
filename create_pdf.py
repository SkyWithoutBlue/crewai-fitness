import os
import sys
from fpdf import FPDF

# =========================================================================
# ЦВЕТОВАЯ ПАЛИТРА ИЗ СТАЙЛГАЙДА CHIPIZUBOVA.ONLINE (БРЕНД-БУК МАЙ 2026)
# =========================================================================
c_dark = (44, 44, 44)           # #2C2C2C - PRIMARY_DARK (Тексты, кнопки, лого)
c_darker = (26, 26, 26)         # #1A1A1A - PRIMARY_DARKER (Заголовки H1)
c_light_dark = (64, 64, 64)     # #404040 - PRIMARY_LIGHT (Вторичный текст)

c_accent = (154, 138, 136)      # #9A8A88 - ACCENT (Теплый пепельно-розовый)
c_accent_light = (181, 168, 166)# #B5A8A6 - ACCENT_LIGHT (Мягкий акцент)
c_accent_dark = (122, 109, 107) # #7A6D6B - ACCENT_DARK (Затемненный акцент)

c_text_muted = (107, 107, 107)  # #6B6B6B - TEXT_MUTED (Цвет основного body-текста)
c_text_light = (138, 138, 138)  # #8A8A8A - TEXT_LIGHT (Мета-данные, подсказки)

c_bg_primary = (255, 255, 255)  # #FFFFFF - BG_PRIMARY (Основной фон)
c_bg_secondary = (248, 248, 248)# #F8F8F8 - BG_SECONDARY (FAQ / блоки)
c_bg_app = (245, 241, 238)      # #F5F1EE - BG_APP (Теплый бежевый фон обложки и PWA)

c_border_primary = (229, 229, 229) # #E5E5E5 - BORDER_PRIMARY
c_border_secondary = (209, 209, 209) # #D1D1D1 - BORDER_SECONDARY

def find_system_fonts():
    """Кроссплатформенный поиск шрифтов: Windows (Arial) → Linux (DejaVuSans)."""
    # Windows
    win_regular = r"C:\Windows\Fonts\arial.ttf"
    win_bold = r"C:\Windows\Fonts\arialbd.ttf"
    if os.path.exists(win_regular):
        return win_regular, win_bold if os.path.exists(win_bold) else win_regular

    # Linux / Streamlit Cloud (DejaVuSans — предустановлен в Debian/Ubuntu)
    linux_paths = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/freefont/FreeSans.ttf", "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"),
    ]
    for reg, bold in linux_paths:
        if os.path.exists(reg):
            return reg, bold if os.path.exists(bold) else reg

    return None, None

def setup_pdf_fonts(pdf):
    """Настраивает шрифты PDF с кроссплатформенной поддержкой кириллицы."""
    font_regular, font_bold = find_system_fonts()
    if font_regular:
        pdf.add_font('Arial', '', font_regular)
        pdf.add_font('Arial', 'B', font_bold)
    else:
        # Крайний fallback — встроенный Helvetica (без кириллицы, но не упадёт)
        pass  # fpdf2 имеет встроенный Arial/Helvetica для латиницы


class PremiumPDF(FPDF):
    def header(self):
        # Верхний колонтитул на страницах начиная со 2-й (БЕЗ использования курсива по стайлгайду)
        if self.page_no() > 1:
            self.set_font('Arial', '', 9)
            self.set_text_color(*c_text_light)
            self.cell(0, 10, 'Бережное Преображение  |  chipizubova.online', 0, 1, 'R')
            self.set_draw_color(*c_border_primary)
            self.set_line_width(0.3)
            self.line(20, 20, 190, 20)
            self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 8)
        self.set_text_color(*c_text_light)
        self.cell(0, 10, f'Страница {self.page_no()}', 0, 0, 'C')

def clean_text(text):
    if not text:
        return ""
    # Очистка эмодзи для стабильной генерации кириллицы
    replacements = {
        "✨": "", "🥰": "", "🥺": "", "🌸": "", "👉": "", "🍳": "", "🥗": "", "🔥": "", "💪": "",
        "🌱": "", "🔬": "", "🎯": "", "⚡": "", "🎬": "", "🎵": "", "🍑": "", "🥛": "", "🌾": "",
        "🥦": "", "😋": "", "🎉": "", "✅": "[V]", "❌": "[X]", "💖": "", "❤️": "", "⭐": "",
        "🌿": "", "🧘": "", "🏃‍♀️": "", "🍽️": "", "🍎": "", "🥑": "", "🚶‍♀️": "", "🛌": "",
        "📝": "", "💬": "", "—": "-", "–": "-", "«": '"', "»": '"', "’": "'", "`": "'",
        "…": "...", "“": '"', "”": '"'
    }
    cleaned = text
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    cleaned = "".join(c for c in cleaned if ord(c) < 65536)
    return cleaned

def draw_brand_logo(pdf, x, y):
    """
    Рисует фирменный логотип Людмилы Чипизубовой точно по SVG-координатам из стайлглайда.
    Состоит из 3 вертикальных прямоугольников + 1 горизонтального внизу, образующих 'Л'.
    """
    pdf.set_fill_color(*c_dark) # #2C2C2C
    # 1. Левый прямоугольник
    pdf.rect(x, y + 8.9, 3.5, 12, 'F', round_corners=True, corner_radius=0.8)
    # 2. Средний прямоугольник (выше)
    pdf.rect(x + 4.3, y + 4.0, 3.5, 24, 'F', round_corners=True, corner_radius=0.8)
    # 3. Правый прямоугольник (самый высокий)
    pdf.rect(x + 8.6, y + 0, 3.5, 30, 'F', round_corners=True, corner_radius=0.8)
    # 4. Горизонтальный прямоугольник (повернутый на 90)
    pdf.rect(x + 12.9, y + 17, 12, 3.7, 'F', round_corners=True, corner_radius=0.8)

def generate_guide_pdf():
    pdf = PremiumPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.c_margin = 1
    
    # Подключение шрифтов с кроссплатформенной поддержкой (Windows + Linux/Streamlit Cloud)
    setup_pdf_fonts(pdf)

    # --- СТРАНИЦА 1: ОБЛОЖКА (В БЕЖЕВОМ СТИЛЕ BG_APP) ---
    pdf.add_page()
    
    # Фон обложки - BG_APP (#F5F1EE)
    pdf.set_fill_color(*c_bg_app)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.ln(25)
    
    # Отрисовка оригинального логотипа по центру
    logo_x = (210 - 25) / 2
    draw_brand_logo(pdf, logo_x, pdf.get_y())
    
    pdf.ln(38)
    
    # Надзаголовок (Badge в стиле сайта)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 6, clean_text("ЛЮДМИЛА ЧИПИЗУБОВА  |  АВТОРСКИЙ ГАЙД"), 0, 1, 'C')
    pdf.ln(8)
    
    # Главный заголовок (адаптировано для DejaVuSans)
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(*c_darker)
    pdf.multi_cell(0, 11, clean_text("БЕРЕЖНОЕ\nПРЕОБРАЖЕНИЕ"), 0, 'C')
    pdf.ln(10)
    
    # Подзаголовок
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    subtitle_text = clean_text("Как вернуть упругость ягодиц и плоский живот без жестких диет, изнуряющих тренировок и насилия над собой")
    pdf.multi_cell(0, 7.5, subtitle_text, 0, 'C')
    
    # Декоративный акцентный разделитель (Accent Divider)
    pdf.ln(20)
    pdf.set_draw_color(*c_accent)
    pdf.set_line_width(1.5)
    pdf.line(85, pdf.get_y(), 125, pdf.get_y())
    
    # Футер обложки
    pdf.set_y(-40)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(*c_accent)
    pdf.cell(0, 6, clean_text("СИЛЬНОЕ ТЕЛО. УВЕРЕННЫЙ ДУХ."), 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(*c_text_light)
    pdf.cell(0, 6, clean_text("chipizubova.online"), 0, 1, 'C')

    # --- СТРАНИЦА 2: ВВЕДЕНИЕ ---
    pdf.add_page()
    pdf.set_text_color(*c_dark)
    
    # H2 Заголовок секции
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(*c_dark)
    pdf.cell(0, 10, clean_text("Привет, моя дорогая!"), 0, 1, 'L')
    pdf.ln(5)
    
    # Межстрочный интервал relaxed (6.5) для шрифта 11 (TEXT_MUTED #6B6B6B)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    
    p1 = ("Если этот гайд сейчас в твоих руках, значит, ты тоже устала от бесконечной борьбы со своим телом. "
          "Устала от чувства вины за съеденный кусочек шоколадки, от утренних взвешиваний со страхом в глазах "
          "и от изнурительного кардио, после которого хочется только одного - лечь и не вставать.")
    pdf.multi_cell(0, 6.5, clean_text(p1), 0, 'L')
    pdf.ln(5)
    
    p2 = ("Возможно, тебе знакома эта несправедливость: Ты стараешься, урезаешь калории, бегаешь по дорожке, "
          "а в зеркале видишь, что любимая попа куда-то исчезла и стала плоской, а упрямый животик все равно торчит "
          "и отказывается уходить.")
    pdf.multi_cell(0, 6.5, clean_text(p2), 0, 'L')
    pdf.ln(5)
    
    p3 = ("Давай договоримся сразу: с тобой все в порядке. Ты не ленивая, у тебя есть сила воли, и ты все делаешь "
          "правильно в рамках тех знаний, которые нам годами навязывал фитнес-рынок (\"меньше ешь, больше бегай\"). "
          "Но эти старые методы не просто устарели - они физиологически вредят женскому организму.")
    pdf.multi_cell(0, 6.5, clean_text(p3), 0, 'L')
    pdf.ln(5)
    
    p4 = ("В этом гайде мы обратимся к современной науке, чтобы понять, как работает твое тело, и вернуть ему "
          "упругость, легкость и тонус бережно, сытно и с абсолютной любовью к себе.")
    pdf.multi_cell(0, 6.5, clean_text(p4), 0, 'L')
    pdf.ln(10)

    # --- ЧАСТЬ 1 ---
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("ЧАСТЬ 1. Почему попа теряет форму: разгадка"), 0, 1, 'L')
    pdf.cell(0, 8, clean_text('"сонных ягодиц"'), 0, 1, 'L')
    pdf.set_text_color(*c_dark)
    pdf.ln(4)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    ch1_p1 = ("Ты можешь делать сотни приседаний, но если твои ягодичные мышцы \"выключены\", вместо красивой формы "
              "ты получишь только перегруженную поясницу и уставшие колени.\n\n"
              "В физиологии существует потрясающий термин - взаимное торможение (reciprocal inhibition).\n\n"
              "В чем суть проблемы?\n"
              "Большинство из нас проводит сидя более 8 часов в день (работа, учеба, машина, диван). Когда ты сидишь, "
              "мышцы-сгибатели бедра постоянно находятся в сокращенном, напряженном состоянии. Мозг, пытаясь "
              "оптимизировать ресурсы, буквально блокирует нервные импульсы, идущие к большой ягодичной мышце.\n\n"
              "Спортивный терапевт доктор Стюарт Макгилл назвал это явление \"глютеальной амнезией\" - то есть "
              "ягодичной амнезией. Твоя попа буквально забывает, как работать!")
    pdf.multi_cell(0, 6.5, clean_text(ch1_p1), 0, 'L')
    pdf.ln(6)
    
    # Визуальная схема в закругленной карточке (rounded-2xl = 16px/5mm)
    pdf.set_fill_color(*c_bg_secondary) # #F8F8F8
    pdf.set_draw_color(*c_border_primary) # #E5E5E5
    pdf.set_line_width(0.4)
    
    # Отрисовка закругленной карточки
    card_y = pdf.get_y()
    pdf.rect(20, card_y, 170, 15, 'DF', round_corners=True, corner_radius=5)
    pdf.set_y(card_y + 4.5)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(*c_dark)
    pdf.cell(0, 6, clean_text("  [Долгое сидение] --> [Сжатие сгибателей] --> [Блокировка ягодиц] --> [Амнезия]"), 0, 1, 'C')
    
    pdf.set_y(card_y + 19)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    ch1_p2 = ("Когда ты с такими \"спящими\" ягодицами садишься на диету ниже 1200 ккал и начинаешь бегать, тело "
              "оказывается в ловушке. Ему не хватает энергии, и оно начинает расщеплять собственные мышцы (процесс "
              "саркопении), чтобы выжить. Жир на бедрах остается, а мышечный каркас попы тает. Результат - "
              "плоские, дряблые ягодицы и потерянный тонус кожи.")
    pdf.multi_cell(0, 6.5, clean_text(ch1_p2), 0, 'L')
    
    # --- СТРАНИЦА 3: РЕШЕНИЕ ЧАСТИ 1 & ЧАСТЬ 2 ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("Как мы это решим бережно?"), 0, 1, 'L')
    pdf.set_text_color(*c_dark)
    pdf.ln(3)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    sol1 = ("* Нейромышечная активация перед тренировкой. Не начинай тренировку с тяжелых весов или прыжков. "
            "Сделай легкую разминку-активацию:\n"
            "   - Упражнение \"Ягодичный мост без веса\": ляг на спину, согни колени, подними таз вверх и сожми ягодицы. "
            "Задержись в верхней точке на 3-5 секунд (3 подхода по 15 повторений).\n"
            "   - Упражнение \"Отведение ноги назад на четвереньках\": мягко, подконтрольно отводи ногу назад и вверх, "
            "концентрируясь именно на работе ягодицы, а не поясницы.\n\n"
            "* Умные силовые нагрузки вместо изнурительного кардио. Ягодицы состоят из мощных мышечных волокон, "
            "которые откликаются на силовую нагрузку, а не на многочасовой бег. Выбирай румынскую тягу на одной ноге, "
            "болгарские сплит-приседания, ягодичный мост. Достаточно 2-3 бережных тренировок в неделю!\n\n"
            "* Белок - строительный материал для упругости. Твоя норма: 1.6 - 2.0 г качественного белка на 1 кг веса. "
            "Включай в каждый прием пищи птицу, рыбу, яйца, творог или бобовые.")
    pdf.multi_cell(0, 6.5, clean_text(sol1), 0, 'L')
    pdf.ln(10)
    
    # ЧАСТЬ 2
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("ЧАСТЬ 2. Почему растет живот: феномен"), 0, 1, 'L')
    pdf.cell(0, 8, clean_text('"кортизолового животика"'), 0, 1, 'L')
    pdf.set_text_color(*c_dark)
    pdf.ln(4)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    ch2_p1 = ("\"Я почти ничего не ем, а живот все равно на месте!\" - как часто я слышу эту фразу. И наука дает на "
              "это очень четкий ответ.\n\n"
              "В чем суть проблемы?\n"
              "Жесткие диеты, дефицит калорий ниже базового метаболизма (менее 1200 ккал), постоянные переживания и "
              "плохой сон воспринимаются твоим древним организмом как сигнал бедствия: \"Внимание! Наступил голод и "
              "война, нужно выживать!\".\n\n"
              "В ответ на этот стресс надпочечники начинают активно вырабатывать гормон кортизол.\n\n"
              "Важный научный факт: у жировых клеток в области живота плотность рецепторов к кортизолу в несколько "
              "раз выше, чем в любой другой части тела! Высокий кортизол заставляет твой организм судорожно копить "
              "жир именно на животе (\"кортизоловый живот\") и задерживать воду. Пытаясь похудеть с помощью голода, "
              "ты буквально заставляешь свой живот расти.")
    pdf.multi_cell(0, 6.5, clean_text(ch2_p1), 0, 'L')

    # --- СТРАНИЦА 4: РЕШЕНИЕ ЧАСТИ 2 & ЧАСТЬ 3 ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("Как мы это решим бережно?"), 0, 1, 'L')
    pdf.set_text_color(*c_dark)
    pdf.ln(3)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    sol2 = ("* Комфортный дефицит калорий (всего 10-15%). Никаких голодовок! Если для поддержания веса тебе "
            "нужно 2000 ккал, мы мягко снижаем планку до 1700-1800 ккал. Ты будешь сытой, довольной, гормоны будут "
            "спокойны, а жир начнет уходить без паники со стороны организма.\n\n"
            "* Углеводы - твои друзья, а не враги. Полный отказ от углеводов взвинчивает кортизол до небес и гарантирует "
            "срывы. Добавляй сложные углеводы (гречка, киноа, овсянка долгой варки, бурый рис). Они помогают вырабатывать "
            "серотонин (гормон радости) и стабилизируют нервную систему.\n\n"
            "* Волшебство сна. Исследования доказали: если ты спишь менее 7-8 часов, твой организм теряет на 55% меньше "
            "жира и на 60% больше мышц при абсолютно одинаковом питании! Ложись спать до 23:00 в темной, прохладной "
            "комнате. Позволь себе восстановиться.")
    pdf.multi_cell(0, 6.5, clean_text(sol2), 0, 'L')
    pdf.ln(10)
    
    # ЧАСТЬ 3
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("ЧАСТЬ 3. Живот, который торчит даже у худых:"), 0, 1, 'L')
    pdf.cell(0, 8, clean_text("восстанавливаем микробиом"), 0, 1, 'L')
    pdf.set_text_color(*c_dark)
    pdf.ln(4)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    ch3_p1 = ("Бывает так: девушка очень стройная, жира на теле практически нет, а в профиль животик все равно "
              "выдается вперед, напоминая шарик. В 90% случаев это не жир. Это вздутие кишечника (дистензия).\n\n"
              "В чем суть проблемы?\n"
              "Когда мы садимся на однообразную диету (\"куриная грудка и огурцы\"), мы устраиваем экологическую "
              "катастрофу внутри своего кишечника. Без разнообразия пищевых волокон полезные бактерии погибают. "
              "Еда начинает застаиваться, вызывая процессы брожения. Кишечник раздувается, а ослабленная поперечная "
              "мышца живота (наш естественный внутренний корсет) не способна удержать этот объем.")
    pdf.multi_cell(0, 6.5, clean_text(ch3_p1), 0, 'L')

    # --- СТРАНИЦА 5: РЕШЕНИЕ ЧАСТИ 3 & ПОШАГОВЫЙ ПЛАН ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("Как мы это решим бережно?"), 0, 1, 'L')
    pdf.set_text_color(*c_dark)
    pdf.ln(3)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    sol3 = ("* Правило \"30 растений в неделю\". Старайся, чтобы в течение недели в твоем рационе присутствовало "
            "30 разных видов растительной пищи (зелень, овощи, орехи, семена, крупы, ягоды). Чем разнообразнее пища, "
            "тем счастливее твоя микрофлора и тем более плоским становится твой живот!\n\n"
            "* Натуральные ферментированные продукты. Добавь в рацион квашеную капусту, кимчи или натуральный йогурт "
            "без сахара. Это живые пробиотики, которые уберут вздутие.\n\n"
            "* Активация глубокого мышечного корсета. Вместо классических скручиваний на пресс, делай упражнения "
            "на глубокую поперечную мышцу живота (например, упражнение \"Мертвый жук\" или дыхание животом). "
            "Это укрепит внутренний мышечный корсет, который будет держать твой животик плоским весь день.")
    pdf.multi_cell(0, 6.5, clean_text(sol3), 0, 'L')
    pdf.ln(10)
    
    # ПОШАГОВЫЙ ПЛАН
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("ТВОЙ ПОШАГОВЫЙ ПЛАН НА НЕДЕЛЮ"), 0, 1, 'L')
    pdf.set_text_color(*c_dark)
    pdf.ln(4)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    plan = ("* Понедельник: Купи в магазине 5 новых видов зелени или овощей, которые раньше не пробовала "
            "(например, рукколу, шпинат, цветную капусту). Начни собирать свои \"30 растений\".\n"
            "* Вторник: Сделай легкую 15-минутную домашнюю тренировку на ягодицы. Начни с 5 минут активации.\n"
            "* Среда: Обрати внимание на свою тарелку. Пусть половину ее займут сочные овощи, четверть - упругий белок "
            "(курочка, рыба или яйца) и четверть - любимый гарнир.\n"
            "* Четверг: Устрой \"вечер без гаджетов\" за 1 час до сна. Прими теплую ванну и ляг спать в 22:30. "
            "Дай своему кортизолу снизиться, а животику - расслабиться.\n"
            "* Пятница: Повтори тренировку на ягодицы. Добавь чуть больше контроля в движениях.\n"
            "* Суббота и Воскресенье: Прогуляйся на свежем воздухе. Сделай 8 000 - 10 000 шагов в приятном темпе. "
            "Это идеальный, мягкий способ жиросжигания без стресса.")
    pdf.multi_cell(0, 6.5, clean_text(plan), 0, 'L')

    # --- СТРАНИЦА 6: ЗАКЛЮЧЕНИЕ & CTA-КАРТОЧКА (rounded-3xl = 24px/8mm) ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("Твое путешествие только начинается..."), 0, 1, 'L')
    pdf.set_text_color(*c_dark)
    pdf.ln(4)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    conc1 = ("Моя хорошая, то, что ты прочитала этот гайд - уже огромная победа. Ты сделала шаг навстречу своему "
             "телу, выбрав путь понимания, а не насилия.\n\n"
             "Но я знаю, как сложно бывает внедрять новые привычки в одиночку. Иногда опускаются руки, иногда затягивает "
             "быт, иногда просто нужен человек, который бережно возьмет за руку, подскажет правильную технику упражнений, "
             "составит вкусное, сытное меню без пресной грудки и скажет: \"Ты все делаешь правильно, у тебя все получается\".\n\n"
             "Именно для этого я создала свою авторскую, бережную систему преображения. Без изнурительных диет, без слез "
             "в спортзале, с фокусом на женское здоровье, гормональный баланс и любовь к себе.")
    pdf.multi_cell(0, 6.5, clean_text(conc1), 0, 'L')
    pdf.ln(8)
    
    # Премиальный CTA-блок с закруглением 24px (8мм) в кремовом стиле BG_APP
    pdf.set_fill_color(*c_bg_app) # #F5F1EE
    pdf.set_draw_color(*c_accent) # #9A8A88
    pdf.set_line_width(0.5)
    
    start_y = pdf.get_y()
    
    # Рисуем закругленный фоновый бокс для CTA (высота 66мм)
    pdf.rect(20, start_y, 170, 66, 'DF', round_corners=True, corner_radius=8)
    
    pdf.set_y(start_y + 4)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 6, clean_text("ЕСЛИ ТЫ ХОЧЕШЬ:"), 0, 1, 'C')
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(*c_dark)
    cta_bullets = ("- Получить четкую, пошаговую программу тренировок под твой уровень подготовки;\n"
                   "- Питаться вкусно, сытно и разнообразно, наблюдая, как тает талия и подтягиваются ягодицы;\n"
                   "- Заниматься в поддерживающем, мягком комьюнити единомышленниц;\n"
                   "- И навсегда забыть о пищевом насилии...")
    pdf.multi_cell(0, 5, clean_text(cta_bullets), 0, 'C')
    pdf.ln(4)
    
    # Отрисовка фирменной скругленной кнопки (rounded-full / pill-button)
    # Ширина 65мм, высота 10мм, радиус скругления 5мм. Заливка c_dark (#2C2C2C), текст белый.
    btn_w = 65
    btn_h = 10
    btn_x = (210 - btn_w) / 2
    btn_y = pdf.get_y()
    
    pdf.set_fill_color(*c_dark)
    pdf.rect(btn_x, btn_y, btn_w, btn_h, 'F', round_corners=True, corner_radius=5)
    
    pdf.set_y(btn_y + 2)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(255, 255, 255) # Белый текст
    pdf.cell(0, 6, clean_text("Выбрать программу"), 0, 1, 'C')
    
    pdf.set_y(btn_y + 12)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 6, clean_text("https://chipizubova.online"), 0, 1, 'C')
    
    pdf.set_y(start_y + 72)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(0, 8, clean_text("Ты достойна того, чтобы жить в упругом, здоровом и любимом теле."), 0, 1, 'C')
    pdf.cell(0, 8, clean_text("До встречи на программе!"), 0, 1, 'C')

    # Сохранение итогового PDF
    pdf_filename = "lead_magnet_guide.pdf"
    pdf.output(pdf_filename)
    print(f"PDF successfully generated in full accordance with Style Guide: {pdf_filename}")

def generate_dynamic_pdf(title="БЕРЕЖНОЕ ПРЕОБРАЖЕНИЕ", subtitle="Как вернуть упругость ягодиц и плоский живот...", markdown_content="", website="https://chipizubova.online", keyword="УВЕРЕННОСТЬ", output_filename="lead_magnet_guide.pdf"):
    pdf = PremiumPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(15, 15, 15)  # Чуть шире для совместимости с DejaVuSans
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.c_margin = 1  # Уменьшаем внутренний отступ ячеек (по умолчанию 2)
    
    setup_pdf_fonts(pdf)

    W = 210  # Ширина A4
    CONTENT_W = W - 30  # 180mm доступная ширина

    # --- СТРАНИЦА 1: ОБЛОЖКА ---
    pdf.add_page()
    pdf.set_fill_color(*c_bg_app)
    pdf.rect(0, 0, W, 297, 'F')
    
    pdf.ln(25)
    logo_x = (W - 25) / 2
    draw_brand_logo(pdf, logo_x, pdf.get_y())
    pdf.ln(38)
    
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(CONTENT_W, 6, clean_text("ЛЮДМИЛА ЧИПИЗУБОВА  |  ИНДИВИДУАЛЬНЫЙ ГАЙД"), 0, 1, 'C')
    pdf.ln(8)
    
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(*c_darker)
    pdf.multi_cell(CONTENT_W, 10, clean_text(title.upper()), 0, 'C')
    pdf.ln(10)
    
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*c_text_muted)
    pdf.multi_cell(CONTENT_W, 6.5, clean_text(subtitle), 0, 'C')
    
    pdf.ln(20)
    pdf.set_draw_color(*c_accent)
    pdf.set_line_width(1.5)
    pdf.line(85, pdf.get_y(), 125, pdf.get_y())
    
    pdf.set_y(-40)
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(*c_accent)
    pdf.cell(CONTENT_W, 6, clean_text("СИЛЬНОЕ ТЕЛО. УВЕРЕННЫЙ ДУХ."), 0, 1, 'C')
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(*c_text_light)
    pdf.cell(CONTENT_W, 6, clean_text(website.replace("https://", "").replace("http://", "")), 0, 1, 'C')

    # --- СТРАНИЦЫ КОНТЕНТА ---
    pdf.add_page()
    pdf.set_text_color(*c_dark)
    
    lines = markdown_content.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue
        
        pdf.set_x(pdf.l_margin)
            
        if line.startswith("# "):
            header_text = line[2:].strip()
            if pdf.page_no() > 2 and pdf.get_y() > 60:
                pdf.add_page()
            pdf.set_x(pdf.l_margin)
            pdf.set_font('Arial', 'B', 16)
            pdf.set_text_color(*c_darker)
            pdf.multi_cell(CONTENT_W, 8, clean_text(header_text), 0, 'L')
            pdf.ln(4)
        elif line.startswith("## "):
            header_text = line[3:].strip()
            if pdf.get_y() > 220:
                pdf.add_page()
            pdf.ln(4)
            pdf.set_x(pdf.l_margin)
            pdf.set_font('Arial', 'B', 13)
            pdf.set_text_color(*c_accent_dark)
            pdf.multi_cell(CONTENT_W, 7, clean_text(header_text), 0, 'L')
            pdf.ln(3)
        elif line.startswith("### "):
            header_text = line[4:].strip()
            if pdf.get_y() > 230:
                pdf.add_page()
            pdf.ln(3)
            pdf.set_x(pdf.l_margin)
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(*c_accent_dark)
            pdf.multi_cell(CONTENT_W, 6, clean_text(header_text), 0, 'L')
            pdf.ln(2)
        elif line.startswith("* ") or line.startswith("- "):
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(*c_text_muted)
            pdf.multi_cell(CONTENT_W, 5.5, clean_text(f"  {line[2:]}"), 0, 'L')
        elif len(line) > 2 and line[0].isdigit() and line[1] in '.':
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(*c_text_muted)
            pdf.multi_cell(CONTENT_W, 5.5, clean_text(line), 0, 'L')
        else:
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(*c_text_muted)
            pdf.multi_cell(CONTENT_W, 5.5, clean_text(line), 0, 'L')

    # --- СТРАНИЦА ЗАКЛЮЧЕНИЯ И CTA ---
    if pdf.get_y() > 180:
        pdf.add_page()
    else:
        pdf.ln(10)
        
    start_y = pdf.get_y()
    card_w = CONTENT_W
    card_x = pdf.l_margin
    
    pdf.set_fill_color(*c_bg_app)
    pdf.set_draw_color(*c_accent)
    pdf.set_line_width(0.5)
    pdf.rect(card_x, start_y, card_w, 66, 'DF', round_corners=True, corner_radius=8)
    
    pdf.set_y(start_y + 4)
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(CONTENT_W, 6, clean_text("ХОЧЕШЬ БЕРЕЖНОГО ПРЕОБРАЖЕНИЯ?"), 0, 1, 'C')
    pdf.ln(2)
    
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(*c_dark)
    cta_bullets = (f"- Получи пошаговую программу тренировок под свой уровень;\n"
                   f"- Питайся вкусно и разнообразно, снижая вес без жестких диет;\n"
                   f"- Напиши кодовое слово '{keyword}' в комментариях к Reels;\n"
                   f"- И начни менять свою жизнь прямо сейчас!")
    pdf.multi_cell(CONTENT_W, 5, clean_text(cta_bullets), 0, 'C')
    pdf.ln(4)
    
    btn_w = 60
    btn_h = 9
    btn_x = (W - btn_w) / 2
    btn_y = pdf.get_y()
    
    pdf.set_fill_color(*c_dark)
    pdf.rect(btn_x, btn_y, btn_w, btn_h, 'F', round_corners=True, corner_radius=4.5)
    
    pdf.set_y(btn_y + 1.5)
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(CONTENT_W, 6, clean_text("Начать преображение"), 0, 1, 'C')
    
    pdf.set_y(btn_y + 11)
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(CONTENT_W, 6, clean_text(website.replace("https://", "").replace("http://", "")), 0, 1, 'C')
    
    pdf.set_y(start_y + 72)
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(*c_accent_dark)
    pdf.cell(CONTENT_W, 8, clean_text("Ты достойна жить в красивом, сильном и здоровом теле."), 0, 1, 'C')
    
    pdf.output(output_filename)
    return output_filename

if __name__ == "__main__":
    generate_guide_pdf()


