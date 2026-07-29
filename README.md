# 🌾 AgroPrice — Mandi Price Tracker & Crop Profit Analyzer

AgroPrice is a web-based **Agritech platform** developed using **Python, Django, MongoDB, PostgreSQL, Django REST Framework, Bootstrap, JavaScript, and PyMongo**.

The system helps farmers monitor mandi crop prices, analyze market trends, compare market rates, and calculate expected crop profitability before selling their produce.

AgroPrice provides separate dashboards for **Farmers and Administrators** with secure authentication, role-based access control, market analytics, and data visualization.


---

# 🚀 Key Features

## 👨‍🌾 Farmer Module

- Farmer Registration and Login
- Secure Authentication System
- Farmer Dashboard
- Latest Mandi Crop Prices
- Crop Watchlist Management
- Historical Price Tracking
- Market Price Comparison
- 30-Day Price Trend Analysis
- Sell/Hold Recommendation
- Revenue Calculator
- Crop Profitability Analysis


---

## 👨‍💼 Admin Module

- Admin Dashboard
- Role-Based Access Control
- Manage Crops
- Manage Mandi Prices
- View Registered Farmers
- Delete Farmer Records
- View Contact Messages
- Upload Bulk Price Data using CSV
- Download Price Reports
- Market Analytics


---

# 📊 Analytics Module

AgroPrice provides market insights using:

- 30-Day Price Trend Analysis
- Average Price Calculation
- Highest Price Detection
- Lowest Price Detection
- Market Comparison
- Price Volatility Analysis
- Profit Margin Calculation
- Break-Even Price Calculation
- Rule-Based Sell Advisor


---

# 🌐 External API Integration

AgroPrice integrates with the **Government of India Open Data Platform (data.gov.in)** for mandi price data.

The application uses the **Agmarknet Mandi Price API** to fetch agricultural market information.

API Data Includes:

- Crop Name
- Market Name
- Commodity Prices
- Quality Information
- Market Updates


## Data Flow

```
data.gov.in Agmarknet API

        ↓

Django API Service

        ↓

Data Processing & Validation

        ↓

MongoDB pricehistory Collection

        ↓

Farmer Dashboard & Analytics
```


API is used for:

- Latest mandi price updates
- Historical price storage
- Market comparison
- Price trend analysis
- Crop analytics


---

# 🌐 REST API

AgroPrice APIs are developed using **Django REST Framework (DRF).**

The application provides APIs for:

- Crop Management
- Mandi Price Data
- Historical Price Records
- Market Comparison
- Analytics
- Profit Calculation
- Watchlist Management


---

# 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/crops/` | View Crop List |
| GET | `/api/v1/prices/today/` | Latest Mandi Prices |
| GET | `/api/v1/prices/history/` | Historical Price Data |
| GET | `/api/v1/prices/compare/` | Compare Market Prices |
| POST | `/api/v1/prices/upload-csv/` | Upload CSV Price Data |
| GET | `/api/v1/analytics/trend/` | Price Trend Analysis |
| POST | `/api/v1/analytics/profit/` | Crop Profit Calculation |


---

# 🗄️ Database

AgroPrice uses **MongoDB** as the primary application database.

MongoDB is integrated with Django using **PyMongo**.

Database:

```
agroprice_db
```


Collections:

```
agroprice_db

├── users
├── crops
├── pricehistory
└── contact_messages
```


## Collection Usage

### users

Stores:

- Farmer profile information
- Phone number
- Farm location
- Preferred crops


### crops

Stores:

- Crop name
- Category
- Unit
- Quality grades


### pricehistory

Stores:

- Crop prices
- Market information
- Quality details
- Historical mandi records


### contact_messages

Stores:

- User contact queries
- Submitted messages


Django's built-in authentication system is used for:

- User login
- Admin authentication
- Password management


---

# 📈 Data Visualization

Interactive charts are implemented using **Chart.js**.

Charts included:

- Crop Price Trend Line Chart
- Market Comparison Chart
- Category Wise Price Analysis
- Price Distribution Visualization


---

# 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend | Python, Django |
| API | Django REST Framework |
| Database | MongoDB |
| Authentication Database | PostgreSQL |
| Database Connector | PyMongo |
| External API | Government Open Data API (data.gov.in) |
| Data Visualization | Chart.js |
| Deployment | Render |
| Version Control | Git & GitHub |
| IDE | Visual Studio Code |


---

# 🏗️ Project Architecture

```
AgroPrice

│
├── accounts
│   └── Authentication and Farmer/Admin Profile Management
│
├── crops
│   └── Crop Management System
│
├── prices
│   └── Mandi Price Management and CSV Processing
│
├── analytics
│   └── Trend Analysis and Profit Calculation
│
├── dashboard
│   └── Farmer and Admin Dashboards
│
├── api
│   └── Django REST Framework APIs
│
├── db
│   └── MongoDB Connection and Repository Layer
│
├── core
│   └── Validators and Common Utilities
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

Move into project directory:

```bash
cd AgroPrice
```


---

## 2. Create Virtual Environment

```bash
python -m venv venv
```


Activate Environment:


### Windows

```bash
venv\Scripts\activate
```


---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```


---

## 4. Configure Environment Variables


Create `.env` file:


```
MONGO_URI=your_mongodb_connection_string

DB_NAME=agroprice_db

SECRET_KEY=your_secret_key

DEBUG=True
```


For production:

```
DEBUG=False
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


Open:

```
http://127.0.0.1:8000/
```


---

# 📂 CSV Price Import Format

AgroPrice supports bulk mandi price upload using CSV.


Format:

```
crop_name,market,price,quality,date
```


Example:

```
Tomato,Pune APMC,2500,Grade-A,2026-07-20
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
- Cultivation Cost
- Labour Cost
- Transportation Cost
- Miscellaneous Expenses


---

# 🐍 Python Concepts Implemented

This project demonstrates:

- Object-Oriented Programming
- Classes and Objects
- Exception Handling
- File Handling
- CSV Processing
- Regular Expressions
- DateTime Operations
- MongoDB CRUD Operations
- MongoDB Aggregation Pipeline
- Repository Pattern
- Multithreading


---

# 🚀 Deployment


AgroPrice is deployed using **Render**.


Live Application:

```
https://agroprice.onrender.com/
```


Deployment Architecture:


```
User

 ↓

Render Web Service

 ↓

Django Application

 ↓

PostgreSQL
(Authentication Data)

 ↓

MongoDB Atlas
(Application Data)

 ↓

data.gov.in API
(Mandi Price Data)
```


Deployment includes:

- Django Web Service
- PostgreSQL Database
- MongoDB Atlas
- Gunicorn WSGI Server
- WhiteNoise Static File Handling


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

🌐 **Live Demo**

https://agroprice.onrender.com/

GitHub:

https://github.com/Kalyani132004

---

# 👩‍💻 Developer


**Kalyani Sonawane**

---

⭐ If you like this project, consider giving it a star on GitHub.
