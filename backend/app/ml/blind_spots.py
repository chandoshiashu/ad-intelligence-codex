from typing import Any

from app.ml.features import count_values, top_keywords


def find_blind_spots(
    company: str,
    competitor: str,
    company_ads: list[dict[str, Any]],
    competitor_ads: list[dict[str, Any]],
) -> list[str]:
    blind_spots = []

    company_keywords = {item["keyword"] for item in top_keywords(company_ads)}
    competitor_keywords = {item["keyword"] for item in top_keywords(competitor_ads)}
    missing_keywords = sorted(competitor_keywords - company_keywords)[:5]
    if missing_keywords:
        blind_spots.append(
            f"{competitor} emphasizes keywords that {company} is not using often: "
            + ", ".join(missing_keywords)
            + "."
        )

    company_platforms = set(count_values(company_ads, "platforms"))
    competitor_platforms = set(count_values(competitor_ads, "platforms"))
    missing_platforms = sorted(competitor_platforms - company_platforms)
    if missing_platforms:
        blind_spots.append(
            f"{company} appears underrepresented on platforms where {competitor} is active: "
            + ", ".join(missing_platforms)
            + "."
        )

    company_ctas = set(count_values(company_ads, "call_to_action"))
    competitor_ctas = set(count_values(competitor_ads, "call_to_action"))
    missing_ctas = sorted(competitor_ctas - company_ctas)
    if missing_ctas:
        blind_spots.append(
            f"{competitor} uses CTA patterns that {company} may want to test: "
            + ", ".join(missing_ctas)
            + "."
        )

    return blind_spots or ["No major blind spots were detected from the available ads."]
