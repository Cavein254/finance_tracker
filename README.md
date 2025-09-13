# 📈 Commodities API

A Django REST Framework (DRF) project for managing commodities, fetching their price history from [Yahoo Finance](https://finance.yahoo.com/) via `yfinance`, and handling user authentication.  
The project uses **Celery** for background tasks and **PostgreSQL** for persistence.  

---

## 🚀 Features

### 📊 Commodities
- `GET /commodities/` → List all commodities  
- `POST /commodities/` → Create a new commodity  
- `GET /commodities/{id}/` → Retrieve a commodity by ID  
- `PUT /commodities/{id}/` → Update a commodity  
- `PATCH /commodities/{id}/` → Partially update a commodity  
- `DELETE /commodities/{id}/` → Delete a commodity  
- `GET /commodities/{symbol}/prices/` → Retrieve commodity prices (from DB or Yahoo Finance, with Celery fetching historical data in the background)

### 👤 Users
- `POST /users/register/` → Register a new user  
- `POST /users/login/` → Log in and receive an auth token  
- `GET /users/me/` → Retrieve the authenticated user  

---

## 🛠️ Tech Stack

- **Backend:** [Django](https://www.djangoproject.com/) + [Django REST Framework](https://www.django-rest-framework.org/)  
- **Task Queue:** [Celery](https://docs.celeryq.dev/)  
- **Data Source:** [yfinance](https://github.com/ranaroussi/yfinance)  
- **Database:** [PostgreSQL](https://www.postgresql.org/)  
- **Containerization:** [Docker](https://www.docker.com/)  

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/commodities-api.git
cd commodities-api
```

---
### 2️⃣ Environment variables
Create a .env file in the root directory:

```bash
# PostgreSQL
DATABASE_URL=postgresql://myuser:mypassword@db:5432/mydb
DB_SSL_REQUIRED=False

# Celery broker (example using Redis)
CELERY_BROKER_URL=redis://redis:6379/0
```


### 3️⃣ Run with Docker Compose
```bash
docker compose up --build
```

This will start:

- django → API server

- db → PostgreSQL

- celery_worker → background task worker
  
- rabbitmq → message queue

### 4️⃣ Run migrations
```bash
docker compose exec django python manage.py migrate
```

---

## 🧪 API Usage
### Example: Get all commodities
```bash
curl -X GET http://localhost:8000/api/v1/commodities/AAPL/prices/ -H "accept: application/json"
```
```json
[
  {
    "id": 1,
    "name": "aapl",
    "symbol": "AAPL",
    "description": "Auto-created commodity for aapl",
    "unit": "unit",
    "commodity_type": "ALTERNATIVE",
    "price": 234.07,
    "updated_at": "2025-09-13T06:55:38.640950Z",
    "latest_price_history": {
      "id": 1256,
      "date": "2025-09-12",
      "open": "229.22",
      "high": "234.51",
      "low": "229.02",
      "close": "234.07",
      "volume": 55776500,
      "commodity": 1
    }
  },
...
]
```
### Example: Login user
```bash
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "strongpassword"}'
```
```json
{
  "token": "11fbaafefa742e30bda55ded308c0ec6bf53f71c",
  "email": "user@example.com"
}
```
### ⚙️ Background Tasks
When fetching commodity prices not found in the DB, the app:

- Fetches current prices from Yahoo Finance.

- Enqueues a Celery task to fetch & persist up to 5 years of historical data.

## 📖 API Documentation (Swagger / ReDoc)
The project comes with interactive API documentation:

Swagger UI → [http://localhost:8000/api/v1/swagger/](http://localhost:8000/api/v1/swagger/)

ReDoc → [http://localhost:8000/api/v1/redoc/](http://localhost:8000/api/v1/redoc/)

## 📜 License
MIT License.
Feel free to fork and contribute 🚀

## ✨ Future Improvements
- JWT-based authentication

- User portfolio tracking

- WebSocket live price updates

