# GitHub Webhook Receiver System

A real-time GitHub webhook receiver application that captures repository events (Push, Pull Request, Merge) and displays them in a live-updating dashboard. Built with Flask, MongoDB, and a modern JavaScript frontend.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Implementation Details](#implementation-details)
- [Development Setup](#development-setup)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)

## Project Overview

This application serves as a webhook receiver for GitHub repositories. When configured as a webhook endpoint in a GitHub repository, it:

1. **Receives** webhook events from GitHub for Push, Pull Request, and Merge actions
2. **Validates** incoming requests using HMAC SHA-256 signature verification
3. **Processes** and normalizes the webhook payload data
4. **Stores** the processed events in MongoDB (configured as a timeseries collection)
5. **Displays** the events in a real-time dashboard that auto-refreshes every 15 seconds

## Architecture

```
┌─────────────────┐      ┌──────────────────────────────────────────────────┐
│                 │      │                 Flask Application                 │
│     GitHub      │      │  ┌────────────┐   ┌────────────┐   ┌──────────┐  │
│   Repository    │──────▶  │  Webhook   │──▶│  Services  │──▶│ Database │  │
│                 │      │  │    API     │   │   Layer    │   │  Layer   │  │
└─────────────────┘      │  └────────────┘   └────────────┘   └──────────┘  │
                         │        │                                 │        │
                         │        ▼                                 ▼        │
                         │  ┌────────────┐                  ┌──────────────┐ │
                         │  │  Schema    │                  │   MongoDB    │ │
                         │  │ Validation │                  │ (Timeseries) │ │
                         │  │ (Pydantic) │                  └──────────────┘ │
                         │  └────────────┘                                   │
                         └──────────────────────────────────────────────────┘
                                           │
                                           ▼
                         ┌──────────────────────────────────────────────────┐
                         │              Frontend Dashboard                   │
                         │  ┌────────────────────────────────────────────┐  │
                         │  │  • Real-time event display                 │  │
                         │  │  • Auto-refresh every 15 seconds           │  │
                         │  │  • Polling with since parameter for        │  │
                         │  │    incremental updates                     │  │
                         │  └────────────────────────────────────────────┘  │
                         └──────────────────────────────────────────────────┘
```

## Project Structure

```
webhook-repo/
├── app/                          # Main application package
│   ├── __init__.py               # Flask app factory, blueprint registration
│   ├── api/                      # API endpoint handlers
│   │   ├── webhook.py            # POST /webhook/receiver - receives GitHub events
│   │   └── github.py             # GET /github/events - retrieves stored events
│   ├── core/                     # Core utilities and configuration
│   │   ├── config.py             # Environment-based configuration class
│   │   └── utils/
│   │       └── validate_headers.py  # HMAC signature validation
│   ├── database/                 # Database layer
│   │   ├── database.py           # MongoDB client and collection setup
│   │   └── github_model.py       # TypedDict models and Action enum
│   ├── error/                    # Custom exception classes
│   │   └── webhook.py            # InvalidSignatureError exception
│   ├── schema/                   # Pydantic models for data validation
│   │   └── webhook.py            # Push, Pull Request, Merge payload schemas
│   └── services/                 # Business logic layer
│       ├── webhook.py            # Stores webhook data to MongoDB
│       └── github.py             # Retrieves events from MongoDB
├── static/                       # Static frontend files
│   └── github.html               # Real-time event dashboard
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── DockerFile                    # Docker image configuration
├── docker-compose.yml            # Multi-container Docker setup
└── .env                          # Active environment configuration
```

## Tech Stack

| Component       | Technology                                           |
|-----------------|------------------------------------------------------|
| **Backend**     | Python 3.13, Flask 3.1.2                             |
| **Database**    | MongoDB (PyMongo 4.16.0) with Timeseries Collection  |
| **Validation**  | Pydantic 2.12.5                                      |
| **CORS**        | Flask-CORS 6.0.2                                     |
| **Frontend**    | Vanilla JavaScript, HTML5, CSS3                      |
| **Containers**  | Docker, Docker Compose                               |

## Implementation Details

### 1. Webhook Receiver (`app/api/webhook.py`)

The webhook receiver endpoint handles incoming GitHub webhook events:

```python
@webhook.route('/receiver', methods=["POST"])
async def receiver():
    # 1. Extract and validate HMAC signature
    sign = request.headers.get("X-Hub-Signature-256")
    validate_webhook(request.get_data(), sign)
    
    # 2. Determine event type from GitHub headers
    action = request.headers.get("X-GitHub-Event")
    
    # 3. Parse payload based on content type
    # Supports both application/json and application/x-www-form-urlencoded
    
    # 4. Route to appropriate handler based on action type
    if action == "push":
        # Handle push events
    elif action == "pull_request":
        # Check if merged or just opened/closed
```

**Key Features:**
- **Signature Validation**: Uses HMAC SHA-256 to verify webhook authenticity
- **Content-Type Handling**: Supports both JSON and form-urlencoded payloads
- **Action Detection**: Distinguishes between Push, Pull Request, and Merge events

### 2. Signature Validation (`app/core/utils/validate_headers.py`)

Implements GitHub's webhook signature verification:

```python
def validate_webhook(payload_body, hash_sign: str):
    hash_object = hmac.new(
        config.github_secret.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    if not hmac.compare_digest(expected_signature, hash_sign):
        raise InvalidSignatureError(message="invalid signature", status_code=401)
```

### 3. Data Models and Schema Validation (`app/schema/webhook.py`)

Pydantic models ensure type-safe data handling:

- **`WebhookPayload`** (alias: `PushWebhookPayload`): Validates push event payloads
- **`PullRequestWebhookPayload`**: Validates pull request and merge event payloads
- **Nested Models**: `User`, `Repository`, `Commit`, `PullRequest`, etc.

### 4. Database Layer (`app/database/database.py`)

MongoDB setup with **Timeseries Collection** for optimized time-based queries:

```python
class Database:
    def __init__(self, host: str, port: int):
        client = MongoClient(host=host, port=port)
        db = client["github_database"]
        try:
            db.create_collection(
                "github",
                timeseries={"timeField": "timestamp"}
            )
        except CollectionInvalid:
            pass  # Collection already exists
        self.github_collection = db["github"]
```

**Stored Document Schema** (`app/database/github_model.py`):

```python
class GitHub(TypedDict):
    request_id: str      # Commit ID or PR ID
    author: str          # User who performed the action
    action: Action       # PUSH, PULL_REQUEST, or MERGE
    from_branch: str     # Source branch
    to_branch: str       # Target branch
    timestamp: str       # ISO format timestamp
```

### 5. Service Layer (`app/services/webhook.py`)

Handles data transformation and storage:

```python
class WebhookService:
    @staticmethod
    async def store_data(data, action: Action):
        if action == Action.push:
            db.insert_one(GitHub(
                action=action.value,
                request_id=data.head_commit.id,
                author=data.head_commit.author.name,
                from_branch=data.ref.replace("refs/heads/", ""),
                to_branch=data.ref.replace("refs/heads/", ""),
                timestamp=data.head_commit.timestamp
            ))
        # Similar handling for pull_request and merge...
```

### 6. Event Retrieval (`app/services/github.py`)

Supports pagination and incremental updates:

```python
class GithubService:
    @staticmethod
    async def git_github_data(since: str | None):
        if since is None:
            # Initial load: Get latest 50 events
            data = list(db.find().sort("_id", -1).limit(50))
        else:
            # Incremental: Get events newer than 'since' ID
            data = list(db.find({
                "_id": {"$gt": ObjectId(since)}
            }).sort("_id", 1))
```

### 7. Frontend Dashboard (`static/github.html`)

Modern, responsive UI with real-time updates:

- **Auto-refresh**: Polls every 15 seconds using incremental updates
- **Event Cards**: Color-coded by action type (Push=Green, PR=Blue, Merge=Purple)
- **Optimized Polling**: Uses `since` parameter to fetch only new events
- **Timestamp Formatting**: Displays in IST with ordinal suffixes

## Development Setup

### Prerequisites

- Python 3.13+
- MongoDB 6.0+
- Docker & Docker Compose (for containerized setup)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd webhook-repo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # OR
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy the local environment template:
   ```bash
   cp .env.local .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   PORT=5000
   DATABASE_HOST="localhost"
   DATABASE_PORT=27017
   REDIS_HOST="localhost"
   REDIS_PORT=6379
   GITHUB_SECRET=your_github_webhook_secret
   ```

5. **Start MongoDB locally**
   ```bash
   # Using MongoDB installed locally
   mongod --dbpath /path/to/data
   
   # OR using Docker
   docker run -d -p 27017:27017 --name mongo_local mongo
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the dashboard**
   - Open `http://localhost:5000/static/github.html` in your browser

### Docker Setup

The project includes a complete Docker Compose configuration for running all services.

1. **Configure Docker environment**
   ```bash
   cp .env.docker .env
   ```
   
   The Docker environment uses container hostnames:
   ```env
   PORT=5000
   DATABASE_HOST="mongo"
   DATABASE_PORT=27017
   REDIS_HOST="redis"
   REDIS_PORT=6379
   GITHUB_SECRET=your_github_webhook_secret
   ```

2. **Build and start containers**
   ```bash
   docker-compose up --build
   ```
   
   This starts three services:
   - `github-webhook`: Flask application (port 5000)
   - `mongo`: MongoDB database (port 27017)
   - `redis`: Redis cache (port 6379)

3. **Access the application**
   - Dashboard: `http://localhost:5000/static/github.html`
   - Webhook endpoint: `http://localhost:5000/webhook/receiver`

4. **Stop containers**
   ```bash
   docker-compose down
   ```
   
   To remove volumes as well:
   ```bash
   docker-compose down -v
   ```

### Configuring GitHub Webhook

1. Go to your GitHub repository → Settings → Webhooks → Add webhook
2. **Payload URL**: `https://your-domain.com/webhook/receiver`
3. **Content type**: `application/json`
4. **Secret**: Same value as `GITHUB_SECRET` in your `.env`
5. **Events**: Select "Let me select individual events"
   - ✅ Pushes
   - ✅ Pull requests

## API Endpoints

### POST `/webhook/receiver`

Receives GitHub webhook events.

**Headers Required:**
- `X-Hub-Signature-256`: HMAC signature for validation
- `X-GitHub-Event`: Event type (`push` or `pull_request`)

**Response:**
- `200`: Event processed successfully
- `400`: Invalid payload
- `409`: Missing required headers
- `500`: Processing error

---

### GET `/github/events`

Retrieves stored GitHub events.

**Query Parameters:**
- `since` (optional): ObjectId of the last event. Returns only newer events.

**Response:**
```json
{
  "data": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "action": "PUSH",
      "author": "john_doe",
      "from_branch": "feature/login",
      "to_branch": "feature/login",
      "timestamp": "2026-01-29T10:30:00Z",
      "request_id": "abc123"
    }
  ]
}
```

## Environment Variables

| Variable         | Description                          | Example              |
|------------------|--------------------------------------|----------------------|
| `PORT`           | Application port                     | `5000`               |
| `DATABASE_HOST`  | MongoDB host                         | `localhost` / `mongo`|
| `DATABASE_PORT`  | MongoDB port                         | `27017`              |
| `REDIS_HOST`     | Redis host (future use)              | `localhost` / `redis`|
| `REDIS_PORT`     | Redis port (future use)              | `6379`               |
| `GITHUB_SECRET`  | Webhook secret for HMAC validation   | `your_secret_key`    |

---

## License

This project is developed as an assignment/assessment project.
