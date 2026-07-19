"""
Seed script — populates MongoDB `pricehistory` collection with 30 days of
randomized-but-realistic price data for each sample crop, across a few
markets. Run AFTER seed_crops.py.

"""
import os
import random
import sys
from datetime import datetime, timedelta

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agroprice.settings.development")
django.setup()

from prices.services.price_service import PriceService  # noqa: E402
from core.utils.regex_validators import ValidationError  # noqa: E402

MARKETS = ["Pune Mandi", "Nashik Mandi", "Nagpur Mandi", "Aurangabad Mandi"]

BASE_PRICES = {
    "Wheat": 2150, "Rice": 3200, "Onion": 1800, "Tomato": 1400, "Potato": 1200,
    "Soybean": 4300, "Cotton": 6800, "Sugarcane": 320, "Maize": 1950, "Groundnut": 5600,
}

QUALITY_OPTIONS = ["FAQ", "Grade-A", "Grade-B", "Premium"]


def run(days: int = 30):
    service = PriceService()
    total = 0

    for crop_name, base_price in BASE_PRICES.items():
        for day_offset in range(days, -1, -1):
            date = datetime.utcnow() - timedelta(days=day_offset)
            for market in random.sample(MARKETS, k=random.randint(1, len(MARKETS))):
                fluctuation = random.uniform(-0.06, 0.06)
                price = round(base_price * (1 + fluctuation), 2)
                quality = random.choice(QUALITY_OPTIONS)
                try:
                    # Directly insert with historical date via repository since
                    # add_price() always stamps "now" — for seeding we bypass
                    # that by writing through the repository with an explicit date.
                    from prices.domain.price_record import PriceRecord
                    record = PriceRecord(crop_name=crop_name, market=market, price=price, quality=quality, date=date)
                    service.repo.insert_one(record.to_dict())
                    total += 1
                except ValidationError as exc:
                    print(f"[skip] {crop_name}: {exc}")

    print(f"Done. Inserted {total} price records across {len(BASE_PRICES)} crops.")


if __name__ == "__main__":
    run()
