#!/usr/bin/env python3
"""Генератор контрактов работников: profiles/<домен>.md

Принцип (решение владельца 2026-10-04):
  ЗАПОЛНЯЕТСЯ то, что ВЫВОДИМО из дерева — состав, описания навыков,
  инструменты, зависимости, запреты, общие проверки.
  ОСТАЁТСЯ СЛОТОМ то, что есть решение владельца — вход, первичный источник,
  необратимое действие домена, домен-проверка, формат результата, память.

Права считает `scripts/_tree.py` — единый сканер для всех скриптов. Раньше база
тулсетов здесь была [file, skills], а в реестре [file, skills, memory]; это
давало 12 ложных строк «лишний тулсет» в каждом контракте.

Запуск: python3 scripts/build_contracts.py
legal — доведён вручную, PROTECTED. partner-built — витрина, SKIP.
"""
import hashlib
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _tree as T

CR = T.CR
OUT = T.PROFILES
PROTECTED = {"legal"}          # доведён вручную: приёмка и сверенные нормы РФ
SKIP = T.SHOWCASE              # витрина, не роль организации
SLOT = "<РЕШЕНИЕ"              # маркер «нужно решение владельца»
TM = "[Т]"                     # маркер типового значения: не решение владельца

# Типовые значения слотов. Это НЕ позиции организации — исполняемый каркас,
# пока владелец не назвал своё. Каждое помечено [Т], чтобы при чтении было
# видно: значение не согласовано.
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

OWNER_DEFAULT = "Михаил (Osmosy)"   # владелец репозитория; он же ревьюер в приёмке
STATUS_PLACEHOLDER = "    статус:      <СТАТУС_ЗАПОЛНИТ_ГЕНЕРАТОР>"
# Строка статуса исключается из отпечатка тела (см. body_hash), поэтому плейсхолдер
# безопасен: хэш считается так же, как если бы статус уже стоял.


def brief(text, n=2, limit=170):
    t = re.sub(r'\s+', ' ', text).strip()
    return " ".join(re.split(r'(?<=[.!?])\s+', t)[:n])[:limit]


def descriptions(d):
    out = {}
    for p in d.rglob("SKILL.md"):
        t = p.read_text(errors="replace")
        m = re.search(r'^description:\s*(.+?)(?=\n[a-z_]+:|\n---)', t, re.S | re.M)
        if m:
            out[p.parent.name] = brief(m.group(1).strip(' "\''))
    return out


def approved_hash(stem):
    """Последний ОДОБРЕННЫЙ отпечаток тела из append-only журнала.

    Журнал `profiles/approvals.jsonl` пишет только человек или внешний human-gate;
    ни один скрипт сюда не пишет — именно поэтому он и есть якорь приёмки. Раньше
    `build_contracts.py` пересчитывал `body-hashes.json` из ТЕКУЩИХ тел и тем самым
    «одобрял» любую правку, а текст ошибки S12 прямым советом предлагал прогнать
    генератор. Цепочка была замкнута сама на себя.
    """
    j = OUT / "approvals.jsonl"
    if not j.exists():
        return None
    found = None
    for line in j.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("stem") == stem:
            found = e
    return found


def status_for(stem, current_text):
    """Статус по ФАКТУ: совпадает ли текущее тело с последним одобренным.

    Статус принадлежит гейту, а не генератору. Поэтому генератор не сохраняет
    прежний статус слепо (тогда правка тела тихо остаётся «принятой») и не
    выдаёт новый (тогда он сам себе гейт) — он выводит статус из сравнения с
    журналом одобрений.
    """
    ap = approved_hash(stem)
    if ap is None:
        return "    статус:      DRAFT — приёмки в журнале нет"
    if body_hash(current_text) == ap.get("body_sha256"):
        return (f"    статус:      ACTIVE — тело совпадает с одобренным "
                f"({ap.get('applied', '?')} {ap.get('date', '?')}, {ap.get('commit', '?')})")
    return (f"    статус:      DRAFT — изменён после приёмки "
            f"(одобрено {ap.get('date', '?')}, {ap.get('commit', '?')})")


def build(dom, r, descs, keep_status=None):
    """Контракт домена. Права — из общего сканера r.

    `keep_status` оставлен для совместимости, но больше НЕ используется: строка
    статуса подставляется позже функцией `apply_status`, после сборки тела.
    """
    ts = T.toolsets_need(r)
    extra = [t for t in ts if t not in T.BASE_TOOLSETS]
    L = []
    A = L.append
    A(f"# Контракт работника: {dom}\n")
    A(f"    роль:        {dom}")
    A( "    версия:      0.1")
    A(STATUS_PLACEHOLDER)
    A(f"    владелец:    {OWNER_DEFAULT}")
    A(f"    домен:       skills/cowork-roles/{dom}/ — {r['skills']} навыков (по дереву)")
    A(f"    источник:    Anthropic Cowork (Apache-2.0) @ {upstream_line()}")
    A("")
    A("## 0. Состав домена (по дереву)\n")
    for n in r["skill_names"]:
        A(f"    {n}")
    A("")
    A("Что делает каждый навык — по его собственному описанию:\n")
    for n in r["skill_names"]:
        if n in descs:
            A(f"    {n:26} {descs[n]}")
    A("")
    A("## 1. Что работник получает на входе\n")
    A("Обязательные поля постановки. Без любого из них — `BLOCKED`, не додумывать.\n")
    A("    задача      <что нужно сделать — одинаково для всех доменов>")
    A("    вход        <файл/текст/данные — путь или содержимое>")
    A(f"    <поле>      {TM} {TYPICAL['field']}")
    A("")
    A("## 2. Источники истины (по приоритету)\n")
    A(f"1. {TM} {TYPICAL['src1']}")
    A(f"2. {TM} {TYPICAL['src2']}")
    A(f"3. {TM} {TYPICAL['src3']}")
    A("4. **Навыки домена — исполняемая истина процесса.** Файлы:")
    A(f"   `skills/cowork-roles/{dom}/skills/<навык>/SKILL.md` ({r['skills']} шт.)")
    A("   Правило дома: при расхождении документа и навыка — прав навык.")
    A("")
    A("## 3. Разрешённые инструменты (least privilege)\n")
    A("Права вычислены `scripts/_tree.py` по дереву домена:\n")
    A("    тулсет         инструменты                          зачем")
    A("    file           read_file, write_file, patch, ...    чтение входа, запись заключения")
    A("    skills         skills_list, skill_view              загрузка навыков домена")
    A("    memory         memory                               факты о практике")
    if "connections" in extra:
        A(f"    connections    manage_connections                   {r['mcp']} MCP-серверов, "
          f"{len(r['conns'])} категорий коннекторов")
    if "browser" in extra:
        A("    browser        browser_*                            "
          + (r["browser_why"] or "решение владельца"))
    if "terminal" in extra:
        A(f"    terminal       terminal, process_manage             {r['py']} Python-скриптов; "
          f"{r['terminal_why'] or 'вызов из навыка'}")
    A("")
    forb = list(T.FORBIDDEN_ALWAYS)
    for c in T.CONDITIONAL:
        if c not in extra:
            forb.append("browser_*" if c == "browser" else c)
    A("Запрещено конструктивно: " + ", ".join(f"`{x}`" for x in forb) + ".\n")
    A("Обоснование по дереву:")
    for c in T.CONDITIONAL:
        if c not in extra:
            if c == "connections":
                A("  - коннекторов у домена нет;")
            elif c == "browser":
                A("  - браузер не требуется: по тексту навыка он не доказывается;")
            elif c == "terminal":
                if r["py"] == 0:
                    A("  - терминал не требуется: в домене нет скриптов;")
                else:
                    A(f"  - терминал не требуется: скриптов {r['py']}, "
                      f"но ни один навык их не вызывает;")
    A("  - делегирование, cron и управление компьютером не требует ни один домен библиотеки.")
    A("")
    A("## 4. Что разрешено и что запрещено\n")
    A(f"**Разрешено:** {TM} {TYPICAL['allow']}\n")
    A("**Запрещено:**\n")
    A(f"- {TM} {TYPICAL['forb1']}")
    A(f"- {TM} {TYPICAL['forb2']}")
    A("- утверждение без источника — понижать до `[web source — verify]`")
    A("- выдумывание отсутствующих данных — помечать `<не указано>`")
    A("")
    A("## 5. Обязательные проверки перед сдачей\n")
    A(f"   1. {TM} {TYPICAL['check']}")
    A("   2. Каждое утверждение имеет тег источника: `[settled — подтверждено <дата>, источник]`")
    A("      либо `[web source — verify]` — проверка общая для всех доменов")
    A("   3. Если хоть одна проверка не прошла — FAIL, а не PASS")
    A("   4. Результат прогоняется через human-gate (exit 2 = сдавать нельзя)")
    A("")
    A("## 6. Формат сдачи\n")
    A("    статус:    PASS | FAIL | BLOCKED")
    A(f"    <поле>:    {TM} {TYPICAL['out']}")
    A("")
    A("    PASS     проверки пройдены, человек принял через human-gate")
    A("    FAIL     проверки не пройдены — перечислить, какие")
    A("    BLOCKED  не хватает входа — назвать, чего")
    A("")
    A("## 7. Память работника\n")
    A(f"    помнит:      {TM} {TYPICAL['keep']}")
    A(f"    забывает:    {TM} {TYPICAL['drop']}")
    A("")
    A("## 8. Зависимости и пробелы (по факту дерева)\n")
    A(f"    навыков               {r['skills']}")
    A(f"    MCP-серверов          {r['mcp']}"
      + (f" ({', '.join(r['mcp_names'][:6])}…)" if r["mcp_names"] else " —"))
    A(f"    категорий коннекторов {len(r['conns'])}")
    A(f"    Python-скриптов       {r['py']}")
    A(f"    тулсетов сверх базы   {', '.join(extra) if extra else '—'}")
    A("")
    if not r["conns"] and not r["mcp"]:
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


def sync_orchestrator():
    """Блок приёмки в agents/orchestrator.md — МЕЖДУ маркерами.

    Зачем: этот блок — не текст о числах, а то, по чему оркестратор принимает
    решение (можно ли доверять полю контракта). Вписанный руками, он расходится
    с фактом молча: уже расходился — говорил «PAGE 2», тогда как контракт
    на странице ревью открывался один, а второй PAGE — плейбук, не контракт.
    """
    o = T.ROOT / "agents" / "orchestrator.md"
    if not o.exists():
        return
    text = o.read_text(errors="replace")
    start = "<!-- gen:acceptance:start -->"
    end = "<!-- gen:acceptance:end -->"
    if start not in text or end not in text:
        print("  orchestrator: маркеров gen:acceptance нет — блок не обновлён")
        return
    a = T.acceptance()
    kind_label = {"PAGE": "открывалась страница ревью",
                  "MANUAL": "доведён вручную",
                  "BATCH": "принято пакетом (по слову владельца)"}
    n_docs = a["contracts"] + len(a["playbooks"])
    lines = [
        start,
        f"Документов: **{n_docs}** — {a['contracts']} контрактов работников "
        f"+ {len(a['playbooks'])} плейбук. Разбивка по типу приёмки:",
        "",
    ]
    for k in ("PAGE", "MANUAL", "BATCH"):
        n = a["by_kind"].get(k, 0)
        if n:
            lines.append(f"    {k:7} {n:3}  {kind_label[k]}")
    for stem, kind in a["playbooks"]:
        lines.append(f"    {kind or '—':7}   1  {stem} — плейбук, не контракт домена")
    lines += [
        "",
        "Якорь приёмки — append-only журнал `profiles/approvals.jsonl`; статус выводится",
        "СРАВНЕНИЕМ тела с последней одобренной версией: совпало → ACTIVE, не совпало →",
        "DRAFT — изменён после приёмки (S12 проверяет именно это, а не падение).",
        "",
        f"Приёмка **формальная** (решение владельца D6): в репозитории типовые сценарии,",
        f"конкретных документов организации нет. Все {n_docs} документов приняты",
        "пакетом (`BATCH`). Когда в домен пойдут реальные документы, его контракт",
        "проходит содержательную приёмку (`PAGE`/`MANUAL`).",
        end,
    ]
    block = "\n".join(lines)
    import re as _re
    new = _re.sub(re.escape(start) + r".*?" + re.escape(end), block, text, flags=_re.S)
    if new != text:
        o.write_text(new)
        print(f"  orchestrator: блок приёмки обновлён ({a['contracts']} контрактов, "
              f"{len(a['playbooks'])} плейбук)")
    else:
        print("  orchestrator: блок приёмки уже актуален")


def upstream_line():
    """Ревизия апстрима, из которой взята копия ролей — для строки «источник».

    Дата синхронизации и коммит апстрима — разные вещи. Здесь именно коммит:
    контракт должен называть, ИЗ ЧЕГО взяты навыки домена, иначе при разборе
    «откуда это правило» не восстановить, какая версия апстрима имелась в виду.
    """
    lock = T.ROOT / "upstream.lock.json"
    if not lock.exists():
        return "ревизия не закреплена (upstream.lock.json отсутствует)"
    d = json.loads(lock.read_text())
    return f"{d['sha'][:12]} ({d['date'][:10]})"


def metrics(text):
    """Три РАЗНЫЕ величины, а не одна «слоты»: типовое, открытые решения владельца,
    незаполненные плейсхолдеры. Раньше gate_status складывал их в одну сумму."""
    return dict(
        typical=text.count(TM),
        open_decisions=text.count(SLOT),
        placeholders=len(re.findall(r'<[а-яё][^>]{2,40}>', text)),
    )


def body_hash(text):
    """sha256 тела контракта БЕЗ строки статуса.

    Правка тела меняет хэш → приёмка перестаёт соответствовать контракту.
    Строка статуса исключена: она часть приёмки, а не предмета ревью.
    """
    lines = [l for l in text.splitlines()
             if not l.strip().startswith("статус:")]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:16]


def main():
    rows = {r["domain"]: r for r in T.scan()}
    made = []
    states = {}
    for dom, r in rows.items():
        if dom in PROTECTED or dom in SKIP:
            continue
        p = OUT / f"{dom}.md"
        # 1. собрать ТЕЛО с плейсхолдером статуса
        body = build(dom, r, descriptions(CR / dom))
        # 2. вывести статус из сравнения с журналом одобрений (не из прежнего текста!)
        st = status_for(dom, body)
        states[dom] = st
        # 3. подставить статус вместо плейсхолдера и записать
        p.write_text(body.replace(STATUS_PLACEHOLDER, st, 1))
        made.append(dom)

    # отпечаток тела — в отдельный файл, рядом с контрактами
    digests = {}
    for p in sorted(OUT.glob("*.md")):
        if p.stem.startswith("_") or p.stem in {"REGISTRY", "READINESS", "STATUS"}:
            continue
        if p.stem.endswith(".review"):
            continue
        # плейбук тоже проходит приёмку — его тело тоже привязываем отпечатком
        digests[p.stem] = body_hash(p.read_text(errors="replace"))
    json.dump(digests, open(OUT / "body-hashes.json", "w"), ensure_ascii=False, indent=1)

    # статус плейбука — тем же правилом (gen-строка, тело без неё)
    pb = OUT / "legal-playbook.md"
    if pb.exists():
        pt = pb.read_text(errors="replace")
        m = re.search(r'^(\s*статус:.*)$', pt, re.M)
        if m:
            st = status_for("legal-playbook", pt)
            if st.strip() != m.group(1).strip():
                pb.write_text(pt.replace(m.group(1), st, 1))
                states["legal-playbook"] = st

    sync_orchestrator()

    print(f"контрактов собрано: {len(made)}")
    act = sum(1 for s in states.values() if "ACTIVE" in s)
    drf = sum(1 for s in states.values() if "DRAFT" in s)
    print(f"  статусы по факту (журнал approvals.jsonl): ACTIVE {act}, DRAFT {drf}")
    for dom, s in states.items():
        if "DRAFT" in s:
            print(f"    DRAFT {dom}")
    tot = dict(typical=0, open_decisions=0, placeholders=0)
    for dom in made:
        m = metrics((OUT / f"{dom}.md").read_text())
        for k in tot:
            tot[k] += m[k]
        print(f"  {dom:26} типовых [Т]: {m['typical']:2}  "
              f"открытых <РЕШЕНИЕ: {m['open_decisions']}  "
              f"плейсхолдеров <…>: {m['placeholders']}")
    print(f"\nИТОГО: типовых [Т] {tot['typical']}, открытых решений "
          f"{tot['open_decisions']}, плейсхолдеров {tot['placeholders']}")
    print("(три разные величины; раньше gate_status складывал их в одну «слоты»)")
    print(f"отпечатки тел: {OUT/'body-hashes.json'} ({len(digests)} шт.)")
    print("пропущено: legal (доведён вручную), partner-built (витрина)")


if __name__ == "__main__":
    main()
