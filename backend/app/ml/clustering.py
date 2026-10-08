from collections import defaultdict
from typing import Any

from app.ml.features import creative_theme


def cluster_creatives(ads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for ad in ads:
        grouped[creative_theme(ad)].append(ad)

    clusters = []
    for theme, items in grouped.items():
        clusters.append(
            {
                "theme": theme,
                "count": len(items),
                "examples": [
                    {
                        "headline": ad.get("headline"),
                        "ad_text": ad.get("ad_text"),
                        "ad_library_url": ad.get("ad_library_url"),
                    }
                    for ad in items[:3]
                ],
            }
        )

    return sorted(clusters, key=lambda item: item["count"], reverse=True)
