<div align="center">

<img src="assets/vector-logo.png" alt="Vector Work" width="200"/>

# Vector Work

[![Architecture: live](https://img.shields.io/badge/Architecture-live_diagram-4f8ff7.svg)](https://osmosy.github.io/vector-work/docs/vector-work.architecture.html)

**Виртуальные сотрудники на базе Hermes Agent — 18 каталогов Cowork: 17 ролей
организации и 1 витрина partner-built; 252 навыка**

[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue.svg)](https://github.com/NousResearch/hermes-agent)
[![Ecosystem: Vector](https://img.shields.io/badge/Ecosystem-Vector-blue.svg)](https://osmosy.github.io/)
[![Domains: 18](https://img.shields.io/badge/Domains-18-green.svg)](#роли)
[![Skills: 252](https://img.shields.io/badge/Skills-252-orange.svg)](https://github.com/anthropics/knowledge-work-plugins)
<!-- gen:sync:start -->
[![Synced upstream: 2026-10-01](https://img.shields.io/badge/synced_upstream-2026__10__01-blueviolet.svg)](https://github.com/anthropics/knowledge-work-plugins/commits/main)
<!-- gen:sync:end -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

Копия [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins)
(23.7k★) для Hermes Agent. 18 каталогов: 17 ролей организации и витрина
partner-built (71 навык). Всего 252 навыка; копия ролей закреплена от
`anthropics/knowledge-work-plugins` @ `8444efcd48f7` (2026-10-01) — см. `upstream.lock.json`.
Активируются по интенту — скажи «проверь NDA» и legal включится сам.

Определения терминов и числа — [docs/VOCABULARY.md](docs/VOCABULARY.md).

### Синхронизация с upstream

Состав сверяется с апстримом: `python3 scripts/check_upstream.py`. Расхождение —
не ошибка сборки, а факт отставания копии; в CI проверка идёт **по расписанию** и
открывает issue, а не красит push.

Состояние сверки и бейдж выводятся из `upstream.lock.json`:
`python3 scripts/check_upstream.py --pin` фиксирует ревизию,
`--write-badge` переписывает бейдж и абзац. Руками эти числа не правятся.

<!-- gen:syncstate:start -->
Состояние сверки на 2026-10-01: копия закреплена от `anthropics/knowledge-work-plugins` @ `8444efcd48f7`. На этой ревизии в апстриме 252 `SKILL.md`, в копии 252. Все каталоги совпадают по числу навыков.
<!-- gen:syncstate:end -->

| Дата | Что обновлено |
|------|---------------|
| 2026-10-01 | синхронизация sales (9 → 36) и small-business (31 → 44) с апстримом @ `8444efcd48f7`; 13 навыков small-business, удалённых апстримом в переделке «Claude for Small Business launch» (15.09), удалены и здесь; добавлен `shared/` |
| 2026-08-29 | предыдущая ревизия копии: `2ed7b64390`. productivity — security-fix (escape file-derived content в dashboard, 06.08); sales — +Monday.com MCP (23.06); small-business — Google MCP удалён upstream (30.07). Полная копия ролей из upstream main |
| 2026-06-20 | восстановление cowork-roles (32 skills) |
| 2026-05-30 | init: 14 ролей |

## Архитектура

```
Задача → Hermes (оркестратор)
           ├── БИЗНЕС: productivity, small-business
           ├── ПРОДУКТ: product-management, engineering, design
           ├── ДАННЫЕ: data, enterprise-search
           ├── ЮРИДИКА: legal
           ├── ФИНАНСЫ: finance
           ├── ЛЮДИ: human-resources
           ├── ОПЕРАЦИИ: operations
           ├── НАУКА: bio-research
           └── МЕТА: cowork-plugin-management
```

## Роли

Числа — по дереву (`scripts/build_registry.py`), не по памяти. Расхождение с
деревом считается дефектом. Колонка «Контракт» — факт приёмки по журналу
`profiles/approvals.jsonl`: `DRAFT` здесь означает, что тело контракта
изменилось после пакетной приёмки 2026-10-04 и требует нового ревью.

| Роль | Для каких задач | Навыков | Контракт |
|------|----------------|---------|----------|
| **small-business** | Инвойсы, учёт, зарплата, налоги, CRM | 44 | DRAFT |
| **data** | SQL-запросы, дашборды, мониторинг, ML | 10 | DRAFT |
| **engineering** | Код-ревью, инциденты, архитектура, деплой | 10 | DRAFT |
| **legal** | Триаж NDA, проверка договоров, комплаенс, риски | 9 | DRAFT |
| **human-resources** | Онбординг, вакансии, собеседования, оценка | 9 | DRAFT |
| **operations** | Процессы, вендоры, закупки, мощности | 9 | DRAFT |
| **sales** | Пайплайн, звонки, прогноз, конкурентная разведка | 36 | DRAFT |
| **finance** | Проводки, аудит, категоризация, отчётность | 8 | DRAFT |
| **marketing** | Контент, кампании, SEO, аналитика | 8 | DRAFT |
| **product-management** | PRD, роадмап, user stories, приоритизация | 8 | DRAFT |
| **design** | Дизайн-ревью, дизайн-система, accessibility | 7 | DRAFT |
| **bio-research** | PubMed, геномика, литература, эксперименты | 6 | DRAFT |
| **customer-support** | Тикеты, эскалации, база знаний, ответы | 5 | DRAFT |
| **enterprise-search** | Поиск по Slack, Notion, Jira | 5 | DRAFT |
| **productivity** | Задачи, календарь, заметки, ежедневный брифинг, тайм-трекинг | 4 | DRAFT |
| **cowork-plugin-management** | Создание и настройка новых ролей (мета) | 2 | DRAFT |
| **pdf-viewer** | Просмотр и разбор PDF | 1 | DRAFT |

### Витрины партнёрских MCP (partner-built, 71 навык)

Роли, написанные под конкретные системы, а не под функцию организации.
В таблице выше не перечислены поштучно — это одна витрина:

| Витрина | Навыков | Под что |
|---------|---------|---------|
| zoom-plugin | 57 | Zoom (встречи, SDK, RTMS, Contact Center) |
| common-room | 6 | Common Room (prospecting, account research) |
| apollo | 3 | Apollo (enrichment, sequences) |
| brand-voice | 3 | Brand voice enforcement |
| slack | 2 | Slack (messaging, search) |

### Домены из внешней библиотеки

Навыки `project-management` (9), `research` (8), `research-ops` (5) лежат **не в этом
репозитории**, а во внешней библиотеке навыков. В витрину Vector Work они входят
как ориентир, но в дереве `skills/cowork-roles/` их нет — поэтому контрактов
в `profiles/` они не имеют. Смешивать их с ролями организации в одной таблице нельзя:
получаются числа, которых в дереве нет.

### Итого

Что лежит **в этом репозитории** (числа по дереву):

    cowork-roles/                18 каталогов, 252 навыка
      из них роли организации     17 каталогов, 181 навык
      витрина partner-built        1 каталог,   71 навык
    skills/ (свои)                3 навыка

Что **не** лежит здесь, а берётся из внешней библиотеки (в числа выше не входит):

    claude-skills/    3 домена, 22 навыка — project-management (9), research (8),
                      research-ops (5). Помечены как внешние: в дереве
                      cowork-roles/ их нет, контрактов в profiles/ они не имеют.

## Быстрый старт

```bash
git clone https://github.com/Osmosy/vector-work.git

# Срабатывает автоматически по интенту
hermes "Проверь этот NDA на риски"           # → legal
hermes "Напиши PRD для фичи экспорта в PDF"  # → product-management
hermes "Создай роль для отдела логистики"     # → cowork-plugin-management
```

## Установка

Установка — копирование каталога навыков в окружение Hermes:

```bash
cp -r skills/cowork-roles ~/.hermes/skills/
```

Состав копии сверяется с деревом репозитория: `python3 scripts/build_registry.py`.

## Структура репозитория

    skills/cowork-roles/   18 каталогов (17 ролей + витрина), 252 навыка
    skills/                3 своих навыка: autonomous-supergoal-patterns,
                           github-repo-research, vector-push
    agents/                orchestrator.md — маршрутизация по интенту
    profiles/              контракты работников (см. ниже)
    docs/                  архитектурная схема

## Контракты работников (profiles/)

Роль = не промпт персонажа, а исполняемые ограничения. Контракт описывает, что
работник получает, какими инструментами вправе пользоваться, что ему запрещено,
какие проверки обязательны и в каком виде он сдаёт результат (PASS/FAIL/BLOCKED).

    profiles/_TEMPLATE.md         шаблон контракта
    profiles/REGISTRY.md          реестр доменов по дереву (генерируется)
    profiles/READINESS.md         зрелость доменов и что нужно каждому
    profiles/<домен>.md           17 контрактов ролей + плейбук legal
    profiles/body-hashes.json     отпечатки тел (правка тела роняет приёмку)
    profiles/REGISTRY.md          реестр (генерируется)
    profiles/STATUS.md            состояние структуры

Реестр пересобирается после изменения состава: `python3 scripts/build_registry.py`.
Он же сверяет числа README с деревом и печатает расхождения.

## Источник

Адаптировано из [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) — Apache 2.0.
