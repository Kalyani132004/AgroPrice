"""PriceRepository — MongoDB access for the `pricehistory` collection.

Contains the aggregation pipelines used for 30-day averages, highest/lowest
price lookups, market comparisons, and trend datasets.
"""
from datetime import datetime, timedelta

from db.base_repository import BaseRepository


class PriceRepository(BaseRepository):
    collection_name = "pricehistory"

    # ---------- basic lookups ----------
    def latest_for_crop(self, crop_name: str) -> dict | None:
        results = self.find({"crop_name": crop_name}, limit=1, sort=[("date", -1)])
        return results[0] if results else None

    def history_for_crop(self, crop_name: str, days: int = 30) -> list:
        since = datetime.utcnow() - timedelta(days=days)
        return self.find(
            {"crop_name": crop_name, "date": {"$gte": since}},
            sort=[("date", 1)],
        )

    def by_market(self, crop_name: str) -> list:
        """All markets' latest price for a given crop — used for Compare Markets."""
        pipeline = [
            {"$match": {"crop_name": crop_name}},
            {"$sort": {"date": -1}},
            {
                "$group": {
                    "_id": "$market",
                    "price": {"$first": "$price"},
                    "date": {"$first": "$date"},
                    "quality": {"$first": "$quality"},
                }
            },
            {"$sort": {"price": -1}},
        ]
        return self.aggregate(pipeline)

    def today_prices(self) -> list:
        """
        Returns the latest available price for each Crop + Market.
        This avoids timezone/date issues and always shows live data.
        """

        pipeline = [
            {
                "$sort": {
                    "date": -1
                }
            },
            {
                "$group": {
                    "_id": {
                        "crop_name": "$crop_name",
                        "market": "$market"
                    },
                    "crop_name": {"$first": "$crop_name"},
                    "market": {"$first": "$market"},
                    "price": {"$first": "$price"},
                    "quality": {"$first": "$quality"},
                    "date": {"$first": "$date"},
                }
            },
            {
                "$sort": {
                    "crop_name": 1,
                    "market": 1
                }
            }
        ]

        return self.aggregate(pipeline)
        
    
    
    # ---------- 30-day average / high / low (aggregation) ----------
    def thirty_day_stats(self, crop_name: str) -> dict:
        since = datetime.utcnow() - timedelta(days=30)
        pipeline = [
            {"$match": {"crop_name": crop_name, "date": {"$gte": since}}},
            {
                "$group": {
                    "_id": "$crop_name",
                    "avg_price": {"$avg": "$price"},
                    "max_price": {"$max": "$price"},
                    "min_price": {"$min": "$price"},
                    "count": {"$sum": 1},
                }
            },
        ]
        result = self.aggregate(pipeline)
        return result[0] if result else {}

    def most_trending(self) -> dict | None:
        """Crop with highest number of price entries in the last 7 days."""
        since = datetime.utcnow() - timedelta(days=7)
        pipeline = [
            {"$match": {"date": {"$gte": since}}},
            {"$group": {"_id": "$crop_name", "updates": {"$sum": 1}}},
            {"$sort": {"updates": -1}},
            {"$limit": 1},
        ]
        result = self.aggregate(pipeline)
        return result[0] if result else None

    def global_high_low(self) -> dict:
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "max_price": {"$max": "$price"},
                    "min_price": {"$min": "$price"},
                }
            }
        ]
        result = self.aggregate(pipeline)
        return result[0] if result else {"max_price": 0, "min_price": 0}
