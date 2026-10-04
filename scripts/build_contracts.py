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
T = "[Т]"                  # маркер типового значения: не решение владельца

# Типовые значения слотов. ВНИМАНИЕ: это НЕ позиции организации — это скелет,
# который делает контракт исполняемым, пока владелец не назвал своё. Каждое
# помечено [Т] именно затем, чтобы при чтении было видно: значение не согласовано.
# Владелец может заменить любое; раздел «Что заполнено типовым» перечисляет их.
TYPICAL = {
    "field":  "сторона (на чьей стороне работник) и срок ответа",
    "src1":   "входной артефакт/данные, приложенные к задаче",
    "src2":   "официальный первоисточник по предмету (документация, реестр, текст нормы)",
    "src3":   "политика или регламент организации по этому домену, если он есть",
    "allow":  "анализ, проверка, подготовка заключения — без изменения предмета",
    "forb1":  "отправка, публикация, платёж, подпись — только подготовка; действие делает человек",
    "forb2":  "сам проверяемый артефакт — заключение пишется отдельным файлом",
    "check":  "каждое утверждение о предмете имеет якорь (цитату или ссылку на источник)",
    "out":    "вердикт одной строкой + находки таблицей + открытые вопросы",
    "keep":   "решения по этому же предмету и принятые пороги",
    "drop":   "текст чужих документов после завершения задачи и черновики",
}


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


def build(dom, s, keep_status=None):
    L = []
    A = L.append
    A(f"# Контракт работника: {dom}\n")
    A(f"    роль:        {dom}")
    A( "    версия:      0.1")
    A(keep_status or "    статус:      DRAFT — каркас, не прошёл human-gate")
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
    A(f"    <поле>      {T} {TYPICAL['field']}")
    A("")
    A("## 2. Источники истины (по приоритету)\n")
    A(f"1. {T} {TYPICAL['src1']}")
    A(f"2. {T} {TYPICAL['src2']}")
    A(f"3. {T} {TYPICAL['src3']}")
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
    A(f"**Разрешено:** {T} {TYPICAL['allow']}\n")
    A("**Запрещено:**\n")
    A(f"- {T} {TYPICAL['forb1']}")
    A(f"- {T} {TYPICAL['forb2']}")
    A("- утверждение без источника — понижать до `[web source — verify]`")
    A("- выдумывание отсутствующих данных — помечать `<не указано>`")
    A("")
    A("## 5. Обязательные проверки перед сдачей\n")
    A(f"   1. {T} {TYPICAL['check']}")
    A("   2. Каждое утверждение имеет тег источника: `[settled — подтверждено <дата>, источник]`")
    A("      либо `[web source — verify]` — проверка общая для всех доменов")
    A("   3. Если хоть одна проверка не прошла — FAIL, а не PASS")
    A("   4. Результат прогоняется через human-gate (exit 2 = сдавать нельзя)")
    A("")
    A("## 6. Формат сдачи\n")
    A("    статус:    PASS | FAIL | BLOCKED")
    A(f"    <поле>:    {T} {TYPICAL['out']}")
    A("")
    A("    PASS     проверки пройдены, человек принял через human-gate")
    A("    FAIL     проверки не пройдены — перечислить, какие")
    A("    BLOCKED  не хватает входа — назвать, чего")
    A("")
    A("## 7. Память работника\n")
    A(f"    помнит:      {T} {TYPICAL['keep']}")
    A(f"    забывает:    {T} {TYPICAL['drop']}")
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
    A("## 9. Что заполнено типовым, а не решением владельца\n")
    A("Поля ниже заполнены **типовым значением** (помечено `[Т]` в тексте), чтобы")
    A("контракт был исполняем с первого дня. Это НЕ позиция организации: замените")
    A("любое на своё. Пока значение типовое, контракт не может считаться согласованным")
    A("по этим полям.\n")
    A("    вход, источники 1–3      общий каркас, не специфика домена")
    A("    разрешено/запрещено      общий каркас «готовить, не действовать»")
    A("    проверка домена          общий якорь вместо домен-специфичного условия")
    A("    формат сдачи             общий вердикт+таблица")
    A("    память                   общий порог «решения и пороги, без чужих текстов»\n")
    A("Что НЕ выдумано и требует решения обязательно: необратимое действие домена,")
    A("первоисточник сверки для конкретной отрасли, домен-специфичное условие проверки.\n")
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
        p = OUT / f"{dom}.md"
        # сохраняем статус приёмки: он принадлежит гейту, а не генератору
        keep = None
        if p.exists():
            keep = next((l for l in p.read_text(errors="replace").splitlines()
                         if l.strip().startswith("статус:")), None)
        p.write_text(build(dom, scan(CR / dom), keep))
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
