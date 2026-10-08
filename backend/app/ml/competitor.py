from typing import Any

from app.ml.features import count_values, top_keywords


def compare_competitors(
    company: str,
    competitor: str,
    company_ads: list[dict[str, Any]],
    competitor_ads: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "ad_volume": {
            company: len(company_ads),
            competitor: len(competitor_ads),
            "leader": _leader(company, competitor, len(company_ads), len(competitor_ads)),
        },
        "keyword_overlap": _keyword_overlap(company_ads, competitor_ads),
        "media_mix": {
            company: count_values(company_ads, "media_type"),
            competitor: count_values(competitor_ads, "media_type"),
        },
        "cta_mix": {
            company: count_values(company_ads, "call_to_action"),
            competitor: count_values(competitor_ads, "call_to_action"),
        },
    }


def _leader(company: str, competitor: str, company_count: int, competitor_count: int) -> str:
    if company_count > competitor_count:
        return company
    if competitor_count > company_count:
        return competitor
    return "tie"


def _keyword_overlap(
    company_ads: list[dict[str, Any]],
    competitor_ads: list[dict[str, Any]],
) -> dict[str, Any]:
    company_keywords = {item["keyword"] for item in top_keywords(company_ads)}
    competitor_keywords = {item["keyword"] for item in top_keywords(competitor_ads)}

    return {
        "shared": sorted(company_keywords & competitor_keywords),
        "company_only": sorted(company_keywords - competitor_keywords),
        "competitor_only": sorted(competitor_keywords - company_keywords),
    }
