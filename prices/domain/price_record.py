""" Represents a single crop price record with market and date information. """
from datetime import datetime


class PriceRecord:
    __slots__ = ("_data",)

    def __init__(self, crop_name: str, market: str, price: float, quality: str, date: datetime = None):
        # Immutable tuple storage: (crop_name, market, price, quality, date)
        self._data = (crop_name, market, float(price), quality, date or datetime.utcnow())

    # read-only properties
    @property
    def crop_name(self) -> str:
        return self._data[0]

    @property
    def market(self) -> str:
        return self._data[1]

    @property
    def price(self) -> float:
        return self._data[2]

    @property
    def quality(self) -> str:
        return self._data[3]

    @property
    def date(self) -> datetime:
        return self._data[4]

    def as_tuple(self) -> tuple:
        return self._data

    def to_dict(self) -> dict:
        """Convert to a MongoDB-ready dictionary document."""
        return {
            "crop_name": self.crop_name,
            "market": self.market,
            "price": self.price,
            "quality": self.quality,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PriceRecord":
        date_val = data.get("date")
        if isinstance(date_val, str):
            date_val = datetime.fromisoformat(date_val)
        return cls(
            crop_name=data.get("crop_name", ""),
            market=data.get("market", ""),
            price=data.get("price", 0),
            quality=data.get("quality", "FAQ"),
            date=date_val,
        )

    def __repr__(self):
        return f"PriceRecord(crop={self.crop_name!r}, market={self.market!r}, price={self.price})"
