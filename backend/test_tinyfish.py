from app.services.tinyfish import get_competitor_ads
from app.services.export import save_ads_to_excel


result = get_competitor_ads("Swiggy")

print("\n========== FINAL RESULT ==========\n")
print(result)

save_ads_to_excel(result, "Swiggy")