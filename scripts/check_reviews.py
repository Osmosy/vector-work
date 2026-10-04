#!/usr/bin/env python3
"""Сверка приёмки по отпечаткам тел — без внешнего human-gate.

В CI нет ~/.hermes, поэтому `gate_status.py` (он зовёт внешний human_gate.py)
там не работает. Этот скрипт проверяет то, что лежит В РЕПОЗИТОРИИ:
у каждого контракта есть review-файл с отпечатком, и отпечаток совпадает.

Код выхода 1, если приёмка расходится с содержимым.

Запуск: python3 scripts/check_reviews.py
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T

OUT = T.PROFILES
APPLIED = {"PAGE", "MANUAL", "BATCH"}


def body_hash(text):
    lines = [l for l in text.splitlines() if not l.strip().startswith("статус:")]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:16]


def main():
    bh = OUT / "body-hashes.json"
    if not bh.exists():
        print("::error::profiles/body-hashes.json отсутствует — прогони build_contracts.py")
        return 1
    hashes = json.loads(bh.read_text())
    bad = 0
    stats = {}
    for stem, h in sorted(hashes.items()):
        md = OUT / f"{stem}.md"
        rv = OUT / f"{stem}.review.md"
        if not rv.exists():
            print(f"::error::{stem}: нет review-файла — приёмки нет")
            bad += 1
            continue
        t = rv.read_text(errors="replace")
        # отпечаток должен совпадать с файлом хэшей
        if f"body_sha256: {h}" not in t:
            print(f"::error::{stem}: отпечаток в review не совпадает ({h})")
            bad += 1
            continue
        # отпечаток должен совпадать с фактическим телом
        if md.exists() and body_hash(md.read_text(errors="replace")) != h:
            print(f"::error::{stem}: тело изменено после приёмки — нужно новое ревью")
            bad += 1
            continue
        kind = "?"
        for line in t.splitlines():
            if line.startswith("applied:"):
                kind = line.split(":", 1)[1].strip()
        if kind not in APPLIED:
            print(f"::error::{stem}: неизвестный тип приёмки «{kind}»")
            bad += 1
            continue
        stats[kind] = stats.get(kind, 0) + 1

    print("приёмка по отпечаткам:")
    for k in sorted(stats):
        print(f"  {k:7} {stats[k]}")
    print(f"контрактов сверено: {len(hashes)}, расхождений: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
