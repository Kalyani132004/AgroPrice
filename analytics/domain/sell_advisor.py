"""
Generates a sell or hold recommendation based on crop price trends and market data.
"""

from core.utils.math_utils import safe_round


class SellAdvisor:
    ABOVE_AVG_THRESHOLD = 1.03   # 3% above average counts as "above"
    BELOW_AVG_THRESHOLD = 0.97   # 3% below average counts as "below"
    VOLATILITY_RATIO = 0.10      # volatility > 10% of average counts as "volatile"

    def __init__(self, trend_summary: dict, current_price: float):
        self.summary = trend_summary or {}
        self.current_price = float(current_price or 0)

    def _score_and_reasons(self) -> tuple:
        avg = self.summary.get("average", 0) or 0
        trend = self.summary.get("trend", "Stable")
        change = self.summary.get("change_percent", 0) or 0
        volatility = self.summary.get("volatility", 0) or 0

        score = 0
        reasons = []

        if avg > 0 and self.current_price > avg * self.ABOVE_AVG_THRESHOLD:
            score += 2
            reasons.append(f"Current price (₹{self.current_price}) is above the 30-day average (₹{safe_round(avg)}).")
        elif avg > 0 and self.current_price < avg * self.BELOW_AVG_THRESHOLD:
            score -= 2
            reasons.append(f"Current price (₹{self.current_price}) is below the 30-day average (₹{safe_round(avg)}).")

        if trend == "Rising":
            score += 2
            reasons.append("Prices have shown a rising trend over the last 30 days.")
        elif trend == "Falling":
            score -= 2
            reasons.append("Prices have shown a falling trend over the last 30 days.")

        if change > 5:
            score += 1
            reasons.append(f"Price is up {change}% over the observed period.")
        elif change < -5:
            score -= 1
            reasons.append(f"Price is down {abs(change)}% over the observed period.")

        if avg > 0 and volatility > avg * self.VOLATILITY_RATIO:
            reasons.append("Prices have been volatile recently — consider selling in smaller batches to reduce risk.")

        return score, reasons

    def recommendation(self) -> dict:
        score, reasons = self._score_and_reasons()

        if score >= 3:
            verdict, confidence = "Sell Now", "High"
        elif score >= 1:
            verdict, confidence = "Lean Sell", "Medium"
        elif score <= -3:
            verdict, confidence = "Hold", "High"
        elif score <= -1:
            verdict, confidence = "Lean Hold", "Medium"
        else:
            verdict, confidence = "Neutral", "Low"

        if not reasons:
            reasons = ["Not enough distinct signals yet — prices are broadly stable near the average."]

        return {
            "verdict": verdict,
            "confidence": confidence,
            "score": score,
            "reasons": reasons,
            "current_price": self.current_price,
            "average_price": safe_round(self.summary.get("average", 0)),
        }
