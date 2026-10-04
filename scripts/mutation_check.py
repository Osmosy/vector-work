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
    """Число проверок — из самого валидатора, не из головы.

    N_CHECKS теперь вычисляется В ПРОГОНЕ (len(seen)), поэтому статически его не
    прочесть: запускаем валидатор на чистом дереве и берём число из его вывода.
    """
    r = subprocess.run([sys.executable, VALIDATOR], cwd=ROOT,
                       capture_output=True, text=True)
    m = re.search(r'проверок выполнено:\s*(\d+)', r.stdout)
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
     "тело изменено после приёмки: статус обязан расходиться с журналом"),
    # N1: генератор НЕ должен перевыпускать приёмку. Ломаем журнал: подменяем
    # одобренный отпечаток на текущий (как делал прежний build_contracts.py) —
    # S12 обязан поймать, что запись журнала не соответствует git-истории.
    ("S12", "profiles/approvals.jsonl", '"commit": "847738e"', '"commit": ""',
     "запись журнала без коммита приёмки"),
    ("S13", "profiles/data.md", "    владелец:    Михаил (Osmosy)",
     "    владелец:    <кто отвечает>",
     "статус ACTIVE при незаполненном владельце"),
    ("S14", "agents/orchestrator.md", "## Роли (18 доменов, 252 навыков)",
     "## Роли: 14 ролей организации",
     "устаревшее «14 ролей» в прозе"),
    ("S14", "AGENTS.md", "252 навыка. Роли описаны", "212 навыков. Роли описаны",
     "устаревшее число навыков в AGENTS.md (N4)"),
    ("S14", "docs/VOCABULARY.md", "контрактов           17", "контрактов           18",
     "число контрактов в VOCABULARY разошлось с фактом (N4)"),
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
    ("S18", "docs/vector-work.architecture.json", "Skills (252)", "Skills (212)",
     "число навыков в схеме разошлось с деревом"),
    ("S19", "README.md", "| **sales** | Пайплайн, звонки, прогноз, конкурентная разведка | 36 | ACTIVE |",
     "| **sales** | Пайплайн, звонки, прогноз, конкурентная разведка | 36 | DRAFT |",
     "колонка «Контракт» в README разошлась с фактом приёмки"),
    ("S11b", "agents/orchestrator.md", "Контрактов работников: **17**",
     "Контрактов работников: **18**", "блок приёмки в оркестраторе разошёлся с фактом"),
    ("S20", "profiles/STATUS.md", "плейсхолдеров <…>       99",
     "плейсхолдеров <…>      128", "число плейсхолдеров в STATUS разошлось с фактом"),
    ("S21", "profiles/REGISTRY.md", "Терминал получает только: `bio-research`",
     "Терминал получает только: `operations`", "проза реестра разошлась с тулсетами"),
    ("S22", "README.md", "Synced upstream: 2026-10-01", "Synced upstream: 2026-08-29",
     "бейдж синхронизации разошёлся с локом"),
    ("S23", "profiles/data.md", "8444efcd48f7", "deadbeef0000",
     "контракт не называет закреплённую ревизию апстрима"),
    ("S24", "skills/cowork-roles/MODIFICATIONS.md", "capacity-plan", "ИКС-ФАЙЛ",
     "изменённый файл убран из MODIFICATIONS.md (N2)"),
    ("S24", "upstream.lock.json", '"files": {', '"files_hidden": {',
     "лок перестал хранить пофайловые хэши (N2)"),
    # --- добираем непокрытые (план от Claude, T12) ---
    ("S6", "profiles/sales.md", "## 3. Разрешённые инструменты (least privilege)",
     "## 3. Инструменты вообще", "контракт без раздела «Разрешённые инструменты»"),
]

# Отдельные случаи, требующие удаления файла
DELETE_CASES = [
    ("S5", "profiles/human-resources.md", "отсутствующий контракт домена"),
    ("S12", "profiles/approvals.jsonl", "журнал приёмки удалён"),
    ("S1", "skills/cowork-roles/pdf-viewer/skills/view-pdf/SKILL.md",
     "каталог домена без SKILL.md"),
    ("S17", "skills/cowork-roles/design/LICENSE", "домен без LICENSE"),
]


SKRIPTS_CANNOT_WRITE = ["scripts/build_contracts.py", "scripts/build_reviews.py",
                        "scripts/check_reviews.py", "scripts/build_registry.py",
                        "scripts/build_readiness.py", "scripts/validate_structure.py"]


def journal_not_written_by_scripts():
    """Инвариант N1: НИ ОДИН скрипт не пишет в журнал приёмки.

    Журнал append-only и принадлежит человеку/внешнему гейту. Если скрипт
    научится в него писать, дефект N1 вернётся целиком (генератор снова сможет
    «одобрять» за владельца), поэтому это проверяется статически по коду.

    Точность важнее строгости окна: смотрим КОНКРЕТНЫЕ строки, где журнал идёт
    в write/dump, а не «write_text рядом с упоминанием» — иначе чтение журнала
    (approved_hash в build_contracts.py) ложно считается записью.
    """
    bad = []
    # запись = journal-переменная в write_text / open(...,'w') / json.dump(...)
    write_pat = re.compile(
        r'(JOURNAL|journal|APPROVALS|approvals)\s*[^\n]{0,20}'
        r'(write_text|\.open\([^)]*[\'"][wa]|json\.dump)')
    # или наоборот: write_text(...) / dump(...) на пути, содержащем approvals.jsonl
    direct_pat = re.compile(r'(write_text|json\.dump)\s*\([^\n]{0,120}approvals\.jsonl')
    for rel in SKRIPTS_CANNOT_WRITE:
        t = (ROOT / rel).read_text(errors="replace")
        for i, line in enumerate(t.splitlines(), 1):
            if "approvals" not in line:
                continue
            if write_pat.search(line) or direct_pat.search(line):
                bad.append(f"{rel}:{i}: пишет в approvals.jsonl")
    return bad


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

    # инвариант N1: журнал приёмки не пишет ни один скрипт
    jbad = journal_not_written_by_scripts()
    if jbad:
        for b in jbad:
            print(f"  MISS N1  {b}")
        miss += 1
    else:
        ok += 1
        print("  OK   N1  ни один скрипт не пишет в журнал приёмки")

    shutil.rmtree(tmp, ignore_errors=True)
    total = ok + miss
    print(f"\nмутаций поймано: {ok}/{total}")
    if n_checks is not None:
        covered = len({m[0] for m in MUTATIONS} | {c[0] for c in DELETE_CASES})
        print(f"проверок в валидаторе: {n_checks}; покрыто мутациями кодов: {covered} "
              f"(+ инвариант N1 отдельно)")
    if notapplied:
        print("\nмутации, которые не применились (паттерн не найден):")
        for n in notapplied:
            print("  ", n)
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
