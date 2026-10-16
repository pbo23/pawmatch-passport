---
name: PaWow, сайт
description: Веб-исполнение системы «Тёплый спутник» для лендинга и гидов PaWow
colors:
  raspberry: "#e84b7a"
  raspberry-ink: "#b5174f"
  raspberry-ink-dark: "#ff86ab"
  raspberry-tint: "rgba(232, 75, 122, 0.12)"
  raspberry-tint-dark: "rgba(232, 75, 122, 0.22)"
  blush: "#fde8ef"
  blush-dark: "#4a2030"
  lilac: "#7b68ee"
  lilac-ink: "#4f3fc0"
  lilac-ink-dark: "#b2a7ff"
  lilac-tint: "rgba(123, 104, 238, 0.14)"
  lilac-tint-dark: "rgba(123, 104, 238, 0.26)"
  mint: "#1d9e75"
  mint-ink: "#127052"
  mint-ink-dark: "#4fd1a5"
  mint-tint: "rgba(29, 158, 117, 0.14)"
  mint-tint-dark: "rgba(29, 158, 117, 0.24)"
  apricot: "#e88a3a"
  apricot-ink: "#9a4f10"
  apricot-ink-dark: "#ffb26b"
  apricot-tint: "rgba(232, 138, 58, 0.16)"
  apricot-tint-dark: "rgba(232, 138, 58, 0.24)"
  blue: "#007aff"
  blue-ink: "#0058b8"
  blue-ink-dark: "#5aa9ff"
  blue-tint: "rgba(0, 122, 255, 0.12)"
  blue-tint-dark: "rgba(0, 122, 255, 0.24)"
  canvas: "#f2f2f7"
  canvas-dark: "#000000"
  card: "#ffffff"
  card-dark: "#1c1c1e"
  fill: "#f2f2f7"
  fill-dark: "#2c2c2e"
  ink: "#1c1c1e"
  ink-dark: "#f5f5f7"
  muted: "#5c5c61"
  muted-dark: "#aeaeb2"
  line: "#d8d8dd"
  line-dark: "#38383a"
  on-accent: "#ffffff"
  on-accent-dark: "#1c1c1e"
typography:
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "clamp(42px, 5.2vw, 74px)"
    fontWeight: 700
    lineHeight: 1.01
    letterSpacing: "-0.035em"
  headline-page:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "clamp(32px, 4.6vw, 60px)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "clamp(28px, 3.2vw, 40px)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "clamp(21px, 2vw, 27px)"
    fontWeight: 600
    lineHeight: 1.18
    letterSpacing: "-0.015em"
  title-card:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1.32
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.5
  body-article:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.62
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.5
  meta:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
  button:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "19px"
    fontWeight: 700
    lineHeight: 1
  clock:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "64px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.03em"
    fontFeature: "tnum"
  time-pill:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1
    fontFeature: "tnum"
rounded:
  badge: "6px"
  xs: "8px"
  sm: "10px"
  md: "12px"
  lg: "14px"
  card: "16px"
  bubble: "18px"
  notification: "22px"
  frame: "24px"
  pill: "999px"
spacing:
  xs: "6px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "20px"
  gutter: "24px"
  card: "30px"
  section: "56px"
components:
  button-primary:
    backgroundColor: "{colors.raspberry}"
    textColor: "{colors.on-accent}"
    typography: "{typography.button}"
    rounded: "{rounded.lg}"
    padding: "0 22px"
    height: "52px"
  button-round:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    size: "44px"
  button-round-hover:
    backgroundColor: "{colors.fill}"
  nav-link:
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "10px 14px"
  nav-link-hover:
    backgroundColor: "{colors.card}"
  chip-chapter:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "9px 15px"
  time-pill:
    backgroundColor: "{colors.mint-tint}"
    textColor: "{colors.mint-ink}"
    typography: "{typography.time-pill}"
    rounded: "{rounded.pill}"
    padding: "6px 9px"
  time-pill-now:
    backgroundColor: "{colors.mint-ink}"
    textColor: "{colors.on-accent}"
    typography: "{typography.time-pill}"
    rounded: "{rounded.pill}"
    padding: "6px 9px"
  icon-tile:
    backgroundColor: "{colors.mint-tint}"
    textColor: "{colors.mint}"
    rounded: "{rounded.md}"
    size: "44px"
  badge-status:
    backgroundColor: "{colors.mint-tint}"
    textColor: "{colors.mint-ink}"
    rounded: "{rounded.badge}"
    padding: "4px 8px"
  card:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.card}"
    padding: "{spacing.card}"
  action-card:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.card}"
    padding: "26px"
  guide-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "24px"
  guide-card-hover:
    backgroundColor: "{colors.fill}"
  field-input:
    backgroundColor: "{colors.fill}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "0 16px"
    height: "52px"
  ui-row-card:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.card}"
    padding: "10px 14px"
  notification:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.notification}"
    padding: "14px 16px"
  chat-bubble:
    backgroundColor: "{colors.fill}"
    textColor: "{colors.ink}"
    rounded: "{rounded.bubble}"
    padding: "9px 13px"
  chat-bubble-me:
    backgroundColor: "{colors.raspberry-tint}"
    textColor: "{colors.ink}"
    rounded: "{rounded.bubble}"
    padding: "9px 13px"
  tip-box:
    backgroundColor: "{colors.blush}"
    rounded: "{rounded.card}"
    padding: "18px 20px"
  gallery-frame:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.frame}"
    width: "min(300px, 76vw)"
---

# Design System: PaWow, сайт

## Overview

**Creative North Star: "Тёплый спутник" (The Warm Companion), веб-исполнение**

Сайт не придумывает свой мир, он переносит в браузер систему приложения.
Родительский документ: DESIGN.md приложения
(/Users/pbo/PawMatch/PawMatch/DESIGN.md, решение владельца от 2026-10-16).
Всё, что там сказано о смысле цветов, плоских карточках, плитках и бейджах,
действует и здесь; этот файл фиксирует, как система легла на веб, и где веб
сознательно отличается.

Каркас тот же: серый холст, белые плоские карточки без теней, системный шрифт
Apple, один малиновый цвет действия и четыре смысловых цвета ролей. Страница
спокойная и воздушная: эмоцию несут фото питомцев и настоящие экраны, а
интерфейс показан фрагментами, собранными из компонентов приложения
(строки с плиткой, уведомления, браузер с паспортом, чат). Сигнатура сайта:
вертикальная линейка дня с часами, меткой «сейчас» и розовой полосой
подсветки, которые движутся только через transform и opacity.

Веб отличается от приложения в трёх местах, и все три продиктованы
контрастом или смыслом: малиновый текст и ссылки темнее кнопки, подпись
кнопки крупнее и жирнее, глава «Соседи и пары» окрашена сиренью. Нейтральные
цвета записаны в hex, потому что у браузера нет системных семантических
цветов; тёмная тема переключается через prefers-color-scheme.

**Key Characteristics:**
- Система приложения, перенесённая без новых украшений
- Малиновый только у действия, малиновые чернила для текста и ссылок
- Плоские карточки r16 на сером холсте, глубина тоном
- Цвета ролей через тройку «цвет, чернила, тонировка»
- Время табличными цифрами: часы дня и метки отметок
- Движение один раз на элемент, только transform и opacity

## Colors

Один ягодный цвет действия поверх нейтральных в духе iOS и четыре смысловых
цвета, у каждого из которых три ступени: насыщенный цвет (точка, иконка),
чернила (текст, AA на светлом и тёмном) и тонировка (подложка).

### Primary
- **Малиновый (Raspberry)**: заливка основной кнопки, акцент чекбокса
  согласия, обводка фокуса поля email, начало фирменного градиента. Белый на нём даёт 3,67:1, поэтому работает только под крупным жирным
  текстом.
- **Малиновые чернила (Raspberry Ink)**: все ссылки, «Читать дальше» в
  карточках гидов, текущий язык в меню, кольцо фокуса. Отличие от приложения:
  там ссылки малиновые, здесь темнее, чтобы держать 5,9:1 на холсте; в тёмной
  теме светлый вариант.
- **Малиновая тонировка (Raspberry Tint)**: выделение текста и своё
  сообщение в чате.
- **Розовая дымка (Blush)**: полоса «сейчас» на линейке дня, ореол метки,
  блок совета в статье. В тёмной теме только тёмный вариант.

### Secondary
- **Сирень (Lilac)**: глава «Соседи и пары» (Buren en maatjes), страховка и
  декларация, плитка «Ищет пару». Вторая половина фирменного градиента.

### Tertiary
- **Мята (Mint)**: глава «Здоровье и бумаги», прививки, статус «Действует»,
  галочки списка доверия, сообщение об успешной подписке (чернилами).
- **Абрикос (Apricot)**: внимание (счёт клиники к декларации).
- **Голубой (Blue)**: глава «Рядом», клиники и места вокруг.

### Neutral
- **Холст (Canvas)**: фон страницы; липкая шапка часов на мобильном.
- **Карточка (Card)**: карточки, чипы, фрагменты интерфейса, круглые кнопки,
  меню языка.
- **Заливка (Fill)**: поле ввода, наведение на карточки и кнопки, чужое
  сообщение в чате, строка адреса во фрагменте браузера. В светлой теме
  совпадает с холстом, в тёмной светлее карточки.
- **Чернила (Ink)**: заголовки и основной текст. Мягче чёрного приложения.
- **Приглушённые чернила (Muted)**: подводки, подписи, мета; 5,96:1 на холсте.
- **Линия (Line)**: линейка дня, разделители в карточке действия, подвал,
  обводка меню языка, нижняя граница липких часов.
- **На акценте (On Accent)**: текст на насыщенной заливке; в тёмной теме для
  метки «сейчас» становится тёмным, потому что чернила роли там светлые.

### Named Rules
**The Raspberry Means Act Rule.** Малиновая заливка только у того, что
нажимают или что выбрано. Главы, заголовки и фоны малиновыми не бывают;
поэтому «Соседи и пары» сиреневые, а не малиновые, как в приложении.

**The Two Raspberries Rule.** Заливка кнопки берётся из Raspberry, любой
малиновый текст из Raspberry Ink. Малиновый текст на светлом фоне цветом
кнопки не пишется.

**The Role Triplet Rule.** Каждый цвет роли используется тройкой: цвет для
точки и иконки, тонировка для подложки, чернила для текста на подложке.
Смысл цвета совпадает с приложением и не меняется между страницами.

## Typography

**Display Font:** SF Pro Display через системный стек (-apple-system, затем Segoe UI, Roboto, Helvetica, Arial)
**Body Font:** SF Pro Text через тот же системный стек

**Character:** Одна системная гарнитура во всех ролях, как в приложении.
Иерархию держат размер, насыщенность и плотный трекинг крупных заголовков;
цифры времени и счётчиков табличные.

### Hierarchy
- **Display** (700, clamp 42 до 74 px, 1.01, трекинг -0.035em): заголовок
  первого экрана, не шире 12ch; на мобильном clamp 36 до 48 px.
- **Headline Page** (700, clamp 32 до 60 px, 1.05 до 1.08): заголовок страницы
  гидов и статьи.
- **Headline** (700, clamp 28 до 40 px, 1.1): заголовки секций; финальный
  призыв крупнее (clamp 32 до 54 px).
- **Title** (600, clamp 21 до 27 px, 1.18): заголовок отметки дня; заголовок
  карточки действия 21 px.
- **Title Card** (600, 19 px, 1.32): заголовок карточки гида.
- **Body** (400, 17 px, 1.5; 16 px до 719 px): основной текст лендинга.
- **Body Article** (400, 18 px, 1.62, не шире 66ch; 17 px на мобильном): текст
  гидов; вводный абзац 20 px.
- **Label** (600, 15 px): чипы глав, подписи кадров, название строки во
  фрагменте.
- **Meta** (400, 13 px, приглушённый): мета, подписи строк, расстояния.
- **Button** (700, 19 px): подпись основной кнопки.
- **Clock** (700, 64 px, табличные цифры; 28 px до 1023 px): часы дня.
- **Time Pill** (600, 14 px, табличные цифры; 13 px на мобильном): метки
  времени.

### Named Rules
**The Large Bold Label Rule.** Подпись на малиновой заливке не меньше 19 px
и 700: только так белый на малиновом проходит AA как крупный текст. В
приложении подпись 15 pt semibold; на вебе так нельзя.

**The Tabular Time Rule.** Время, расстояния и числа во фрагментах набираются
табличными цифрами, чтобы колонки не прыгали при смене значения.

## Layout

Контейнер 1180 px с полями 24 px (16 px до 719 px). Первый экран и финальный
призыв сеткой «текст и колонка 400 px» с промежутком 56 px; до 1023 px
складываются в одну колонку, карточка действия не шире 560 px. Линейка дня:
колонка часов 196 px и лента отметок; отметка делится на колонку времени
64 px, текст и фрагмент интерфейса (0.95 к 1.05). До 1023 px часы становятся
липкой полосой во всю ширину над лентой, фрагмент уходит под текст; до 719 px
колонка времени 52 px. Галерея экранов прокручивается горизонтально со
снапом, края выровнены по контейнеру. Гиды: три колонки, две до 1023 px,
одна до 719 px. Ритм секций 40, 56, 64, 72 и 96 px; внутри карточек 22 до
30 px; промежутки 8, 12, 16, 20 px. Любая нажимаемая зона от 44 px.

## Elevation & Depth

Сайт плоский, как приложение: глубина передаётся тоном (карточка на холсте,
заливка при наведении). Теней нет ни у карточек, ни у кнопок. Единственная
box-shadow на сайте не тень, а ореол: кольцо розовой дымки 4 px вокруг
метки «сейчас». Меню языка, единственный плавающий элемент, отделено
обводкой линией 1 px, а не тенью и не самодельным стеклом. Нижний край кадров
галереи растворяется маской, чтобы обрезанный экран не заканчивался резкой
кромкой.

### Shadow Vocabulary
- **Ореол метки** (`box-shadow: 0 0 0 4px var(--blush)`): только метка
  «сейчас» на линейке дня.

### Named Rules
**The Flat Card Rule.** Карточки без тени и без обводки; если карточке нужна
граница, ей нужен другой тон фона.

**The No Card in Card Rule.** Подсветка «сейчас» ложится под время и текст
отметки, фрагмент интерфейса остаётся отдельной карточкой на холсте.

## Shapes

Чем крупнее элемент, тем больше радиус, как в приложении: бейдж 6 px,
адресная строка и логотип 8 px, QR и пункт меню 10 px, плитка и поле 12 px,
кнопка и меню 14 px, карточки 16 px, пузырь чата 18 px, уведомление 22 px,
кадр экрана 24 px. Навигация, чипы, метки времени и круглые кнопки
полностью скруглены. Аватары и точки глав круглые. Кольцо фокуса 3 px
малиновыми чернилами со смещением 2 px и скруглением 8 px.

## Components

### Buttons
Одна основная кнопка на блок, крупная и тактильная.
- **Shape:** скругление 14 px, высота от 52 px.
- **Primary:** малиновая заливка, белая подпись Button, отступы 0 22 px;
  во всю ширину в карточке действия и на мобильном.
- **Hover / Focus:** наведение затемняет (brightness 0.94), нажатие сжимает
  до 0.98 за 150 мс; фокус общим кольцом.
- **Disabled:** непрозрачность 40%.
- **Round:** круг 44 px на фоне карточки со стрелкой, при наведении заливка;
  листает галерею.
- **Text link:** «Читать дальше», «Все статьи», «Подробнее» малиновыми
  чернилами 600 со стрелкой, зона 44 px.

### Chips
- **Style:** капсула на фоне карточки, текст Label чернилами, слева точка
  10 px цвета главы.
- **State:** легенда глав над линейкой дня; ссылка-чип при наведении берёт
  заливку. Выбранного состояния на сайте нет.

### Cards / Containers
- **Corner Style:** 16 px.
- **Background:** карточка; блок совета в статье на розовой дымке.
- **Shadow Strategy:** без тени (The Flat Card Rule).
- **Border:** нет.
- **Internal Padding:** 30 px (22 px на мобильном), карточка действия 26 px
  (20 px), карточка гида 24 px, вопросы 18 на 20 px.

### Inputs / Fields
- **Style:** поле email на заливке, без рамки, скругление 12 px, высота
  52 px, текст 17 px; подпись поля 13 px 600 приглушённым.
- **Focus:** обводка 2 px малиновым вплотную к полю.
- **Consent:** чекбокс 20 px с малиновым accent-color и подписью 14 px.
- **Success:** форма скрывает поле и согласие, статус пишется мятными
  чернилами 600.

### Navigation
Логотип и название 19 px 700 слева, ссылки-капсулы 15 px 500 справа
(наведение даёт фон карточки), меню языка капсулой на карточке со шевроном,
раскрывается вниз (в подвале вверх) карточкой r14 с обводкой. До 719 px
остаются только ссылки, помеченные как обязательные.

### Day Timeline (Signature)
Липкие часы: цифры Clock прокручиваются полосами к времени текущей отметки
(650 мс), ниже день недели. Линейка 2 px цветом линии; метка «сейчас» 12 px
цветом чернил с ореолом дымки едет по ней через transform (600 мс). Под
текущей отметкой проявляется полоса розовой дымки r16 (opacity, 500 мс).
Метка времени отметки окрашена цветом главы (тонировка и чернила), в момент
«сейчас» заливается чернилами главы с текстом On Accent. Без JS метка стоит
на первой отметке; при «уменьшить движение» всё видно сразу.

### Action Card and Notify Form (Signature)
Карточка r16 справа на первом экране и в финале: заголовок 21 px 600,
подсказка 15 px приглушённым, разделитель линией, затем поле email и кнопка
в ряд (на мобильном столбиком), согласие и строка мелкого шрифта 13 px с
иконкой 14 px.

### UI Fragments (Signature)
Компоненты приложения, собранные в HTML: карточка со строками (плитка или
аватар 40 px, название Label, подпись Meta, бейдж или значение 22 px справа),
уведомление r22 с иконкой r9, браузер с точками и адресной строкой, QR на
белом, стрелка потока, чат с пузырями. Плитка 44 px r12 на тонировке роли с
иконкой цвета роли; градиент малиновый → сиреневый только у плитки
взаимного совпадения. Бейдж r6, 12 px 600, чернила роли на её тонировке.
Фрагмент собирается, когда до отметки доходит полоса: части въезжают со
сдвигом 110 мс, бейджи встают из 0.85.

### Gallery Frame (Signature)
Кадр настоящего экрана 5:7, r24, ширина min(300 px, 76vw), фон светлого
холста, нижние 14% растворяются маской; широкие экраны вписываются целиком.
Подпись Label под кадром.

### Guide Card
Карточка r16 с отступом 24 px: заголовок Title Card, описание 15 px
приглушённым, внизу «Читать дальше» малиновыми чернилами и время чтения
Meta. Наведение меняет фон на заливку.

## Do's and Don'ts

### Do:
- **Do** сверять любое новое решение с DESIGN.md приложения; сайт его исполнение, а не отдельная система.
- **Do** заливать малиновым только кнопки и выбранное, а малиновый текст и ссылки писать Raspberry Ink (The Two Raspberries Rule).
- **Do** набирать подпись на малиновой заливке 19 px 700 (The Large Bold Label Rule).
- **Do** красить главы и роли тройкой цвет, тонировка, чернила: мята здоровье, сирень соседи, пары и страховка, голубой рядом и клиники, абрикос внимание.
- **Do** ставить карточки r16 на холст без тени и обводки.
- **Do** набирать время и числа табличными цифрами.
- **Do** двигать только transform и opacity, один раз на элемент, с ease cubic-bezier(.2,.8,.2,1) за 450 до 650 мс, и показывать всё сразу при «уменьшить движение».
- **Do** держать нажимаемые зоны от 44 px и видимое кольцо фокуса.

### Don't:
- **Don't** красить малиновым главы, заголовки, фоны и декоративные точки.
- **Don't** писать малиновый текст цветом кнопки (#e84b7a) на светлом фоне.
- **Don't** добавлять тени карточкам, кнопкам и фрагментам.
- **Don't** брать светлую розовую дымку в тёмной теме.
- **Don't** ставить градиент малиновый → сиреневый вне фирменного момента взаимного совпадения.
- **Don't** вкладывать карточку в карточку: подсветка «сейчас» идёт под текстом, фрагмент остаётся отдельной карточкой.
- **Don't** подменять системный стек веб-шрифтом.
