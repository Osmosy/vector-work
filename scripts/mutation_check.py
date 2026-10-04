#!/usr/bin/env python3
"""Мутационная проверка самого валидатора структуры.

Правило дома: проверка, которая «должна ловить», но не ловит, — это баг.
Поэтому каждая проверка доказывается мутацией: ломаем ровно одно утверждение
на КОПИИ дерева и ждём соответствующий ERROR. Копия делается без .git,
чтобы случайный `git checkout` не вернул исправленный файл и не дал ложный
«зелёный» (эта ошибка была допущена при первом прогоне).

Код выхода 1, если хоть одна мутация не поймана.
"""
import shutil, subprocess, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "node_modules", "__pycache__", ".venv"}


def copy_tree(dst):
    def ignore(dirpath, names):
        return [n for n in names if n in SKIP]
    shutil.copytree(ROOT, dst, ignore=ignore)


def run_validator(where):
    r = subprocess.run([sys.executable, "scripts/validate_structure.py"],
                       cwd=where, capture_output=True, text=True)
    return r.stdout + r.stderr


def edit(where, rel, old, new):
    p = pathlib.Path(where) / rel
    t = p.read_text()
    assert old in t, f"мутация не применилась: {rel}: {old[:40]!r} не найдено"
    p.write_text(t.replace(old, new, 1))


MUTATIONS = [
    ("S3", "README.md", "| **legal** | Триаж NDA, проверка договоров, комплаенс, риски | 9 |",
                     "| **legal** | Триаж NDA, проверка договоров, комплаенс, риски | 6 |",
     "число навыков в таблице ролей README"),
    ("S4", "README.md", "badge/Domains-18-green", "badge/Domains-17-green",
     "бейдж числа доменов"),
    ("S4", "README.md", "badge/Skills-212-orange", "badge/Skills-211-orange",
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
]

DELETE_CONTRACT = ("S5", "profiles/human-resources.md", "отсутствующий контракт домена")


def main():
    tmp = tempfile.mkdtemp(prefix="vw-mut-")
    ok = miss = 0
    for code, rel, old, new, what in MUTATIONS:
        # каждая мутация — на свежей копии, чтобы не накапливались
        shutil.rmtree(tmp, ignore_errors=True)
        copy_tree(tmp)
        edit(tmp, rel, old, new)
        out = run_validator(tmp)
        if f"ERROR {code}" in out:
            ok += 1
            print(f"  OK   {code}  {what}")
        else:
            miss += 1
            print(f"  MISS {code}  {what}  ← проверка НЕ ловит это")

    # отдельно: удаление контракта
    shutil.rmtree(tmp, ignore_errors=True)
    copy_tree(tmp)
    (pathlib.Path(tmp) / DELETE_CONTRACT[1]).unlink()
    out = run_validator(tmp)
    if f"ERROR {DELETE_CONTRACT[0]}" in out:
        ok += 1
        print(f"  OK   {DELETE_CONTRACT[0]}  {DELETE_CONTRACT[2]}")
    else:
        miss += 1
        print(f"  MISS {DELETE_CONTRACT[0]}  {DELETE_CONTRACT[2]}")

    shutil.rmtree(tmp, ignore_errors=True)
    total = ok + miss
    print(f"\nмутаций поймано: {ok}/{total}")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
