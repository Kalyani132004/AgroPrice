"""
Manages the farmer's watchlist by adding, removing, and tracking crops with price alerts.
"""

from db.repositories.crop_repository import CropRepository
from db.repositories.price_repository import PriceRepository
from db.repositories.user_profile_repository import UserProfileRepository


class WatchlistService:
    def __init__(self):
        self.profile_repo = UserProfileRepository()
        self.price_repo = PriceRepository()
        self.crop_repo = CropRepository()

    # ---------- read ----------
    def get_raw_watchlist(self, auth_user_id: int) -> list:
        profile = self.profile_repo.find_by_auth_id(auth_user_id) or {}
        return profile.get("watchlist", [])

    def is_watchlisted(self, auth_user_id: int, crop_name: str) -> bool:
        return any(item.get("crop_name") == crop_name for item in self.get_raw_watchlist(auth_user_id))

    def get_watchlist_with_prices(self, auth_user_id: int) -> list:
        """Enriches each watchlist entry with its crop_id, latest live price, and alert status."""
        enriched = []
        for item in self.get_raw_watchlist(auth_user_id):
            crop_name = item.get("crop_name")
            threshold = item.get("alert_threshold")
            latest = self.price_repo.latest_for_crop(crop_name)
            price = latest.get("price") if latest else None
            alert_triggered = bool(threshold and price is not None and price >= threshold)

            crop_doc = self.crop_repo.find_by_name(crop_name)
            crop_id = str(crop_doc["_id"]) if crop_doc else None

            enriched.append({
                "crop_name": crop_name,
                "crop_id": crop_id,
                "alert_threshold": threshold,
                "latest_price": price,
                "market": latest.get("market") if latest else None,
                "alert_triggered": alert_triggered,
            })
        return enriched

    # ---------- write ----------
    def add(self, auth_user_id: int, crop_name: str, alert_threshold: float = None):
        # Remove any existing entry for this crop first (avoid duplicates), then add fresh.
        self.profile_repo.collection.update_one(
            {"auth_user_id": auth_user_id}, {"$pull": {"watchlist": {"crop_name": crop_name}}}
        )
        self.profile_repo.collection.update_one(
            {"auth_user_id": auth_user_id},
            {"$push": {"watchlist": {"crop_name": crop_name, "alert_threshold": alert_threshold}}},
        )

    def remove(self, auth_user_id: int, crop_name: str):
        self.profile_repo.collection.update_one(
            {"auth_user_id": auth_user_id}, {"$pull": {"watchlist": {"crop_name": crop_name}}}
        )

    def toggle(self, auth_user_id: int, crop_name: str, alert_threshold: float = None) -> bool:
        """Adds if absent, removes if present. Returns True if now watchlisted."""
        if self.is_watchlisted(auth_user_id, crop_name):
            self.remove(auth_user_id, crop_name)
            return False
        self.add(auth_user_id, crop_name, alert_threshold)
        return True
