""" Math module — rounding, averages, percentage change, std-dev """
import math


def safe_round(value: float, digits: int = 2) -> float:
    if value is None:
        return 0.0
    return round(value, digits)


def mean(values: list) -> float:
    if not values:
        return 0.0
    return safe_round(sum(values) / len(values))


def percentage_change(old_value: float, new_value: float) -> float:
    """Returns % change from old to new. Positive = increase, negative = decrease."""
    if not old_value:
        return 0.0
    return safe_round(((new_value - old_value) / old_value) * 100)


def std_deviation(values: list) -> float:
    """Population standard deviation — used to gauge price volatility."""
    if len(values) < 2:
        return 0.0
    avg = mean(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    return safe_round(math.sqrt(variance))


def profit_margin(revenue: float, cost: float) -> float:
    """Profit margin % = (revenue - cost) / revenue * 100."""
    if revenue <= 0:
        return 0.0
    return safe_round(((revenue - cost) / revenue) * 100)
