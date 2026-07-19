"""Prices views — Today's Prices, Historical Prices, Compare Markets, CSV ops."""
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.decorators import admin_required
from core.utils.regex_validators import ValidationError
from crops.services.crop_service import CropService
from prices.services.csv_import_export import CSVImportExportService
from prices.services.price_service import PriceService


def today_prices_view(request):
    service = PriceService()
    prices = service.today_prices()
    return render(request, "prices/today_prices.html", {"prices": prices})


def historical_prices_view(request):
    crop_service = CropService()
    price_service = PriceService()

    crop_name = request.GET.get("crop", "")
    days = int(request.GET.get("days", 30))

    history = price_service.history(crop_name, days=days) if crop_name else []
    stats = price_service.thirty_day_stats(crop_name) if crop_name else {}

    return render(request, "prices/historical_prices.html", {
        "crops": crop_service.list_all(),
        "selected_crop": crop_name,
        "days": days,
        "history": history,
        "stats": stats,
    })


def compare_markets_view(request):
    crop_service = CropService()
    price_service = PriceService()

    crop_name = request.GET.get("crop", "")
    comparisons = price_service.compare_markets(crop_name) if crop_name else []

    return render(request, "prices/compare_markets.html", {
        "crops": crop_service.list_all(),
        "selected_crop": crop_name,
        "comparisons": comparisons,
    })


@admin_required
def upload_csv_view(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        service = CSVImportExportService()
        result = service.import_prices(request.FILES["csv_file"])
        if result.success_count:
            messages.success(request, f"{result.success_count} price record(s) imported successfully.")
        if result.error_rows:
            for err in result.error_rows[:5]:
                messages.warning(request, f"Row {err['row']}: {err['reason']}")
        return redirect("prices:upload_csv")

    return render(request, "prices/upload_csv.html")


@admin_required
def download_csv_view(request):
    crop_name = request.GET.get("crop") or None
    service = CSVImportExportService()
    csv_content = service.export_prices(crop_name)

    response = HttpResponse(csv_content, content_type="text/csv")
    filename = f"agroprice_{crop_name or 'all'}_prices.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@admin_required
def add_price_view(request):
    crop_service = CropService()
    price_service = PriceService()

    if request.method == "POST":
        try:
            price_service.add_price(
                crop_name=request.POST.get("crop_name", ""),
                market=request.POST.get("market", ""),
                price=request.POST.get("price", "0"),
                quality=request.POST.get("quality", "FAQ"),
            )
            messages.success(request, "Price added successfully.")
        except ValidationError as exc:
            messages.error(request, str(exc))
        return redirect("prices:add_price")

    return render(request, "prices/add_price.html", {"crops": crop_service.list_all()})
