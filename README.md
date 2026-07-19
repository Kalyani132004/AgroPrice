# 🌾 AgroPrice — Mandi Price Tracker & Crop Profit Analyzer

AgroPrice is a web-based agricultural price analysis platform developed using **Python, Django, MongoDB, Bootstrap, and Django REST Framework**. 
It helps farmers track live crop prices, analyze market trends, calculate profits, and make better selling decisions.

The system provides separate dashboards for **Farmers** and **Administrators**, making crop price management and market analysis simple and efficient.

---

### 👨‍🌾 Farmer Module
- Farmer Registration & Login
- Personalized Dashboard
- Live Crop Prices
- Crop Watchlist
- Price Alerts
- Trend Analysis
- Sell/Hold Recommendation
- Revenue & Profit Calculator
- Market Price Comparison

### 👨‍💼 Admin Module
- Admin Dashboard
- Manage Crops
- Manage Crop Prices
- View Registered Farmers
- View Contact Messages
- Bulk Price Upload using CSV
- Reports & Analytics

### 📊 Analytics
- 30-Day Price Trend Analysis
- Average Price
- Highest & Lowest Price
- Market Volatility
- Profit Margin Calculation
- Break-even Price
- Rule-Based Sell Advisor

### 🌐 REST API
- Crop APIs
- Price APIs
- Analytics APIs
- Watchlist APIs

# 💾 Database

MongoDB Collections

- users
- crops
- pricehistory
- contact_messages

---

# 📊 Charts Used

- Price Trend Line Chart
- Category Bar Chart
- Crop Price Pie Chart


## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5, Vanilla JS, Chart.js |
| Backend | Python, Django, Django REST Framework |
| Database | MongoDB (PyMongo) — auto-fallback to in-memory `mongomock` if unreachable |
| Auth | Django's built-in `auth_user` (sessions) |

---

## 🚀 Getting Started

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/AgroPrice.git
```


### 1. Clone & create a virtual environment
```bash
cd agroprice
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env if you have a real MongoDB instance running.
# If MONGO_URI is unreachable, the app automatically uses in-memory mongomock —
# perfect for instant demos, but data won't persist between restarts.
```

To use a **real MongoDB**, install MongoDB Community Server locally (or use MongoDB Atlas)
and set `MONGO_URI` accordingly, e.g.:
```
MONGO_URI=mongodb://localhost:27017

```

### 4. Run Django migrations (for auth/sessions/Profile — SQLite by default)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an admin (staff) account
```bash
python manage.py createsuperuser
```
> ⚠️ Any user created with `is_staff=True` can log in via **Admin Login**. Regular
> farmers register through the **Farmer Registration** page instead.

### 6. Seed sample data (recommended for demo/viva)
```bash
python scripts/seed_crops.py
python scripts/seed_prices.py
python scripts/create_mongo_indexes.py
```

### 7. Run the development server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000**

---

## 🗂️ Project Structure

See `docs/architecture.md` for the full explanation of every folder and file.

```
agroprice/        → Django settings, root urls, wsgi/asgi
db/                → MongoDB connection + repository layer (CRUD/aggregation)
core/              → Home/About/Contact/404 + shared utils (regex, math, datetime, csv)
accounts/          → Farmer/Admin auth, Profile, dual Django+MongoDB registration
crops/             → Crop domain class, CropService, Crop List/Detail/Manage
prices/            → PriceRecord domain class, PriceService, CSV import/export, threading loader
analytics/         → TrendAnalyzer, ProfitCalculator, Trend/Calculator pages
dashboard/         → Farmer/Admin dashboards, Reports
api/               → DRF serializers + views (REST API layer)
static/            → CSS (base/components/dashboard/animations) + JS (per-feature files)
templates/          → Shared includes (navbar, footer, toast, modal, pagination) + base.html
scripts/           → Seed data + MongoDB index creation
```

---

## 🔌 Key REST API Endpoints

| Method | Endpoint | Description |
| GET | `/api/v1/crops/?q=wheat` | Search/list crops |
| POST | `/api/v1/crops/` | Create crop (admin) |
| GET | `/api/v1/crops/<id>/` | Crop details |
| GET | `/api/v1/prices/today/` | Today's prices |
| GET | `/api/v1/prices/history/?crop=Wheat&days=30` | Historical prices |
| GET | `/api/v1/prices/compare/?crop=Wheat` | Compare markets |
| POST | `/api/v1/prices/upload-csv/` | Bulk CSV upload (admin) |
| GET | `/api/v1/analytics/trend/?crop=Wheat&days=30` | Trend analysis |
| POST | `/api/v1/analytics/profit/` | Profit calculator |

---

## 🐍 Python Concepts Demonstrated

- **Dictionaries** — crop-price mappings, MongoDB documents
- **Tuples** — `PriceRecord` internal storage
- **List comprehensions** — `TrendAnalyzer`
- **CSV module** — `csv_utils.py`, `csv_import_export.py`
- **Math module** — `math_utils.py` (mean, std-dev, profit margin)
- **Datetime module** — `datetime_utils.py` (30-day windows, formatting)
- **Exception Handling** — repository layer, `AuthService` rollback
- **OOP** — `Crop`, `PriceRecord`, `TrendAnalyzer`, `ProfitCalculator` classes
- **Regex** — `regex_validators.py` (crop names, quality, phone, price)
- **Threading** — `MultiCropLoader` (concurrent dashboard price fetch)


# 🔮 Future Enhancements

- SMS Price Alerts
- Email Notifications
- AI-based Price Prediction
- Weather Forecast Integration
- Mobile Application
- Multi-language Support


# 👩‍💻 Developer

**Kalyani Sonawane**