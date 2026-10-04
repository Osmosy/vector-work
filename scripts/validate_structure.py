#!/usr/bin/env python3
"""Валидатор структуры vector-work. Гоняется в CI на каждый push.

Проверяет только СТРУКТУРНЫЕ инварианты — то, что можно доказать по дереву.
Устаревшие числа считаются дефектом, а не стилистикой.

Коды выхода: 0 — чисто, 1 — есть ошибки (печатаются все, не первая).

Проверки:
  S1  каждый каталог домена имеет SKILL.md хотя бы в одном навыке
  S2  число навыков в домене совпадает для дерева и профиля
  S3  все числа таблицы ролей README совпадают с деревом
  S4  бейджи Domains/Skills совпадают с деревом
  S5  каждый домен (кроме витрин) имеет контракт profiles/<домен>.md
  S6  каждый контракт, кроме партнёрских, объявляет тулсеты
  S7  ни один контракт не даёт запрещённых везде тулсетов
  S8  LICENSE существует и бейдж лицензии совпадает с типом файла
  S9  REGISTRY.md и README согласованы по числу доменов
  S10 READINESS.md не ссылается на несуществующие домены
  S11 orchestrator.md описывает все домены и его числа совпадают с деревом
"""
import sys, re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CR = ROOT / "skills" / "cowork-roles"
PR = ROOT / "profiles"
SKIP_CONTRACT = {"partner-built"}     # витрина, контракта не имеет
# файлы в profiles/, которые не являются контрактами домена
NOT_CONTRACT = {"_TEMPLATE", "REGISTRY", "READINESS", "STATUS"}
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T
ALWAYS_FORBIDDEN = ["delegate_task", "cronjob_manage", "computer_use"]
# Осознанные расширения прав сверх вычисленных по дереву. Каждое должно быть
# названо здесь явно — иначе проверка S7b валит контракт. Так новый лишний
# тулсет не проскочит молча.
EXTRA_ALLOWED = {
    "legal": {"web"},   # сверка действующей редакции нормы по первоисточнику
}
errors, notes = [], []
checks_seen = set()   # коды фактически выполненных проверок (для честного счётчика)


def tree_domains():
    out = {}
    for d in sorted(CR.iterdir()):
        if d.is_dir():
            out[d.name] = sum(1 for _ in d.rglob("SKILL.md"))
    return out


def contract_toolsets(p):
    """Тулсеты, объявленные в разделе 3 контракта."""
    t = p.read_text(errors="replace")
    m = re.search(r'## 3\. Разрешённые инструменты.*?(?=\n## )', t, re.S)
    if not m:
        return None
    return set(re.findall(r'^\s{4}([a-z_]+)\s{2,}', m.group(0), re.M))


def registry_expected(domain):
    """Тулсеты, вычисленные по дереву (REGISTRY.md) — верхняя граница прав.

    В REGISTRY.md две таблицы: состав (без бэктиков) и тулсеты (в бэктиках).
    Строка домена встречается в обеих — берём ту, где есть `тулсеты`.
    """
    reg = PR / "REGISTRY.md"
    if not reg.exists():
        return []
    t = reg.read_text(errors="replace")
    for m in re.finditer(rf'^\|\s*{re.escape(domain)}\s*\|(.+)\|\s*$', t, re.M):
        found = re.findall(r'`([a-z_]+)`', m.group(1))
        if found:
            return found
    return []


dom = tree_domains()
print(f"доменов в дереве: {len(dom)}, навыков: {sum(dom.values())}")

checks_seen.update({'S1','S2'})
# S1 / S2
for name, n in dom.items():
    if n == 0:
        errors.append(f"S1 {name}: каталог домена без SKILL.md")
for f in PR.glob("*.md"):
    if f.stem in SKIP_CONTRACT or f.stem in NOT_CONTRACT or f.stem.startswith("_"):
        continue
    if f.stem.endswith("-playbook") or f.stem.endswith(".review"):
        continue
    t = f.read_text(errors="replace")
    m = re.search(r'домен:\s+skills/cowork-roles/([a-z-]+)/\s*—\s*(\d+)', t)
    if not m:
        errors.append(f"S2 {f.name}: не найдено объявление домена")
        continue
    dname, dnum = m.group(1), int(m.group(2))
    if dname in dom and dom[dname] != dnum:
        errors.append(f"S2 {f.name}: объявлено {dnum} навыков, в дереве {dom[dname]}")

checks_seen.add('S3')
# S3 — числа таблицы ролей README
rd = (ROOT / "README.md").read_text(errors="replace")
roles = re.findall(r'^\|\s*\*{0,2}([a-z-]+)\*{0,2}\s*\|[^|]*\|\s*(\d+)\s*\|', rd, re.M)
for name, num in roles:
    if name in dom and int(num) != dom[name]:
        errors.append(f"S3 README роль {name}: {num} ≠ дерево {dom[name]}")

checks_seen.add('S4')
# S4 — бейджи
for badge, val in (("Domains", len(dom)), ("Skills", sum(dom.values()))):
    m = re.search(rf'badge/{badge}-(\d+)-', rd)
    if not m:
        errors.append(f"S4 бейдж {badge} не найден")
    elif int(m.group(1)) != val:
        errors.append(f"S4 бейдж {badge}: {m.group(1)} ≠ {val}")

checks_seen.update({'S5','S6','S7','S7b'})
# S5 / S6 / S7
for name in dom:
    if name in SKIP_CONTRACT:
        continue
    p = PR / f"{name}.md"
    if not p.exists():
        errors.append(f"S5 нет контракта profiles/{name}.md")
        continue
    ts = contract_toolsets(p)
    if ts is None:
        errors.append(f"S6 {p.name}: нет раздела «Разрешённые инструменты»")
    else:
        if not ts:
            errors.append(f"S6 {p.name}: тулсеты не объявлены")
        for f in ALWAYS_FORBIDDEN:
            if f in ts:
                errors.append(f"S7 {p.name}: запрещённый везде тулсет «{f}» в правах")
        # S7b — строгий least-privilege: контракт не вправе превысить то,
        # что вычислено по дереву, плюс осознанно разрешённое в EXTRA_ALLOWED
        expect = set(registry_expected(name)) | EXTRA_ALLOWED.get(name, set())
        extra = ts - expect
        for e in sorted(extra):
            if e not in ALWAYS_FORBIDDEN:
                errors.append(f"S7b {p.name}: тулсет «{e}» не требуется доменом по дереву")

checks_seen.add('S8')
# S8 — лицензия
lic = ROOT / "LICENSE"
if not lic.exists():
    errors.append("S8 LICENSE отсутствует, но на него ссылается бейдж")
else:
    head = lic.read_text(errors="replace")[:400]
    kind = "MIT" if "MIT License" in head else ("Apache" if "Apache License" in head else None)
    m = re.search(r'badge/License-([A-Za-z0-9.%]+)-', rd)
    badge_kind = (m.group(1) if m else "").replace("%20", " ").replace(".0", "")
    if kind and badge_kind and kind.lower() not in badge_kind.lower():
        errors.append(f"S8 LICENSE={kind}, бейдж={badge_kind}")

checks_seen.add('S9')
# S9
reg = (PR / "REGISTRY.md")
if not reg.exists():
    errors.append("S9 profiles/REGISTRY.md отсутствует")
else:
    m = re.search(r'Доменов:\s*\*\*(\d+)\*\*', reg.read_text(errors="replace"))
    if not m or int(m.group(1)) != len(dom):
        errors.append(f"S9 REGISTRY.md: доменов {m.group(1) if m else '?'} ≠ {len(dom)}")

checks_seen.add('S10')
# S10
rm = (PR / "READINESS.md")
if rm.exists():
    for name in re.findall(r'^\s{4}([a-z][a-z-]{2,})\s+\d+\s+\d+', rm.read_text(errors="replace"), re.M):
        if name not in dom and name not in {"domain"}:
            notes.append(f"S10 READINESS.md упоминает «{name}», которого нет в дереве")

checks_seen.add('S11')
# S11 — оркестратор не отстаёт от дерева: числа ролей в agents/orchestrator.md
orch = ROOT / "agents" / "orchestrator.md"
if not orch.exists():
    errors.append("S11 agents/orchestrator.md отсутствует")
else:
    t = orch.read_text(errors="replace")
    seen = set()
    for name, num in re.findall(r'\*{0,2}([a-z][a-z-]+)\*{0,2}\s*\((\d+)\)', t):
        seen.add(name)
        if name in dom and int(num) != dom[name]:
            errors.append(f"S11 orchestrator.md {name}: {num} ≠ дерево {dom[name]}")
    missing = set(dom) - seen - SKIP_CONTRACT   # витрины не обязаны быть ролью в списке
    if missing:
        errors.append(f"S11 orchestrator.md не описывает домены: {', '.join(sorted(missing))}")

checks_seen.add('S12')
# S12 — приёмка подкреплена отпечатком тела. Правка тела без нового ревью — ошибка.
import hashlib as _hl
import json as _json
bh = OUT_HASHES = PR / "body-hashes.json"
if not bh.exists():
    errors.append("S12 profiles/body-hashes.json отсутствует — прогони build_contracts.py")
else:
    hashes = _json.loads(bh.read_text()) if bh.exists() else {}
    for stem, h in hashes.items():
        md = PR / f"{stem}.md"
        rv = PR / f"{stem}.review.md"
        if not rv.exists():
            errors.append(f"S12 {stem}: статус без review-файла — приёмки нет")
            continue
        rt = rv.read_text(errors="replace")
        m = re.search(r'body_sha256:\s*([0-9a-f]{8,64})', rt)
        if not m:
            errors.append(f"S12 {stem}.review.md: нет отпечатка тела (body_sha256)")
        elif m.group(1) != h:
            errors.append(f"S12 {stem}: тело изменено после приёмки "
                          f"(review {m.group(1)}, сейчас {h}) — нужно новое ревью")
        # отпечаток в файле хэшей должен совпадать с фактическим телом
        if md.exists():
            lines = [l for l in md.read_text(errors="replace").splitlines()
                     if not l.strip().startswith("статус:")]
            actual = _hl.sha256("\n".join(lines).encode()).hexdigest()[:16]
            if actual != h:
                errors.append(f"S12 {stem}: body-hashes.json устарел "
                              f"({h} ≠ {actual}) — прогони build_contracts.py")

checks_seen.add('S13')
# S13 — статус ACTIVE не держится на незаполненном плейсхолдере владельца.
# Шапка контракта — блок метаданных с отступом, а НЕ первый абзац текста
# (первый абзац — заголовок «# Контракт работника: X»).
for stem in (hashes if bh.exists() else []):
    md = PR / f"{stem}.md"
    if not md.exists():
        continue
    head_lines = []
    for line in md.read_text(errors="replace").splitlines():
        if line.strip() and not line.startswith(("#", "    ")):
            break
        head_lines.append(line)
    head = "\n".join(head_lines)
    if "ACTIVE" in head and "<кто отвечает>" in head:
        errors.append(f"S13 {stem}: статус ACTIVE при незаполненном владельце "
                      f"«<кто отвечает>» — назначь владельца или понизь статус")

checks_seen.add('S14')
# S14 — в публичных текстах нет устаревших утверждений о СОСТАВЕ и чужого локального пути.
# Историческая строка журнала синхронизации («init: 14 ролей») — не утверждение о
# текущем составе, поэтому строки таблицы журнала из проверки исключены.
PUBLIC = ["README.md", "agents/orchestrator.md", "agent-description.md"]
for rel in PUBLIC:
    p = ROOT / rel
    if not p.exists():
        continue
    t = p.read_text(errors="replace")
    for line in t.splitlines():
        if line.lstrip().startswith("|"):        # таблицы (журнал, роли) — не проза
            continue
        if re.search(r'\b14\s+(профессиональных\s+)?рол', line):
            errors.append(f"S14 {rel}: устаревшее «14 ролей» в прозе — "
                          f"ролей {T.totals()['roles']}")
            break
    if rel != "README.md" and "claude-skills/" in t:
        errors.append(f"S14 {rel}: локальный путь `claude-skills/`, которого нет в дереве")

checks_seen.add('S15')
# S15 — пути в публичных текстах существуют (skills/, profiles/, agents/, docs/)
for rel in PUBLIC:
    p = ROOT / rel
    if not p.exists():
        continue
    for path in re.findall(r'`((?:skills|profiles|agents|docs)/[^`\s]+)`', p.read_text(errors="replace")):
        if any(ch in path for ch in "<>*"):
            continue
        if not (ROOT / path.rstrip("/")).exists():
            errors.append(f"S15 {rel}: путь `{path}` не существует")

checks_seen.add('S16')
# S16 — число своих навыков равно дереву и в README, и в словаре (два места, один факт).
# Строка должна говорить именно про СВОИ навыки, поэтому ищем «сво… навык» в пределах
# одной строки, а не по всему файлу (иначе ловит «212 навыков» выше по тексту).
own = T.own_skills()
for rel in ["README.md", "docs/VOCABULARY.md"]:
    q = ROOT / rel
    if not q.exists():
        continue
    for line in q.read_text(errors="replace").splitlines():
        m = re.search(r'(\d+)\s+сво[а-яё]*\s+навык', line)
        if m:
            if int(m.group(1)) != len(own):
                errors.append(f"S16 {rel}: своих навыков {m.group(1)}, "
                              f"в дереве {len(own)}")
            break

# S17 — у каждого домена верхнего уровня есть LICENSE (у витрины — у каждой витрины).
checks_seen.add('S17')
for d in sorted(CR.iterdir()):
    if not d.is_dir():
        continue
    if d.name in SKIP_CONTRACT:            # partner-built — лицензии у витрин
        for sub in sorted(d.iterdir()):
            if sub.is_dir() and not (sub / "LICENSE").exists() and not (sub / "LICENSE.txt").exists():
                errors.append(f"S17 partner-built/{sub.name}: нет LICENSE")
        continue
    if not (d / "LICENSE").exists() and not (d / "LICENSE.txt").exists():
        errors.append(f"S17 {d.name}: нет LICENSE")
if not (ROOT / "LICENSES" / "Apache-2.0.txt").exists():
    errors.append("S17 LICENSES/Apache-2.0.txt отсутствует — текст апстрима не сохранён")

# S18 — числа в архитектурной схеме (json + html) совпадают с деревом.
# Схема — собранный артефакт без генератора в репозитории, поэтому её числа
# расходятся молча: устаревшее «17 доменов» жило и в json, и в 6 местах html.
checks_seen.add('S18')
_tot = T.totals()
for rel in ["docs/vector-work.architecture.json", "docs/vector-work.architecture.html"]:
    q = ROOT / rel
    if not q.exists():
        errors.append(f"S18 {rel} отсутствует")
        continue
    s = q.read_text(errors="replace")
    m = re.search(r'(\d+)\s+доменов', s)
    if m and int(m.group(1)) != _tot["domains"]:
        errors.append(f"S18 {rel}: «{m.group(0)}», в дереве {_tot['domains']} каталогов")
    # каждый домен дерева должен упоминаться в схеме (витрины — тоже)
    for dom in sorted(tree_domains()):
        # сокращения схемы (PM/HR) считаются упоминанием
        aliases = {"product-management": "PM", "human-resources": "HR"}
        if dom not in s and aliases.get(dom, "\x00") not in s:
            errors.append(f"S18 {rel}: домен {dom} не показан на схеме")

# Счётчик проверок — из ФАКТА, а не хардкод: собираем коды, которые реально
# срабатывали (checks_seen наполняется при каждой выполненной проверке).
seen = set(checks_seen) | {re.match(r'(S\d+b?)', e).group(1) for e in errors}
CODES = sorted(seen)
print("\nпроверок выполнено: %d, ошибок: %d" % (len(seen), len(errors)))
print("коды: " + ", ".join(CODES))
for e in errors:
    print(f"  ERROR {e}")
for n in notes:
    print(f"  note  {n}")
sys.exit(1 if errors else 0)
