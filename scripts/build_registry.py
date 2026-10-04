#!/usr/bin/env python3
"""Генератор реестра доменов vector-work: profiles/REGISTRY.md + profiles/registry.json

Считает по ДЕРЕВУ через общий сканер `scripts/_tree.py` — единый источник правды
о составе и правах. Печатает расхождения README vs дерево; на чистом дереве их 0.

Запуск: python3 scripts/build_registry.py
Ничего домен-специфичного не утверждает: только то, что доказано деревом.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T

OUT = T.PROFILES


def registry_md(rows, tot):
    L = []
    A = L.append
    A("# Реестр доменов Vector Work\n")
    A("Сгенерировано `scripts/build_registry.py` через `scripts/_tree.py` по дереву.")
    A(f"Доменов: **{tot['domains']}** ({tot['roles']} ролей организации + "
      f"{tot['showcases']} витрина) · навыков: **{tot['skills']}** · "
      f"своих навыков экосистемы: **{tot['own_skills']}**\n")

    A("## Состав доменов\n")
    A("| Домен | Роль | Навыков | MCP-серверов | Категорий коннекторов | Python |")
    A("|---|---|---|---|---|---|")
    for r in rows:
        A(f"| {r['domain']} | {'витрина' if r['showcase'] else 'роль'} | {r['skills']} | "
          f"{r['mcp']} | {len(r['conns'])} | {r['py']} |")
    A("")

    A("## Тулсеты по домену (least privilege)\n")
    A("База одинакова для всех: " + ", ".join(f"`{t}`" for t in T.BASE_TOOLSETS) + ".\n")
    A("| Домен | Тулсеты | Сверх базы — чем доказано |")
    A("|---|---|---|")
    for r in rows:
        ts = T.toolsets_need(r)
        extra = [t for t in ts if t not in T.BASE_TOOLSETS]
        why = []
        if "connections" in extra:
            why.append(f"коннекторы ({len(r['conns'])} кат., {r['mcp']} MCP)")
        if "browser" in extra:
            why.append(r["browser_why"] or "браузер")
        if "terminal" in extra:
            why.append(r["terminal_why"] or "скрипты")
        A(f"| {r['domain']} | `{'`, `'.join(ts)}` | {'; '.join(why) or '—'} |")
    A("")

    A("## Права: безусловный запрет и «по требованию»\n")
    A("**Запрещено всем доменам без исключений** — не требует ни один навык библиотеки:\n")
    A("    " + ", ".join(f"`{c}`" for c in T.FORBIDDEN_ALWAYS))
    A("")
    A("**Выдаётся только по требованию домена** (обоснование — в таблице выше):\n")
    A("    " + ", ".join(f"`{c}`" for c in T.CONDITIONAL))
    A("")
    term = [r["domain"] for r in rows if "terminal" in T.toolsets_need(r)]
    if term:
        A(f"Терминал получает только: {', '.join(f'`{d}`' for d in term)} — "
          f"у этих доменов есть скрипты, вызываемые навыком.")
    else:
        A("Терминал не получает ни один домен.")
    if T.BROWSER_OVERRIDES:
        A("Браузер выдаётся явным решением владельца: " +
          ", ".join(f"`{d}`" for d in T.BROWSER_OVERRIDES) + ".")
    else:
        A("Браузер не выдан ни одному домену: по тексту навыка он не доказывается "
          "(эвристика давала ложные срабатывания на «открывается в браузере», "
          "«сайт-визиты», «кликабельные карточки»). Выдаётся решением владельца.")
    A("")
    return "\n".join(L)


def main():
    rows = T.scan()
    tot = T.totals(rows)
    dif = T.discrepancies(rows)

    (OUT / "REGISTRY.md").write_text(registry_md(rows, tot))
    json.dump(rows, open(OUT / "registry.json", "w"), ensure_ascii=False, indent=1)

    print("=" * 72)
    print("README vs ДЕРЕВО — расхождения")
    print("=" * 72)
    if dif:
        print(f"{'домен':26} {'README':>7} {'дерево':>7}")
        for d, a, b in dif:
            print(f"{d:26} {str(a):>7} {str(b):>7}")
    print(f"\nрасхождений: {len(dif)}")

    print("\n" + "=" * 72)
    print("СОСТОЯНИЕ ДОМЕНОВ")
    print("=" * 72)
    print(f"{'домен':24} {'навыков':>7} {'mcp':>4} {'конн':>5}  тулсеты")
    for r in rows:
        print(f"{r['domain']:24} {r['skills']:>7} {r['mcp']:>4} {len(r['conns']):>5}  "
              f"{'+'.join(T.toolsets_need(r))}")
    print(f"\nВСЕГО: доменов {tot['domains']} "
          f"({tot['roles']} ролей + {tot['showcases']} витрина), навыков {tot['skills']}, "
          f"своих {tot['own_skills']}")
    print(f"навыков, зависящих от коннекторов: "
          f"{sum(r['skills'] for r in rows if r['conns'] or r['mcp'])}")
    print(f"доменов без коннекторов вообще: "
          f"{sum(1 for r in rows if not r['conns'] and not r['mcp'])}")
    print(f"\nзаписано: {OUT/'REGISTRY.md'} и {OUT/'registry.json'}")
    return 1 if dif else 0


if __name__ == "__main__":
    sys.exit(main())
