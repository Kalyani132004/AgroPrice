"""PriceService — business logic layer for all price operations."""
from core.utils.datetime_utils import format_display_date
from core.utils.math_utils import mean, safe_round
from core.utils.regex_validators import validate_crop_name, validate_quality, validate_price, ValidationError
from db.base_repository import RepositoryError
from db.repositories.price_repository import PriceRepository
from prices.domain.price_record import PriceRecord


class PriceService:
    def __init__(self):
        self.repo = PriceRepository()

    # ---------- CRUD ----------
    def add_price(self, crop_name: str, market: str, price, quality: str) -> str:
        try:
            crop_name = validate_crop_name(crop_name)
            quality = validate_quality(quality)
            price = validate_price(price)
        except ValidationError:
            raise

        record = PriceRecord(crop_name=crop_name, market=market.strip().title(), price=price, quality=quality)
        try:
            return self.repo.insert_one(record.to_dict())
        except RepositoryError as exc:
            raise ValidationError(f"Could not save price: {exc}") from exc

    def update_price(self, price_id: str, **updates) -> bool:
        try:
            return self.repo.update_one(price_id, updates)
        except RepositoryError as exc:
            raise ValidationError(str(exc)) from exc

    def delete_price(self, price_id: str) -> bool:
        try:
            return self.repo.delete_one(price_id)
        except RepositoryError as exc:
            raise ValidationError(str(exc)) from exc

    # ---------- Read / analytics ----------
    def today_prices(self) -> list:
        rows = self.repo.today_prices()
        for r in rows:
            r["crop_name"] = r.pop("_id")
            r["date_display"] = format_display_date(r.get("date"))
        return rows

    def history(self, crop_name: str, days: int = 30) -> list:
        docs = self.repo.history_for_crop(crop_name, days=days)
        records = [PriceRecord.from_dict(d) for d in docs]
        return [
            {"date": r.date, "date_display": format_display_date(r.date), "price": r.price, "market": r.market}
            for r in records
        ]

    def compare_markets(self, crop_name: str) -> list:
        rows = self.repo.by_market(crop_name)
        for r in rows:
            r["market"] = r.pop("_id")
            r["date_display"] = format_display_date(r.get("date"))
        return rows

    def thirty_day_stats(self, crop_name: str) -> dict:
        stats = self.repo.thirty_day_stats(crop_name)
        if not stats:
            return {"avg_price": 0, "max_price": 0, "min_price": 0, "count": 0}
        stats["avg_price"] = safe_round(stats.get("avg_price", 0))
        return stats

    def trend_series(self, crop_name: str, days: int = 30) -> dict:
        """Returns {labels: [...], prices: [...]} for Chart.js line chart."""
        history = self.history(crop_name, days=days)
        labels = [h["date_display"].split(",")[0] for h in history]
        prices = [h["price"] for h in history]
        return {"labels": labels, "prices": prices, "average": mean(prices)}

    def global_snapshot(self) -> dict:
        return self.repo.global_high_low()

    def trending_crop(self) -> str:
        result = self.repo.most_trending()
        return result["_id"] if result else "N/A"
