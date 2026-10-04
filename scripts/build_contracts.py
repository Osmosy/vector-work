#!/usr/bin/env python3
"""Генератор контрактов работников: profiles/<домен>.md

Принцип (решение владельца 2026-10-04):
  ЗАПОЛНЯЕТСЯ то, что ВЫВОДИМО из дерева — состав, описания навыков,
  инструменты, зависимости, запреты (чего не требует ни один навык домена),
  общие проверки.
  ОСТАЁТСЯ СЛОТОМ то, что есть решение владельца — вход, первичный источник,
  необратимое действие домена, домен-проверка, формат результата, память.

Ничего домен-специфичного не утверждается как факт: слот = приглашение решить.

Запуск: python3 scripts/build_contracts.py
legal — доведён вручную, PROTECTED. partner-built — витрина, SKIP.
"""
import re, json, pathlib

ROOT = pathlib.Path.home() / "projects" / "vector-work"
CR = ROOT / "skills" / "cowork-roles"
OUT = ROOT / "profiles"
PROTECTED = {"legal"}
SKIP = {"partner-built"}
ALWAYS_FORBIDDEN = ["delegate_task", "cronjob_manage", "computer_use"]
SLOT = "<РЕШЕНИЕ"          # единый маркер «нужно решение владельца»


def brief(text, n=2, limit=170):
    t = re.sub(r'\s+', ' ', text).strip()
    return " ".join(re.split(r'(?<=[.!?])\s+', t)[:n])[:limit]


def scan(d):
    names = sorted(p.parent.name for p in d.rglob("SKILL.md"))
    descs = {}
    for p in d.rglob("SKILL.md"):
        t = p.read_text(errors="replace")
        m = re.search(r'^description:\s*(.+?)(?=\n[a-z_]+:|\n---)', t, re.S | re.M)
        if m:
            descs[p.parent.name] = brief(m.group(1).strip(' "\''))
    conns = set()
    for f in d.rglob("*.md"):
        conns.update(x.strip() for x in re.findall(r'~~([a-z][a-z ]{3,30})', f.read_text(errors="replace")))
    py = sum(1 for _ in d.rglob("*.py"))
    mcp = []
    mp = d / ".mcp.json"
    if mp.exists():
        try:
            mcp = sorted(json.loads(mp.read_text()).get("mcpServers", {}).keys())
        except Exception:
            pass
    browser = terminal = False
    for p in d.rglob("SKILL.md"):
        t = p.read_text(errors="replace").lower()
        browser |= bool(re.search(r'browser|web page|navigate to https|screenshot', t))
        terminal |= bool(re.search(r'python3 scripts/|run the script|execute the command', t))
    tools = ["file", "skills"]
    if conns or mcp:
        tools.append("connections")
    if browser:
        tools.append("browser")
    if py and terminal:
        tools.append("terminal")
    tools.append("memory")
    return dict(names=names, descs=descs, conns=sorted(conns), mcp=mcp, py=py,
                browser=browser, terminal=terminal, tools=tools)


def build(dom, s):
    L = []
    A = L.append
    A(f"# Контракт работника: {dom}\n")
    A(f"    роль:        {dom}")
    A( "    версия:      0.1")
    A( "    статус:      DRAFT — каркас, не прошёл human-gate")
    A( "    владелец:    <кто отвечает>")
    A(f"    домен:       skills/cowork-roles/{dom}/ — {len(s['names'])} навыков (по дереву)")
    A( "    источник:    Anthropic Cowork (Apache-2.0)")
    A("")
    A("## 0. Состав домена (по дереву)\n")
    for n in s["names"]:
        A(f"    {n}")
    A("")
    A("Что делает каждый навык — по его собственному описанию:\n")
    for n in s["names"]:
        if n in s["descs"]:
            A(f"    {n:26} {s['descs'][n]}")
    A("")
    A("## 1. Что работник получает на входе\n")
    A("Обязательные поля постановки. Без любого из них — `BLOCKED`, не додумывать.\n")
    A("    задача      <что нужно сделать — одинаково для всех доменов>")
    A("    вход        <файл/текст/данные — путь или содержимое>")
    A(f"    <поле>      {SLOT}: какие поля нужны именно этому домену>")
    A("")
    A("## 2. Источники истины (по приоритету)\n")
    A(f"1. {SLOT}: первичный источник — что здесь считается «оригиналом»>")
    A(f"2. {SLOT}: внешний первоисточник для сверки>")
    A(f"3. {SLOT}: внутренний документ организации — политика, регламент>")
    A("4. **Навыки домена — исполняемая истина процесса.** Файлы:")
    A(f"   `skills/cowork-roles/{dom}/skills/<навык>/SKILL.md` ({len(s['names'])} шт.)")
    A("   Правило дома: при расхождении документа и навыка — прав навык.")
    A("")
    A("## 3. Разрешённые инструменты (least privilege)\n")
    A("Права объявлены минимальным набором — по факту требований навыков домена:\n")
    A("    тулсет         инструменты                          зачем")
    A("    file           read_file, write_file, patch, ...    чтение входа, запись заключения")
    A("    skills         skills_list, skill_view              загрузка навыков домена")
    A("    memory         memory                               факты о практике")
    if "connections" in s["tools"]:
        A(f"    connections    manage_connections                   {len(s['mcp'])} MCP-серверов, "
          f"{len(s['conns'])} категорий коннекторов")
    if "browser" in s["tools"]:
        A("    browser        browser_*                            навыки домена адресуют веб-страницы")
    if "terminal" in s["tools"]:
        A(f"    terminal       terminal, process_manage             {s['py']} Python-скриптов в домене")
    A("")
    forb = list(ALWAYS_FORBIDDEN)
    if "browser" not in s["tools"]:
        forb.append("browser_*")
    if "terminal" not in s["tools"]:
        forb.append("terminal")
    A("Запрещено конструктивно: " + ", ".join(f"`{x}`" for x in forb) + ".\n")
    A("Обоснование по дереву:")
    if "browser" not in s["tools"]:
        A("  - браузер не требует ни один навык домена;")
    if "terminal" not in s["tools"]:
        A("  - терминал не требуется: в домене нет исполняемых скриптов, вызываемых навыком;")
    A("  - делегирование, cron и управление компьютером не требует ни один домен библиотеки.")
    A("")
    A("## 4. Что разрешено и что запрещено\n")
    A(f"**Разрешено:** {SLOT}: список действий домена>\n")
    A("**Запрещено:**\n")
    A(f"- {SLOT}: необратимое действие этого домена — отправка/публикация/платёж; только подготовка>")
    A(f"- {SLOT}: что нельзя менять в проверяемом артефакте>")
    A("- утверждение без источника — понижать до `[web source — verify]`")
    A("- выдумывание отсутствующих данных — помечать `<не указано>`")
    A("")
    A("## 5. Обязательные проверки перед сдачей\n")
    A(f"   1. {SLOT}: машинно проверяемое условие домена>")
    A("   2. Каждое утверждение имеет тег источника: `[settled — подтверждено <дата>, источник]`")
    A("      либо `[web source — verify]` — проверка общая для всех доменов")
    A("   3. Если хоть одна проверка не прошла — FAIL, а не PASS")
    A("   4. Результат прогоняется через human-gate (exit 2 = сдавать нельзя)")
    A("")
    A("## 6. Формат сдачи\n")
    A("    статус:    PASS | FAIL | BLOCKED")
    A(f"    <поле>:    {SLOT}: что содержит результат этого домена>")
    A("")
    A("    PASS     проверки пройдены, человек принял через human-gate")
    A("    FAIL     проверки не пройдены — перечислить, какие")
    A("    BLOCKED  не хватает входа — назвать, чего")
    A("")
    A("## 7. Память работника\n")
    A(f"    помнит:      {SLOT}: что сохраняется между задачами>")
    A(f"    забывает:    {SLOT}: что не сохраняется>")
    A("")
    A("## 8. Зависимости и пробелы (по факту дерева)\n")
    A(f"    навыков               {len(s['names'])}")
    A(f"    MCP-серверов          {len(s['mcp'])}" + (f" ({', '.join(s['mcp'][:6])}…)" if s["mcp"] else " —"))
    A(f"    категорий коннекторов {len(s['conns'])}")
    A(f"    Python-скриптов       {s['py']}")
    A(f"    нужен браузер         {'да' if s['browser'] else '—'}")
    A("")
    if not s["mcp"] and not s["conns"]:
        A("**Внешних систем не требует** — работает на тексте и шаблонах.")
    else:
        A("**Требует внешних систем.** Пока ни один коннектор домена не подключён, результат")
        A("будет каркасным либо построенным на общих дефолтах, а не на данных организации.")
        A("Подключение — задача владельца (см. `READINESS.md`).")
    A("")
    A("## Приёмка\n")
    A("Контракт не вступает в силу, пока не прошёл `human-gate`: названный ревьюер, нулевой")
    A(f"открытый BLOCKER (`close` возвращает 0). Прогон — `profiles/{dom}.review.md`.")
    A("")
    return "\n".join(L)


def main():
    rows = json.load(open(OUT / "registry.json"))
    made = []
    for r in rows:
        dom = r["domain"]
        if dom in PROTECTED or dom in SKIP:
            continue
        (OUT / f"{dom}.md").write_text(build(dom, scan(CR / dom)))
        made.append(dom)
    print(f"контрактов собрано: {len(made)}")
    tot = 0
    for dom in made:
        t = (OUT / f"{dom}.md").read_text()
        n = t.count(SLOT)
        tot += n
        print(f"  {dom:28} слотов {SLOT}>: {n}")
    print(f"\nвсего слотов на {len(made)} доменов: {tot}")
    print("пропущено: legal (доведён вручную), partner-built (витрина)")


if __name__ == "__main__":
    main()
