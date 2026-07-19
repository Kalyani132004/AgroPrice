"""
Analyzes crop price history to identify trends, averages, and market changes.
"""

from core.utils.math_utils import mean, safe_round, std_deviation, percentage_change


class TrendAnalyzer:
    def __init__(self, price_history: list):
        self.history = price_history or []
        self.prices = [entry["price"] for entry in self.history if "price" in entry]

    def average(self) -> float:
        return mean(self.prices)

    def highest(self) -> float:
        return max(self.prices) if self.prices else 0.0

    def lowest(self) -> float:
        return min(self.prices) if self.prices else 0.0

    def volatility(self) -> float:
        """Standard deviation of prices — higher = more unstable market."""
        return std_deviation(self.prices)

    def trend_direction(self) -> str:
        """Compares first-half average vs second-half average."""
        if len(self.prices) < 2:
            return "Stable"
        midpoint = len(self.prices) // 2
        first_half_avg = mean(self.prices[:midpoint])
        second_half_avg = mean(self.prices[midpoint:])
        if second_half_avg > first_half_avg * 1.02:
            return "Rising"
        if second_half_avg < first_half_avg * 0.98:
            return "Falling"
        return "Stable"

    def change_percent(self) -> float:
        """% change from the earliest to the latest recorded price."""
        if len(self.prices) < 2:
            return 0.0
        return percentage_change(self.prices[0], self.prices[-1])

    def summary(self) -> dict:
        return {
            "average": self.average(),
            "highest": self.highest(),
            "lowest": self.lowest(),
            "volatility": self.volatility(),
            "trend": self.trend_direction(),
            "change_percent": self.change_percent(),
            "data_points": len(self.prices),
        }
