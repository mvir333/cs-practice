"""Точка входа: читает журнал, печатает три числа и пишет report.txt."""

from logstats import count_levels, top_errors, format_report


def main():
    path = input().strip()

    # Первый проход: считаем уровни
    with open(path, encoding="utf-8") as log:
        counts = count_levels(log)

    # Второй проход: собираем частые ошибки
    with open(path, encoding="utf-8") as log:
        errors = top_errors(log, 10)

    total_ok = sum(v for k, v in counts.items() if k != "BROKEN")
    error_count = counts.get("ERROR", 0)
    broken = counts.get("BROKEN", 0)

    print(total_ok)
    print(error_count)
    print(broken)

    report = format_report(counts, errors)
    with open("report.txt", "w", encoding="utf-8") as out:
        out.write(report)


if __name__ == "__main__":
    main()
