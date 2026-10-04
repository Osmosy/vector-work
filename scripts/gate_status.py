#!/usr/bin/env python3
"""Состояние гейта (human-gate) по всем контрактам Vector Work.

Показывает, что уже принято, что ждёт ревью, сколько слотов осталось.
Гейт — внешний инструмент: скрипт только читает его состояние, ничего не закрывает.

Запуск: python3 scripts/gate_status.py
"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PR = ROOT / "profiles"
HG = pathlib.Path.home() / ".hermes/skills/claude-skills/engineering/human-gate/scripts/human_gate.py"
NOT_CONTRACT = {"_TEMPLATE", "REGISTRY", "READINESS", "STATUS"}


def gate(artifact):
    """Статус гейта для артефакта (читаем через сам human-gate)."""
    try:
        r = subprocess.run([sys.executable, str(HG), "status", artifact,
                            "--state-dir", str(PR / ".human-gate")],
                           cwd=PR, capture_output=True, text=True, timeout=30)
        return (r.stdout + r.stderr).strip()
    except Exception as e:
        return f"status недоступен: {e}"


def main():
    contracts = []
    for f in sorted(PR.glob("*.md")):
        if f.stem in NOT_CONTRACT or f.stem.startswith("_") or f.stem.endswith(".review"):
            continue
        contracts.append(f)
    print(f"контрактов в profiles/: {len(contracts)}\n")
    print(f"{'контракт':30} {'статус':14} {'слотов':>7}  {'страница ревью'}")
    print("-" * 84)
    active = draft = 0
    total_slots = 0
    for f in contracts:
        t = f.read_text(errors="replace")
        m = next((l.strip() for l in t.splitlines() if l.strip().startswith("статус:")), "статус: ?")
        st = "ACTIVE" if "ACTIVE" in m else ("DRAFT" if "DRAFT" in m else "PLAYBOOK" if "ЧЕРНОВИК" in m else "?")
        if st == "ACTIVE":
            active += 1
        else:
            draft += 1
        slots = t.count("<РЕШЕНИЕ") + t.count("[Т")
        total_slots += slots
        page = f.with_suffix(".review.html")
        print(f"{f.stem:30} {st:14} {slots:>7}  {'есть' if page.exists() else '— нет'}")
    print("-" * 84)
    print(f"ACTIVE: {active}   DRAFT: {draft}   слотов <РЕШЕНИЕ> всего: {total_slots}")
    print()
    print("Чтобы принять контракт:")
    print("  1. открыть profiles/<контракт>.review.html в браузере")
    print("  2. отменить замечания (или не отмечать, если их нет)")
    print("  3. экспорт в profiles/<контракт>.review.md")
    print("  4. агент применяет и закрывает гейт (close -> exit 0)")
    print()
    print("Проверить один артефакт вручную:")
    print(f"  python3 {HG} status <контракт>.md --state-dir {PR/'.human-gate'}")


if __name__ == "__main__":
    main()
