# Контракт работника: small-business

    роль:        small-business
    версия:      0.1
    статус:      DRAFT — каркас, не прошёл human-gate
    владелец:    <кто отвечает>
    домен:       skills/cowork-roles/small-business/ — 31 навыков (по дереву)
    источник:    Anthropic Cowork (Apache-2.0)

## 0. Состав домена (по дереву)

    business-pulse
    call-list
    canva-creator
    cash-flow-snapshot
    close-month
    content-strategy
    contract-review
    crm-cleanup
    crm-maintenance
    customer-pulse
    customer-pulse-check
    friday-brief
    handle-complaint
    invoice-chase
    job-post-builder
    lead-triage
    margin-analyzer
    monday-brief
    month-end-prep
    month-heads-up
    plan-payroll
    price-check
    quarterly-review
    review-contract
    run-campaign
    sales-brief
    smb-onboard
    smb-router
    tax-prep
    tax-season-organizer
    ticket-deflector

Что делает каждый навык — по его собственному описанию:

    business-pulse             > Produces a one-page cross-functional business snapshot for SMB owners — cash position (QuickBooks), sales trend (PayPal/Square), pipeline movement (HubSpot), this week'
    call-list                  Ranks the top-5 leads most worth calling today, supplies talking points from email history, blocks time on the calendar, and drafts follow-up messages. Accepts optional c
    canva-creator              > Takes an approved content brief and executes a campaign end-to-end: builds the posting calendar, generates Canva designs for social posts, drafts caption and email copy
    cash-flow-snapshot         > Reads AR/AP, historical cash timing, and known fixed costs from QuickBooks, PayPal, Stripe, or Square — or a CSV upload — and produces a 30/60/90-day cash flow forecast
    close-month                Closes the month — reconciles QB vs payment processors, flags gaps, writes P&L narrative, exports close packet. Accepts optional month and save-to arguments.
    content-strategy           > Analyzes sales data from PayPal and QuickBooks to find top performers and slow movers, layers in seasonality, and produces a prioritized 30-day content brief: what to p
    contract-review            > Lightweight NDA, MSA, and vendor contract review for SMBs without legal on staff. Reads contracts from local files, Gmail attachments, or DocuSign envelopes; flags non-
    crm-cleanup                Scans HubSpot for stale deals, duplicate contacts, and missing fields, then fixes what the owner approves. Accepts optional scope argument for deals, contacts, or all.
    crm-maintenance            > Keeps HubSpot current without the owner opening it: creates and updates contacts and deals from email and calendar context, logs notes and calls, and flags stale record
    customer-pulse             > Aggregates PayPal disputes, HubSpot feedback and tickets, and email sentiment (plus pasted or exported Google/Yelp reviews) into a themes report with verbatim evidence 
    customer-pulse-check       Synthesizes themes from PayPal disputes, HubSpot tickets, and review exports into a top-3 fixable issues list with drafted response templates. Accepts optional since-date
    friday-brief               Delivers the Friday end-of-week pulse — revenue vs prior week, top sellers, wins and watches. Accepts optional lookback window of 7 or 14 days.
    handle-complaint           Handles an incoming customer complaint end-to-end — pulls context, drafts a response, and suggests an operational fix. Accepts optional email or ticket ID argument.
    invoice-chase              > Drafts overdue-invoice reminder emails from QuickBooks and PayPal data, matched to each customer's payment history and tone (gentle for good customers, firm for repeat 
    job-post-builder           > Builds end-to-end hiring packets — job post, structured interview guide with scoring rubric, and offer letter template — from a hiring brief. Triggers on: "help me hire
    lead-triage                > Scores inbound HubSpot leads by engagement signals, company fit, and urgency markers to produce a "call these 5 today" list with talking points, drafts the follow-ups, 
    margin-analyzer            > Analyzes unit economics by product or service using PayPal merchant insights and QuickBooks cost data, benchmarks against inflation and cost changes, and shows pricing-
    monday-brief               Generates a one-page Monday morning briefing — cash, sales, pipeline, week ahead, top three to-dos. Accepts optional post destination and save-to arguments.
    month-end-prep             > Walks an SMB owner through month-end close: reconciles QuickBooks against PayPal (and Square/Stripe) settlements, flags uncategorized transactions, suspicious duplicate
    month-heads-up             Runs on the 25th — shows the next 30-day cash-flow outlook and flags anything that needs attention before month-end. Accepts optional 30 or 60 day horizon.
    plan-payroll               Forecasts cash, ranks overdue invoices, and stages PayPal reminders so the owner can confidently run payroll. Accepts optional horizon and payroll-date arguments.
    price-check                Produces a margin-by-product table and three pricing-scenario data views so the owner can see the full financial picture before making a pricing decision. Accepts optiona
    quarterly-review           Generates a full QBR narrative — revenue trend, margin trend, customer health, top opportunities and risks — as a presentation-ready PDF or deck. Accepts optional quarter
    review-contract            Reviews a contract in plain English, surfaces red flags with severity ratings, and produces a marked-up docx/PDF with suggested redlines. Accepts optional file path or Do
    run-campaign               Runs an end-to-end marketing campaign — sales analysis, content brief, Canva assets, HubSpot send. Accepts optional lookback and channel arguments.
    sales-brief                Surfaces top and bottom sellers, identifies seasonality patterns, and produces a 2-week content brief to push winners and clear slow movers. Accepts optional lookback win
    smb-onboard                > Claude as the trainer. Walks an SMB owner through connecting their first two tools, runs one recipe to prove immediate value, interviews them about their business (indu
    smb-router                 > The front door to the Small Business plugin. Listens to what the owner needs right now — vague or specific — and routes them to the best skill or slash command for the 
    tax-prep                   Prepares tax-season materials — quarterly estimated tax calculation or year-end 1099 prep — and produces an accountant handoff packet. Accepts optional mode and year argu
    tax-season-organizer       > Prepares tax-season materials for small business owners — framed as deliverables for their accountant, not tax advice. Two modes: (1) quarterly estimated tax calculatio
    ticket-deflector           > Reads a forwarded customer email or ticket, pulls order/refund status from PayPal and account history from HubSpot, drafts a tone-matched reply in the owner's writing v

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
   `skills/cowork-roles/small-business/skills/<навык>/SKILL.md` (31 шт.)
   Правило дома: при расхождении документа и навыка — прав навык.

## 3. Разрешённые инструменты (least privilege)

Права объявлены минимальным набором — по факту требований навыков домена:

    тулсет         инструменты                          зачем
    file           read_file, write_file, patch, ...    чтение входа, запись заключения
    skills         skills_list, skill_view              загрузка навыков домена
    memory         memory                               факты о практике
    connections    manage_connections                   11 MCP-серверов, 0 категорий коннекторов
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

    навыков               31
    MCP-серверов          11 (canva, docusign, gmail, google calendar, google drive, hubspot…)
    категорий коннекторов 0
    Python-скриптов       0
    нужен браузер         да

**Требует внешних систем.** Пока ни один коннектор домена не подключён, результат
будет каркасным либо построенным на общих дефолтах, а не на данных организации.
Подключение — задача владельца (см. `READINESS.md`).

## Приёмка

Контракт не вступает в силу, пока не прошёл `human-gate`: названный ревьюер, нулевой
открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/small-business.review.md`.
