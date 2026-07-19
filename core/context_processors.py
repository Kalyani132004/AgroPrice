"""Site-wide template context — available in every template automatically."""


def site_context(request):
    return {
        "SITE_NAME": "AgroPrice",
        "SITE_TAGLINE": "Mandi Price Tracker & Crop Profit Analyzer",
    }
