import json
from concurrent.futures import ThreadPoolExecutor
from inspect import signature
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from app.ml.pipeline import analyze_competitors
from app.services.tinyfish import get_competitor_ads

router = APIRouter()


class AnalyzeRequest(BaseModel):
    company: str = Field(min_length=1)
    competitor: str = Field(min_length=1)


@router.post("/analyze")
def analyze(request: AnalyzeRequest):
    company = request.company.strip()
    competitor = request.competitor.strip()

    if not company or not competitor:
        raise HTTPException(
            status_code=400,
            detail="Company and competitor are required.",
        )

    if company.lower() == competitor.lower():
        raise HTTPException(
            status_code=400,
            detail="Company and competitor must be different.",
        )

    try:
        company_ads, competitor_ads = _collect_ads(company, competitor)

        result = _run_ml_pipeline(company_ads, competitor_ads, company, competitor)
        return _json_safe(result)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Analysis failed unexpectedly.",
        ) from exc


def _collect_ads(company: str, competitor: str) -> tuple[dict[str, Any], dict[str, Any]]:
    with ThreadPoolExecutor(max_workers=2) as executor:
        company_future = executor.submit(get_competitor_ads, company)
        competitor_future = executor.submit(get_competitor_ads, competitor)
        return company_future.result(), competitor_future.result()


def _run_ml_pipeline(
    company_ads: dict[str, Any],
    competitor_ads: dict[str, Any],
    company: str,
    competitor: str,
) -> Any:
    pipeline_params = signature(analyze_competitors).parameters

    if "company" in pipeline_params or "competitor" in pipeline_params:
        return analyze_competitors(
            company=company,
            competitor=competitor,
            company_ads=company_ads,
            competitor_ads=competitor_ads,
        )

    return analyze_competitors(
        company_ads,
        competitor_ads,
        historical_company_ads=None,
        historical_competitor_ads=None,
    )


def _json_safe(value: Any) -> Any:
    value = _sanitize(value)

    try:
        encoded = jsonable_encoder(value)
        json.dumps(encoded)
        return encoded
    except TypeError:
        raise


def _sanitize(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, dict):
        return {str(key): _sanitize(item) for key, item in value.items()}

    if isinstance(value, (list, tuple, set)):
        return [_sanitize(item) for item in value]

    if hasattr(value, "to_dict"):
        return _sanitize(value.to_dict())

    if hasattr(value, "tolist"):
        return _sanitize(value.tolist())

    if hasattr(value, "item"):
        return _sanitize(value.item())

    return str(value)
