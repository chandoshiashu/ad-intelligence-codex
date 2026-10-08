import json
from typing import Any


AD_FIELDS = [
    "advertiser_name",
    "ad_archive_id",
    "ad_text",
    "headline",
    "description",
    "call_to_action",
    "start_date",
    "platforms",
    "media_type",
    "landing_page_url",
    "ad_library_url",
]


def normalize_ads(raw: Any) -> list[dict[str, Any]]:
    data = _coerce_payload(raw)
    ads = data.get("ads", []) if isinstance(data, dict) else data

    if not isinstance(ads, list):
        return []

    return [_normalize_ad(ad) for ad in ads if isinstance(ad, dict)]


def _coerce_payload(raw: Any) -> Any:
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"ads": []}

    return raw or {"ads": []}


def _normalize_ad(ad: dict[str, Any]) -> dict[str, Any]:
    normalized = {field: ad.get(field) for field in AD_FIELDS}

    platforms = normalized.get("platforms")
    if platforms is None:
        normalized["platforms"] = []
    elif isinstance(platforms, str):
        normalized["platforms"] = [platforms]
    elif not isinstance(platforms, list):
        normalized["platforms"] = list(platforms) if platforms else []

    for key in ["ad_text", "headline", "description", "call_to_action"]:
        if normalized.get(key) is not None:
            normalized[key] = str(normalized[key]).strip()

    return normalized
