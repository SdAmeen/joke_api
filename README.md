# Jokes API Project

## 📌 Overview
A FastAPI-powered application that fetches jokes from JokeAPI, processes them, and stores them in a SQLite database with comprehensive API endpoints.

## ✨ Features
- 🎭 Fetch jokes from JokeAPI
- 💾 Store jokes in SQLite database
- 🔍 Retrieve and paginate stored jokes
- 🚀 Asynchronous processing
- 🛡️ Data validation and error handling

## 🛠 Technology Stack
- **Framework**: FastAPI
- **Database**: SQLAlchemy with SQLite
- **HTTP Client**: httpx
- **Data Validation**: Pydantic
- **Logging**: Python logging module

## 📦 Project Structure
```
jokes_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application setup
│   ├── database.py         # Database configuration
│   ├── models/             # SQLAlchemy database models
│   │   └── joke.py
│   ├── schemas/            # Pydantic validation models
│   │   └── joke.py
│   └── routes/             # API route handlers
│       └── jokes.py
│
├── requirements.txt
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step-by-Step Setup
1. Clone the repository
   ```bash
   git clone
   cd jokes-api
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Running the Application

### Start the Server
```bash
uvicorn app.main:app --reload
```

### Access Points
- **Swagger UI**: `http://localhost:8000/docs`
- **API Base URL**: `http://localhost:8000/api/v1/jokes`

## 📡 API Endpoints

### 1. Fetch Jokes
- **Endpoint**: `POST /api/v1/jokes/fetch-jokes`
- **Description**: Fetch and store jokes from JokeAPI
- **Parameters**:
  - `num_jokes` (optional, default: 100): Number of jokes to fetch

### 2. Get Jokes
- **Endpoint**: `GET /api/v1/jokes/jokes`
- **Description**: Retrieve stored jokes
- **Parameters**:
  - `skip` (optional, default: 0): Number of jokes to skip
  - `limit` (optional, default: 50): Maximum number of jokes to return

## 🧪 Testing Methods

### 1. Swagger UI
- Navigate to `http://localhost:8000/docs`
- Interactively test API endpoints

### 2. cURL
```bash
# Fetch Jokes
curl -X POST "http://localhost:8000/api/v1/jokes/fetch-jokes"

# Get Jokes
curl "http://localhost:8000/api/v1/jokes/jokes"
```



## 🔍 Key Considerations
- First request might take longer due to API calls
- Jokes are fetched and stored asynchronously
- Internet connection required for JokeAPI access



