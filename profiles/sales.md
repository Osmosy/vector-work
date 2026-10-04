# Контракт работника: sales

    роль:        sales
    версия:      0.1
    статус:      ACTIVE — тело совпадает с одобренным (BATCH 2026-10-04, b34761f)
    владелец:    Михаил (Osmosy)
    домен:       skills/cowork-roles/sales/ — 36 навыков (по дереву)
    источник:    Anthropic Cowork (Apache-2.0) @ 8444efcd48f7 (2026-10-01)

## 0. Состав домена (по дереву)

    account-context
    account-plan
    account-research
    account-tiering
    call-prep
    call-summary
    close-plan
    competitive-intelligence
    create-an-asset
    crm-hygiene-check
    customer-health
    customer-voice
    daily-briefing
    deal-advance-gap
    deal-review
    deal-signals
    deal-slip-scenario
    draft-outreach
    end-of-day
    expansion-whitespace
    forecast
    handle-objection
    inbox-sweep
    lead-triage
    log-activity
    pipeline-review
    renewal-radar
    rep-context
    route-lead
    schedule-meeting
    setup
    stakeholder-map
    team-pipeline
    update-opportunity
    weekly-wrap
    win-loss-review

Что делает каждый навык — по его собственному описанию:

    account-context            360-degree view of an account - CRM data, recent email threads, docs, transcripts, and internal chat chatter, synthesized into one brief. Use when the user asks "tell me 
    account-plan               Build or refresh a strategic account plan - current state, goals, stakeholder coverage, opportunity map, risks, and the action plan - written to a doc and key fields sync
    account-research           Research a target company and optionally a specific contact - company overview, recent news, likely priorities, and fit against your ICP. Cross-references existing CRM re
    account-tiering            Score and tier a list of accounts (or your full book) against ICP fit and engagement signals to prioritize where to spend time. Use when the user asks to "tier my account
    call-prep                  Pre-call brief for an upcoming meeting - attendees, account history, prior call context from transcripts, open opportunity status, and suggested discovery questions. Use 
    call-summary               Turn a call transcript or call notes into a customer follow-up email draft, an internal chat summary, and proposed CRM updates. Use when the user says "call summary", "fo
    close-plan                 Build the business case and mutual action plan for a deal - the why-buy/why-now story, the ROI framing, and the dated step-by-step path to signature shared with the custo
    competitive-intelligence   Competitive analysis two ways - the in-deal play against a named competitor, and win/loss patterns, competitor mentions, and battlecards across the book. Use when the use
    create-an-asset            Build a customer deck, one-pager or leave-behind from your account data, call notes and approved materials, with no made-up numbers. Use when the user asks for a sales as
    crm-hygiene-check          Read-only audit of your CRM opportunities for missing fields, stale dates, and stage mismatches - outputs a fix checklist to apply by hand or through update-opportunity. 
    customer-health            Health check on a customer account and QBR-ready prep - relationship strength, engagement trend, risk signals, value delivered, and the agenda that makes the review worth
    customer-voice             Surface what customers are actually saying - direct attributed quotes on a topic across call transcripts and email, across your accounts. Use when the user asks "what are
    daily-briefing             Morning rundown - today's meetings with account context, opps closing soon with stale flags, waiting customer emails, and the day's top actions. Use when the user says "d
    deal-advance-gap           Forward-looking gap check on one opportunity - exactly what is missing to advance it to the next stage and to close, with who does what by when. Use when the user asks "w
    deal-review                Deep-dive on a single opportunity - signal-adjusted health score, risks, gaps in qualification, and recommended next actions. Use when the user asks "review the [account]
    deal-signals               Proactive watch over your book - deals gone quiet, close dates slipping into view, champion changes, renewal windows opening, competitor mentions - surfaced as a short al
    deal-slip-scenario         Model what happens to your number if a deal slips, shrinks, or dies - quota impact, coverage ratio change, and the substitute pipeline needed to stay on plan. Use when th
    draft-outreach             Draft a personalized outreach email or multi-touch sequence to a prospect, create it as an email draft for review, and add the contact to a sequence in your sales engagem
    end-of-day                 The closing beat of the day - every call processed or explicitly skipped, the CRM brought current, commitments captured, and tomorrow's top three teed up. Use when the us
    expansion-whitespace       Find the expansion whitespace in an account or a book - what they own vs. what they could own, the evidence for each play, and the open opps to create.
    forecast                   Generate the commit / best-case / pipeline narrative for a forecast call or a 1:1 with your manager - what's closing, what's at risk, what changed since last time. Use wh
    handle-objection           Work through a live objection or competitive threat - what's really being said, the response that has worked before, and the proof points to use, grounded in your own win
    inbox-sweep                Batch-process unread customer emails - classify, prioritize, and draft replies. Use when the user asks "sweep my inbox", "what customer emails need a reply", "draft repli
    lead-triage                Score and route an inbound lead, or rank a backlog of leads, against your ICP and qualification framework, then recommend a priority and next action. Use when the user as
    log-activity               Log a call, meeting, or email exchange to the CRM after the fact as a completed activity on the right account, opportunity, and contact - drafted from your description or
    pipeline-review            Stage-by-stage pipeline health check - coverage, aging, conversion, and at-risk deals - from CRM opportunity data. Use when the user asks "review my pipeline", "pipeline 
    renewal-radar              Upcoming renewals with timing, risk, and uplift potential - and the renewal opportunity records to keep them honest. Use when the user asks "what renewals are coming up",
    rep-context                Leader's prep on a single rep before a 1:1 - their pipeline, recent activity, what they've been working on per chat and calendar, and where they might need help. Use when
    route-lead                 Decide who owns an unrouted lead or opportunity and manage the handoff - deterministic routing by the org's own rules, a routing card the human router accepts or override
    schedule-meeting           Find a time, draft the invite, and book the meeting on Google Calendar or Outlook - then log it to the CRM as an event on the right account and opportunity. Use when the 
    setup                      First-run setup - checks which tools are connected, shows what's connected and what each one unlocks, learns how you write from your sent email, and renders a starter das
    stakeholder-map            Map the people in a deal or account - roles, influence, sentiment, who's missing, and your best access path to the people you haven't reached. Use when the user asks "who
    team-pipeline              Leader view - roll up a team's pipeline by rep and stage, flag at-risk deals, and surface coaching moments. Use when the user asks "show my team's pipeline", "team foreca
    update-opportunity         Guided updates to an opportunity - push the stage, move the close date, set next steps, fix amount or forecast category. Shows the before/after, writes what you ask for o
    weekly-wrap                End-of-week summary for a rep or leader - what closed, what moved, what slipped, and what's on deck Monday. Optionally drafts a chat post to the team channel.
    win-loss-review            Analyze recently closed opportunities to find patterns in what wins and what loses - stage of loss, common objections from transcripts, deal characteristics. Leader-focus

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
   `skills/cowork-roles/sales/skills/<навык>/SKILL.md` (36 шт.)
   Правило дома: при расхождении документа и навыка — прав навык.

## 3. Разрешённые инструменты (least privilege)

Права вычислены `scripts/_tree.py` по дереву домена:

    тулсет         инструменты                          зачем
    file           read_file, write_file, patch, ...    чтение входа, запись заключения
    skills         skills_list, skill_view              загрузка навыков домена
    memory         memory                               факты о практике
    connections    manage_connections                   23 MCP-серверов, 10 категорий коннекторов

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

    навыков               36
    MCP-серверов          23 (apollo, atlassian, calendly, clay, close, crunchbase…)
    категорий коннекторов 10
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
открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/sales.review.md`.
