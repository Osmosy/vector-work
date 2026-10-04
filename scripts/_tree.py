#!/usr/bin/env python3
"""Единый сканер дерева vector-work. Единственный источник правды о составе.

Все скрипты (build_registry, build_contracts, validate_structure) импортируют
отсюда — раньше было три копии логики с РАСХОДЯЩИМИСЯ правилами:
  база тулсетов:   реестр [file, skills, memory] против контрактов [file, skills]
  запреты:         5 элементов против 3
  регэксп коннекторов: ~~([a-z][a-z ]*) против ~~([a-z][a-z ]{3,30})
Это давало 12 ложных строк в контракте каждого домена. Теперь одно место.

Правило: числа берутся из дерева, а не из памяти.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CR = ROOT / "skills" / "cowork-roles"
PROFILES = ROOT / "profiles"

# --- политика прав, одна на весь репозиторий ---

# Тулсет, который не получает НИ ОДИН домен, независимо от содержимого навыков.
FORBIDDEN_ALWAYS = ["delegate_task", "cronjob_manage", "computer_use"]

# Тулсеты «по требованию»: выдаются, если домен это доказывает, и перечисляются
# с обоснованием. В отличие от FORBIDDEN_ALWAYS, здесь запрет не безусловный.
CONDITIONAL = ["connections", "browser", "terminal"]

# База одинакова для всех работников: чтение входа, навыки домена, память о практике.
BASE_TOOLSETS = ["file", "skills", "memory"]

# Осознанные расширения прав сверх вычисленных по дереву. Каждое названо явно,
# иначе проверка S7b валит контракт — так лишний тулсет не проскочит молча.
EXTRA_ALLOWED = {
    "legal": {"web"},   # сверка действующей редакции нормы по первоисточнику
}

# Один регэксп плейсхолдеров коннекторов для всех сканеров.
CONN_RE = re.compile(r'~~([a-z][a-z ]{2,30})')

# Браузер: по тексту навыка НЕ доказывается. Проверено 2026-10-04 на живом
# прогоне — все срабатывания оказались ложными:
#   «opens directly in a browser»     — про РЕЗУЛЬТАТ (HTML-артефакт), не про действие
#   «clickable competitor tabs»       — про артефакт
#   «site visits in HubSpot»          — метрика коннектора
#   «click-through rate»              — метрика
#   «screenshot»                      — ВХОД от пользователя
# Поэтому браузер не выводится эвристикой: он выдаётся по решению владельца
# и перечисляется явно в OVERRIDES ниже. Лучше не выдать лишнего, чем выдать
# право по ложному совпадению слова.
BROWSER_OVERRIDES = {}   # домен -> причина, если владелец решит выдать браузер

# Терминал: домен должен И иметь скрипты, И вызывать их из навыка. Упоминание
# «run the script» в тексте без единого .py — болтовня, а не требование
# (так operations получал terminal при py=0).
TERMINAL_RE = re.compile(r'(run the script|python3 scripts/|execute the command)')

# Домены-витрины: каталог есть, но это не роль организации. Контракта не имеет,
# в таблицу ролей README не обязан попадать.
SHOWCASE = {"partner-built"}


def _readme_declared():
    """Числа из таблицы ролей README (заявление) — для сверки с деревом."""
    rp = ROOT / "README.md"
    if not rp.exists():
        return {}
    t = rp.read_text(errors="replace")
    out = {}
    for m in re.finditer(r"^\|\s*\*{0,2}([a-z-]+)\*{0,2}\s*\|[^|]*\|\s*(\d+)\s*\|", t, re.M):
        out[m.group(1)] = int(m.group(2))
    return out


def _mcp_names(d):
    """MCP-серверы домена. У витрин .mcp.json лежат ВНУТРИ витрин — сканируем
    рекурсивно, иначе partner-built даёт 0 при трёх реальных файлах."""
    names = set()
    for mp in d.rglob(".mcp.json"):
        try:
            names.update(json.loads(mp.read_text()).get("mcpServers", {}).keys())
        except Exception:
            pass
    return sorted(names)


def scan_domain(d):
    """Всё, что можно доказать по дереву для одного домена."""
    skill_paths = sorted(d.rglob("SKILL.md"))
    skills = sorted(p.parent.name for p in skill_paths)

    conns = set()
    for f in d.rglob("*.md"):
        conns.update(x.strip() for x in CONN_RE.findall(f.read_text(errors="replace")))
    conns = sorted(c for c in conns if len(c) > 2)

    py = sum(1 for _ in d.rglob("*.py"))
    mcp = _mcp_names(d)

    # признаки «по требованию» — с запоминанием, ЧТО именно их включило
    browser_why = terminal_why = None
    for p in skill_paths:
        t = p.read_text(errors="replace")
        low = t.lower()
        if terminal_why is None:
            m = TERMINAL_RE.search(low)
            if m:
                terminal_why = f"{p.parent.name}: «{m.group(1)}»"
    # браузер — только по явному решению владельца, не по совпадению слова
    if d.name in BROWSER_OVERRIDES:
        browser_why = BROWSER_OVERRIDES[d.name]

    return dict(
        domain=d.name,
        skills=len(skills),
        skill_names=skills,
        mcp=len(mcp),
        mcp_names=mcp,
        conns=conns,
        py=py,
        need_browser=browser_why is not None,
        need_terminal=terminal_why is not None,
        browser_why=browser_why,
        terminal_why=terminal_why,
        showcase=d.name in SHOWCASE,
    )


def toolsets_need(r):
    """Тулсеты домена. Одна функция для реестра И для контрактов.

    Колонка «нужен терминал» в реестре и наличие тулсета `terminal` считаются
    ОТСЮДА ЖЕ — раньше колонка смотрела need_terminal, а тулсет `py and
    need_terminal`, что давало «да / нет» для одного домена.
    """
    t = list(BASE_TOOLSETS)
    if r["conns"] or r["mcp"]:
        t.append("connections")
    if r["need_browser"]:
        t.append("browser")
    # терминал — только если домен реально может запускать скрипты
    if r["need_terminal"] and r["py"] > 0:
        t.append("terminal")
    return t


def scan():
    """Состав всех доменов по дереву."""
    return [scan_domain(d) for d in sorted(CR.iterdir()) if d.is_dir()]


def declared():
    return _readme_declared()


def discrepancies(rows=None):
    """Расхождения «README vs дерево». Витрина — не расхождение: она в таблице
    витрин, а не в таблице ролей. Возвращает список (домен, README, дерево)."""
    rows = rows if rows is not None else scan()
    decl = declared()
    names = {r["domain"] for r in rows}
    dif = []
    for r in rows:
        d = r["domain"]
        if r["showcase"]:
            continue                      # витрина отдельной полкой, не расхождение
        if d in decl and decl[d] != r["skills"]:
            dif.append((d, decl[d], r["skills"]))
        elif d not in decl:
            dif.append((d, "—", r["skills"]))
    for k in decl:
        if k not in names:
            dif.append((k, decl[k], "нет в дереве"))
    return dif


def own_skills():
    """Свои навыки экосистемы: каталоги в skills/ вне cowork-roles/, с SKILL.md."""
    out = []
    for d in sorted((ROOT / "skills").iterdir()):
        if not d.is_dir() or d.name == "cowork-roles":
            continue
        if (d / "SKILL.md").exists():
            out.append(d.name)
    return out


def totals(rows=None):
    rows = rows if rows is not None else scan()
    return dict(
        domains=len(rows),
        skills=sum(r["skills"] for r in rows),
        showcases=sum(1 for r in rows if r["showcase"]),
        roles=sum(1 for r in rows if not r["showcase"]),
        own_skills=len(own_skills()),
    )
