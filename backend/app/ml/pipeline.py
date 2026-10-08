from typing import Any

from app.ml.anomaly import detect_anomalies
from app.ml.blind_spots import find_blind_spots
from app.ml.clustering import cluster_creatives
from app.ml.competitor import compare_competitors
from app.ml.performance import estimate_performance
from app.ml.preprocessing import normalize_ads
from app.ml.recommendations import build_recommendations
from app.ml.similarity import find_similar_creatives
from app.ml.strategy import summarize_strategies
from app.ml.trends import summarize_trends


def analyze_competitors(
    company: str,
    competitor: str,
    company_ads: Any,
    competitor_ads: Any,
) -> dict[str, Any]:
    normalized_company_ads = normalize_ads(company_ads)
    normalized_competitor_ads = normalize_ads(competitor_ads)
    all_ads = normalized_company_ads + normalized_competitor_ads

    return {
        "company": company,
        "competitor": competitor,
        "overview": {
            "company_ads_found": len(normalized_company_ads),
            "competitor_ads_found": len(normalized_competitor_ads),
            "total_ads_analyzed": len(all_ads),
            "data_source": "Meta Ad Library via TinyFish",
        },
        "strategies": summarize_strategies(
            normalized_company_ads,
            normalized_competitor_ads,
        ),
        "creative_clusters": cluster_creatives(normalized_competitor_ads),
        "similar_creatives": find_similar_creatives(
            normalized_company_ads,
            normalized_competitor_ads,
        ),
        "performance": {
            company: estimate_performance(normalized_company_ads),
            competitor: estimate_performance(normalized_competitor_ads),
        },
        "trends": {
            company: summarize_trends(normalized_company_ads),
            competitor: summarize_trends(normalized_competitor_ads),
        },
        "anomalies": detect_anomalies(all_ads),
        "competitor_comparison": compare_competitors(
            company,
            competitor,
            normalized_company_ads,
            normalized_competitor_ads,
        ),
        "blind_spots": find_blind_spots(
            company,
            competitor,
            normalized_company_ads,
            normalized_competitor_ads,
        ),
        "recommendations": build_recommendations(
            company,
            competitor,
            normalized_company_ads,
            normalized_competitor_ads,
        ),
    }
