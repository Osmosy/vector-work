# Контракт работника: human-resources

    роль:        human-resources
    версия:      0.1
    статус:      DRAFT — каркас, не прошёл human-gate
    владелец:    <кто отвечает>
    домен:       skills/cowork-roles/human-resources/ — 9 навыков (по дереву)
    источник:    Anthropic Cowork (Apache-2.0)

## 0. Состав домена (по дереву)

    comp-analysis
    draft-offer
    interview-prep
    onboarding
    org-planning
    people-report
    performance-review
    policy-lookup
    recruiting-pipeline

Что делает каждый навык — по его собственному описанию:

    comp-analysis              Analyze compensation — benchmarking, band placement, and equity modeling. Trigger with "what should we pay a [role]", "is this offer competitive", "model this equity gran
    draft-offer                Draft an offer letter with comp details and terms. Use when a candidate is ready for an offer, assembling a total comp package (base, equity, signing bonus), writing the 
    interview-prep             Create structured interview plans with competency-based questions and scorecards. Trigger with "interview plan for", "interview questions for", "how should we interview",
    onboarding                 Generate an onboarding checklist and first-week plan for a new hire. Use when someone has a start date coming up, building the pre-start task list (accounts, equipment, b
    org-planning               Headcount planning, org design, and team structure optimization. Trigger with "org planning", "headcount plan", "team structure", "reorg", "who should we hire next", or w
    people-report              Generate headcount, attrition, diversity, or org health reports. Use when pulling a headcount snapshot for leadership, analyzing turnover trends by team, preparing divers
    performance-review         Structure a performance review with self-assessment, manager template, and calibration prep. Use when review season kicks off and you need a self-assessment template, wri
    policy-lookup              Find and explain company policies in plain language. Trigger with "what's our PTO policy", "can I work remotely from another country", "how do expenses work", or any plai
    recruiting-pipeline        Track and manage recruiting pipeline stages. Trigger with "recruiting update", "candidate pipeline", "how many candidates", "hiring status", or when the user discusses so

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
   `skills/cowork-roles/human-resources/skills/<навык>/SKILL.md` (9 шт.)
   Правило дома: при расхождении документа и навыка — прав навык.

## 3. Разрешённые инструменты (least privilege)

Права объявлены минимальным набором — по факту требований навыков домена:

    тулсет         инструменты                          зачем
    file           read_file, write_file, patch, ...    чтение входа, запись заключения
    skills         skills_list, skill_view              загрузка навыков домена
    memory         memory                               факты о практике
    connections    manage_connections                   0 MCP-серверов, 6 категорий коннекторов

Запрещено конструктивно: `delegate_task`, `cronjob_manage`, `computer_use`, `browser_*`, `terminal`.

Обоснование по дереву:
  - браузер не требует ни один навык домена;
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
    MCP-серверов          0 —
    категорий коннекторов 6
    Python-скриптов       0
    нужен браузер         —

**Требует внешних систем.** Пока ни один коннектор домена не подключён, результат
будет каркасным либо построенным на общих дефолтах, а не на данных организации.
Подключение — задача владельца (см. `READINESS.md`).

## Приёмка

Контракт не вступает в силу, пока не прошёл `human-gate`: названный ревьюер, нулевой
открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/human-resources.review.md`.
