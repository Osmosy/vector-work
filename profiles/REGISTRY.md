# Реестр доменов Vector Work

Сгенерировано `scripts/build_registry.py` через `scripts/_tree.py` по дереву.
Доменов: **18** (17 ролей организации + 1 витрина) · навыков: **252** · своих навыков экосистемы: **3**

## Состав доменов

| Домен | Роль | Навыков | MCP-серверов | Категорий коннекторов | Python |
|---|---|---|---|---|---|
| bio-research | роль | 6 | 11 | 19 | 25 |
| cowork-plugin-management | роль | 2 | 0 | 8 | 0 |
| customer-support | роль | 5 | 8 | 9 | 0 |
| data | роль | 10 | 8 | 5 | 1 |
| design | роль | 7 | 0 | 5 | 0 |
| engineering | роль | 10 | 10 | 7 | 0 |
| enterprise-search | роль | 5 | 7 | 21 | 0 |
| finance | роль | 8 | 0 | 4 | 0 |
| human-resources | роль | 9 | 0 | 6 | 0 |
| legal | роль | 9 | 7 | 8 | 0 |
| marketing | роль | 8 | 13 | 14 | 0 |
| operations | роль | 9 | 6 | 8 | 0 |
| partner-built | витрина | 71 | 12 | 4 | 0 |
| pdf-viewer | роль | 1 | 1 | 0 | 0 |
| product-management | роль | 8 | 16 | 11 | 0 |
| productivity | роль | 4 | 9 | 8 | 0 |
| sales | роль | 36 | 23 | 10 | 0 |
| small-business | роль | 44 | 35 | 0 | 0 |

## Тулсеты по домену (least privilege)

База одинакова для всех: `file`, `skills`, `memory`.

| Домен | Тулсеты | Сверх базы — чем доказано |
|---|---|---|
| bio-research | `file`, `skills`, `memory`, `connections`, `terminal` | коннекторы (19 кат., 11 MCP); single-cell-rna-qc: «python3 scripts/» |
| cowork-plugin-management | `file`, `skills`, `memory`, `connections` | коннекторы (8 кат., 0 MCP) |
| customer-support | `file`, `skills`, `memory`, `connections` | коннекторы (9 кат., 8 MCP) |
| data | `file`, `skills`, `memory`, `connections` | коннекторы (5 кат., 8 MCP) |
| design | `file`, `skills`, `memory`, `connections` | коннекторы (5 кат., 0 MCP) |
| engineering | `file`, `skills`, `memory`, `connections` | коннекторы (7 кат., 10 MCP) |
| enterprise-search | `file`, `skills`, `memory`, `connections` | коннекторы (21 кат., 7 MCP) |
| finance | `file`, `skills`, `memory`, `connections` | коннекторы (4 кат., 0 MCP) |
| human-resources | `file`, `skills`, `memory`, `connections` | коннекторы (6 кат., 0 MCP) |
| legal | `file`, `skills`, `memory`, `connections` | коннекторы (8 кат., 7 MCP) |
| marketing | `file`, `skills`, `memory`, `connections` | коннекторы (14 кат., 13 MCP) |
| operations | `file`, `skills`, `memory`, `connections` | коннекторы (8 кат., 6 MCP) |
| partner-built | `file`, `skills`, `memory`, `connections` | коннекторы (4 кат., 12 MCP) |
| pdf-viewer | `file`, `skills`, `memory`, `connections` | коннекторы (0 кат., 1 MCP) |
| product-management | `file`, `skills`, `memory`, `connections` | коннекторы (11 кат., 16 MCP) |
| productivity | `file`, `skills`, `memory`, `connections` | коннекторы (8 кат., 9 MCP) |
| sales | `file`, `skills`, `memory`, `connections` | коннекторы (10 кат., 23 MCP) |
| small-business | `file`, `skills`, `memory`, `connections` | коннекторы (0 кат., 35 MCP) |

## Права: безусловный запрет и «по требованию»

**Запрещено всем доменам без исключений** — не требует ни один навык библиотеки:

    `delegate_task`, `cronjob_manage`, `computer_use`

**Выдаётся только по требованию домена** (обоснование — в таблице выше):

    `connections`, `browser`, `terminal`

Терминал получает только: `bio-research` — у этих доменов есть скрипты, вызываемые навыком.
Браузер не выдан ни одному домену: по тексту навыка он не доказывается (эвристика давала ложные срабатывания на «открывается в браузере», «сайт-визиты», «кликабельные карточки»). Выдаётся решением владельца.
