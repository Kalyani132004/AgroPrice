"""
Calculates revenue, cost, profit, profit margin, and break-even price for a crop.
"""
from core.utils.math_utils import safe_round, profit_margin


class ProfitCalculator:
    def __init__(self, quantity: float, selling_price_per_unit: float,
                 cultivation_cost: float = 0, transport_cost: float = 0,
                 labour_cost: float = 0, misc_cost: float = 0):
        self.quantity = max(float(quantity), 0)
        self.selling_price_per_unit = max(float(selling_price_per_unit), 0)
        self.cultivation_cost = max(float(cultivation_cost), 0)
        self.transport_cost = max(float(transport_cost), 0)
        self.labour_cost = max(float(labour_cost), 0)
        self.misc_cost = max(float(misc_cost), 0)

    def total_revenue(self) -> float:
        return safe_round(self.quantity * self.selling_price_per_unit)

    def total_cost(self) -> float:
        return safe_round(
            self.cultivation_cost + self.transport_cost + self.labour_cost + self.misc_cost
        )

    def net_profit(self) -> float:
        return safe_round(self.total_revenue() - self.total_cost())

    def profit_margin_percent(self) -> float:
        return profit_margin(self.total_revenue(), self.total_cost())

    def break_even_price(self) -> float:
        if self.quantity <= 0:
            return 0.0
        return safe_round(self.total_cost() / self.quantity)

    def is_profitable(self) -> bool:
        return self.net_profit() > 0

    def summary(self) -> dict:
        return {
            "total_revenue": self.total_revenue(),
            "total_cost": self.total_cost(),
            "net_profit": self.net_profit(),
            "profit_margin_percent": self.profit_margin_percent(),
            "break_even_price": self.break_even_price(),
            "is_profitable": self.is_profitable(),
        }
