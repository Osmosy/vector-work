#!/usr/bin/env python3
"""Генератор READINESS.md — зрелость доменов и что нужно каждому.

Раньше READINESS.md был помечен как сгенерированный, но его писал не скрипт:
в нём жили ручные утверждения, расходящиеся с REGISTRY (legal: web vs connections,
engineering: браузер — vs да). Теперь генерируется из того же сканера.

Ручной раздел «Порядок оживления» сохраняется между маркерами.

Запуск: python3 scripts/build_readiness.py
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T

OUT = T.PROFILES
MARK_BEGIN = "<!-- gen:keep-begin -->"
MARK_END = "<!-- gen:keep-end -->"

DEFAULT_KEEP = """## Порядок, в котором имеет смысл оживлять (ручной раздел)

Когда появятся системы, порядок задаёт не размер домена, а число навыков,
которые заработают от одного коннектора:

    1. legal           9 навыков ← 1 источник (документы) + плейбук
    2. finance         8 навыков ← 1 источник (ERP/выгрузка)
    3. human-resources 9 навыков ← 1 источник (кадровая система)
    4. data           10 навыков ← 1 источник (хранилище/БД)

Это гипотеза порядка, а не решение. Решение — за владельцем.
"""


def main():
    rows = T.scan()
    tot = T.totals(rows)
    # сохранить ручной раздел, если он есть
    p = OUT / "READINESS.md"
    keep = DEFAULT_KEEP
    if p.exists():
        m = re.search(re.escape(MARK_BEGIN) + r'(.*?)' + re.escape(MARK_END),
                      p.read_text(errors="replace"), re.S)
        if m:
            keep = m.group(1).strip() + "\n"

    with_conn = [r for r in rows if r["conns"] or r["mcp"]]
    no_conn = [r for r in rows if not r["conns"] and not r["mcp"]]
    term = [r["domain"] for r in rows if "terminal" in T.toolsets_need(r)]

    L = []
    A = L.append
    A("# Готовность доменов Vector Work\n")
    A("Сгенерировано `scripts/build_readiness.py` через `scripts/_tree.py` по дереву.")
    A("Не оценивает качество — показывает, что домену нужно, чтобы заработать.\n")

    A("## Три слоя зрелости\n")
    A("    СЛОЙ 1  Структура   контракт работника есть, права определены")
    A("    СЛОЙ 2  Установка   навыки стоят в ~/.hermes/skills (вне репозитория)")
    A("    СЛОЙ 3  Данные      источники подключены, вход есть\n")
    A("Завод строится на слое 1. Слой 3 появится, когда появятся системы.\n")

    A("## Что нужно каждому домену (по факту дерева)\n")
    A("| Домен | Навыков | MCP | Коннекторов | Python | Тулсеты сверх базы |")
    A("|---|---|---|---|---|---|")
    for r in rows:
        extra = [t for t in T.toolsets_need(r) if t not in T.BASE_TOOLSETS]
        A(f"| {r['domain']} | {r['skills']} | {r['mcp']} | {len(r['conns'])} | "
          f"{r['py']} | {', '.join(extra) if extra else '—'} |")
    A("")

    A("## Зависимость от внешних систем\n")
    if no_conn:
        A(f"Доменов, работающих БЕЗ внешних систем: {len(no_conn)} — "
          + ", ".join(f"`{r['domain']}`" for r in no_conn))
    else:
        A("Доменов без внешних систем нет.")
    A("")
    A(f"Доменов, требующих коннекторов: {len(with_conn)} из {len(rows)}.")
    A("Пока ни один коннектор не подключён, результат будет каркасным либо построенным")
    A("на общих дефолтах, а не на данных организации. Это свойство апстрима: он написан")
    A("под корпоративные MCP-системы (Slack, Jira, Salesforce, Box).\n")
    if term:
        A(f"Терминал требуется доменам: {', '.join(f'`{d}`' for d in term)}.\n")

    A("## Распределение по числу навыков\n")
    by_size = sorted(rows, key=lambda r: -r["skills"])
    for r in by_size[:6]:
        A(f"    {r['skills']:3}  {r['domain']}")
    A(f"        ...  всего {tot['skills']} {T.plural(tot['skills'], 'навык', 'навыка', 'навыков')} "
          f"в {tot['domains']} каталогах\n")

    A(MARK_BEGIN)
    A(keep.rstrip())
    A(MARK_END)
    A("")
    p.write_text("\n".join(L))
    print(f"READINESS.md собран: {len(rows)} доменов, "
          f"{len(no_conn)} без коннекторов, {len(with_conn)} с коннекторами")
    print(f"ручной раздел: {'сохранён' if MARK_BEGIN in p.read_text() else 'потерян'}")


if __name__ == "__main__":
    main()
