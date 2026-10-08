import pandas as pd
from pathlib import Path


def save_ads_to_excel(data, company):

    ads = data.get("ads", [])

    if not ads:
        print("No ads found.")
        return None

    rows = []

    for ad in ads:
        rows.append({
            "advertiser_name": ad.get("advertiser_name"),
            "ad_archive_id": ad.get("ad_archive_id"),
            "ad_text": ad.get("ad_text"),
            "headline": ad.get("headline"),
            "description": ad.get("description"),
            "call_to_action": ad.get("call_to_action"),
            "start_date": ad.get("start_date"),
            "platforms": ", ".join(ad.get("platforms", [])),
            "media_type": ad.get("media_type"),
            "landing_page_url": ad.get("landing_page_url"),
            "ad_library_url": ad.get("ad_library_url")
        })

    df = pd.DataFrame(rows)

    # Create output directory
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Safe filename
    filename = output_dir / f"{company.lower()}_ads.xlsx"

    df.to_excel(filename, index=False)

    print(f"\nSaved {len(df)} ads to:")
    print(filename)

    return filename