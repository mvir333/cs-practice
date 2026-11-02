"""Разбор журнала: подсчёт уровней и частых ошибок."""

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def parse_event(line: str) -> dict:
    """Строка журнала -> словарь {"time", "level", "message"}.

    Негодная строка -> ValueError.
    """
    parts = line.split(" ", 2)  # максимум 3 куска: время, уровень, сообщение
    if len(parts) != 3:
        raise ValueError(f"неверный формат строки: {line!r}")

    time, level, message = parts
    if level not in VALID_LEVELS:
        raise ValueError(f"незнакомый уровень: {level!r}")

    return {"time": time, "level": level, "message": message}


def count_levels(lines) -> dict:
    """Сколько строк каждого уровня. Испорченные — под ключом BROKEN."""
    counts = {}
    for line in lines:
        line = line.strip()
        if not line:  # пустые строки пропускаем
            continue
        try:
            event = parse_event(line)
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
        else:
            lvl = event["level"]
            counts[lvl] = counts.get(lvl, 0) + 1
    return counts


def top_errors(lines, n: int) -> list[list]:
    """n самых частых сообщений уровня ERROR: пары [сообщение, сколько раз].

    При равенстве частот — по алфавиту.
    """
    freq = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            event = parse_event(line)
        except ValueError:
            continue  # испорченные тут не нужны
        if event["level"] != "ERROR":
            continue
        msg = event["message"]
        freq[msg] = freq.get(msg, 0) + 1

    items = [[msg, cnt] for msg, cnt in freq.items()]
    items.sort(key=lambda pair: (-pair[1], pair[0]))
    return items[:n]


def format_report(counts: dict, errors: list[list]) -> str:
    """Текст отчёта по готовым подсчётам."""
    lines = ["Отчёт по журналу", ""]
    for level in sorted(counts):  # уровни по алфавиту
        lines.append(f"{level}: {counts[level]}")
    lines.append("")
    lines.append("Частые ошибки:")
    for msg, cnt in errors:
        lines.append(f"- {msg} — {cnt}")
    return "\n".join(lines) + "\n"
