# Vector Work

Виртуальные сотрудники на базе Hermes Agent. 14 профессиональных ролей из экосистемы Cowork (Anthropic), адаптированных под российский рынок.

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

## Как это работает

1. Ты ставишь задачу — обычным языком
2. Hermes находит подходящую роль по интенту
3. Навыки роли загружаются автоматически
4. Результат — как от профильного сотрудника

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

## Быстрый старт

```bash
git clone https://github.com/Osmosy/vector-work.git

# Пример: «проверь этот NDA»
hermes --skills vector-work "Проверь этот NDA на риски"

# Пример: «подготовь PRD»
hermes --skills vector-work "Напиши PRD для фичи экспорта в PDF"

# Создать новую роль под свою задачу
hermes --skills vector-work "Создай роль для отдела логистики"
```

## Установка

Роли уже установлены в Hermes через Cowork Roles:
```bash
ls ~/.hermes/skills/cowork-roles/
```

Если нет — установить:
```bash
git clone https://github.com/anthropics/knowledge-work-plugins /tmp/cowork
cp -r /tmp/cowork/plugins/* ~/.hermes/skills/cowork-roles/
```

## Источник

Адаптировано из [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) — 17 ролей, 141 навык. Лицензия: Apache 2.0.
