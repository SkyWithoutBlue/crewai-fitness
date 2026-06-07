// ============================================================
// FIGMA CONSOLE CODE — Гайд «Уверенность — это навык»
// Вставьте в Figma → DevTools (Ctrl+Alt+I) → Console → Enter
// ============================================================

(async () => {
  // ---------- БРЕНД-СТИЛЬ ----------
  const BRAND = {
    dark: { r: 0.173, g: 0.173, b: 0.173 },       // #2C2C2C
    darker: { r: 0.102, g: 0.102, b: 0.102 },      // #1A1A1A
    accent: { r: 0.604, g: 0.541, b: 0.533 },      // #9A8A88
    accentDark: { r: 0.478, g: 0.427, b: 0.420 },  // #7A6D6B
    textMuted: { r: 0.420, g: 0.420, b: 0.420 },   // #6B6B6B
    textLight: { r: 0.541, g: 0.541, b: 0.541 },   // #8A8A8A
    bgApp: { r: 0.961, g: 0.945, b: 0.933 },       // #F5F1EE
    bgCard: { r: 0.973, g: 0.973, b: 0.973 },      // #F8F8F8
    white: { r: 1, g: 1, b: 1 },
    border: { r: 0.898, g: 0.898, b: 0.898 },      // #E5E5E5
  };

  const W = 1080;
  const H = 1350;

  // ---------- Загрузка шрифта Roboto ----------
  await figma.loadFontAsync({ family: "Roboto", style: "Regular" });
  await figma.loadFontAsync({ family: "Roboto", style: "Medium" });
  await figma.loadFontAsync({ family: "Roboto", style: "Bold" });

  // ---------- ХЕЛПЕРЫ ----------
  function createText(parent, x, y, w, content, size, style, color, align) {
    const t = figma.createText();
    t.x = x;
    t.y = y;
    t.resize(w, 1);
    t.textAutoResize = "HEIGHT";
    t.fontName = { family: "Roboto", style: style || "Regular" };
    t.fontSize = size;
    t.characters = content;
    t.fills = [{ type: "SOLID", color: color }];
    t.textAlignHorizontal = align || "LEFT";
    t.lineHeight = { value: size * 1.5, unit: "PIXELS" };
    parent.appendChild(t);
    return t;
  }

  function createRect(parent, x, y, w, h, color, radius) {
    const r = figma.createRectangle();
    r.x = x;
    r.y = y;
    r.resize(w, h);
    r.fills = [{ type: "SOLID", color: color }];
    if (radius) r.cornerRadius = radius;
    parent.appendChild(r);
    return r;
  }

  function createSlide(name, bgColor) {
    const frame = figma.createFrame();
    frame.name = name;
    frame.resize(W, H);
    frame.fills = [{ type: "SOLID", color: bgColor }];
    return frame;
  }

  const slides = [];
  let offsetX = 0;

  // ============================================================
  // СЛАЙД 1: ОБЛОЖКА
  // ============================================================
  const s1 = createSlide("01 — Обложка", BRAND.bgApp);
  s1.x = offsetX; offsetX += W + 80;

  // Декоративная линия сверху
  createRect(s1, 0, 0, W, 6, BRAND.accent, 0);

  // Бейдж
  createRect(s1, 290, 280, 500, 50, BRAND.white, 25);
  createText(s1, 290, 290, 500, "ЛЮДМИЛА ЧИПИЗУБОВА  |  ГАЙД", 22, "Medium", BRAND.accentDark, "CENTER");

  // Главный заголовок
  createText(s1, 100, 420, 880, "УВЕРЕННОСТЬ —\nЭТО НАВЫК", 96, "Bold", BRAND.darker, "CENTER");

  // Подзаголовок
  createText(s1, 120, 680, 840, "Как перестать сомневаться и начать\nдействовать: научный подход к прокачке\nуверенности через тело и мозг", 34, "Regular", BRAND.textMuted, "CENTER");

  // Акцентная линия
  createRect(s1, 440, 900, 200, 4, BRAND.accent, 2);

  // Слоган
  createText(s1, 100, 950, 880, "СИЛЬНОЕ ТЕЛО. УВЕРЕННЫЙ ДУХ.", 26, "Bold", BRAND.accent, "CENTER");

  // Сайт
  createText(s1, 100, 1010, 880, "chipizubova.online", 24, "Regular", BRAND.textLight, "CENTER");

  // Номер слайда
  createText(s1, 100, 1250, 880, "1 / 5", 20, "Regular", BRAND.textLight, "CENTER");

  slides.push(s1);

  // ============================================================
  // СЛАЙД 2: ПЕТЛЯ КОМПЕТЕНЦИЙ
  // ============================================================
  const s2 = createSlide("02 — Петля компетенций", BRAND.white);
  s2.x = offsetX; offsetX += W + 80;

  createRect(s2, 0, 0, W, 6, BRAND.accent, 0);

  createText(s2, 80, 70, 920, "ЧАСТЬ 1", 22, "Bold", BRAND.accent, "LEFT");
  createText(s2, 80, 110, 920, "Петля отсутствия\nкомпетенций", 64, "Bold", BRAND.darker, "LEFT");

  // Карточка с фактом
  createRect(s2, 60, 310, 960, 200, BRAND.bgApp, 24);
  createText(s2, 100, 335, 880, "НАУЧНЫЙ ФАКТ", 20, "Bold", BRAND.accentDark, "LEFT");
  createText(s2, 100, 375, 880, "Уверенность — это побочный продукт\nкомпетентности. Она не приходит ДО действия,\nона приходит ПОСЛЕ накопленного опыта.", 30, "Regular", BRAND.textMuted, "LEFT");

  // Визуальная схема
  createRect(s2, 60, 550, 960, 80, BRAND.bgCard, 16);
  createText(s2, 80, 565, 920, "Нет опыта → Мозг: «Опасно!» → Блокировка → Бездействие", 26, "Medium", BRAND.dark, "CENTER");

  // Решение
  createRect(s2, 60, 680, 960, 340, BRAND.white, 24);
  const s2border = createRect(s2, 60, 680, 960, 340, BRAND.white, 24);
  s2border.strokes = [{ type: "SOLID", color: BRAND.border }];
  s2border.strokeWeight = 2;

  createText(s2, 100, 710, 880, "РЕШЕНИЕ: МЕТОД МИКРО-ПОБЕД", 24, "Bold", BRAND.accentDark, "LEFT");
  createText(s2, 100, 760, 880, "1.  Разбей задачу на 10 маленьких частей\n2.  Выполни первую, самую простую\n3.  Зафиксируй результат — запиши!\n4.  Получи дофаминовый отклик\n5.  Мозг записал: «Я могу»", 28, "Regular", BRAND.textMuted, "LEFT");

  // Пример
  createRect(s2, 60, 1060, 960, 180, BRAND.bgApp, 20);
  createText(s2, 100, 1085, 880, "ПРИМЕР", 18, "Bold", BRAND.accent, "LEFT");
  createText(s2, 100, 1120, 880, "Страшно в зал? Не начинай с часовой программы.\n5 приседаний дома → 10 завтра → через неделю\nты уже в зале, и это ощущается естественно.", 26, "Regular", BRAND.textMuted, "LEFT");

  createText(s2, 100, 1260, 880, "2 / 5", 20, "Regular", BRAND.textLight, "CENTER");

  slides.push(s2);

  // ============================================================
  // СЛАЙД 3: ГОРМОНАЛЬНЫЙ ШУМ
  // ============================================================
  const s3 = createSlide("03 — Гормональный шум", BRAND.white);
  s3.x = offsetX; offsetX += W + 80;

  createRect(s3, 0, 0, W, 6, BRAND.accent, 0);

  createText(s3, 80, 70, 920, "ЧАСТЬ 2", 22, "Bold", BRAND.accent, "LEFT");
  createText(s3, 80, 110, 920, "Гормональный шум\nи «голос страха»", 64, "Bold", BRAND.darker, "LEFT");

  // Факт-карточка
  createRect(s3, 60, 320, 960, 180, BRAND.bgApp, 24);
  createText(s3, 100, 345, 880, "НАУЧНЫЙ ФАКТ", 20, "Bold", BRAND.accentDark, "LEFT");
  createText(s3, 100, 385, 880, "Ты не можешь «думать» уверенно, если\nтвой организм в состоянии стресса. Недосып\nснижает активность префронтальной коры на 60%.", 28, "Regular", BRAND.textMuted, "LEFT");

  // Биохимия — 4 карточки
  const bioItems = [
    "Высокий кортизол\nподавляет серотонин",
    "Низкий серотонин\nусиливает тревожность",
    "Нестабильный сахар\nперепады настроения",
    "Недосып: кора\nмозга «спит»"
  ];
  for (let i = 0; i < 4; i++) {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const cx = 60 + col * 490;
    const cy = 540 + row * 170;
    createRect(s3, cx, cy, 470, 150, BRAND.bgCard, 20);
    createText(s3, cx + 30, cy + 35, 410, bioItems[i], 28, "Medium", BRAND.dark, "LEFT");
  }

  // Решение
  createText(s3, 80, 920, 920, "РЕШЕНИЕ: ЗАКРОЙ БАЗУ", 24, "Bold", BRAND.accentDark, "LEFT");
  createText(s3, 80, 970, 920, "•  Сон 7-8 часов, ложись до 23:00\n•  Белок в каждый приём пищи\n•  Сложные углеводы для серотонина\n•  20 мин прогулки = −30% кортизола", 28, "Regular", BRAND.textMuted, "LEFT");

  createText(s3, 100, 1260, 880, "3 / 5", 20, "Regular", BRAND.textLight, "CENTER");

  slides.push(s3);

  // ============================================================
  // СЛАЙД 4: ПРАВИЛО 5 МИНУТ
  // ============================================================
  const s4 = createSlide("04 — Правило 5 минут", BRAND.white);
  s4.x = offsetX; offsetX += W + 80;

  createRect(s4, 0, 0, W, 6, BRAND.accent, 0);

  createText(s4, 80, 70, 920, "ЧАСТЬ 3", 22, "Bold", BRAND.accent, "LEFT");
  createText(s4, 80, 110, 920, "Иллюзия\n«идеального момента»", 64, "Bold", BRAND.darker, "LEFT");

  // Факт
  createRect(s4, 60, 320, 960, 160, BRAND.bgApp, 24);
  createText(s4, 100, 340, 880, "НАУЧНЫЙ ФАКТ", 20, "Bold", BRAND.accentDark, "LEFT");
  createText(s4, 100, 378, 880, "Мотивация не появляется ДО действия —\nона появляется В ПРОЦЕССЕ. Страх не исчезнет,\nпока ты не начнёшь.", 28, "Regular", BRAND.textMuted, "LEFT");

  // Правило 5 минут — большая карточка
  createRect(s4, 60, 530, 960, 380, BRAND.dark, 24);
  createText(s4, 100, 560, 880, "ПРАВИЛО 5 МИНУТ", 32, "Bold", BRAND.white, "CENTER");
  createText(s4, 100, 620, 880, "Пообещай себе заниматься делом\nвсего 5 минут. После преодоления порога\nвхода страх отступает.", 30, "Regular", { r: 0.85, g: 0.85, b: 0.85 }, "CENTER");

  createText(s4, 100, 780, 880, "Не хочешь тренироваться?\n→ Надень форму и сделай 5 мин разминки\n\nНе хочешь готовить полезное?\n→ Просто порежь один овощ", 26, "Regular", { r: 0.75, g: 0.75, b: 0.75 }, "CENTER");

  // 7-дневный план (компактно)
  createText(s4, 80, 960, 920, "ТВОЙ 7-ДНЕВНЫЙ ПЛАН", 24, "Bold", BRAND.accentDark, "LEFT");

  const days = [
    "День 1 — Запиши 3 своих победы за месяц",
    "День 2 — Сон до 23:00 + белок в завтрак",
    "День 3 — Сделай одно дело на 5 минут",
    "День 4 — 20 мин прогулки без телефона",
    "День 5 — Разбей большую задачу на 5 шагов",
    "День 6 — Замени «не могу» на «пока учусь»",
    "День 7 — Оцени изменения за неделю"
  ];
  createText(s4, 80, 1005, 920, days.join("\n"), 24, "Regular", BRAND.textMuted, "LEFT");

  createText(s4, 100, 1260, 880, "4 / 5", 20, "Regular", BRAND.textLight, "CENTER");

  slides.push(s4);

  // ============================================================
  // СЛАЙД 5: CTA
  // ============================================================
  const s5 = createSlide("05 — CTA", BRAND.bgApp);
  s5.x = offsetX;

  createRect(s5, 0, 0, W, 6, BRAND.accent, 0);

  createText(s5, 100, 200, 880, "УВЕРЕННОСТЬ —\nЭТО МЫШЦА", 80, "Bold", BRAND.darker, "CENTER");

  createText(s5, 100, 440, 880, "Её невозможно накачать, наблюдая,\nкак тренируются другие.\nЕё нужно прорабатывать через\nмикро-нагрузки каждый день.", 34, "Regular", BRAND.textMuted, "CENTER");

  // Акцентная линия
  createRect(s5, 440, 660, 200, 4, BRAND.accent, 2);

  // CTA блок
  createRect(s5, 140, 720, 800, 300, BRAND.white, 32);
  createText(s5, 180, 750, 720, "Хочешь систему, которая\nсделает тебя сильнее?", 32, "Bold", BRAND.darker, "CENTER");

  createText(s5, 180, 850, 720, "Напиши «ДЕЙСТВИЕ» в комментариях\nи получи персональный план\nпрокачки уверенности!", 28, "Regular", BRAND.textMuted, "CENTER");

  // Кнопка
  createRect(s5, 320, 975, 440, 70, BRAND.dark, 35);
  createText(s5, 320, 990, 440, "НАПИСАТЬ", 28, "Bold", BRAND.white, "CENTER");

  // Сайт
  createText(s5, 100, 1100, 880, "chipizubova.online", 28, "Bold", BRAND.accentDark, "CENTER");
  createText(s5, 100, 1150, 880, "СИЛЬНОЕ ТЕЛО. УВЕРЕННЫЙ ДУХ.", 22, "Medium", BRAND.accent, "CENTER");

  createText(s5, 100, 1260, 880, "5 / 5", 20, "Regular", BRAND.textLight, "CENTER");

  slides.push(s5);

  // ---------- Центрирование в viewport ----------
  figma.viewport.scrollAndZoomIntoView(slides);
  figma.notify("✅ Гайд «Уверенность» — 5 слайдов создано!");
})();
