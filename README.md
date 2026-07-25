# 🌾 AgroPrice — Mandi Price Tracker & Crop Profit Analyzer

AgroPrice is a web-based **Agritech platform** developed using **Python, Django, MongoDB, Bootstrap, JavaScript, and Django REST Framework**.

The system helps farmers monitor mandi crop prices, analyze market trends, compare market rates, and calculate expected crop profitability before selling their produce.

AgroPrice provides separate dashboards for **Farmers** and **Administrators** with secure role-based authentication and data-driven insights.

---

# 🚀 Key Features

## 👨‍🌾 Farmer Module

- Farmer Registration and Login
- Secure Authentication
- Personalized Farmer Dashboard
- Live Mandi Crop Prices
- Crop Watchlist Management
- Price Trend Analysis
- Market Price Comparison
- Sell/Hold Recommendation
- Revenue & Profit Calculator
- Crop Profitability Analysis


---

## 👨‍💼 Admin Module

- Admin Dashboard
- Role-Based Access Control
- Manage Crops
- Manage Crop Prices
- View Registered Farmers
- View Contact Messages
- Upload Bulk Price Data using CSV
- Download Price Reports
- Market Analytics


---

# 📊 Analytics Module

AgroPrice provides crop market analysis using:

- 30-Day Price Trend Analysis
- Average Price Calculation
- Highest Price Detection
- Lowest Price Detection
- Market Volatility Analysis
- Profit Margin Calculation
- Break-even Price Calculation
- Rule-Based Sell Advisor


---

# 🌐 REST API

Developed using **Django REST Framework (DRF)**.

Available APIs:

- Crop APIs
- Price APIs
- Analytics APIs
- Watchlist APIs


---

# 🗄️ Database

AgroPrice uses **MongoDB** as the primary database.

MongoDB is integrated with Django using **PyMongo**.

## Database Collections

```
agroprice_db

├── users
├── crops
├── pricehistory
└── contact_messages
```

---

# 📈 Data Visualization

Interactive charts are implemented using **Chart.js**.

Charts included:

- Crop Price Trend Line Chart
- Category Wise Price Bar Chart
- Crop Price Distribution Chart


---

# 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend | Python, Django |
| API | Django REST Framework |
| Database | MongoDB |
| Database Connector | PyMongo |
| Visualization | Chart.js |
| Version Control | Git & GitHub |
| IDE | Visual Studio Code |


---

# 🏗️ Project Architecture

```
AgroPrice
│
├── accounts
│   └── Authentication, Farmer/Admin Profile Management
│
├── crops
│   └── Crop Management System
│
├── prices
│   └── Mandi Price Management & CSV Processing
│
├── analytics
│   └── Trend Analysis & Profit Calculator
│
├── dashboard
│   └── Farmer/Admin Dashboard
│
├── api
│   └── REST API Services
│
├── db
│   └── MongoDB Connection & Repository Layer
│
├── core
│   └── Common Utilities
│
├── templates
│   └── Django HTML Templates
│
├── static
│   └── CSS, JavaScript, Images
│
└── scripts
    └── Database Utility Scripts
```

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/Kalyani132004/AgroPrice.git
```

Move into project folder:

```bash
cd AgroPrice
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## 4. Configure MongoDB

Start MongoDB locally:

```
mongodb://localhost:27017
```

Database name:

```
agroprice_db
```

---

## 5. Apply Django Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## 6. Create Admin Account

```bash
python manage.py createsuperuser
```

---

## 7. Run Development Server

```bash
python manage.py runserver
```

Open browser:

```
http://127.0.0.1:8000/
```

---

# 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/crops/` | View Crop List |
| GET | `/api/v1/prices/today/` | Today's Prices |
| GET | `/api/v1/prices/history/` | Historical Price Data |
| GET | `/api/v1/prices/compare/` | Market Comparison |
| POST | `/api/v1/prices/upload-csv/` | Upload CSV Price Data |
| GET | `/api/v1/analytics/trend/` | Price Trend Analysis |
| POST | `/api/v1/analytics/profit/` | Profit Calculation |


---

# 🐍 Python Concepts Implemented

This project demonstrates:

- Object-Oriented Programming
- Classes and Objects
- Exception Handling
- File Handling
- CSV Processing
- Regular Expressions
- Datetime Operations
- MongoDB CRUD Operations
- Aggregation Queries
- Multithreading


---

# 📂 CSV Price Import Format

CSV file format:

```
crop_name,market,price,quality,date
```

Example:

```
Tomato,Pune APMC,2500,A,2026-07-20
```

---

# 💰 Crop Profit Calculator

Farmers can calculate expected profit using:

```
Profit = Total Revenue - Total Cultivation Cost
```

Calculation includes:

- Crop Quantity
- Selling Price
- Labour Cost
- Transportation Cost
- Miscellaneous Expenses

---

# 🔮 Future Enhancements

- AI-Based Crop Price Prediction
- Weather Forecast Integration
- SMS Price Alerts
- Email Notifications
- Mobile Application
- Multi-language Support
- Advanced Market Forecasting


---

# 👩‍💻 Developer

**Kalyani Sonawane**

GitHub:

https://github.com/Kalyani132004


---

⭐ If you like this project, consider giving it a star on GitHub.