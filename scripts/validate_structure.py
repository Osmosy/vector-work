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
  S11b блок приёмки в orchestrator.md (между маркерами) не отстал от факта
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


def rows_of_tree():
    return sorted(tree_domains())


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

checks_seen.add('S11b')
# S11b — блок приёмки в orchestrator.md (между маркерами gen:acceptance) не отстал.
# Сверяем НЕ текст с текстом, а блок с ФАКТОМ: число контрактов, плейбуков и
# разбивка по видам приёмки. Ручная правка блока видна сразу.
if orch.exists():
    _ot = orch.read_text(errors="replace")
    _s, _e = "<!-- gen:acceptance:start -->", "<!-- gen:acceptance:end -->"
    if _s not in _ot or _e not in _ot:
        errors.append("S11b orchestrator.md: нет маркеров gen:acceptance")
    else:
        _blk = _ot.split(_s, 1)[1].split(_e, 1)[0]
        _acc = T.acceptance()
        _m = re.search(r'Контрактов работников:\s*\*{0,2}(\d+)\*{0,2}', _blk)
        if not _m:
            errors.append("S11b orchestrator.md: в блоке нет «Контрактов работников: N»")
        elif int(_m.group(1)) != _acc["contracts"]:
            errors.append(f"S11b orchestrator.md: контрактов {_m.group(1)} "
                          f"≠ факт {_acc['contracts']}")
        _m2 = re.search(r'плейбуков:\s*(\d+)', _blk)
        if _m2 and int(_m2.group(1)) != len(_acc["playbooks"]):
            errors.append(f"S11b orchestrator.md: плейбуков {_m2.group(1)} "
                          f"≠ факт {len(_acc['playbooks'])}")
        for _k, _n in _acc["by_kind"].items():
            _mk = re.search(rf'^\s*{_k}\s+(\d+)\s', _blk, re.M)
            if not _mk:
                errors.append(f"S11b orchestrator.md: нет строки приёмки {_k}")
            elif int(_mk.group(1)) != _n:
                errors.append(f"S11b orchestrator.md: {_k} {_mk.group(1)} ≠ факт {_n}")

checks_seen.add('S20')
# S20 — числа метрик в STATUS.md совпадают с фактом (три величины раздельно).
# Раньше здесь стояли 128 плейсхолдеров при факте 115 и 3 открытых при факте 4 —
# вписанное вручную число расходится молча и читается как состояние.
_st = (PR / "STATUS.md").read_text(errors="replace")
_mt = dict(typical=0, open_decisions=0, placeholders=0)
for _p in sorted(PR.glob("*.md")):
    if _p.stem.startswith("_") or _p.stem in NOT_CONTRACT or _p.stem.endswith(".review"):
        continue
    _x = _p.read_text(errors="replace")
    _mt["typical"] += _x.count("[Т]")
    _mt["open_decisions"] += _x.count("<РЕШЕНИЕ")
    _mt["placeholders"] += len(re.findall(r'<[а-яё][^>]{2,40}>', _x))
for _label, _re_pat, _val in [
    ("типовых полей", r'типовых полей \[Т\]\s+(\d+)', _mt["typical"]),
    ("открытых решений", r'открытых решений\s+(\d+)', _mt["open_decisions"]),
    ("плейсхолдеров", r'плейсхолдеров\s*(?:<…>)?\s+(\d+)', _mt["placeholders"]),
]:
    _m = re.search(_re_pat, _st)
    if not _m:
        errors.append(f"S20 STATUS.md: нет числа «{_label}»")
    elif int(_m.group(1)) != _val:
        errors.append(f"S20 STATUS.md: {_label} {_m.group(1)} ≠ факт {_val}")

checks_seen.add('S21')
# S21 — прозаические абзацы REGISTRY.md про терминал и браузер совпадают с
# таблицей тулсетов. Раньше здесь было противоречие: колонка говорила «да» у двух
# доменов, тулсет выдан одному, а нижний абзац — что терминал не нужен никому.
_reg = (PR / "REGISTRY.md").read_text(errors="replace")
_rows = {r["domain"]: r for r in T.scan()}
_real_term = sorted(d for d, r in _rows.items() if "terminal" in T.toolsets_need(r))
_real_brw = sorted(d for d, r in _rows.items() if "browser" in T.toolsets_need(r))
for _lbl, _real in (("Терминал получает только:", _real_term),
                    ("Браузер по решению владельца:", _real_brw),
                    ("Браузер получает только:", _real_brw)):
    _m = re.search(re.escape(_lbl) + r'([^\n.]*)', _reg)
    if not _m:
        continue
    _named = sorted(re.findall(r'`([a-z][a-z-]+)`', _m.group(1)))
    if _named != _real:
        errors.append(f"S21 REGISTRY.md «{_lbl}» названы {_named}, "
                      f"а тулсет выдан {_real}")

checks_seen.add('S22')
# S22 — бейдж синхронизации в README называет ревизию из upstream.lock.json.
# Бейдж с датой, которой нет в локе, — то же враньё, что бейдж без сверки.
_lock = ROOT / "upstream.lock.json"
_rd = (ROOT / "README.md").read_text(errors="replace")
if not _lock.exists():
    errors.append("S22 upstream.lock.json отсутствует — ревизия апстрима не закреплена")
else:
    _L = json.loads(_lock.read_text())
    _want_date = _L["date"][:10]
    _m = re.search(r'gen:sync:start.*?Synced upstream:\s*([0-9-]{10})', _rd, re.S)
    if not _m:
        errors.append("S22 README: нет бейджа синхронизации между gen:sync")
    elif _m.group(1) != _want_date:
        errors.append(f"S22 README бейдж {_m.group(1)} ≠ лок {_want_date}")
    # абзац состояния должен называть тот же усечённый sha
    _m2 = re.search(r'gen:syncstate:start.*?`([0-9a-f]{12})`', _rd, re.S)
    if not _m2:
        errors.append("S22 README: абзац состояния не называет ревизию")
    elif _m2.group(1) != _L["sha"][:12]:
        errors.append(f"S22 README ревизия {_m2.group(1)} ≠ лок {_L['sha'][:12]}")

checks_seen.add('S23')
# S23 — контракты называют закреплённую ревизию апстрима в строке «источник».
# Иначе «откуда это правило» не восстановить при разборе.
if _lock.exists():
    _sha12 = json.loads(_lock.read_text())["sha"][:12]
    for _c in sorted(PR.glob("*.md")):
        if (_c.stem.startswith("_") or _c.stem in NOT_CONTRACT
                or _c.stem.endswith(".review") or _c.stem.endswith("-playbook")):
            continue
        _src = re.search(r'^\s*источник:\s*(.+)$', _c.read_text(errors="replace"), re.M)
        if not _src:
            errors.append(f"S23 {_c.name}: нет строки «источник»")
        elif "Anthropic Cowork" in _src.group(1) and _sha12 not in _src.group(1):
            errors.append(f"S23 {_c.name}: источник без закреплённой ревизии {_sha12}")

checks_seen.add('S24')
# S24 — каждое отличие от апстрима либо отсутствует, либо указано в MODIFICATIONS.md.
# Дефект N2 (внешний аудит 2026-10-04): лок хранил только ЧИСЛО навыков, поэтому
# «stale: {}» был ложным — у трёх доменов не было .mcp.json и CONNECTORS.md, девять
# README устарели, два SKILL.md изменены, и ничего из этого не виделось. Apache-2.0
# §4(b) требует отмечать изменённые файлы.
_lock24 = ROOT / "upstream.lock.json"
if _lock24.exists():
    _L24 = json.loads(_lock24.read_text())
    _mod_md = CR / "MODIFICATIONS.md"
    _mod_txt = _mod_md.read_text(errors="replace") if _mod_md.exists() else ""
    if not _mod_md.exists():
        errors.append("S24 skills/cowork-roles/MODIFICATIONS.md отсутствует")
    for _f in _L24.get("modified", []):
        if _f not in _mod_txt:
            errors.append(f"S24 изменённый файл не отмечен в MODIFICATIONS.md: {_f}")
    for _f in _L24.get("upstream_only", []):
        errors.append(f"S24 файл есть в апстриме, а у нас нет: {_f}")
    # Лок обязан ХРАНИТЬ пофайловые хэши. Без них «modified/upstream_only» пусты по
    # построению — и отличия снова невидимы (ровно дефект N2). Проверяем наличие
    # ключей и их непустоту там, где они обязаны быть.
    for _k in ("files", "files_local"):
        if not _L24.get(_k):
            errors.append(f"S24 upstream.lock.json без пофайловых хэшей «{_k}» — "
                          f"отличия от апстрима не видны, прогони --pin")
    if "modified" not in _L24 or "upstream_only" not in _L24:
        errors.append("S24 upstream.lock.json: нет ключей modified/upstream_only")
    for _f in _L24.get("locally_added", []):
        if _f not in _mod_txt:
            errors.append(f"S24 наше добавление не отмечено в MODIFICATIONS.md: {_f}")

checks_seen.add('S12')
# S12 — статус выведен из ЖУРНАЛА одобрений, а не из генерируемого файла хэшей.
# Дефект N1 (внешний аудит 2026-10-04): раньше S12 сверяла текущее тело с
# `body-hashes.json`, который генератор пересчитывал из ТЕКУЩИХ тел, и текст ошибки
# прямым советом предлагал прогнать генератор. Любая правка тела «одобрялась» двумя
# командами. Теперь якорь — append-only журнал `profiles/approvals.jsonl`, который
# не пишет ни один скрипт. Расхождение — НЕ ошибка CI (состояние честное: DRAFT),
# но оно обязано быть отражено в строке статуса контракта.
import hashlib as _hl
import json as _json
JOURNAL = PR / "approvals.jsonl"
_jr = {}
if not JOURNAL.exists():
    errors.append("S12 profiles/approvals.jsonl отсутствует — журнал приёмки не найден")
else:
    for _line in JOURNAL.read_text(errors="replace").splitlines():
        _line = _line.strip()
        if not _line:
            continue
        try:
            _e = _json.loads(_line)
        except Exception:
            errors.append(f"S12 approvals.jsonl: нечитаемая строка: {_line[:60]}")
            continue
        for _f in ("stem", "body_sha256", "applied", "reviewer", "date", "commit"):
            if _f not in _e:
                errors.append(f"S12 approvals.jsonl: запись без поля «{_f}»")
            elif not str(_e.get(_f)).strip():
                errors.append(f"S12 approvals.jsonl ({_e.get('stem','?')}): "
                              f"пустое поле «{_f}»")
        _jr[_e.get("stem")] = _e          # побеждает последняя запись

    for stem, ap in _jr.items():
        md = PR / f"{stem}.md"
        if not md.exists():
            errors.append(f"S12 approvals.jsonl: запись для несуществующего {stem}.md")
            continue
        _lines = [l for l in md.read_text(errors="replace").splitlines()
                  if not l.strip().startswith("статус:")]
        actual = _hl.sha256("\n".join(_lines).encode()).hexdigest()[:16]
        st_line = next((l for l in md.read_text(errors="replace").splitlines()
                        if l.strip().startswith("статус:")), "")
        if actual == ap.get("body_sha256"):
            if "ACTIVE" not in st_line:
                errors.append(f"S12 {stem}: тело совпадает с одобренным, "
                              f"а статус не ACTIVE — прогони build_contracts.py")
        else:
            if "DRAFT" not in st_line:
                errors.append(f"S12 {stem}: тело изменено после приёмки, "
                              f"а статус не DRAFT (одобрено {ap.get('commit')})")

    # каждый документ (кроме плейбука, у него gen-строка) должен иметь запись в журнале
    for _p in sorted(PR.glob("*.md")):
        if (_p.stem.startswith("_") or _p.stem in {"REGISTRY", "READINESS", "STATUS", "OWNER-DECISIONS"}
                or _p.stem.endswith(".review") or _p.stem == "legal-playbook"):
            continue
        if _p.stem not in _jr:
            errors.append(f"S12 {_p.stem}: нет записи в approvals.jsonl — приёмки нет")

checks_seen.add('S13')
# S13 — статус ACTIVE не держится на незаполненном плейсхолдере владельца.
# Шапка контракта — блок метаданных с отступом, а НЕ первый абзац текста
# (первый абзац — заголовок «# Контракт работника: X»).
_bh = PR / "body-hashes.json"
hashes = _json.loads(_bh.read_text()) if _bh.exists() else {}
_PLACEHOLDERS = ("<кто отвечает>", "<владелец>", "<домен>", "<НАЗНАЧИТЬ>")
for stem in (hashes if hashes else []):
    md = PR / f"{stem}.md"
    if not md.exists():
        continue
    head_lines = []
    for line in md.read_text(errors="replace").splitlines():
        if line.strip() and not line.startswith(("#", "    ")):
            break
        head_lines.append(line)
    head = "\n".join(head_lines)
    if "ACTIVE" in head:
        for ph in _PLACEHOLDERS:
            if ph in head:
                errors.append(f"S13 {stem}: статус ACTIVE при незаполненном "
                              f"плейсхолдере «{ph}» — заполни или понизь статус")

checks_seen.add('S14')
# S14 — в публичных текстах нет устаревших утверждений о СОСТАВЕ и чужого локального пути.
# Обобщено по N4 (внешний аудит 2026-10-04): раньше ловилась ОДНА фраза «14 ролей»,
# поэтому «212 навыков» в AGENTS.md и старая ревизия в README проходили зелёными.
# Теперь сверяются все числа состава во всех *.md вне деревьев навыков.
# Явный opt-out для исторических мест — маркер <!-- noqa:S14 --> в той же строке.
PUBLIC = ["README.md", "AGENTS.md", "agent-description.md",
          "agents/orchestrator.md", "docs/VOCABULARY.md"]
_tot14 = T.totals()
_sha14 = ""
if (ROOT / "upstream.lock.json").exists():
    _sha14 = json.loads((ROOT / "upstream.lock.json").read_text())["sha"][:12]
_FACTS14 = {
    "навык": _tot14["skills"], "домен": _tot14["domains"],
    "каталог": _tot14["domains"], "рол": _tot14["roles"],
    "контракт": _tot14["contracts"] if "contracts" in _tot14 else 17,
}
for rel in PUBLIC:
    p = ROOT / rel
    if not p.exists():
        continue
    for i, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
        if line.lstrip().startswith("|"):        # таблицы (журнал, роли) — не проза
            continue
        if "noqa:S14" in line:                   # явное исключение
            continue
        if re.search(r'\b14\s+(профессиональных\s+)?рол', line):
            errors.append(f"S14 {rel}:{i}: устаревшее «14 ролей» — ролей {_tot14['roles']}")
        for word, fact in _FACTS14.items():
            # ОБА порядка: «252 навыка» и «контрактов 17» — в таблицах VOCABULARy
            # слово идёт первым, и первый порядок такое просто не находил.
            for m in re.finditer(rf'(\d+)\s+{word}(?:ов|а|ей|ь)?\b'
                                 rf'|{word}(?:ов|а|ей|ь)?\s+(\d+)\b',
                                 line, re.I):
                val = int(m.group(1) or m.group(2))
                if val == fact or val < 5:
                    continue
                # Подмножество — не расхождение, но только когда число относится
                # к подмножеству: маркер должен идти ПЕРЕД числом («витрина — 71
                # навык», «из них 181 навык»). Маркер ПОСЛЕ числа — не оправдание:
                # так «252 навыка (17 ролей + витрина)» прошло бы при 212.
                pre = line[max(0, m.start() - 90):m.start()]
                # Маркер подмножества действует, только если он «тянется» к числу:
                # между ним и числом нет ЗАКРЫТОЙ скобки/точки/запятой-конца.
                # Так «partner-built (71 навык)» — подмножество, а «partner-built),
                # 252 навыка» — итог всего дерева (маркер закрыт, к числу не относится).
                if re.search(r'[).;]', pre[-25:]):
                    pre = ""
                SUBSET = ("витрин", "partner-built", "роли организации", "ролей организации",
                          "своих", "claude-skills", "из них", "внешн", "подмножеств",
                          "сверх базы", "у роли", "в контракте")
                if any(w in pre for w in SUBSET):
                    continue
                errors.append(f"S14 {rel}:{i}: «{m.group(0)}» ≠ {fact} по дереву")
        if _sha14 and re.search(r'`(?!' + _sha14 + r')[0-9a-f]{12}`', line) \
                and re.search(r'(апстрим|upstream)', line, re.I):
            errors.append(f"S14 {rel}:{i}: короткий sha рядом с «апстрим» ≠ {_sha14}")
    # claude-skills/ — чужой локальный путь, если он подаётся как существующий.
    # В VOCABULARY он прямо назван отсутствующим, это объяснение, а не ссылка.
    if rel != "README.md":
        _t = p.read_text(errors="replace")
        if "claude-skills/" in _t and not re.search(
                r'(нет в репозитории|не лежит|отсутствует|в этом репозитории нет|в репозитории нет)',
                _t, re.S):
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
    # число навыков на схеме тоже сверяется: раньше S18 смотрела только домены,
    # а «Skills (212)» жило в узле и в 9 местах html без всякой проверки
    _sk = re.search(r'Skills \((\d+)\)', s)
    if _sk and int(_sk.group(1)) != _tot["skills"]:
        errors.append(f"S18 {rel}: «Skills ({_sk.group(1)})», в дереве {_tot['skills']}")
    _nv = re.search(r'(\d+)\s+навыков', s)
    if _nv and int(_nv.group(1)) > 50 and int(_nv.group(1)) != _tot["skills"]:
        errors.append(f"S18 {rel}: «{_nv.group(0)}», в дереве {_tot['skills']}")
    # каждый домен дерева должен упоминаться в схеме (витрины — тоже)
    for dom in sorted(tree_domains()):
        # сокращения схемы (PM/HR) считаются упоминанием
        aliases = {"product-management": "PM", "human-resources": "HR"}
        if dom not in s and aliases.get(dom, "\x00") not in s:
            errors.append(f"S18 {rel}: домен {dom} не показан на схеме")

# S19 — колонка «Контракт» в таблице ролей README соответствует ФАКТУ приёмки.
# Источник факта — журнал approvals.jsonl (не review-файлы: они больше не якорь).
# Сейчас все контракты в DRAFT, поэтому колонка обязана говорить DRAFT, а не ACTIVE.
checks_seen.add('S19')
_rd = (ROOT / "README.md").read_text(errors="replace")
for r in rows_of_tree():
    dom = r
    m = re.search(rf'\|\s*\*\*{re.escape(dom)}\*\*\s*\|[^|]*\|[^|]*\|\s*([^|]*?)\s*\|',
                  _rd)
    if not m:
        continue
    cell = m.group(1).strip()
    ap = _jr.get(dom) if "_jr" in globals() else None
    if ap is None:
        continue
    md_dom = PR / f"{dom}.md"
    if not md_dom.exists():
        continue
    _l = [l for l in md_dom.read_text(errors="replace").splitlines()
          if not l.strip().startswith("статус:")]
    cur = _hl.sha256("\n".join(_l).encode()).hexdigest()[:16]
    fact = "ACTIVE" if cur == ap.get("body_sha256") else "DRAFT"
    if fact == "DRAFT" and "DRAFT" not in cell:
        errors.append(f"S19 README: {dom} — «{cell}», а тело изменено после приёмки "
                      f"(факт DRAFT)")
    elif fact == "ACTIVE" and "ACTIVE" not in cell:
        errors.append(f"S19 README: {dom} — «{cell}», а приёмка действительна "
                      f"(факт ACTIVE)")

# Счётчик проверок — из ФАКТА, а не хардкод: собираем коды, которые реально
# срабатывали (checks_seen наполняется при каждой выполненной проверке).
N_CHECKS = None   # вычисляется ниже из факта (checks_seen)
seen = set(checks_seen) | {re.match(r'(S\d+b?)', e).group(1) for e in errors}
CODES = sorted(seen)
N_CHECKS = len(seen)
print("\nпроверок выполнено: %d, ошибок: %d" % (N_CHECKS, len(errors)))
print("коды: " + ", ".join(CODES))
for e in errors:
    print(f"  ERROR {e}")
for n in notes:
    print(f"  note  {n}")
sys.exit(1 if errors else 0)
