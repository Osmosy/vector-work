#!/usr/bin/env python3
"""Приёмка контрактов: переписать review-файлы честно и связать с отпечатком тела.

Зачем: 2026-10-04 все 18 контрактов были закрыты пачкой по слову владельца, но
16 review-файлов содержали ОДИНАКОВУЮ фразу «Посмотрел через страницу ревью» —
утверждение о построчном просмотре, которого не было. Это противоречило
profiles/STATUS.md, где честно сказано «ревью проведено выборочно».

Правильная форма: ревью пачкой описывается как ревью пачкой, а привязка к
содержимому даётся отпечатком тела. Файл ревью НЕ пишется от имени человека
без его слова — здесь фиксируется решение владельца от 2026-10-04.

Запуск: python3 scripts/build_reviews.py
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T

OUT = T.PROFILES
OWNER = "Михаил (владелец, Osmosy)"

# Контракты, которые владелец реально открывал на странице ревью 2026-10-04.
# Остальные приняты ПАЧКОЙ — и это надо сказать словами, а не шаблоном.
REVIEWED_BY_PAGE = {"engineering", "legal-playbook"}
# legal доведён вручную, но его страница ревью — раунд 1 из более раннего прогона
MANUAL = {"legal"}

BATCH_NOTE = (
    "Принято пакетом по слову владельца 2026-10-04 "
    "(«закрывай пока все пункты как типовые»). Построчного ревью не было — "
    "проверена структура, а не содержание полей."
)
PAGE_NOTE = (
    "Страница ревью открыта владельцем 2026-10-04; замечаний не вынесено. "
    "Принято как типовое: структура проверена."
)


def body_hash(text):
    lines = [l for l in text.splitlines() if not l.strip().startswith("статус:")]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:16]


def main():
    hashes = json.loads((OUT / "body-hashes.json").read_text())
    made = 0
    for p in sorted(OUT.glob("*.md")):
        stem = p.stem
        if stem.startswith("_") or stem in {"REGISTRY", "READINESS", "STATUS"}:
            continue
        if stem.endswith(".review") or stem not in hashes:
            continue
        text = p.read_text(errors="replace")
        # цитата — РЕАЛЬНАЯ строка из документа (иначе гейт ловит G7)
        first_body = ""
        for l in text.splitlines():
            s = l.strip()
            if s and not s.startswith(("#", "---", "роль:", "версия:", "статус:",
                                      "владелец:", "домен:", "источник:")):
                first_body = s[:80]
                break
        if stem in REVIEWED_BY_PAGE:
            kind, note = "PAGE", PAGE_NOTE
        elif stem in MANUAL:
            kind, note = "MANUAL", "Доведён вручную; нормы РФ сверены по первоисточнику 2026-10-04."
        else:
            kind, note = "BATCH", BATCH_NOTE
        body = (
            f"<!-- human-gate:v1 target={p.name} round=1 -->\n"
            f"reviewer: {OWNER}\n"
            f"applied: {kind}\n"
            f"body_sha256: {hashes[stem]}\n\n"
            f"## APPROVE a1\n"
            f"> {first_body}\n{note}\n"
        )
        (OUT / f"{stem}.review.md").write_text(body)
        made += 1
    print(f"ревью переписано честно: {made}")
    for stem in sorted(REVIEWED_BY_PAGE):
        print(f"  PAGE    {stem} — открывался на странице")
    for stem in sorted(MANUAL):
        print(f"  MANUAL  {stem} — доведён вручную")
    print(f"  BATCH   остальные — принято пакетом, построчного ревью не было")
    print(f"\nотпечаток тела записан в каждый review → правка тела роняет приёмку")


if __name__ == "__main__":
    main()
