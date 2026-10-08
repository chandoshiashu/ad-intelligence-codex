import re
from collections import Counter
from typing import Any


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "this",
    "that",
    "your",
    "you",
    "are",
    "from",
    "get",
    "now",
    "our",
    "all",
    "new",
    "into",
    "off",
    "use",
    "to",
    "of",
    "in",
    "on",
    "at",
    "a",
    "an",
    "is",
    "it",
}


def ad_text(ad: dict[str, Any]) -> str:
    parts = [
        ad.get("headline"),
        ad.get("description"),
        ad.get("ad_text"),
        ad.get("call_to_action"),
    ]
    return " ".join(str(part) for part in parts if part).strip()


def top_keywords(ads: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    words: Counter[str] = Counter()

    for ad in ads:
        for word in re.findall(r"[a-zA-Z][a-zA-Z0-9]+", ad_text(ad).lower()):
            if word not in STOPWORDS and len(word) > 2:
                words[word] += 1

    return [{"keyword": word, "count": count} for word, count in words.most_common(limit)]


def count_values(ads: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: Counter[str] = Counter()

    for ad in ads:
        value = ad.get(field)
        if isinstance(value, list):
            counts.update(str(item) for item in value if item)
        elif value:
            counts[str(value)] += 1

    return dict(counts.most_common())


def creative_theme(ad: dict[str, Any]) -> str:
    text = ad_text(ad).lower()

    theme_rules = [
        ("Discounts and Offers", ["off", "deal", "discount", "sale", "cashback", "free"]),
        ("Convenience", ["fast", "quick", "instant", "easy", "delivery", "doorstep"]),
        ("Choice and Variety", ["range", "variety", "options", "collection", "menu"]),
        ("Trust and Quality", ["quality", "trusted", "safe", "fresh", "verified"]),
        ("Seasonal Campaigns", ["festive", "diwali", "summer", "winter", "season"]),
        ("App Installs", ["download", "install", "app"]),
    ]

    for theme, keywords in theme_rules:
        if any(keyword in text for keyword in keywords):
            return theme

    return "General Brand Messaging"
