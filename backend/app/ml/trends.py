from collections import Counter
from datetime import datetime
from typing import Any


def summarize_trends(ads: list[dict[str, Any]]) -> dict[str, Any]:
    starts_by_month: Counter[str] = Counter()
    missing_dates = 0

    for ad in ads:
        month = _month_key(ad.get("start_date"))
        if month:
            starts_by_month[month] += 1
        else:
            missing_dates += 1

    return {
        "starts_by_month": dict(sorted(starts_by_month.items())),
        "missing_start_dates": missing_dates,
    }


def _month_key(value: Any) -> str | None:
    if not value:
        return None

    raw = str(value).strip()
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%b %d, %Y", "%B %d, %Y"]

    for date_format in formats:
        try:
            return datetime.strptime(raw, date_format).strftime("%Y-%m")
        except ValueError:
            continue

    if len(raw) >= 7 and raw[4] == "-":
        return raw[:7]

    return None
