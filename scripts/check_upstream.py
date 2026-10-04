#!/usr/bin/env python3
"""Сверка состава с апстримом anthropics/knowledge-work-plugins + пиннинг ревизии.

Зачем: бейдж синхронизации — утверждение о свежести, и без сверки он стареет
молча. Плюс у копии должна быть названа РЕВИЗИЯ, из которой она взята: дата
синхронизации и дата коммита апстрима — разные вещи.

Расхождение с апстримом — НЕ ошибка кода: апстрим живой, копия отстаёт по своей
воле. Скрипт печатает отчёт и выходит 0; в CI он идёт по расписанию и открывает
issue, а не красит push.

Пиннинг `upstream.lock.json` фиксирует, из какого коммита взята копия:
    repo, sha, date, skill_md (в апстриме), local_skill_md, stale (отстающие каталоги)

Запуск:
    python3 scripts/check_upstream.py --pin            # зафиксировать ревизию
    python3 scripts/check_upstream.py --write-badge    # переписать бейдж и блок README
    python3 scripts/check_upstream.py [--by-domain|--json]
Переменные: UPSTREAM=owner/repo, GH_TOKEN (лимит API 5000/ч вместо 60/ч)
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
LOCK = ROOT / "upstream.lock.json"
README = ROOT / "README.md"

# Блоки в README пишутся между маркерами — руками не правятся.
# Две пары: бейдж наверху и абзац состояния в разделе «Синхронизация».
START = "<!-- gen:sync:start -->"
END = "<!-- gen:sync:end -->"
STATE_START = "<!-- gen:syncstate:start -->"
STATE_END = "<!-- gen:syncstate:end -->"


def api(path):
    req = urllib.request.Request(f"https://api.github.com/{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "vector-work-check")
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def upstream_meta(sha=None):
    """Апстрим на конкретном коммите (или HEAD ветки): коммит + разбивка навыков."""
    info = api(f"repos/{UPSTREAM}")
    branch = info.get("default_branch", "main")
    if sha:
        c = api(f"repos/{UPSTREAM}/commits/{sha}")
        sha_now = c["sha"]
    else:
        c = api(f"repos/{UPSTREAM}/commits/{branch}")
        sha_now = c["sha"]
    date = c["commit"]["committer"]["date"]
    tree = api(f"repos/{UPSTREAM}/git/trees/{sha_now}?recursive=1")
    by_domain = {}
    for t in tree.get("tree", []):
        if t["type"] == "blob" and t["path"].endswith("SKILL.md") and "/skills/" in t["path"]:
            top = t["path"].split("/")[0]
            by_domain[top] = by_domain.get(top, 0) + 1
    return dict(repo=UPSTREAM, branch=branch, sha=sha_now, date=date,
                skill_md=sum(by_domain.values()), by_domain=by_domain)


def local_by_role():
    return {d.name: sum(1 for _ in d.rglob("SKILL.md"))
            for d in sorted(CR.iterdir()) if d.is_dir()}


def read_lock():
    return json.loads(LOCK.read_text()) if LOCK.exists() else None


def do_pin(sha=None):
    """Зафиксировать ревизию апстрима, ИЗ КОТОРОЙ взята копия.

    Без аргумента берётся HEAD ветки. С аргументом — конкретный коммит: копия
    могла быть взята раньше, и пиннинг HEAD записал бы неверную ревизию.
    """
    meta = upstream_meta(sha=sha)
    local = local_by_role()
    meta["local_skill_md"] = sum(local.values())
    meta["matched_count"] = sum(1 for k in local if meta["by_domain"].get(k) == local[k])
    meta["stale"] = {k: {"local": local[k], "upstream": meta["by_domain"][k]}
                     for k in sorted(local)
                     if k in meta["by_domain"] and meta["by_domain"][k] != local[k]}
    old = read_lock()
    LOCK.write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    print(f"лок записан: {LOCK.name}")
    print(f"  апстрим {meta['repo']} @ {meta['sha'][:12]} ({meta['date'][:10]})")
    print(f"  в апстриме {meta['skill_md']} SKILL.md, локально {meta['local_skill_md']}")
    print(f"  совпадающих каталогов {meta['matched_count']} из {len(local)}, "
          f"отстающих {len(meta['stale'])}")
    if old and old.get("sha") != meta["sha"]:
        print(f"  апстрим сдвинулся с {old['sha'][:12]}")
    return 0


def do_write_badge():
    lock = read_lock()
    if not lock:
        print("upstream.lock.json не найден — сначала `--pin`")
        return 1
    if not README.exists():
        print("README.md не найден")
        return 1
    text = README.read_text(errors="replace")
    if START not in text or END not in text:
        print(f"в README нет маркеров {START} / {END}")
        return 1

    d = lock["date"][:10].replace("-", "__")
    stale = lock.get("stale", {})
    if stale:
        items = ", ".join(f"`{k}` ({v['upstream']} против {v['local']})"
                          for k, v in list(stale.items())[:6])
        tail = f"Отстают каталоги: {items}."
    else:
        tail = "Все каталоги совпадают по числу навыков."

    # 1. бейдж
    badge = "\n".join([
        START,
        f"[![Synced upstream: {lock['date'][:10]}](https://img.shields.io/badge/"
        f"synced_upstream-{d}-blueviolet.svg)]"
        f"(https://github.com/{lock['repo']}/commits/main)",
        END,
    ])
    # 2. абзац состояния
    state = "\n".join([
        STATE_START,
        f"Состояние сверки на {lock['date'][:10]}: копия закреплена от "
        f"`{lock['repo']}` @ `{lock['sha'][:12]}`. На этой ревизии в апстриме "
        f"{lock['skill_md']} `SKILL.md`, в копии {lock['local_skill_md']}. {tail}",
        STATE_END,
    ])

    new = text
    for s, e, block in ((START, END, badge), (STATE_START, STATE_END, state)):
        if s not in new or e not in new:
            print(f"в README нет маркеров {s} / {e}")
            return 1
        new = re.sub(re.escape(s) + r".*?" + re.escape(e), block, new, flags=re.S)
    if new == text:
        print("бейдж и блок синхронизации уже актуальны")
        return 0
    README.write_text(new)
    print(f"бейдж и абзац синхронизации обновлены (ревизия {lock['sha'][:12]})")
    return 0


def do_check():
    """Проверка БЕЗ записи: бейдж и абзац состояния совпадают с локом.

    Нужна потому, что `--write-badge` меняет файл: в CI это недопустимо —
    проверка обязана только читать и падать, а не править дерево.
    """
    lock = read_lock()
    if not lock:
        print("upstream.lock.json не найден — ревизия не закреплена")
        return 1
    text = README.read_text(errors="replace")
    d = lock["date"][:10].replace("-", "__")
    want_badge_date = lock["date"][:10]
    want_sha = lock["sha"][:12]
    bad = []
    m = re.search(r'gen:sync:start.*?Synced upstream:\s*([0-9-]{10})', text, re.S)
    if not m:
        bad.append("нет бейджа между gen:sync")
    elif m.group(1) != want_badge_date:
        bad.append(f"бейдж {m.group(1)} ≠ лок {want_badge_date}")
    m2 = re.search(r'gen:syncstate:start.*?`([0-9a-f]{12})`', text, re.S)
    if not m2:
        bad.append("абзац состояния не называет ревизию")
    elif m2.group(1) != want_sha:
        bad.append(f"ревизия {m2.group(1)} ≠ лок {want_sha}")
    if want_sha not in text:
        bad.append(f"ревизии {want_sha} нет в README")
    if bad:
        for b in bad:
            print(f"  РАСХОЖДЕНИЕ {b}")
        print("прогони: python3 scripts/check_upstream.py --write-badge")
        return 1
    print(f"бейдж и абзац синхронизации совпадают с локом ({want_sha})")
    return 0


def main():
    if "--pin" in sys.argv:
        i = sys.argv.index("--pin")
        sha = sys.argv[i + 1] if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("-") else None
        return do_pin(sha)
    if "--write-badge" in sys.argv:
        return do_write_badge()
    if "--check" in sys.argv:
        return do_check()

    as_json = "--json" in sys.argv
    by_domain = "--by-domain" in sys.argv
    lock = read_lock()
    local = local_by_role()
    local_skills = sum(local.values())
    try:
        meta = upstream_meta(sha=(lock or {}).get("sha"))
    except Exception as e:
        msg = f"апстрим недоступен: {type(e).__name__}: {e}"
        print(msg if not as_json else json.dumps({"ok": False, "error": msg},
                                                 ensure_ascii=False))
        return 0

    up, up_total = meta["by_domain"], meta["skill_md"]
    report = {"upstream": UPSTREAM, "sha": meta["sha"][:12], "date": meta["date"][:10],
              "upstream_skill_md": up_total, "local_skill_md": local_skills,
              "delta": up_total - local_skills, "ok": True,
              "pinned_sha": (lock or {}).get("sha", "")[:12],
              "pin_matches": bool(lock) and lock.get("sha") == meta["sha"]}
    if as_json:
        if by_domain:
            report["by_domain"] = {k: {"local": local.get(k, 0), "upstream": up.get(k, 0),
                                       "delta": up.get(k, 0) - local.get(k, 0)}
                                   for k in sorted(set(local) | set(up))}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    if not by_domain:
        print(f"апстрим {UPSTREAM} @ {meta['sha'][:12]} ({meta['date'][:10]}): "
              f"SKILL.md {up_total}, групп {len(up)}")
        print(f"локально в cowork-roles/:      SKILL.md {local_skills}, каталогов {len(local)}")
        if lock:
            same = lock.get("sha") == meta["sha"]
            print(f"закреплено: {lock['sha'][:12]} — "
                  + ("совпадает с апстримом" if same else "апстрим сдвинулся, обнови --pin"))
        else:
            print("закрепления нет — прогони --pin, чтобы зафиксировать ревизию")
        d = report["delta"]
        if d == 0:
            print("расхождение: 0 — копия совпадает по числу навыков")
        elif d > 0:
            print(f"расхождение: +{d} в апстриме")
        else:
            print(f"расхождение: {d} — локально больше (свои навыки или откат апстрима)")
        print("\nдетально по каталогам: python3 scripts/check_upstream.py --by-domain")
        return 0

    keys = sorted(set(local) | set(up),
                  key=lambda k: -abs(up.get(k, 0) - local.get(k, 0)))
    print(f"апстрим {UPSTREAM} @ {meta['sha'][:12]} ({meta['date'][:10]})\n")
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
