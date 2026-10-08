from typing import Any

from app.ml.features import count_values, top_keywords


def summarize_strategies(
    company_ads: list[dict[str, Any]],
    competitor_ads: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "company": {
            "top_keywords": top_keywords(company_ads),
            "calls_to_action": count_values(company_ads, "call_to_action"),
            "platforms": count_values(company_ads, "platforms"),
            "media_mix": count_values(company_ads, "media_type"),
        },
        "competitor": {
            "top_keywords": top_keywords(competitor_ads),
            "calls_to_action": count_values(competitor_ads, "call_to_action"),
            "platforms": count_values(competitor_ads, "platforms"),
            "media_mix": count_values(competitor_ads, "media_type"),
        },
    }
