"""CropRepository — MongoDB access for the `crops` collection."""
import re

from db.base_repository import BaseRepository


class CropRepository(BaseRepository):
    collection_name = "crops"

    def find_by_name(self, name: str) -> dict | None:
        return self.find_one({"name": {"$regex": f"^{re.escape(name)}$", "$options": "i"}})

    def search(self, query: str, limit: int = 20) -> list:
        """Case-insensitive partial-match search on crop name/category."""
        regex = {"$regex": re.escape(query), "$options": "i"}
        return self.find({"$or": [{"name": regex}, {"category": regex}]}, limit=limit)

    def list_by_category(self, category: str) -> list:
        return self.find({"category": {"$regex": f"^{re.escape(category)}$", "$options": "i"}})

    def all_names(self) -> list:
        return [doc["name"] for doc in self.find({}, sort=[("name", 1)])]

    def category_counts(self) -> list:
        """Aggregation: count of crops per category."""
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        return self.aggregate(pipeline)
