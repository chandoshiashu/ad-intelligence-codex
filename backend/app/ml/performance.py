from typing import Any

from app.ml.features import count_values


def estimate_performance(ads: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "active_ads": len(ads),
        "media_mix": count_values(ads, "media_type"),
        "platform_distribution": count_values(ads, "platforms"),
        "cta_distribution": count_values(ads, "call_to_action"),
        "landing_pages": count_values(ads, "landing_page_url"),
    }
