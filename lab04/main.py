import sys

from stats import average_by_city, parse_record, read_valid, warmest_city


def main():
    lines = sys.stdin.read().splitlines()

    records = read_valid(lines)

    skipped = 0
    for line in lines:
        if line.strip() == "":
            continue
        try:
            parse_record(line)
        except ValueError:
            skipped += 1

    print(len(records))
    print(skipped)

    best = warmest_city(records)
    if best == "":
        print(0.0)
    else:
        avg = average_by_city(records)
        print(f"{avg[best]:.1f}")


if __name__ == "__main__":
    main()
