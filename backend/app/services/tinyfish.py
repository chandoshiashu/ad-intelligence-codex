import json
import os
import re
from typing import Any
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

load_dotenv()

TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY")

TINYFISH_URL = "https://agent.tinyfish.ai/v1/automation/run-sse"

AD_FIELDS = {
    "advertiser_name": None,
    "ad_archive_id": None,
    "ad_text": None,
    "headline": None,
    "description": None,
    "call_to_action": None,
    "start_date": None,
    "platforms": [],
    "media_type": None,
    "landing_page_url": None,
    "ad_library_url": None,
}


def get_competitor_ads(company: str, country: str = "IN") -> dict[str, Any]:
    company = company.strip()
    country = country.strip().upper()

    if not TINYFISH_API_KEY:
        raise RuntimeError("TINYFISH_API_KEY is not set")

    if not company:
        raise RuntimeError("Company is required")

    query = urlencode(
        {
            "active_status": "active",
            "ad_type": "all",
            "country": country,
            "q": company,
        }
    )
    ad_library_url = f"https://www.facebook.com/ads/library/?{query}"

    goal = f"""
        Open the Meta Ad Library public website.

        We are researching the advertiser:

        "{company}"

        Country: {country}
        Ad status: Active

        IMPORTANT:
        Only return advertisements whose actual advertiser/Page name belongs
        to "{company}".

        DO NOT return ads from other companies just because the ad text
        mentions "{company}".

        For example, if searching for Swiggy:

        VALID:
        - Swiggy
        - Swiggy India
        - Swiggy Delivery
        - Swiggy Food
        - clearly identifiable official Swiggy pages

        INVALID:
        - KitKat
        - Coca-Cola
        - another brand mentioning Swiggy
        - unrelated advertisers

        Extract up to 10 valid ads.

        For each valid ad, extract:

        - advertiser_name
        - ad_archive_id
        - ad_text
        - headline
        - description
        - call_to_action
        - start_date
        - platforms
        - media_type
        - landing_page_url
        - ad_library_url

        Rules:

        1. Only use information visible on the public Meta Ad Library.
        2. Do not log in.
        3. Do not invent information.
        4. If a field is unavailable, use null.
        5. Do not include unrelated advertisers.
        6. Do not purchase anything.

        Return JSON only.

        Use exactly this structure:

        {{
            "company": "{company}",
            "country": "{country}",
            "ads": []
        }}
        """

    print("Starting TinyFish...", flush=True)
    print(f"Company: {company}", flush=True)
    print(f"URL: {ad_library_url}", flush=True)

    response = requests.post(
        TINYFISH_URL,
        headers={
            "X-API-Key": TINYFISH_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "url": ad_library_url,
            "goal": goal,
        },
        stream=True,
        timeout=(20, 180),
    )

    print("TinyFish HTTP status:", response.status_code, flush=True)

    if not response.ok:
        raise RuntimeError(
            f"TinyFish HTTP error {response.status_code}"
        )

    final_result = None

    for line in response.iter_lines(decode_unicode=True):

        if not line:
            continue

        if not line.startswith("data:"):
            continue

        payload = line[5:].strip()

        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            continue

        event_type = event.get("type")

        if event_type == "STARTED":
            print("TinyFish agent started.", flush=True)

        elif event_type == "STREAMING_URL":
            streaming_url = event.get("streaming_url")

            if streaming_url:
                print(f"TinyFish live browser: {streaming_url}", flush=True)

        elif event_type == "PROGRESS":
            print("TinyFish progress update received.", flush=True)

        elif event_type == "COMPLETE":
            final_result = event.get("result")
            break

    if final_result is None:
        raise RuntimeError(
            "TinyFish finished without returning a result."
        )

    return _normalize_result(final_result, company, country)


def _normalize_result(result: Any, company: str, country: str) -> dict[str, Any]:
    data = _parse_result(result)
    raw_ads = data.get("ads", []) if isinstance(data, dict) else []

    normalized_ads = []
    for ad in raw_ads:
        if not isinstance(ad, dict):
            continue

        normalized = _normalize_ad(ad)
        if _belongs_to_company(normalized.get("advertiser_name"), company):
            normalized_ads.append(normalized)

    return {
        "company": company,
        "country": country,
        "ads": normalized_ads,
    }


def _parse_result(result: Any) -> dict[str, Any]:
    if isinstance(result, dict):
        return result

    if not isinstance(result, str):
        return {"ads": []}

    text = result.strip()
    text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text).strip()

    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {"ads": []}
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return {"ads": []}

        try:
            parsed = json.loads(match.group(0))
            return parsed if isinstance(parsed, dict) else {"ads": []}
        except json.JSONDecodeError:
            return {"ads": []}


def _normalize_ad(ad: dict[str, Any]) -> dict[str, Any]:
    normalized = {}

    for field, default in AD_FIELDS.items():
        value = ad.get(field)
        if field == "platforms":
            normalized[field] = _normalize_platforms(value)
        else:
            normalized[field] = str(value).strip() if value not in [None, ""] else default

    return normalized


def _normalize_platforms(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return list(value) if hasattr(value, "__iter__") else [value]


def _belongs_to_company(advertiser_name: Any, company: str) -> bool:
    if not advertiser_name:
        return False

    advertiser = str(advertiser_name).lower()
    requested = company.lower()
    return requested in advertiser or advertiser in requested
