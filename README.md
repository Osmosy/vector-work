<div align="center">

<img src="assets/vector-logo.png" alt="Vector Work" width="200"/>

# Vector Work

[![Architecture: live](https://img.shields.io/badge/Architecture-live_diagram-4f8ff7.svg)](https://osmosy.github.io/vector-work/docs/vector-work.architecture.html)

**Виртуальные сотрудники на базе Hermes Agent — 17 доменов Cowork (Anthropic), 212 навыков**

[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue.svg)](https://github.com/NousResearch/hermes-agent)
[![Ecosystem: Vector](https://img.shields.io/badge/Ecosystem-Vector-blue.svg)](https://osmosy.github.io/)
[![Domains: 18](https://img.shields.io/badge/Domains-18-green.svg)](#роли)
[![Skills: 212](https://img.shields.io/badge/Skills-212-orange.svg)](https://github.com/anthropics/knowledge-work-plugins)
[![Sync: 2026-08-30](https://img.shields.io/badge/Sync-2026__08__30-blueviolet.svg)](https://github.com/anthropics/knowledge-work-plugins/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

Копия [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins)
(23.7k★) для Hermes Agent. 17 доменов-ролей (212 навыков), синхронизировано
с upstream 2026-08-30. Активируются по интенту — скажи «проверь NDA» и legal включится сам.

### Синхронизация с upstream

| Дата | Что обновлено |
|------|---------------|
| 2026-08-30 | productivity — security-fix (escape file-derived content в dashboard, 06.08); sales — +Monday.com MCP (23.06); small-business — Google MCP удалён upstream (30.07). Полная копия 17 доменов из upstream main |
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
деревом считается дефектом.

| Роль | Для каких задач | Навыков | Контракт |
|------|----------------|---------|----------|
| **small-business** | Инвойсы, учёт, зарплата, налоги, CRM | 31 | — |
| **data** | SQL-запросы, дашборды, мониторинг, ML | 10 | — |
| **engineering** | Код-ревью, инциденты, архитектура, деплой | 10 | — |
| **legal** | Триаж NDA, проверка договоров, комплаенс, риски | 9 | ACTIVE |
| **human-resources** | Онбординг, вакансии, собеседования, оценка | 9 | — |
| **operations** | Процессы, вендоры, закупки, мощности | 9 | — |
| **sales** | Пайплайн, звонки, прогноз, конкурентная разведка | 9 | — |
| **finance** | Проводки, аудит, категоризация, отчётность | 8 | — |
| **marketing** | Контент, кампании, SEO, аналитика | 8 | — |
| **product-management** | PRD, роадмап, user stories, приоритизация | 8 | — |
| **design** | Дизайн-ревью, дизайн-система, accessibility | 7 | — |
| **bio-research** | PubMed, геномика, литература, эксперименты | 6 | — |
| **customer-support** | Тикеты, эскалации, база знаний, ответы | 5 | — |
| **enterprise-search** | Поиск по Slack, Notion, Jira | 5 | — |
| **productivity** | Задачи, календарь, заметки, ежедневный брифинг, тайм-трекинг | 4 | — |
| **cowork-plugin-management** | Создание и настройка новых ролей (мета) | 2 | — |
| **pdf-viewer** | Просмотр и разбор PDF | 1 | — |

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

### Домены из другого источника (claude-skills)

Навыки этих доменов лежат не в `cowork-roles/`, а в `claude-skills/`:

| Роль | Навыков | Источник |
|------|---------|---------|
| project-management | 9 | `claude-skills/project-management/` — Atlassian MCP |
| research | 8 | `claude-skills/research/` — академические исследования |
| research-ops | 5 | `claude-skills/research-ops/` — enterprise R&D (→ Vector Marketing) |

Эти домены входят в витрину Vector Work, но их навыки живут в другой библиотеке.
Смешивать их с `cowork-roles/` в одной таблице нельзя — получаются числа,
которых в дереве нет.

### Итого

    cowork-roles/   18 каталогов, 212 навыков
    claude-skills/  3 домена, 22 навыка (project-management, research, research-ops)
    partner-built   71 из 212 — витрина партнёрских MCP, а не роли организации

## Быстрый старт

```bash
git clone https://github.com/Osmosy/vector-work.git

# Срабатывает автоматически по интенту
hermes "Проверь этот NDA на риски"           # → legal
hermes "Напиши PRD для фичи экспорта в PDF"  # → product-management
hermes "Создай роль для отдела логистики"     # → cowork-plugin-management
```

## Установка

Роли установлены в Hermes: `~/.hermes/skills/cowork-roles/` — **212 навыков**
(совпадает с деревом репозитория 1:1).

## Структура репозитория

    skills/cowork-roles/   18 доменов-ролей, 212 навыков (Anthropic Cowork)
    skills/                4 своих навыка экосистемы
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
    profiles/legal.md             контракт роли legal (ACTIVE)
    profiles/legal-playbook.md    каркас плейбука переговоров и NDA

Реестр пересобирается после изменения состава: `python3 scripts/build_registry.py`.
Он же сверяет числа README с деревом и печатает расхождения.

## Источник

Адаптировано из [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) — Apache 2.0.
