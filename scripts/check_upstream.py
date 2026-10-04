#!/usr/bin/env python3
"""Сверка состава с апстримом anthropics/knowledge-work-plugins.

Зачем: бейдж «Sync: 2026-08-30» — это утверждение о свежести. Без сверки он
стареет молча. Скрипт берёт дерево апстрима через GitHub API и сравнивает:
    - список каталогов-ролей
    - число SKILL.md

Расхождение — это НЕ ошибка кода: апстрим живой, наша копия отстаёт по своей воле.
Скрипт печатает отчёт и выходит 0 всегда; в CI он запускается по расписанию и
открывает issue, а не красит push.

Запуск: python3 scripts/check_upstream.py [--json]
Переменные: UPSTREAM=owner/repo, GH_TOKEN (для API-лимита 5000/ч вместо 60/ч)
"""
import json
import os
import pathlib
import re
import sys
import urllib.request

UPSTREAM = os.environ.get("UPSTREAM", "anthropics/knowledge-work-plugins")
ROOT = pathlib.Path(__file__).resolve().parent.parent
CR = ROOT / "skills" / "cowork-roles"


def api(path):
    req = urllib.request.Request(f"https://api.github.com/{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "vector-work-check")
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def upstream_by_role():
    """Апстрим: каталоги верхнего уровня и число SKILL.md в каждом."""
    info = api(f"repos/{UPSTREAM}")
    branch = info.get("default_branch", "main")
    tree = api(f"repos/{UPSTREAM}/git/trees/{branch}?recursive=1")
    out = {}
    for t in tree.get("tree", []):
        if t["type"] == "blob" and t["path"].endswith("SKILL.md"):
            top = t["path"].split("/")[0]
            out[top] = out.get(top, 0) + 1
    return branch, out


def local_roles():
    out = {}
    for d in sorted(CR.iterdir()):
        if d.is_dir():
            out[d.name] = sum(1 for _ in d.rglob("SKILL.md"))
    return out


def main():
    as_json = "--json" in sys.argv
    by_domain = "--by-domain" in sys.argv
    local = local_roles()
    local_skills = sum(local.values())
    try:
        branch, up = upstream_by_role()
    except Exception as e:
        msg = f"апстрим недоступен: {type(e).__name__}: {e}"
        print(msg if not as_json else json.dumps({"ok": False, "error": msg},
                                                 ensure_ascii=False))
        return 0

    up_total = sum(up.values())
    report = {
        "upstream": UPSTREAM,
        "branch": branch,
        "upstream_skill_md": up_total,
        "local_skill_md": local_skills,
        "delta": up_total - local_skills,
        "ok": True,
    }
    if as_json:
        if by_domain:
            report["by_domain"] = {k: {"local": local.get(k, 0), "upstream": up.get(k, 0),
                                       "delta": up.get(k, 0) - local.get(k, 0)}
                                   for k in sorted(set(local) | set(up))}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    if not by_domain:
        print(f"апстрим {UPSTREAM} ({branch}): SKILL.md {up_total}, групп {len(up)}")
        print(f"локально в cowork-roles/:      SKILL.md {local_skills}, каталогов {len(local)}")
        d = report["delta"]
        if d == 0:
            print("расхождение: 0 — копия совпадает по числу навыков")
        elif d > 0:
            print(f"расхождение: +{d} в апстриме — апстрим ушёл вперёд, обнови бейдж")
        else:
            print(f"расхождение: {d} — локально больше (свои навыки или откат апстрима)")
        print("\nдетально по каталогам: python3 scripts/check_upstream.py --by-domain")
        return 0

    keys = sorted(set(local) | set(up),
                  key=lambda k: -abs(up.get(k, 0) - local.get(k, 0)))
    print(f"апстрим {UPSTREAM} ({branch}) против локальной копии\n")
    print(f"{'каталог':28} {'лок':>4} {'апстр':>6} {'разница':>8}")
    print("-" * 52)
    stale = []
    for k in keys:
        l, u = local.get(k, 0), up.get(k, 0)
        d = u - l
        if d > 0:
            stale.append((k, d))
        mark = "" if d == 0 else ("  ← апстрим вперёд" if d > 0 else "  ← локально больше")
        print(f"{k:28} {l:>4} {u:>6} {d:>+8}{mark}")
    print("-" * 52)
    print(f"{'ИТОГО':28} {local_skills:>4} {up_total:>6} {up_total - local_skills:>+8}")
    print("\nотстают: " + (", ".join(f"{k} (+{d})" for k, d in stale) if stale
                           else "нет — все каталоги совпадают"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
