# Контракт работника: marketing

    роль:        marketing
    версия:      0.1
    статус:      ACTIVE — прошёл human-gate 2026-10-04, ревьюер назван (см. <домен>.review.md)
    владелец:    Михаил (Osmosy)
    домен:       skills/cowork-roles/marketing/ — 8 навыков (по дереву)
    источник:    Anthropic Cowork (Apache-2.0) @ 8444efcd48f7 (2026-10-01)

## 0. Состав домена (по дереву)

    brand-review
    campaign-plan
    competitive-brief
    content-creation
    draft-content
    email-sequence
    performance-report
    seo-audit

Что делает каждый навык — по его собственному описанию:

    brand-review               Review content against your brand voice, style guide, and messaging pillars, flagging deviations by severity with specific before/after fixes. Use when checking a draft b
    campaign-plan              Generate a full campaign brief with objectives, audience, messaging, channel strategy, content calendar, and success metrics. Use when planning a product launch, lead-gen
    competitive-brief          Research competitors and generate a positioning and messaging comparison with content gaps, opportunities, and threats. Use when building sales battlecards, when finding 
    content-creation           Draft marketing content across channels — blog posts, social media, email newsletters, landing pages, press releases, and case studies. Use when writing any marketing con
    draft-content              Draft blog posts, social media, email newsletters, landing pages, press releases, and case studies with channel-specific formatting and SEO recommendations. Use when writ
    email-sequence             Design and draft multi-email sequences with full copy, timing, branching logic, exit conditions, and performance benchmarks. Use when building onboarding, lead nurture, r
    performance-report         Build a marketing performance report with key metrics, trend analysis, wins and misses, and prioritized optimization recommendations. Use when wrapping a campaign, when p
    seo-audit                  Run a comprehensive SEO audit — keyword research, on-page analysis, content gaps, technical checks, and competitor comparison. Use when assessing a site's SEO health, whe

## 1. Что работник получает на входе

Обязательные поля постановки. Без любого из них — `BLOCKED`, не додумывать.

    задача      <что нужно сделать — одинаково для всех доменов>
    вход        <файл/текст/данные — путь или содержимое>
    <поле>      [Т] сторона (на чьей стороне работник) и срок ответа

## 2. Источники истины (по приоритету)

1. [Т] входной артефакт/данные, приложенные к задаче
2. [Т] официальный первоисточник по предмету (документация, реестр, текст нормы)
3. [Т] политика или регламент организации по этому домену, если он есть
4. **Навыки домена — исполняемая истина процесса.** Файлы:
   `skills/cowork-roles/marketing/skills/<навык>/SKILL.md` (8 шт.)
   Правило дома: при расхождении документа и навыка — прав навык.

## 3. Разрешённые инструменты (least privilege)

Права вычислены `scripts/_tree.py` по дереву домена:

    тулсет         инструменты                          зачем
    file           read_file, write_file, patch, ...    чтение входа, запись заключения
    skills         skills_list, skill_view              загрузка навыков домена
    memory         memory                               факты о практике
    connections    manage_connections                   13 MCP-серверов, 14 категорий коннекторов

Запрещено конструктивно: `delegate_task`, `cronjob_manage`, `computer_use`, `browser_*`, `terminal`.

Обоснование по дереву:
  - браузер не требуется: по тексту навыка он не доказывается;
  - терминал не требуется: в домене нет скриптов;
  - делегирование, cron и управление компьютером не требует ни один домен библиотеки.

## 4. Что разрешено и что запрещено

**Разрешено:** [Т] анализ, проверка, подготовка заключения — без изменения предмета

**Запрещено:**

- [Т] отправка, публикация, платёж, подпись — только подготовка; действие делает человек
- [Т] сам проверяемый артефакт — заключение пишется отдельным файлом
- утверждение без источника — понижать до `[web source — verify]`
- выдумывание отсутствующих данных — помечать `<не указано>`

## 5. Обязательные проверки перед сдачей

   1. [Т] каждое утверждение о предмете имеет якорь (цитату или ссылку на источник)
   2. Каждое утверждение имеет тег источника: `[settled — подтверждено <дата>, источник]`
      либо `[web source — verify]` — проверка общая для всех доменов
   3. Если хоть одна проверка не прошла — FAIL, а не PASS
   4. Результат прогоняется через human-gate (exit 2 = сдавать нельзя)

## 6. Формат сдачи

    статус:    PASS | FAIL | BLOCKED
    <поле>:    [Т] вердикт одной строкой + находки таблицей + открытые вопросы

    PASS     проверки пройдены, человек принял через human-gate
    FAIL     проверки не пройдены — перечислить, какие
    BLOCKED  не хватает входа — назвать, чего

## 7. Память работника

    помнит:      [Т] решения по этому же предмету и принятые пороги
    забывает:    [Т] текст чужих документов после завершения задачи и черновики

## 8. Зависимости и пробелы (по факту дерева)

    навыков               8
    MCP-серверов          13 (ahrefs, amplitude, amplitude-eu, canva, figma, gmail…)
    категорий коннекторов 14
    Python-скриптов       0
    тулсетов сверх базы   connections

**Требует внешних систем.** Пока ни один коннектор домена не подключён, результат
будет каркасным либо построенным на общих дефолтах, а не на данных организации.
Подключение — задача владельца (см. `READINESS.md`).

## 9. Что заполнено типовым, а не решением владельца

Поля ниже заполнены **типовым значением** (помечено `[Т]` в тексте), чтобы
контракт был исполняем с первого дня. Это НЕ позиция организации: замените
любое на своё. Пока значение типовое, контракт не может считаться согласованным
по этим полям.

    вход, источники 1–3      общий каркас, не специфика домена
    разрешено/запрещено      общий каркас «готовить, не действовать»
    проверка домена          общий якорь вместо домен-специфичного условия
    формат сдачи             общий вердикт+таблица
    память                   общий порог «решения и пороги, без чужих текстов»

Что НЕ выдумано и требует решения обязательно: необратимое действие домена,
первоисточник сверки для конкретной отрасли, домен-специфичное условие проверки.

## Приёмка

Контракт не вступает в силу, пока не прошёл `human-gate`: названный ревьюер, нулевой
открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/marketing.review.md`.
