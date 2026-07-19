"""Generates crop recommendations by analyzing price history and market trends."""

from analytics.domain.sell_advisor import SellAdvisor
from analytics.domain.trend_analyzer import TrendAnalyzer
from prices.services.price_service import PriceService


class AdvisorService:
    def __init__(self):
        self.price_service = PriceService()

    def recommend(self, crop_name: str, days: int = 30) -> dict:
        history = self.price_service.history(crop_name, days=days)

        if not history:
            return {
                "verdict": "No Data", "confidence": "—", "score": 0,
                "reasons": ["Not enough price history yet to generate a recommendation."],
                "current_price": 0, "average_price": 0,
            }

        analyzer = TrendAnalyzer(history)
        summary = analyzer.summary()
        current_price = history[-1]["price"]

        advisor = SellAdvisor(trend_summary=summary, current_price=current_price)
        return advisor.recommendation()
