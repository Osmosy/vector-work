#!/usr/bin/env python3
"""Черновики и отчёт по приёмке. НЕ пишет приёмку — только показывает состояние.

Почему переписан (дефект N1, найденный внешним аудитом 2026-10-04): раньше этот
скрипт ЗАПИСЫВАЛ `*.review.md` от имени владельца, беря отпечаток из только что
пересчитанного `body-hashes.json`. Вместе с `build_contracts.py` это замыкало
цепочку: правка тела → S12 просит прогнать генератор → генератор пересчитал хэш →
скрипт выдал новую приёмку от имени владельца → снова зелёно. Приёмка переставала
что-либо защищать. Так уже произошло с телами всех 18 документов.

Новый порядок:
    1. ревьюер открывает `profiles/<домен>.review.html` (внешний human-gate);
    2. его решение ложится в `profiles/approvals.jsonl` — append-only журнал;
    3. `build_contracts.py` выводит статус ИЗ ЖУРНАЛА: хэш совпал → ACTIVE,
       не совпал → DRAFT — изменён после приёмки.

Этот скрипт только ПОКАЗЫВАЕТ расхождения; писать приёмку он не умеет.

Запуск:
    python3 scripts/build_reviews.py                    # отчёт по журналу
    python3 scripts/build_reviews.py --draft <домен>    # черновик для ревьюера
"""
import hashlib
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T

OUT = T.PROFILES
JOURNAL = OUT / "approvals.jsonl"


def body_hash(text):
    lines = [l for l in text.splitlines() if not l.strip().startswith("статус:")]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:16]


def journal_last():
    """Последняя запись журнала по каждому документу (append-only, побеждает поздняя)."""
    out = {}
    if not JOURNAL.exists():
        return out
    for line in JOURNAL.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except Exception:
            continue
        out[e.get("stem")] = e
    return out


def documents():
    names = []
    for p in sorted(OUT.glob("*.md")):
        if p.stem.startswith("_") or p.stem in {"REGISTRY", "READINESS", "STATUS"}:
            continue
        if p.stem.endswith(".review"):
            continue
        names.append(p)
    return names


def report():
    jr = journal_last()
    print(f"журнал приёмки: {JOURNAL.name} — {len(jr)} документов с записью")
    print(f"{'документ':26} {'одобрено':>10} {'текущее':>10}  состояние")
    print("-" * 68)
    drift = 0
    for p in documents():
        cur = body_hash(p.read_text(errors="replace"))
        ap = jr.get(p.stem)
        appr = ap.get("body_sha256", "—") if ap else "—"
        if not ap:
            state = "приёмки нет → DRAFT"
            drift += 1
        elif appr == cur:
            state = f"ACTIVE ({ap.get('applied')} {ap.get('commit')})"
        else:
            state = "ИЗМЕНЁН после приёмки → DRAFT"
            drift += 1
        print(f"{p.stem:26} {appr:>10} {cur:>10}  {state}")
    print("-" * 68)
    print(f"расхождений с журналом: {drift}")
    if drift:
        print("Приёмку выдаёт ЧЕЛОВЕК: строка в approvals.jsonl (append-only), не скрипт.")
    return 0


def draft(dom):
    p = OUT / f"{dom}.md"
    if not p.exists():
        print(f"{dom}.md не найден")
        return 1
    text = p.read_text(errors="replace")
    first_body = ""
    for l in text.splitlines():
        s = l.strip()
        if s and not s.startswith(("#", "---", "роль:", "версия:", "статус:",
                                   "владелец:", "домен:", "источник:")):
            first_body = s[:80]
            break
    print(f"--- черновик для {dom}.review.md; заполняет РЕВЬЮЕР, не скрипт ---")
    print("reviewer: <кто ревьюит>")
    print("applied:  <PAGE|MANUAL|BATCH>")
    print(f"body_sha256: {body_hash(text)}")
    print("## APPROVE a1")
    print(f"> {first_body}")
    print("<что ревьюер решил — его словами>")
    print()
    print("Затем строка в profiles/approvals.jsonl:")
    print(json.dumps(dict(stem=dom, body_sha256=body_hash(text), applied="<вид>",
                          reviewer="<кто>", date="<дата>", commit="<коммит>"),
                     ensure_ascii=False))
    return 0


def main():
    if "--draft" in sys.argv:
        i = sys.argv.index("--draft")
        return draft(sys.argv[i + 1]) if i + 1 < len(sys.argv) else 1
    return report()


if __name__ == "__main__":
    sys.exit(main())
