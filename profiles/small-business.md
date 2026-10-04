# Контракт работника: small-business

    роль:        small-business
    версия:      0.1
    статус:      DRAFT — изменён после приёмки (одобрено 2026-10-04, 847738e)
    владелец:    Михаил (Osmosy)
    домен:       skills/cowork-roles/small-business/ — 44 навыков (по дереву)
    источник:    Anthropic Cowork (Apache-2.0) @ 8444efcd48f7 (2026-10-01)

## 0. Состав домена (по дереву)

    ad-manager
    ap-processor
    brand-style
    build-agent
    build-connector
    business-pulse
    call-list
    canva-creator
    cash-flow-snapshot
    close-month
    content-strategy
    contract-review
    crm-autopilot
    grant-rfp-writer
    grow-pipeline
    growth-pulse
    hiring-screener
    inbox-manager
    inventory-planner
    invoice-chase
    job-post-builder
    lead-finder
    lead-triage
    marketing-monday
    monday-brief
    month-end-prep
    outreach-composer
    pay-the-bills
    payroll-prep
    plan-payroll
    proposal-builder
    reactivate
    report-builder
    report-pack
    restock
    review-reputation
    seo-ai-visibility
    smb-onboard
    smb-router
    social-content-engine
    speed-to-lead
    tax-prep
    tax-season-organizer
    ticket-deflector

Что делает каждый навык — по его собственному описанию:

    ad-manager                 > The ads consultant that becomes an ads agent. Reads paid-ad performance natively through the TikTok Ads connector, or via a build-connector Zapier connection for other 
    ap-processor               > Works the bill pile end to end: reads bills and vendor statements out of the AP inbox or from uploaded PDFs and phone photos, pulls out vendor, amount, due date, and li
    brand-style                > Sets and updates the owner's brand look and output preferences, which every page and document the plugin produces then follows automatically. Captures the brand from a 
    build-agent                > Turns a task the owner keeps doing by hand into a named, reusable skill they can trigger by name or put on a schedule. Watches them do it once or listens to them descri
    build-connector            > Gets Claude talking to a tool nobody built an official connector for. Works out what the system is, checks the Claude connector directory for an existing connector firs
    business-pulse             > Produces a one-page cross-functional business snapshot for SMB owners — cash position (the ledger: MYOB, NetSuite, QuickBooks, Xero, or Zoho Books), sales trend (PayPal
    call-list                  Builds today's call list. Runs lead-triage to rank the top-5 leads most worth calling, supplies talking points from email history, blocks time on the calendar, and drafts
    canva-creator              > Takes an approved content brief and executes a campaign end-to-end: builds the posting calendar, generates Canva designs for social posts, drafts caption and email copy
    cash-flow-snapshot         > Reads AR/AP, historical cash timing, and known fixed costs from the ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) or from PayPal, Square, or Stripe — or a CS
    close-month                Closes the books and turns them into a decision as a three-link chain — month-end-prep reconciles the ledger against every connected payment processor and writes the P&L 
    content-strategy           > Analyzes sales data from PayPal and QuickBooks to find top performers and slow movers, layers in seasonality, and produces a prioritized 30-day content brief: what to p
    contract-review            > Lightweight NDA, MSA, and vendor contract review for SMBs without legal on staff. Reads contracts from local files, mail attachments (Gmail or M365), a connected file s
    crm-autopilot              > Keeps the CRM current without the owner ever opening it. Creates and updates contacts and deals from email, calendar, and call transcripts; logs activity automatically;
    grant-rfp-writer           > Finds grant and solicitation opportunities the organization actually qualifies for, runs a hard go/no-go before anyone starts writing, drafts the application or respons
    grow-pipeline              Fills the funnel end to end without the owner babysitting it — reads the market and the competition for context, builds a ranked list of named prospects with a reason att
    growth-pulse               > Answers one question for an SMB owner — is the growth engine actually working? Pulls sales trend by channel, funnel conversion, campaign return, best and worst performi
    hiring-screener            > Takes a pile of applications and turns it into a ranked shortlist, scored only against the job's stated rubric, with drafted replies to every candidate, scheduled inter
    inbox-manager              > Turns a full inbox into a short, ranked list of what actually needs the owner. Reads the mail, sorts it into needs-you, drafted-and-waiting, and handled, writes replies
    inventory-planner          > Works out what to reorder and when, from what is actually selling: pulls sales history and stock on hand from Shopify, Square, NetSuite, or an uploaded CSV, computes 7-
    invoice-chase              > Drafts overdue-invoice reminder emails from the ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) plus PayPal, Stripe, and Airwallex data, matched to each custom
    job-post-builder           > Builds end-to-end hiring packets — job post, structured interview guide with scoring rubric, and offer letter template — from a hiring brief. Triggers on: "help me hire
    lead-finder                > Builds a ranked list of prospects worth contacting. Works out the owner's ideal customer profile from the customers they already have, finds look-alike companies and th
    lead-triage                > Scores inbound HubSpot leads by engagement signals, company fit, and urgency markers, ranks the ones worth a call today with talking points, drafts the follow-ups, and 
    marketing-monday           Delivers the weekly growth briefing as one merged read — whether the growth engine is working, what customers are saying in public and private, what competitors actually 
    monday-brief               Runs the owner's Monday morning briefing as a two-link chain — business-pulse for the cross-connector snapshot of cash, sales, and pipeline, and report-builder for any sa
    month-end-prep             > Reconciles the accounting ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) against PayPal, Shopify, Square, and Stripe settlements, flags transactions that need
    outreach-composer          > Writes prospect outreach and follow-up sequences that sound like the owner wrote them, not like an AI did. Learns a voice profile from the owner's own sent mail, ground
    pay-the-bills              Works the bill pile from the AP inbox all the way to a staged payment run — reads and codes every bill, then checks the cash position before a dollar is committed, then s
    payroll-prep               > Gets payroll ready to run without anyone getting shorted: pulls timesheets from Gusto, QuickBooks Payroll, or an uploaded spreadsheet, totals regular, overtime, and PTO
    plan-payroll               Runs the payroll-confidence chain end to end — forecasts cash across the payroll window with cash-flow-snapshot, ranks and drafts overdue-invoice reminders with invoice-c
    proposal-builder           > Turns whatever came out of a discovery conversation — a call transcript, a voice memo, jobsite photos, an RFP document, a set of drawings, or scrappy notes — into a bra
    reactivate                 Wins back customers who have quietly stopped buying — finds the ones whose gap has stretched past their own normal rhythm or who are showing churn signals, ranks them by 
    report-builder             > Turns a plain-English description of a recurring report into a real, repeatable report — defines the metrics, pulls them from whatever data sources are connected, deliv
    report-pack                Delivers the owner's custom recurring report pack on a set cadence — runs the saved report definition from report-builder, wraps it in a business-pulse snapshot so the nu
    restock                    Turns what is actually selling into a reorder decision and gets it all the way into the books — computes sales velocity and conservative stockout dates per item, sizes th
    review-reputation          > Watches what customers are saying in public and in private, then does something about it. Aggregates Google, Yelp, and Facebook reviews alongside disputes, tickets, and
    seo-ai-visibility          > Audits and fixes both halves of being found — classic search and AI answers. Search side: rankings, site structure, page speed, titles and descriptions, and content tha
    smb-onboard                > Claude as the trainer. Walks an SMB owner through connecting their first two tools, runs one recipe to prove immediate value, interviews them about their business (indu
    smb-router                 > The front door to the Small Business plugin. Listens to what the owner needs right now — vague or specific — and routes them to the best skill or slash command for the 
    social-content-engine      > Runs the owner's content operation as a standing thing rather than a one-off: keeps a rolling posting calendar, learns the owner's voice, generates on-brand Canva graph
    speed-to-lead              > Makes sure no inbound lead goes unanswered. Watches web forms, the shared inbox, and the CRM for new inquiries, qualifies each one against the owner's criteria, drafts 
    tax-prep                   Prepares tax materials as a two-link chain — month-end-prep confirms the books are closed and reconciled first, then tax-season-organizer calculates the quarterly estimat
    tax-season-organizer       > Prepares tax-season materials for the owner's accountant, not tax advice. US federal tax; a non-US business gets its closed-books packet instead.
    ticket-deflector           > Reads a forwarded customer email or ticket, pulls order and refund status from a payments connector (PayPal, Square, or Stripe) or Shopify, account history from the CRM

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
   `skills/cowork-roles/small-business/skills/<навык>/SKILL.md` (44 шт.)
   Правило дома: при расхождении документа и навыка — прав навык.

## 3. Разрешённые инструменты (least privilege)

Права вычислены `scripts/_tree.py` по дереву домена:

    тулсет         инструменты                          зачем
    file           read_file, write_file, patch, ...    чтение входа, запись заключения
    skills         skills_list, skill_view              загрузка навыков домена
    memory         memory                               факты о практике
    connections    manage_connections                   35 MCP-серверов, 0 категорий коннекторов

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

    навыков               44
    MCP-серверов          35 (airwallex-agentos, apollo-io, atlassian-rovo, canva, clay, docusign…)
    категорий коннекторов 0
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
открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/small-business.review.md`.
