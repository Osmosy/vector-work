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
ALWAYS_FORBIDDEN = ["delegate_task", "cronjob_manage", "computer_use"]
# Осознанные расширения прав сверх вычисленных по дереву. Каждое должно быть
# названо здесь явно — иначе проверка S7b валит контракт. Так новый лишний
# тулсет не проскочит молча.
EXTRA_ALLOWED = {
    "legal": {"web"},   # сверка действующей редакции нормы по первоисточнику
}
errors, notes = [], []


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

# S3 — числа таблицы ролей README
rd = (ROOT / "README.md").read_text(errors="replace")
roles = re.findall(r'^\|\s*\*{0,2}([a-z-]+)\*{0,2}\s*\|[^|]*\|\s*(\d+)\s*\|', rd, re.M)
for name, num in roles:
    if name in dom and int(num) != dom[name]:
        errors.append(f"S3 README роль {name}: {num} ≠ дерево {dom[name]}")

# S4 — бейджи
for badge, val in (("Domains", len(dom)), ("Skills", sum(dom.values()))):
    m = re.search(rf'badge/{badge}-(\d+)-', rd)
    if not m:
        errors.append(f"S4 бейдж {badge} не найден")
    elif int(m.group(1)) != val:
        errors.append(f"S4 бейдж {badge}: {m.group(1)} ≠ {val}")

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

# S9
reg = (PR / "REGISTRY.md")
if not reg.exists():
    errors.append("S9 profiles/REGISTRY.md отсутствует")
else:
    m = re.search(r'Доменов:\s*\*\*(\d+)\*\*', reg.read_text(errors="replace"))
    if not m or int(m.group(1)) != len(dom):
        errors.append(f"S9 REGISTRY.md: доменов {m.group(1) if m else '?'} ≠ {len(dom)}")

# S10
rm = (PR / "READINESS.md")
if rm.exists():
    for name in re.findall(r'^\s{4}([a-z][a-z-]{2,})\s+\d+\s+\d+', rm.read_text(errors="replace"), re.M):
        if name not in dom and name not in {"domain"}:
            notes.append(f"S10 READINESS.md упоминает «{name}», которого нет в дереве")

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

print(f"\nпроверок: 11, ошибок: {len(errors)}")
for e in errors:
    print(f"  ERROR {e}")
for n in notes:
    print(f"  note  {n}")
sys.exit(1 if errors else 0)
