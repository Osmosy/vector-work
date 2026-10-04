# Реестр доменов Vector Work

Сгенерировано `scripts/build_registry.py` по дереву, не по README.
Доменов: **18** · навыков: **212**

| Домен | Навыков | MCP-серверов | Категорий коннекторов | Python | Нужен браузер | Нужен терминал |
|---|---|---|---|---|---|---|
| bio-research | 6 | 11 | 19 | 25 | — | да |
| cowork-plugin-management | 2 | 0 | 8 | 0 | — | — |
| customer-support | 5 | 8 | 9 | 0 | да | — |
| data | 10 | 8 | 5 | 1 | да | — |
| design | 7 | 0 | 5 | 0 | да | — |
| engineering | 10 | 10 | 7 | 0 | да | — |
| enterprise-search | 5 | 7 | 21 | 0 | — | — |
| finance | 8 | 0 | 4 | 0 | да | — |
| human-resources | 9 | 0 | 6 | 0 | — | — |
| legal | 9 | 7 | 8 | 0 | — | — |
| marketing | 8 | 13 | 14 | 0 | да | — |
| operations | 9 | 6 | 8 | 0 | — | да |
| partner-built | 71 | 0 | 4 | 0 | да | — |
| pdf-viewer | 1 | 1 | 0 | 0 | да | — |
| product-management | 8 | 16 | 11 | 0 | да | — |
| productivity | 4 | 9 | 8 | 0 | да | — |
| sales | 9 | 14 | 10 | 0 | да | — |
| small-business | 31 | 11 | 0 | 0 | да | — |

## Обязательные тулсеты по домену (least privilege)

Базовые для всех: `file`, `skills`. Остальное — только если домен это требует.

| Домен | Тулсеты |
|---|---|
| bio-research | `file`, `skills`, `memory`, `connections`, `terminal` |
| cowork-plugin-management | `file`, `skills`, `memory`, `connections` |
| customer-support | `file`, `skills`, `memory`, `connections`, `browser` |
| data | `file`, `skills`, `memory`, `connections`, `browser` |
| design | `file`, `skills`, `memory`, `connections`, `browser` |
| engineering | `file`, `skills`, `memory`, `connections`, `browser` |
| enterprise-search | `file`, `skills`, `memory`, `connections` |
| finance | `file`, `skills`, `memory`, `connections`, `browser` |
| human-resources | `file`, `skills`, `memory`, `connections` |
| legal | `file`, `skills`, `memory`, `connections` |
| marketing | `file`, `skills`, `memory`, `connections`, `browser` |
| operations | `file`, `skills`, `memory`, `connections` |
| partner-built | `file`, `skills`, `memory`, `connections`, `browser` |
| pdf-viewer | `file`, `skills`, `memory`, `connections`, `browser` |
| product-management | `file`, `skills`, `memory`, `connections`, `browser` |
| productivity | `file`, `skills`, `memory`, `connections`, `browser` |
| sales | `file`, `skills`, `memory`, `connections`, `browser` |
| small-business | `file`, `skills`, `memory`, `connections`, `browser` |

## Запрещено конструктивно для всех доменов

Ни один домен библиотеки не требует:

    `terminal`, `delegate_task`, `cronjob_manage`, `browser_exec`, `computer_use`

Проверка: ни в одном навыке нет вызова команд терминала, делегирования,
cron или управления компьютером. Домены работают на тексте, шаблонах и данных.
