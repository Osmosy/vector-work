# Контракт работника: sales

    роль:        sales
    версия:      0.1
    статус:      DRAFT — каркас, не прошёл human-gate
    владелец:    <кто отвечает>
    домен:       skills/cowork-roles/sales/ — 9 навыков (по дереву)
    источник:    Anthropic Cowork (Apache-2.0)

## 0. Состав домена (по дереву)

    account-research
    call-prep
    call-summary
    competitive-intelligence
    create-an-asset
    daily-briefing
    draft-outreach
    forecast
    pipeline-review

Что делает каждый навык — по его собственному описанию:

    account-research           Research a company or person and get actionable sales intel. Works standalone with web search, supercharged when you connect enrichment tools or your CRM.
    call-prep                  Prepare for a sales call with account context, attendee research, and suggested agenda. Works standalone with user input and web research, supercharged when you connect y
    call-summary               Process call notes or a transcript — extract action items, draft follow-up email, generate internal summary. Use when pasting rough notes or a transcript after a discover
    competitive-intelligence   Research your competitors and build an interactive battlecard. Outputs an HTML artifact with clickable competitor cards and a comparison matrix.
    create-an-asset            Generate tailored sales assets (landing pages, decks, one-pagers, workflow demos) from your deal context. Describe your prospect, audience, and goal — get a polished, bra
    daily-briefing             Start your day with a prioritized sales briefing. Works standalone when you tell me your meetings and priorities, supercharged when you connect your calendar, CRM, and em
    draft-outreach             Research a prospect then draft personalized outreach. Uses web research by default, supercharged with enrichment and CRM.
    forecast                   Generate a weighted sales forecast with best/likely/worst scenarios, commit vs. upside breakdown, and gap analysis.
    pipeline-review            Analyze pipeline health — prioritize deals, flag risks, get a weekly action plan. Use when running a weekly pipeline review, deciding which deals to focus on this week, s

## 1. Что работник получает на входе

Обязательные поля постановки. Без любого из них — `BLOCKED`, не додумывать.

    задача      <что нужно сделать — одинаково для всех доменов>
    вход        <файл/текст/данные — путь или содержимое>
    <поле>      <РЕШЕНИЕ: какие поля нужны именно этому домену>

## 2. Источники истины (по приоритету)

1. <РЕШЕНИЕ: первичный источник — что здесь считается «оригиналом»>
2. <РЕШЕНИЕ: внешний первоисточник для сверки>
3. <РЕШЕНИЕ: внутренний документ организации — политика, регламент>
4. **Навыки домена — исполняемая истина процесса.** Файлы:
   `skills/cowork-roles/sales/skills/<навык>/SKILL.md` (9 шт.)
   Правило дома: при расхождении документа и навыка — прав навык.

## 3. Разрешённые инструменты (least privilege)

Права объявлены минимальным набором — по факту требований навыков домена:

    тулсет         инструменты                          зачем
    file           read_file, write_file, patch, ...    чтение входа, запись заключения
    skills         skills_list, skill_view              загрузка навыков домена
    memory         memory                               факты о практике
    connections    manage_connections                   14 MCP-серверов, 10 категорий коннекторов
    browser        browser_*                            навыки домена адресуют веб-страницы

Запрещено конструктивно: `delegate_task`, `cronjob_manage`, `computer_use`, `terminal`.

Обоснование по дереву:
  - терминал не требуется: в домене нет исполняемых скриптов, вызываемых навыком;
  - делегирование, cron и управление компьютером не требует ни один домен библиотеки.

## 4. Что разрешено и что запрещено

**Разрешено:** <РЕШЕНИЕ: список действий домена>

**Запрещено:**

- <РЕШЕНИЕ: необратимое действие этого домена — отправка/публикация/платёж; только подготовка>
- <РЕШЕНИЕ: что нельзя менять в проверяемом артефакте>
- утверждение без источника — понижать до `[web source — verify]`
- выдумывание отсутствующих данных — помечать `<не указано>`

## 5. Обязательные проверки перед сдачей

   1. <РЕШЕНИЕ: машинно проверяемое условие домена>
   2. Каждое утверждение имеет тег источника: `[settled — подтверждено <дата>, источник]`
      либо `[web source — verify]` — проверка общая для всех доменов
   3. Если хоть одна проверка не прошла — FAIL, а не PASS
   4. Результат прогоняется через human-gate (exit 2 = сдавать нельзя)

## 6. Формат сдачи

    статус:    PASS | FAIL | BLOCKED
    <поле>:    <РЕШЕНИЕ: что содержит результат этого домена>

    PASS     проверки пройдены, человек принял через human-gate
    FAIL     проверки не пройдены — перечислить, какие
    BLOCKED  не хватает входа — назвать, чего

## 7. Память работника

    помнит:      <РЕШЕНИЕ: что сохраняется между задачами>
    забывает:    <РЕШЕНИЕ: что не сохраняется>

## 8. Зависимости и пробелы (по факту дерева)

    навыков               9
    MCP-серверов          14 (apollo, atlassian, clay, close, fireflies, gmail…)
    категорий коннекторов 10
    Python-скриптов       0
    нужен браузер         да

**Требует внешних систем.** Пока ни один коннектор домена не подключён, результат
будет каркасным либо построенным на общих дефолтах, а не на данных организации.
Подключение — задача владельца (см. `READINESS.md`).

## Приёмка

Контракт не вступает в силу, пока не прошёл `human-gate`: названный ревьюер, нулевой
открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/sales.review.md`.
