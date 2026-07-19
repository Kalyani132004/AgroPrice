"""Crops views — Crop List, Crop Details, Manage Crops (Admin CRUD)."""
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from accounts.services.watchlist_service import WatchlistService
from analytics.services.advisor_service import AdvisorService
from core.decorators import admin_required, farmer_required
from core.utils.regex_validators import ValidationError
from crops.services.crop_service import CropService
from prices.services.price_service import PriceService


def crop_list_view(request):
    service = CropService()
    query = request.GET.get("q", "").strip()

    crops = service.search(query) if query else service.list_all()

    paginator = Paginator(crops, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "crops/crop_list.html", {
        "page_obj": page_obj,
        "query": query,
        "categories": service.category_breakdown(),
    })


def crop_detail_view(request, crop_id):
    crop_service = CropService()
    price_service = PriceService()
    advisor_service = AdvisorService()

    crop = crop_service.get_by_id(crop_id)
    if not crop:
        messages.error(request, "Crop not found.")
        return redirect("crops:crop_list")

    stats = price_service.thirty_day_stats(crop.name)
    market_prices = price_service.compare_markets(crop.name)
    history = price_service.history(crop.name, days=30)
    recommendation = advisor_service.recommend(crop.name, days=30)

    is_watchlisted = False
    if request.user.is_authenticated and not request.user.is_staff:
        is_watchlisted = WatchlistService().is_watchlisted(request.user.id, crop.name)

    return render(request, "crops/crop_detail.html", {
        "crop": crop,
        "stats": stats,
        "market_prices": market_prices,
        "history": history,
        "recommendation": recommendation,
        "is_watchlisted": is_watchlisted,
    })


@farmer_required
def toggle_watchlist_view(request, crop_id):
    crop_service = CropService()
    crop = crop_service.get_by_id(crop_id)
    if not crop:
        messages.error(request, "Crop not found.")
        return redirect("crops:crop_list")

    threshold_raw = request.POST.get("alert_threshold", "").strip()
    threshold = None
    if threshold_raw:
        try:
            threshold = float(threshold_raw)
        except ValueError:
            messages.warning(request, "Alert price must be a number — ignored.")

    watchlist_service = WatchlistService()
    now_watchlisted = watchlist_service.toggle(request.user.id, crop.name, threshold)

    if now_watchlisted:
        messages.success(request, f"{crop.name} added to your watchlist{f' with an alert at ₹{threshold}' if threshold else ''}.")
    else:
        messages.info(request, f"{crop.name} removed from your watchlist.")

    return redirect("crops:crop_detail", crop_id=crop_id)


@admin_required
def manage_crops_view(request):
    service = CropService()

    if request.method == "POST":
        action = request.POST.get("action")
        try:
            if action == "add":
                grades = [g.strip() for g in request.POST.get("quality_grades", "").split(",") if g.strip()]
                service.add_crop(
                    name=request.POST.get("name", ""),
                    category=request.POST.get("category", ""),
                    unit=request.POST.get("unit", "Quintal"),
                    quality_grades=grades or ["FAQ"],
                    description=request.POST.get("description", ""),
                )
                messages.success(request, "Crop added successfully.")
            elif action == "delete":
                service.delete_crop(request.POST.get("crop_id"))
                messages.success(request, "Crop deleted.")
        except ValidationError as exc:
            messages.error(request, str(exc))
        return redirect("crops:manage_crops")

    crops = service.list_all()
    return render(request, "crops/manage_crops.html", {"crops": crops})
