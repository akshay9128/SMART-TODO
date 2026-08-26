# SMART TODO

An AI-powered personal TODO assistant built with **FastAPI**. You talk to it in plain English (or voice), and it creates, lists, updates, completes, and deletes tasks. It also reminds you when something is due, remembers preferences like reminder time, and can set up repeating tasks.

This is a backend API (no web UI yet). You can try it from Swagger, any HTTP client, or the included microphone script.

---

## What it does

- **Natural-language task control** — say *“add a work task to submit the report tomorrow at 5 pm high priority”* instead of filling forms
- **CRUD task API** — title, category, priority (`low` / `medium` / `high`), due time, completed flag
- **Auth** — register, login (JWT), and user-scoped tasks
- **Reminders** — background scheduler checks due tasks and writes notifications
- **Recurring tasks** — daily / weekly phrases like *every day* or *every Monday* spawn the next occurrence after a reminder fires
- **User memory** — store preferences (for example preferred reminder time) and reuse them when creating tasks
- **Voice** — `voice.py` listens on your mic, transcribes speech, and sends the text to the agent
- **Conflict check** — creating a task at the same due time as an existing incomplete task asks for confirmation
- **Delete confirmation** — deleting through the agent requires an extra confirm step

The “AI” layer is a **rule-based NLP agent** (`TaskAgent`): keyword intents plus regex for dates, times, priority, category, and task IDs. It is not an LLM.

---

## Tech stack

| Area | Choice |
|------|--------|
| API | FastAPI, Uvicorn, Pydantic |
| Database | SQLite (`todo.db`) + SQLAlchemy 2.0 |
| Migrations | Alembic |
| Auth | JWT (`PyJWT`), password hashing (`pwdlib`) |
| Scheduler | APScheduler |
| Voice client | SpeechRecognition + microphone |

---

## Project structure

```
AI-TODO/
├── app/
│   ├── agents/          # Natural-language intent parser
│   ├── core/            # Config, auth, security, logging
│   ├── database/        # Engine, session, table create
│   ├── models/          # Task, User, Notification, UserMemory
│   ├── routers/         # HTTP endpoints
│   ├── schemas/         # Request / response models
│   ├── services/        # Agent, memory, reminders, confirmation
│   └── utils/           # Date, time, and recurrence parsers
├── alembic/             # Schema migrations
├── run.py               # Dev server entry
├── voice.py             # Mic → login → /agent/
└── requirements.txt
```

---

## Getting started

### Prerequisites

- Python 3.11+
- A microphone if you want to use `voice.py`
- Windows, macOS, or Linux

### Install

```bash
git clone https://github.com/akshay9128/SMART-TODO.git
cd SMART-TODO

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Tables are created automatically on startup (`create_database()`). You can also apply Alembic migrations if you prefer that workflow:

```bash
alembic upgrade head
```

### Run the API

```bash
python run.py
```

Server: [http://127.0.0.1:8000](http://127.0.0.1:8000)

| URL | Purpose |
|-----|---------|
| `/` | Welcome + version |
| `/health` | Health check |
| `/docs` | Swagger UI |
| `/redoc` | ReDoc |

---

## Auth flow

1. **Register** — `POST /users/`

```json
{
  "username": "akshay",
  "email": "akshay@example.com",
  "password": "your-password"
}
```

2. **Login** — `POST /users/login` (OAuth2 form: `username` + `password`)

Returns `access_token`. Send it as:

```
Authorization: Bearer <token>
```

3. **Current user** — `GET /users/me`

Protected routes: `/tasks`, `/agent`, `/notifications`, `/memory`.

---

## Talking to the agent

`POST /agent/` with JSON:

```json
{
  "text": "add a work task to finish the assignment tomorrow at 6 pm high priority",
  "confirmed": false
}
```

### Intents

| Intent | Example phrases |
|--------|-----------------|
| Create | *create*, *add*, *make* |
| List | *show*, *list*, *display* |
| Update | *update*, *change*, *rename*, *edit* |
| Complete | *complete*, *finish*, *done* |
| Delete | *delete*, *remove* |

### Useful phrases

```
Add a personal task to call mom tomorrow at 7 pm
Create a high priority work task to review PRs today at 3 pm
Add a study task to revise notes every day at 8 am
Show my tasks
Complete task 12
Update task 12 to low priority
Delete task 12
```

Relative dates: `today`, `tomorrow`, weekdays. Times: `3 pm`, `15:00`. Categories: `work`, `personal`, `study`, `health`. Recurrence: `every day` / `everyday` / `daily`, `every week` / `weekly`, `every Monday`.

Deletes and some scheduling conflicts need a second call with `"confirmed": true`.

---

## REST APIs (summary)

**Tasks** (`/tasks`)

- `POST /` — create
- `GET /` — list (optional query: `category`, `priority`, `completed`)
- `GET /{id}` — one task
- `PUT /{id}` — update
- `DELETE /{id}` — delete

**Notifications** (`/notifications`)

- `GET /` — list (newest first)
- `PATCH /{id}/read` — mark read

**Memory** (`/memory`)

- `POST /` — save a key/value memory
- `GET /` — list
- `GET /{id}`, `PUT /{id}`, `DELETE /{id}`
- `POST /preferred-reminder-time` — e.g. `{ "time": "8 pm" }`

When a preferred reminder time is stored, new tasks with a due date can get `reminder_at` from that preference.

---

## Reminders and recurrence

APScheduler runs every **10 seconds**:

1. Find incomplete tasks whose `reminder_at` is due and not yet reminded
2. Print a console reminder and insert a `Notification`
3. If the task is recurring, insert the **next** occurrence (daily = +1 day, weekly = +7 days) with the same reminder offset

---

## Voice client

With the API running:

1. Register a user, then set `USERNAME` and `PASSWORD` at the top of `voice.py`
2. Set `DEVICE_INDEX` to your microphone (the script prints devices on error)
3. Run:

```bash
python voice.py
```

It logs in, listens, transcribes with Google Speech Recognition, and posts to `/agent/`. If the agent asks to confirm a delete, speak *yes*, *confirm*, or *delete it*.

---

## Configuration

- App name / version: `app/core/config.py` (optional `.env` via `pydantic-settings`)
- SQLite URL: `app/database/connection.py` (`sqlite:///todo.db`)
- JWT secret: `app/core/security.py` — change `SECRET_KEY` before any real deployment

`.env`, `todo.db`, `.venv/`, `uploads/`, and audio dumps are gitignored.

---

## Status

Personal learning project: FastAPI backend, SQLAlchemy, JWT, a scheduler, and a small NLP + voice loop. Next natural steps would be a frontend, env-based secrets, and swapping or augmenting the rule-based agent with a real LLM if you want broader language understanding.
