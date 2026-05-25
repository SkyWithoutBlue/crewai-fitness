import os

def generate_brand_svg():
    # Размеры фреймов А4 (пропорции ~1:1.41)
    frame_w = 400
    frame_h = 565
    gap = 50
    
    # Полный SVG с двумя фреймами (Обложка и CTA-блок) бок о бок для Figma
    svg_content = f"""<svg width="{frame_w * 2 + gap}" height="{frame_h}" viewBox="0 0 {frame_w * 2 + gap} {frame_h}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Подключение шрифта Geist для Figma -->
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&amp;display=swap');
      .sans-text {{
        font-family: 'Geist', 'Inter', -apple-system, sans-serif;
      }}
    </style>
  </defs>

  <!-- ================================================================= -->
  <!-- ФРЕЙМ 1: ОБЛОЖКА ГАЙДА (x=0, y=0) -->
  <!-- ================================================================= -->
  <g id="Page_1_Cover">
    <!-- Фон фрейма: BG_App (#F5F1EE) -->
    <rect width="{frame_w}" height="{frame_h}" fill="#F5F1EE" rx="16"/>
    
    <!-- 1.1 Оригинальный Логотип по центру (масштабированный) -->
    <g id="Logo_Mark" transform="translate(180, 50) scale(1.2)">
      <rect x="0.109" y="8.9" width="7" height="12" rx="1" transform="rotate(0.52 0.109 8.9)" fill="#2C2C2C"/>
      <rect x="8.63" y="3.95" width="7" height="24" rx="1" transform="rotate(0.52 8.63 3.95)" fill="#2C2C2C"/>
      <rect x="17.35" y="0" width="7" height="30" rx="1" transform="rotate(0.52 17.35 0)" fill="#2C2C2C"/>
      <rect x="34.40" y="22.6" width="7.48" height="17" rx="1" transform="rotate(90.32 34.40 22.6)" fill="#2C2C2C"/>
    </g>

    <!-- 1.2 Надзаголовок (Badge) -->
    <text class="sans-text" x="200" y="140" fill="#7A6D6B" font-size="10" font-weight="600" letter-spacing="0.14em" text-anchor="middle">ЛЮДМИЛА ЧИПИЗУБОВА  |  АВТОРСКИЙ ГАЙД</text>

    <!-- 1.3 Главный заголовок H1 (PRIMARY_DARKER #1A1A1A) -->
    <text class="sans-text" x="200" y="200" fill="#1A1A1A" font-size="34" font-weight="700" letter-spacing="-0.025em" text-anchor="middle">БЕРЕЖНОЕ</text>
    <text class="sans-text" x="200" y="245" fill="#1A1A1A" font-size="34" font-weight="700" letter-spacing="-0.025em" text-anchor="middle">ПРЕОБРАЖЕНИЕ</text>

    <!-- 1.4 Декоративная линия подзаголовка -->
    <rect x="170" y="275" width="60" height="2" fill="#9A8A88" rx="1"/>

    <!-- 1.5 Подзаголовок (Hero subtitle) -->
    <foreignObject x="40" y="300" width="320" height="100">
      <div xmlns="http://www.w3.org/1999/xhtml" class="sans-text" style="color: #6B6B6B; font-size: 13px; line-height: 1.65; text-align: center; font-weight: 400;">
        Как вернуть упругость ягодиц и плоский живот без жестких диет, изнуряющих тренировок и насилия над собой
      </div>
    </foreignObject>

    <!-- 1.6 Слоган бренда -->
    <text class="sans-text" x="200" y="490" fill="#9A8A88" font-size="11" font-weight="700" letter-spacing="0.1em" text-anchor="middle">СИЛЬНОЕ ТЕЛО. УВЕРЕННЫЙ ДУХ.</text>
    
    <!-- 1.7 Адрес сайта -->
    <text class="sans-text" x="200" y="520" fill="#8A8A8A" font-size="11" font-weight="400" text-anchor="middle">chipizubova.online</text>
  </g>

  <!-- ================================================================= -->
  <!-- ФРЕЙМ 2: ЗАКЛЮЧЕНИЕ И CTA (x=450, y=0) -->
  <!-- ================================================================= -->
  <g id="Page_2_CTA" transform="translate({frame_w + gap}, 0)">
    <!-- Фон фрейма: BG_Primary (#FFFFFF) -->
    <rect width="{frame_w}" height="{frame_h}" fill="#FFFFFF" rx="16"/>
    
    <!-- Заголовок страницы -->
    <text class="sans-text" x="30" y="60" fill="#7A6D6B" font-size="18" font-weight="700">Твое путешествие</text>
    <text class="sans-text" x="30" y="85" fill="#7A6D6B" font-size="18" font-weight="700">только начинается...</text>

    <!-- Основной текст -->
    <foreignObject x="30" y="110" width="340" height="150">
      <div xmlns="http://www.w3.org/1999/xhtml" class="sans-text" style="color: #6B6B6B; font-size: 11px; line-height: 1.6; text-align: left;">
        Моя хорошая, то, что ты прочитала этот гайд - уже огромная победа. Ты сделала шаг навстречу своему телу, выбрав путь понимания, а не насилия. Но я знаю, как сложно бывает внедрять новые привычки в одиночку. Иногда опускаются руки, иногда затягивает быт...
      </div>
    </foreignObject>

    <!-- Фирменный CTA-блок с закруглением 24px (rounded-3xl) и заливкой BG_App (#F5F1EE) -->
    <g id="CTA_Card" transform="translate(30, 260)">
      <rect width="340" height="230" fill="#F5F1EE" stroke="#9A8A88" stroke-width="1" rx="24"/>
      
      <!-- Заголовок карточки -->
      <text class="sans-text" x="170" y="30" fill="#7A6D6B" font-size="12" font-weight="700" letter-spacing="0.1em" text-anchor="middle">ЕСЛИ ТЫ ХОЧЕШЬ:</text>
      
      <!-- Пункты списка -->
      <foreignObject x="25" y="45" width="290" height="110">
        <ul xmlns="http://www.w3.org/1999/xhtml" class="sans-text" style="color: #2C2C2C; font-size: 10px; line-height: 1.6; padding-left: 12px; margin: 0;">
          <li style="margin-bottom: 4px;">Получить четкую пошаговую программу тренировок под твой уровень;</li>
          <li style="margin-bottom: 4px;">Питаться вкусно, сытно и наблюдать, как тает талия;</li>
          <li style="margin-bottom: 4px;">Заниматься в поддерживающем женском комьюнити;</li>
          <li>И навсегда забыть о пищевом насилии.</li>
        </ul>
      </foreignObject>

      <!-- Фирменная скругленная CTA-кнопка (rounded-full / pill-button) -->
      <!-- Заливка #2C2C2C, при наведении эффект shine. Вектор скругления 9999px (rx=15 для высоты 30) -->
      <g id="CTA_Button" transform="translate(70, 150)">
        <rect width="200" height="30" fill="#2C2C2C" rx="15"/>
        <text class="sans-text" x="100" y="19" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Выбрать программу</text>
      </g>
      
      <!-- Ссылка на сайт -->
      <text class="sans-text" x="170" y="205" fill="#7A6D6B" font-size="12" font-weight="700" text-anchor="middle">https://chipizubova.online</text>
    </g>

    <!-- Финальная фраза -->
    <text class="sans-text" x="200" y="525" fill="#7A6D6B" font-size="10" font-weight="700" text-anchor="middle">Ты достойна жить в здоровом и любимом теле!</text>
  </g>
</svg>
"""
    svg_filename = "lead_magnet_guide.svg"
    with open(svg_filename, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Figma-ready SVG successfully generated: {svg_filename}")

if __name__ == "__main__":
    generate_brand_svg()
