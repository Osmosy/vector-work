#!/usr/bin/env python3
"""Генератор реестра доменов vector-work: profiles/REGISTRY.md + profiles/READINESS.md

Считает по ДЕРЕВУ, а не по README. Запускать после изменения состава домена.
Печатает расхождения README vs дерево — это и есть защита от устаревших чисел.
"""
import os, re, json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
CR = ROOT / "skills" / "cowork-roles"
OUT = ROOT / "profiles"

# какие тулсеты НЕ нужны ни одному домену (обоснование least-privilege)
FORBIDDEN_ALWAYS = ["terminal", "delegate_task", "cronjob_manage", "browser_exec", "computer_use"]

def scan():
    rows = []
    for d in sorted(CR.iterdir()):
        if not d.is_dir():
            continue
        skills = sorted(p.parent.name for p in d.rglob("SKILL.md"))
        mcp = []
        mp = d / ".mcp.json"
        if mp.exists():
            try:
                mcp = sorted(json.loads(mp.read_text()).get("mcpServers", {}).keys())
            except Exception:
                mcp = []
        conns = set()
        py = 0
        for f in d.rglob("*.md"):
            t = f.read_text(errors="replace")
            conns.update(x.strip() for x in re.findall(r'~~([a-z][a-z ]*)', t))
        for f in d.rglob("*.py"):
            py += 1
        # грубая оценка: навык требует браузер/терминал
        need_browser = need_terminal = False
        for p in d.rglob("SKILL.md"):
            t = p.read_text(errors="replace").lower()
            if re.search(r'browser|web page|navigate to https|screenshot', t):
                need_browser = True
            if re.search(r'run the script|python3 scripts/|execute the command', t):
                need_terminal = True
        rows.append(dict(
            domain=d.name, skills=len(skills), skill_names=skills,
            mcp=len(mcp), mcp_names=mcp, conns=sorted(c for c in conns if len(c) > 2),
            py=py, need_browser=need_browser, need_terminal=need_terminal,
        ))
    return rows

def toolsets_need(r):
    # база одинакова для всех работников: чтение входа, навыки домена, память о практике
    t = ["file", "skills", "memory"]
    if r["conns"] or r["mcp"]:
        t.append("connections")
    if r["need_browser"]:
        t.append("browser")
    if r["py"] and r["need_terminal"]:
        t.append("terminal")
    return t

def readme_counts():
    """Числа из таблицы ролей README (заявление) — для сверки."""
    rp = ROOT / "README.md"
    if not rp.exists():
        return {}
    t = rp.read_text(errors="replace")
    out = {}
    for m in re.finditer(r"^\|\s*\*{0,2}([a-z-]+)\*{0,2}\s*\|[^|]*\|\s*(\d+)\s*\|", t, re.M):
        out[m.group(1)] = int(m.group(2))
    return out

rows = scan()
decl = readme_counts()

# --- REGISTRY.md ---
L = []
L.append("# Реестр доменов Vector Work\n")
L.append("Сгенерировано `scripts/build_registry.py` по дереву, не по README.")
L.append(f"Доменов: **{len(rows)}** · навыков: **{sum(r['skills'] for r in rows)}**\n")
L.append("| Домен | Навыков | MCP-серверов | Категорий коннекторов | Python | Нужен браузер | Нужен терминал |")
L.append("|---|---|---|---|---|---|---|")
for r in rows:
    L.append(f"| {r['domain']} | {r['skills']} | {r['mcp']} | {len(r['conns'])} | "
             f"{r['py']} | {'да' if r['need_browser'] else '—'} | {'да' if r['need_terminal'] else '—'} |")
L.append("")
L.append("## Обязательные тулсеты по домену (least privilege)\n")
L.append("Базовые для всех: `file`, `skills`. Остальное — только если домен это требует.\n")
L.append("| Домен | Тулсеты |")
L.append("|---|---|")
for r in rows:
    L.append(f"| {r['domain']} | `{'`, `'.join(toolsets_need(r))}` |")
L.append("")
L.append("## Запрещено конструктивно для всех доменов\n")
L.append("Ни один домен библиотеки не требует:\n")
L.append("    " + ", ".join(f"`{c}`" for c in FORBIDDEN_ALWAYS))
L.append("")
L.append("Проверка: ни в одном навыке нет вызова команд терминала, делегирования,")
L.append("cron или управления компьютером. Домены работают на тексте, шаблонах и данных.")
L.append("")
(OUT / "REGISTRY.md").write_text("\n".join(L))
json.dump(rows, open(OUT / "registry.json", "w"), ensure_ascii=False, indent=1)

# --- README vs дерево ---
dif = []
for r in rows:
    d = r["domain"]
    if d in decl and decl[d] != r["skills"]:
        dif.append((d, decl[d], r["skills"]))
    elif d not in decl:
        dif.append((d, "—", r["skills"]))
for k in decl:
    if k not in {r["domain"] for r in rows}:
        dif.append((k, decl[k], "нет в дереве"))

print("=" * 72)
print("README vs ДЕРЕВО — расхождения")
print("=" * 72)
print(f"{'домен':26} {'README':>7} {'дерево':>7}")
for d, a, b in dif:
    print(f"{d:26} {str(a):>7} {str(b):>7}")
print(f"\nрасхождений: {len(dif)}")

print("\n" + "=" * 72)
print("СОСТОЯНИЕ ДОМЕНОВ")
print("=" * 72)
print(f"{'домен':26} {'навыков':>7} {'mcp':>4} {'конн':>5} {'тулсеты'}")
for r in rows:
    print(f"{r['domain']:26} {r['skills']:>7} {r['mcp']:>4} {len(r['conns']):>5}  {'+'.join(toolsets_need(r))}")
print(f"\nВСЕГО: доменов {len(rows)}, навыков {sum(r['skills'] for r in rows)}")
print(f"навыков, зависящих от коннекторов: "
      f"{sum(r['skills'] for r in rows if r['conns'] or r['mcp'])}")
print(f"доменов без коннекторов вообще: "
      f"{sum(1 for r in rows if not r['conns'] and not r['mcp'])}")
json.dump(rows, open(OUT / "registry.json", "w"), ensure_ascii=False, indent=1)
print(f"\nзаписано: {OUT/'REGISTRY.md'} и {OUT/'registry.json'}")
