#!/usr/bin/env python3
"""Сверка приёмки с append-only журналом — без внешнего human-gate.

В CI нет ~/.hermes, поэтому `gate_status.py` (он зовёт внешний human_gate.py)
там не работает. Этот скрипт сверяет то, что лежит В РЕПОЗИТОРИИ, с якорем —
журналом `profiles/approvals.jsonl`.

Переписан после дефекта N1 (внешний аудит 2026-10-04): раньше он сверял
review-файлы с `body-hashes.json`, который генератор пересчитывал из ТЕКУЩИХ тел.
Скрипт, генератор хэшей и файл хэшей составляли замкнутый круг — любая правка
тела «подтверждалась» сама собой.

Теперь якорь — журнал, куда пишет только человек (или внешний гейт), а скрипты
не пишут вообще. Расхождение тела с журналом — это НЕ ошибка: контракт должен
быть в DRAFT, и статус проверяется как согласованный с фактом.

Код выхода 1, только если: журнала нет, запись неполная, либо строка статуса
противоречит факту (одобрено, а стоит DRAFT — или наоборот).

Запуск: python3 scripts/check_reviews.py
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T

OUT = T.PROFILES
JOURNAL = OUT / "approvals.jsonl"
APPLIED = {"PAGE", "MANUAL", "BATCH"}
FIELDS = ("stem", "body_sha256", "applied", "reviewer", "date", "commit")


def body_hash(text):
    lines = [l for l in text.splitlines() if not l.strip().startswith("статус:")]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:16]


def main():
    if not JOURNAL.exists():
        print("::error::profiles/approvals.jsonl отсутствует — журнала приёмки нет")
        return 1
    jr = {}
    bad = 0
    for line in JOURNAL.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except Exception:
            print(f"::error::approvals.jsonl: нечитаемая строка: {line[:60]}")
            bad += 1
            continue
        miss = [f for f in FIELDS if f not in e]
        if miss:
            print(f"::error::approvals.jsonl {e.get('stem','?')}: нет полей {miss}")
            bad += 1
        if e.get("applied") not in APPLIED:
            print(f"::error::{e.get('stem','?')}: неизвестный вид «{e.get('applied')}»")
            bad += 1
        jr[e.get("stem")] = e

    stats = {}
    active = draft = 0
    for stem, ap in sorted(jr.items()):
        md = OUT / f"{stem}.md"
        if not md.exists():
            print(f"::error::{stem}: запись в журнале, а файла нет")
            bad += 1
            continue
        actual = body_hash(md.read_text(errors="replace"))
        st_line = next((l for l in md.read_text(errors="replace").splitlines()
                        if l.strip().startswith("статус:")), "")
        if actual == ap["body_sha256"]:
            active += 1
            if "ACTIVE" not in st_line:
                print(f"::error::{stem}: одобрено, а статус не ACTIVE")
                bad += 1
        else:
            draft += 1
            if "DRAFT" not in st_line:
                print(f"::error::{stem}: тело изменено после приёмки, а статус не DRAFT")
                bad += 1
        stats[ap["applied"]] = stats.get(ap["applied"], 0) + 1

    print("приёмка по журналу approvals.jsonl:")
    for k in sorted(stats):
        print(f"  {k:7} {stats[k]}")
    print(f"документов в журнале: {len(jr)}, по факту: ACTIVE {active}, DRAFT {draft}")
    print(f"расхождений: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
