#!/usr/bin/env python3
"""Сводка состояния контрактов Vector Work.

Считает по дереву. Работает и БЕЗ внешнего human-gate: если `human_gate.py` из
~/.hermes не найден, скрипт печатает это одной строкой и выходит 0 — он не
притворяется, что гейт закрыт, и не зависит от домашнего каталога.

Метрики раздельные (раньше складывались в одну «слоты» и это скрывало разницу):
    типовых [Т]         заполнено типовым каркасом, не решением владельца
    открытых <РЕШЕНИЕ   решение нельзя вывести из дерева
    плейсхолдеров <…>   незаполненные

Приёмка берётся из review-файлов (PAGE / MANUAL / BATCH) и сверяется с отпечатком
тела. Страницы .review.html в репозиторий не входят (.gitignore) — их отсутствие
не провал гейта.

Запуск: python3 scripts/gate_status.py
"""
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T

OUT = T.PROFILES
HG = pathlib.Path(os.environ.get(
    "HUMAN_GATE",
    pathlib.Path.home() / ".hermes/skills/claude-skills/engineering/human-gate/scripts/human_gate.py"))
STATE = OUT / ".human-gate"


def metrics(text):
    return dict(
        typical=text.count("[Т]"),
        open_decisions=text.count("<РЕШЕНИЕ"),
        placeholders=len(re.findall(r'<[а-яё][^>]{2,40}>', text)),
    )


def applied_kind(review_path):
    if not review_path.exists():
        return "нет"
    m = re.search(r'applied:\s*(\w+)', review_path.read_text(errors="replace"))
    return m.group(1) if m else "?"


def main():
    bh = OUT / "body-hashes.json"
    hashes = json.loads(bh.read_text()) if bh.exists() else {}

    contracts = [p for p in sorted(OUT.glob("*.md"))
                 if not p.stem.startswith("_")
                 and p.stem not in {"REGISTRY", "READINESS", "STATUS"}
                 and not p.stem.endswith(".review")]

    print(f"{'контракт':26} {'приёмка':8} {'[Т]':>4} {'<РЕШ':>5} {'<…>':>5}  отпечаток")
    print("-" * 78)
    tot = dict(typical=0, open_decisions=0, placeholders=0)
    kinds = {}
    for p in contracts:
        m = metrics(p.read_text(errors="replace"))
        for k in tot:
            tot[k] += m[k]
        kind = applied_kind(OUT / f"{p.stem}.review.md")
        kinds[kind] = kinds.get(kind, 0) + 1
        print(f"{p.stem:26} {kind:8} {m['typical']:>4} {m['open_decisions']:>5} "
              f"{m['placeholders']:>5}  {hashes.get(p.stem, '—')}")
    print("-" * 78)
    print(f"ИТОГО по {len(contracts)} контрактам:")
    print(f"  типовых [Т] {tot['typical']}, открытых <РЕШЕНИЕ {tot['open_decisions']}, "
          f"плейсхолдеров <…> {tot['placeholders']}")
    print("  (три РАЗНЫЕ величины, а не одна «слоты»)")
    print("  приёмка: " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))

    print()
    if not HG.exists():
        print(f"внешний human-gate не найден: {HG}")
        print("  это не провал гейта: состояние гейта локально и в репозиторий не входит.")
        print("  приёмку в репозитории сверяет: python3 scripts/check_reviews.py")
        return 0

    print(f"внешний human-gate: {HG}")
    print(f"состояние гейта: {STATE} "
          f"({'есть' if STATE.exists() else 'нет — страницы ревью не открывались'})")
    print("Чтобы принять контракт: открыть profiles/<контракт>.review.html,")
    print("отметить замечания, экспорт → profiles/<контракт>.review.md,")
    print("затем: python3 scripts/build_reviews.py (переписать приёмку честно)")
    print("Приёмку по отпечаткам сверяет: python3 scripts/check_reviews.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
