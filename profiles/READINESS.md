# Готовность доменов Vector Work

Сгенерировано `scripts/build_readiness.py` через `scripts/_tree.py` по дереву.
Не оценивает качество — показывает, что домену нужно, чтобы заработать.

## Три слоя зрелости

    СЛОЙ 1  Структура   контракт работника есть, права определены
    СЛОЙ 2  Установка   навыки стоят в ~/.hermes/skills (вне репозитория)
    СЛОЙ 3  Данные      источники подключены, вход есть

Завод строится на слое 1. Слой 3 появится, когда появятся системы.

## Что нужно каждому домену (по факту дерева)

| Домен | Навыков | MCP | Коннекторов | Python | Тулсеты сверх базы |
|---|---|---|---|---|---|
| bio-research | 6 | 11 | 19 | 25 | connections, terminal |
| cowork-plugin-management | 2 | 0 | 8 | 0 | connections |
| customer-support | 5 | 8 | 9 | 0 | connections |
| data | 10 | 8 | 5 | 1 | connections |
| design | 7 | 9 | 7 | 0 | connections |
| engineering | 10 | 10 | 7 | 0 | connections |
| enterprise-search | 5 | 7 | 21 | 0 | connections |
| finance | 8 | 6 | 11 | 0 | connections |
| human-resources | 9 | 5 | 8 | 0 | connections |
| legal | 9 | 7 | 8 | 0 | connections |
| marketing | 8 | 13 | 14 | 0 | connections |
| operations | 9 | 6 | 8 | 0 | connections |
| partner-built | 71 | 12 | 4 | 0 | connections |
| pdf-viewer | 1 | 1 | 0 | 0 | connections |
| product-management | 8 | 16 | 11 | 0 | connections |
| productivity | 4 | 9 | 8 | 0 | connections |
| sales | 36 | 23 | 10 | 0 | connections |
| small-business | 44 | 35 | 0 | 0 | connections |

## Зависимость от внешних систем

Доменов без внешних систем нет.

Доменов, требующих коннекторов: 18 из 18.
Пока ни один коннектор не подключён, результат будет каркасным либо построенным
на общих дефолтах, а не на данных организации. Это свойство апстрима: он написан
под корпоративные MCP-системы (Slack, Jira, Salesforce, Box).

Терминал требуется доменам: `bio-research`.

## Распределение по числу навыков

     71  partner-built
     44  small-business
     36  sales
     10  data
     10  engineering
      9  human-resources
        ...  всего 252 навыков в 18 каталогах

<!-- gen:keep-begin -->
## Порядок, в котором имеет смысл оживлять (ручной раздел)

Когда появятся системы, порядок задаёт не размер домена, а число навыков,
которые заработают от одного коннектора:

    1. legal           9 навыков ← 1 источник (документы) + плейбук
    2. finance         8 навыков ← 1 источник (ERP/выгрузка)
    3. human-resources 9 навыков ← 1 источник (кадровая система)
    4. data           10 навыков ← 1 источник (хранилище/БД)

Это гипотеза порядка, а не решение. Решение — за владельцем.
<!-- gen:keep-end -->
