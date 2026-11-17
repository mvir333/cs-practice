def parse_record(line: str) -> dict:
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError(f"ожидалось 3 поля, получено {len(parts)}: {line!r}")
    
    city, temp_str, date = parts
    city = city.strip()
    date = date.strip()
    temp_str = temp_str.strip()
    
    if not city or not date:
        raise ValueError(f"пустой город или дата: {line!r}")
    
    try:
        temp = float(temp_str)
    except ValueError:
        raise ValueError(f"температура не число: {temp_str!r}")
        
    return {"city": city, "temperature": temp, "date": date}


def read_valid(lines: list[str]) -> list[dict]:
    records = []
    for line in lines:
        if line.strip() == "":
            continue
        try:
            records.append(parse_record(line))
        except ValueError:
            continue
    return records


def average_by_city(records: list[dict]) -> dict:
    total = {}
    count = {}
    for r in records:
        city = r["city"]
        total[city] = total.get(city, 0.0) + r["temperature"]
        count[city] = count.get(city, 0) + 1
    return {city: round(total[city] / count[city], 1) for city in total}


def warmest_city(records: list[dict]) -> str:
    avg = average_by_city(records)
    if not avg:
        return ""
    best = None
    for city, value in avg.items():
        if best is None:
            best = city
        elif value > avg[best]:
            best = city
        elif value == avg[best] and city < best:
            best = city
    return best
