# Контракт работника: finance

    роль:        finance
    версия:      0.1
    статус:      DRAFT — каркас, не прошёл human-gate
    владелец:    <кто отвечает>
    домен:       skills/cowork-roles/finance/ — 8 навыков (по дереву)
    источник:    Anthropic Cowork (Apache-2.0)

## 0. Состав домена (по дереву)

    audit-support
    close-management
    financial-statements
    journal-entry
    journal-entry-prep
    reconciliation
    sox-testing
    variance-analysis

Что делает каждый навык — по его собственному описанию:

    audit-support              Support SOX 404 compliance with control testing methodology, sample selection, and documentation standards. Use when generating testing workpapers, selecting audit sample
    close-management           Manage the month-end close process with task sequencing, dependencies, and status tracking. Use when planning the close calendar, tracking close progress, identifying blo
    financial-statements       Generate financial statements (income statement, balance sheet, cash flow) with period-over-period comparison and variance analysis. Use when preparing a monthly or quart
    journal-entry              Prepare journal entries with proper debits, credits, and supporting detail. Use when booking month-end accruals (AP, payroll, prepaid), recording depreciation or amortiza
    journal-entry-prep         Prepare journal entries with proper debits, credits, and supporting documentation for month-end close. Use when booking accruals, prepaid amortization, fixed asset deprec
    reconciliation             Reconcile accounts by comparing GL balances to subledgers, bank statements, or third-party data. Use when performing bank reconciliations, GL-to-subledger recs, intercomp
    sox-testing                Generate SOX sample selections, testing workpapers, and control assessments. Use when planning quarterly or annual SOX 404 testing, pulling a sample for a control (revenu
    variance-analysis          Decompose financial variances into drivers with narrative explanations and waterfall analysis. Use when analyzing budget vs.

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
   `skills/cowork-roles/finance/skills/<навык>/SKILL.md` (8 шт.)
   Правило дома: при расхождении документа и навыка — прав навык.

## 3. Разрешённые инструменты (least privilege)

Права объявлены минимальным набором — по факту требований навыков домена:

    тулсет         инструменты                          зачем
    file           read_file, write_file, patch, ...    чтение входа, запись заключения
    skills         skills_list, skill_view              загрузка навыков домена
    memory         memory                               факты о практике
    connections    manage_connections                   0 MCP-серверов, 4 категорий коннекторов
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

    навыков               8
    MCP-серверов          0 —
    категорий коннекторов 4
    Python-скриптов       0
    нужен браузер         да

**Требует внешних систем.** Пока ни один коннектор домена не подключён, результат
будет каркасным либо построенным на общих дефолтах, а не на данных организации.
Подключение — задача владельца (см. `READINESS.md`).

## Приёмка

Контракт не вступает в силу, пока не прошёл `human-gate`: названный ревьюер, нулевой
открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/finance.review.md`.
