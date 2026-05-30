<div align="center">

<img src="assets/vector-logo.png" alt="Vector Work" width="200"/>

# Vector Work

**Виртуальные сотрудники на базе Hermes Agent — 14 профессиональных ролей из Cowork (Anthropic)**

[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue.svg)](https://github.com/NousResearch/hermes-agent)
[![Roles: 14](https://img.shields.io/badge/Roles-14-green.svg)](#роли)
[![Skills: 141](https://img.shields.io/badge/Skills-141-orange.svg)](https://github.com/anthropics/knowledge-work-plugins)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

</div>

---

14 профессиональных ролей (141 навык) из экосистемы Cowork (Anthropic), адаптированных под российский рынок. Активируются по интенту — скажи «проверь NDA» и legal включится сам.

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

| Роль | Для каких задач | Навыков |
|------|----------------|---------|
| **productivity** | Задачи, календарь, заметки, ежедневный брифинг | 3 |
| **product-management** | PRD, роадмап, user stories, приоритизация | 7 |
| **legal** | Триаж NDA, проверка договоров, комплаенс, риски | 6 |
| **finance** | Проводки, аудит, категоризация, отчётность | 6 |
| **data** | SQL-запросы, дашборды, мониторинг, ML | 6 |
| **engineering** | Код-ревью, инциденты, архитектура, деплой | 7 |
| **design** | Дизайн-ревью, дизайн-система, accessibility | 6 |
| **human-resources** | Онбординг, вакансии, собеседования, оценка | 6 |
| **operations** | Процессы, вендоры, закупки, мощности | 6 |
| **enterprise-search** | Поиск по Slack, Notion, Jira | 4 |
| **bio-research** | PubMed, геномика, литература, эксперименты | 5 |
| **small-business** | Инвойсы, учёт, зарплата, налоги, CRM | 31 |
| **cowork-plugin-management** | Создание и настройка новых ролей (мета) | 4 |
| **project-management** | Senior PM, Scrum Master, Jira, Confluence, Atlassian admin | 9 |
| **research** | Обзор литературы, гранты, патенты, syllabus | 8 |
| **productivity** | Тайм-трекинг, фокус-сессии, meeting notes | 6 |

### Новые домены (claude-skills, май 2026)

| Роль | Навыков | Источник |
|------|---------|---------|
| project-management | 9 | `claude-skills/project-management/` — 12 Python-тулов, Atlassian MCP |
| research | 8 | `claude-skills/research/` — академические исследования |
| productivity | 6 | `claude-skills/productivity/` — личная продуктивность |
| research-ops | 5 | `claude-skills/research-ops/` — enterprise R&D (→ Vector Marketing) |

## Быстрый старт

```bash
git clone https://github.com/Osmosy/vector-work.git

# Срабатывает автоматически по интенту
hermes "Проверь этот NDA на риски"           # → legal
hermes "Напиши PRD для фичи экспорта в PDF"  # → product-management
hermes "Создай роль для отдела логистики"     # → cowork-plugin-management
```

## Установка

Роли уже установлены в Hermes: `~/.hermes/skills/cowork-roles/` (141 навык).

## Источник

Адаптировано из [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) — Apache 2.0.
