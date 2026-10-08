from collections import Counter
from typing import Any


def detect_anomalies(ads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    anomalies = []
    archive_ids = [ad.get("ad_archive_id") for ad in ads if ad.get("ad_archive_id")]
    duplicate_ids = [ad_id for ad_id, count in Counter(archive_ids).items() if count > 1]

    if duplicate_ids:
        anomalies.append(
            {
                "type": "duplicate_ads",
                "severity": "medium",
                "message": "Duplicate Meta Ad Library archive ids were found.",
                "items": duplicate_ids,
            }
        )

    missing_text = sum(1 for ad in ads if not ad.get("ad_text") and not ad.get("headline"))
    if missing_text:
        anomalies.append(
            {
                "type": "missing_creative_text",
                "severity": "low",
                "message": f"{missing_text} ads are missing headline and body text.",
                "items": [],
            }
        )

    missing_urls = sum(1 for ad in ads if not ad.get("ad_library_url"))
    if missing_urls:
        anomalies.append(
            {
                "type": "missing_source_url",
                "severity": "low",
                "message": f"{missing_urls} ads are missing a source URL.",
                "items": [],
            }
        )

    return anomalies
