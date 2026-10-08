from difflib import SequenceMatcher
from typing import Any

from app.ml.features import ad_text


def find_similar_creatives(
    company_ads: list[dict[str, Any]],
    competitor_ads: list[dict[str, Any]],
    limit: int = 5,
) -> list[dict[str, Any]]:
    pairs = []

    for company_ad in company_ads:
        company_text = ad_text(company_ad)
        if not company_text:
            continue

        for competitor_ad in competitor_ads:
            competitor_text = ad_text(competitor_ad)
            if not competitor_text:
                continue

            score = SequenceMatcher(None, company_text.lower(), competitor_text.lower()).ratio()
            if score >= 0.2:
                pairs.append(
                    {
                        "similarity_score": round(score, 2),
                        "company_ad": {
                            "headline": company_ad.get("headline"),
                            "ad_text": company_ad.get("ad_text"),
                            "ad_library_url": company_ad.get("ad_library_url"),
                        },
                        "competitor_ad": {
                            "headline": competitor_ad.get("headline"),
                            "ad_text": competitor_ad.get("ad_text"),
                            "ad_library_url": competitor_ad.get("ad_library_url"),
                        },
                    }
                )

    return sorted(pairs, key=lambda item: item["similarity_score"], reverse=True)[:limit]
