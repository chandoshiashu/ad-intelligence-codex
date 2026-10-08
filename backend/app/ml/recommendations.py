from typing import Any

from app.ml.features import count_values, top_keywords


def build_recommendations(
    company: str,
    competitor: str,
    company_ads: list[dict[str, Any]],
    competitor_ads: list[dict[str, Any]],
) -> list[str]:
    recommendations = []

    if len(competitor_ads) > len(company_ads):
        recommendations.append(
            f"Increase active creative testing; {competitor} has a higher visible ad volume."
        )
    else:
        recommendations.append(
            "Maintain active creative rotation, but use competitor themes to sharpen positioning."
        )

    competitor_keywords = [item["keyword"] for item in top_keywords(competitor_ads, limit=3)]
    if competitor_keywords:
        recommendations.append(
            "Run a message test around competitor-visible themes: "
            + ", ".join(competitor_keywords)
            + "."
        )

    competitor_media = count_values(competitor_ads, "media_type")
    if competitor_media:
        top_media = next(iter(competitor_media))
        recommendations.append(
            f"Create at least one campaign variant using {top_media}, the competitor's most visible media type."
        )

    competitor_ctas = count_values(competitor_ads, "call_to_action")
    if competitor_ctas:
        top_cta = next(iter(competitor_ctas))
        recommendations.append(f"Test a '{top_cta}' CTA variant against current best performers.")

    recommendations.append(
        "Review landing pages for the top similar creatives to identify offer and funnel differences."
    )

    return recommendations
