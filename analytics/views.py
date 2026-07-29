# Analytics views — Trend Analysis and Revenue/Profit Calculator pages.

import json

from django.shortcuts import render

from analytics.domain.profit_calculator import ProfitCalculator
from analytics.domain.trend_analyzer import TrendAnalyzer
from analytics.services.advisor_service import AdvisorService
from crops.services.crop_service import CropService
from prices.services.price_service import PriceService


def trend_analysis_view(request):
    crop_service = CropService()
    price_service = PriceService()

    crop_name = request.GET.get("crop", "")
    history, summary, chart_data, recommendation = [], {}, {"labels": [], "prices": []}, None

    if crop_name:
        history = price_service.history(crop_name, days=30)
        analyzer = TrendAnalyzer(history)
        summary = analyzer.summary()
        chart_data = {
            "labels": [h["date_display"].split(",")[0] for h in history],
            "prices": [h["price"] for h in history],
        }
        recommendation = AdvisorService().recommend(crop_name, days=30)

    return render(request, "analytics/trend_analysis.html", {
        "crops": crop_service.list_all(),
        "selected_crop": crop_name,
        "summary": summary,
        "chart_data_json": json.dumps(chart_data),
        "recommendation": recommendation,
    })


def revenue_calculator_view(request):
    crop_service = CropService()
    result = None

    def format_inr(amount):
        amount = float(amount)

        sign = "-" if amount < 0 else ""
        amount = abs(amount)

        integer = int(amount)
        decimal = amount - integer

        s = str(integer)

        if len(s) > 3:
            last3 = s[-3:]
            rest = s[:-3]

            parts = []
            while len(rest) > 2:
                parts.insert(0, rest[-2:])
                rest = rest[:-2]

            if rest:
                parts.insert(0, rest)

            s = ",".join(parts) + "," + last3

        if decimal:
            s += f"{decimal:.2f}"[1:]

        return f"{sign}₹{s}"

    if request.method == "POST":
        calculator = ProfitCalculator(
            quantity=request.POST.get("quantity", 0),
            selling_price_per_unit=request.POST.get("selling_price", 0),
            cultivation_cost=request.POST.get("cultivation_cost", 0),
            transport_cost=request.POST.get("transport_cost", 0),
            labour_cost=request.POST.get("labour_cost", 0),
            misc_cost=request.POST.get("misc_cost", 0),
        )

        result = calculator.summary()

        # Format currency values in Indian format
        result["total_revenue"] = format_inr(result["total_revenue"])
        result["total_cost"] = format_inr(result["total_cost"])
        result["net_profit"] = format_inr(result["net_profit"])
        result["break_even_price"] = format_inr(result["break_even_price"])

    return render(
        request,
        "analytics/revenue_calculator.html",
        {
            "crops": crop_service.list_all(),
            "result": result,
        },
    )