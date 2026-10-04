#!/usr/bin/env python3
"""Мутационная проверка самого валидатора структуры.

Правило дома: проверка, которая «должна ловить», но не ловит, — это баг.
Поэтому каждая проверка доказывается мутацией: ломаем ровно одно утверждение
на КОПИИ дерева и ждём соответствующий ERROR. Копия делается без .git,
чтобы случайный `git checkout` не вернул исправленный файл и не дал ложный
«зелёный» (эта ошибка была допущена при первом прогоне).

Счётчик проверок берётся из валидатора, а не хардкодится: иначе он разойдётся
с фактом (так и было — «проверок: 11» при 16 фактических).

Код выхода 1, если хоть одна мутация не поймана.
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "node_modules", "__pycache__", ".venv"}
VALIDATOR = "scripts/validate_structure.py"


def copy_tree(dst):
    def ignore(dirpath, names):
        return [n for n in names if n in SKIP]
    shutil.copytree(ROOT, dst, ignore=ignore)


def run_validator(where):
    r = subprocess.run([sys.executable, VALIDATOR], cwd=where,
                       capture_output=True, text=True)
    return r.stdout + r.stderr


def edit(where, rel, old, new):
    p = pathlib.Path(where) / rel
    t = p.read_text()
    assert old in t, f"мутация НЕ ПРИМЕНИЛАСЬ: {rel}: {old[:50]!r} не найдено"
    p.write_text(t.replace(old, new, 1))


def declared_checks():
    """Число проверок — из самого валидатора, не из головы."""
    t = (ROOT / VALIDATOR).read_text(errors="replace")
    m = re.search(r'^N_CHECKS\s*=\s*(\d+)', t, re.M)
    return int(m.group(1)) if m else None


# Мутации: (код проверки, файл, что ломаем, чем заменяем, описание)
MUTATIONS = [
    ("S3", "README.md",
     "| **legal** | Триаж NDA, проверка договоров, комплаенс, риски | 9 |",
     "| **legal** | Триаж NDA, проверка договоров, комплаенс, риски | 6 |",
     "число навыков в таблице ролей README"),
    ("S4", "README.md", "badge/Domains-18-green", "badge/Domains-17-green",
     "бейдж числа доменов"),
    ("S4", "README.md", "badge/Skills-252-orange", "badge/Skills-211-orange",
     "бейдж числа навыков"),
    ("S2", "profiles/data.md", "data/ — 10 навыков", "data/ — 99 навыков",
     "число навыков в контракте домена"),
    ("S7b", "profiles/design.md", "    memory         memory", "    terminal       terminal",
     "лишний тулсет сверх вычисленного по дереву"),
    ("S7", "profiles/marketing.md", "    memory         memory", "    delegate_task  delegate_task",
     "запрещённый везде тулсет"),
    ("S9", "profiles/REGISTRY.md", "Доменов: **18**", "Доменов: **17**",
     "число доменов в реестре"),
    ("S8", "README.md", "badge/License-MIT-yellow", "badge/License-Apache%202.0-yellow",
     "лицензия в бейдже против файла LICENSE"),
    ("S11", "agents/orchestrator.md", "engineering (10)", "engineering (4)",
     "число роли в orchestrator.md разошлось с деревом"),
    ("S11", "agents/orchestrator.md", "finance (8), human-resources (9), operations (9)",
     "finance (8), operations (9)",
     "orchestrator.md перестал описывать домен human-resources"),
    # --- новые: S12-S16 (план от Claude, T1/T4/T11/T12) ---
    ("S12", "profiles/sales.md", "    версия:      0.1", "    версия:      9.9",
     "правка тела контракта после приёмки (отпечаток разошёлся)"),
    ("S13", "profiles/data.md", "    владелец:    Михаил (Osmosy)",
     "    владелец:    <кто отвечает>",
     "статус ACTIVE при незаполненном владельце"),
    ("S14", "agents/orchestrator.md", "## Роли (18 доменов, 252 навыков)",
     "## Роли: 14 ролей организации",
     "устаревшее «14 ролей» в прозе"),
    ("S15", "README.md", "[docs/VOCABULARY.md](docs/VOCABULARY.md)",
     "[docs/VOCABULARY.md](docs/NOPE.md)\n\nСм. `docs/NOPE.md`.",
     "путь `docs/NOPE.md` не существует"),
    ("S16", "README.md", "3 своих навыка: autonomous-supergoal-patterns",
     "9 своих навыка: autonomous-supergoal-patterns",
     "число своих навыков разошлось с деревом"),
    ("S18", "docs/vector-work.architecture.json", "18 каталогов", "17 доменов",
     "число доменов в схеме разошлось с деревом"),
    ("S18", "docs/vector-work.architecture.json", "bio-research", "",
     "домен пропал со схемы"),
    ("S18", "docs/vector-work.architecture.html", "17 ролей + витрина partner-built", "17 доменов",
     "число в html-схеме разошлось с деревом"),
    ("S19", "README.md", "| ACTIVE (пакет) |", "| — |",
     "колонка «Контракт» разошлась с приёмкой"),
    ("S11b", "agents/orchestrator.md", "Контрактов работников: **17**",
     "Контрактов работников: **18**", "блок приёмки в оркестраторе разошёлся с фактом"),
    ("S20", "profiles/STATUS.md", "плейсхолдеров <…>      115",
     "плейсхолдеров <…>      128", "число плейсхолдеров в STATUS разошлось с фактом"),
    ("S21", "profiles/REGISTRY.md", "Терминал получает только: `bio-research`",
     "Терминал получает только: `operations`", "проза реестра разошлась с тулсетами"),
    ("S22", "README.md", "Synced upstream: 2026-10-01", "Synced upstream: 2026-08-29",
     "бейдж синхронизации разошёлся с локом"),
    ("S23", "profiles/data.md", "8444efcd48f7", "deadbeef0000",
     "контракт не называет закреплённую ревизию апстрима"),
    # --- добираем непокрытые (план от Claude, T12) ---
    ("S6", "profiles/sales.md", "## 3. Разрешённые инструменты (least privilege)",
     "## 3. Инструменты вообще", "контракт без раздела «Разрешённые инструменты»"),
]

# Отдельные случаи, требующие удаления файла
DELETE_CASES = [
    ("S5", "profiles/human-resources.md", "отсутствующий контракт домена"),
    ("S12", "profiles/sales.review.md", "приёмка без review-файла"),
    ("S1", "skills/cowork-roles/pdf-viewer/skills/view-pdf/SKILL.md",
     "каталог домена без SKILL.md"),
    ("S17", "skills/cowork-roles/design/LICENSE", "домен без LICENSE"),
]


def main():
    n_checks = declared_checks()
    tmp = tempfile.mkdtemp(prefix="vw-mut-")
    ok = miss = 0
    notapplied = []

    for code, rel, old, new, what in MUTATIONS:
        shutil.rmtree(tmp, ignore_errors=True)
        copy_tree(tmp)
        try:
            edit(tmp, rel, old, new)
        except AssertionError as e:
            notapplied.append(f"{code} {what}: {e}")
            miss += 1
            print(f"  SKIP {code}  {what}  ← мутация не применилась")
            continue
        out = run_validator(tmp)
        if f"ERROR {code}" in out:
            ok += 1
            print(f"  OK   {code}  {what}")
        else:
            miss += 1
            print(f"  MISS {code}  {what}  ← проверка НЕ ловит это")

    for code, rel, what in DELETE_CASES:
        shutil.rmtree(tmp, ignore_errors=True)
        copy_tree(tmp)
        (pathlib.Path(tmp) / rel).unlink()
        out = run_validator(tmp)
        if f"ERROR {code}" in out:
            ok += 1
            print(f"  OK   {code}  {what}")
        else:
            miss += 1
            print(f"  MISS {code}  {what}")

    shutil.rmtree(tmp, ignore_errors=True)
    total = ok + miss
    print(f"\nмутаций поймано: {ok}/{total}")
    if n_checks is not None:
        covered = len({m[0] for m in MUTATIONS} | {c[0] for c in DELETE_CASES})
        print(f"проверок в валидаторе: {n_checks}; покрыто мутациями кодов: {covered}")
    if notapplied:
        print("\nмутации, которые не применились (паттерн не найден):")
        for n in notapplied:
            print("  ", n)
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
