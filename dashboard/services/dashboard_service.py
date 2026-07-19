# dashboard data for farmer and admin users
import json

from accounts.models import Profile
from accounts.services.watchlist_service import WatchlistService
from analytics.services.advisor_service import AdvisorService
from crops.services.crop_service import CropService
from prices.services.multi_crop_loader import MultiCropLoader
from prices.services.price_service import PriceService


class DashboardService:
    def __init__(self):
        self.crop_service = CropService()
        self.price_service = PriceService()
        self.watchlist_service = WatchlistService()
        self.advisor_service = AdvisorService()

    def farmer_dashboard_data(self, user=None) -> dict:
        watchlist_items = []
        if user is not None and getattr(user, "is_authenticated", False):
            watchlist_items = self.watchlist_service.get_watchlist_with_prices(user.id)

        has_watchlist = bool(watchlist_items)

        if has_watchlist:
            crop_names = [item["crop_name"] for item in watchlist_items]
        else:
            crops = self.crop_service.list_all()
            crop_names = [c.name for c in crops[:8]]

        # Threaded concurrent fetch 
        loader = MultiCropLoader()
        latest_prices = loader.load_many(crop_names) if crop_names else {}

        # Attach a Sell/Hold recommendation to each watchlist crop
        for item in watchlist_items:
            item["recommendation"] = self.advisor_service.recommend(item["crop_name"], days=30)

        snapshot = self.price_service.global_snapshot()
        trending = self.price_service.trending_crop()

        pie_labels = [name for name, doc in latest_prices.items() if doc]
        pie_values = [doc["price"] for doc in latest_prices.values() if doc]

        return {
            "total_crops": self.crop_service.total_count(),
            "highest_price": snapshot.get("max_price", 0),
            "lowest_price": snapshot.get("min_price", 0),
            "trending_crop": trending,
            "latest_prices": latest_prices,
            "watchlist_items": watchlist_items,
            "has_watchlist": has_watchlist,
            "pie_chart_json": json.dumps({"labels": pie_labels, "values": pie_values}),
        }

    def admin_dashboard_data(self) -> dict:
        base = self.farmer_dashboard_data(user=None)
        base["total_users"] = Profile.objects.filter(role="farmer").count()
        base["category_breakdown"] = self.crop_service.category_breakdown()
        base["bar_chart_json"] = json.dumps({
            "labels": [c["_id"] for c in base["category_breakdown"]],
            "values": [c["count"] for c in base["category_breakdown"]],
        })
        return base
