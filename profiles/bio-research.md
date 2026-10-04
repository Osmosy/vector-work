# Контракт работника: bio-research

    роль:        bio-research
    версия:      0.1
    статус:      DRAFT — каркас, не прошёл human-gate
    владелец:    <кто отвечает>
    домен:       skills/cowork-roles/bio-research/ — 6 навыков (по дереву)
    источник:    Anthropic Cowork (Apache-2.0)

## 0. Состав домена (по дереву)

    instrument-data-to-allotrope
    nextflow-development
    scientific-problem-selection
    scvi-tools
    single-cell-rna-qc
    start

Что делает каждый навык — по его собственному описанию:

    instrument-data-to-allotrope Convert laboratory instrument output files (PDF, CSV, Excel, TXT) to Allotrope Simple Model (ASM) JSON format or flattened 2D CSV. Use this skill when scientists need to 
    nextflow-development       Run nf-core bioinformatics pipelines (rnaseq, sarek, atacseq) on sequencing data. Use when analyzing RNA-seq, WGS/WES, or ATAC-seq data—either local FASTQs or public data
    scientific-problem-selection This skill should be used when scientists need help with research problem selection, project ideation, troubleshooting stuck projects, or strategic scientific decisions. 
    scvi-tools                 Deep learning for single-cell analysis using scvi-tools. This skill should be used when users need (1) data integration and batch correction with scVI/scANVI, (2) ATAC-se
    single-cell-rna-qc         Performs quality control on single-cell RNA-seq data (.h5ad or .h5 files) using scverse best practices with MAD-based filtering and comprehensive visualizations. Use when
    start                      Set up your bio-research environment and explore available tools. Use when first getting oriented with the plugin, checking which literature, drug-discovery, or visualiza

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
   `skills/cowork-roles/bio-research/skills/<навык>/SKILL.md` (6 шт.)
   Правило дома: при расхождении документа и навыка — прав навык.

## 3. Разрешённые инструменты (least privilege)

Права объявлены минимальным набором — по факту требований навыков домена:

    тулсет         инструменты                          зачем
    file           read_file, write_file, patch, ...    чтение входа, запись заключения
    skills         skills_list, skill_view              загрузка навыков домена
    memory         memory                               факты о практике
    connections    manage_connections                   11 MCP-серверов, 19 категорий коннекторов
    terminal       terminal, process_manage             25 Python-скриптов в домене

Запрещено конструктивно: `delegate_task`, `cronjob_manage`, `computer_use`, `browser_*`.

Обоснование по дереву:
  - браузер не требует ни один навык домена;
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

    навыков               6
    MCP-серверов          11 (benchling, biorender, biorxiv, c-trials, chembl, consensus…)
    категорий коннекторов 19
    Python-скриптов       25
    нужен браузер         —

**Требует внешних систем.** Пока ни один коннектор домена не подключён, результат
будет каркасным либо построенным на общих дефолтах, а не на данных организации.
Подключение — задача владельца (см. `READINESS.md`).

## Приёмка

Контракт не вступает в силу, пока не прошёл `human-gate`: названный ревьюер, нулевой
открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/bio-research.review.md`.
