"""Datetime module — 30-day windows, formatting, date parsing."""
from datetime import datetime, timedelta


def days_ago(n: int) -> datetime:
    return datetime.utcnow() - timedelta(days=n)


def thirty_day_window() -> tuple:
    end = datetime.utcnow()
    start = end - timedelta(days=30)
    return start, end


def format_display_date(dt) -> str:
    """Human-friendly date, e.g. '08 Jul 2026, 06:45 PM'."""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return dt
    if not dt:
        return "-"
    return dt.strftime("%d %b %Y, %I:%M %p")


def parse_csv_date(value: str) -> datetime:
    """Parses common CSV date formats (DD-MM-YYYY, YYYY-MM-DD, DD/MM/YYYY)."""
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {value}")


def time_since(dt) -> str:
    """'2 hours ago' style relative timestamp for dashboard 'Last Updated'."""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return "just now"
    if not dt:
        return "never"
    delta = datetime.utcnow() - dt
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60} min ago"
    if seconds < 86400:
        return f"{seconds // 3600} hr ago"
    return f"{seconds // 86400} day(s) ago"
