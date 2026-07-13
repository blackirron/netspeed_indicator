# Netspeed Indicator

Forked from the sprint's base FastAPI template.

---

## Netspeed Indicator

**What it does:** A live browser widget showing your current download and
upload throughput, with a scrolling oscilloscope-style trace of recent
samples. Runs a real timed download/upload against its own backend every
time you hit "Run test" (or leave "Auto" on for a reading every 10s).

**Why it exists:** A quick, always-open tab that tells you if your current
connection is actually the bottleneck before you blame your app/router/wifi.

**Live demo:** [link once deployed]

**Note:** this app does NOT use the Claude API — `ANTHROPIC_API_KEY` in
`.env` can be left blank.

---

## Running locally

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your environment variables
cp .env.example .env
# then edit .env and paste your real ANTHROPIC_API_KEY

# 4. Run the dev server (auto-reloads on code changes)
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` — FastAPI auto-generates an interactive
API tester here. This is the fastest way to try your endpoints without
building a frontend first.

## Running with Docker

```bash
docker build -t my-app .
docker run -p 8000:8000 --env-file .env my-app
```

## Project structure

```
app/
├── core/       config + auth
├── routers/    HTTP endpoints (thin — no logic)
├── services/   actual logic (Claude API calls, etc.)
└── main.py     wires it together
```

## Adding a new feature to this app

1. Create `app/services/your_feature.py` — the actual logic
2. Create `app/routers/your_feature.py` — request/response models + thin endpoint (copy `chat.py`'s pattern)
3. Register it in `app/main.py`: `app.include_router(your_feature.router)`

## Deployment

Deployed on: [Railway / Render / Fly.io — fill in]

Environment variables to set on the platform dashboard:
- `ANTHROPIC_API_KEY`
- `API_AUTH_TOKEN`
- `ENVIRONMENT=production`
- `ALLOWED_ORIGINS` (your frontend's real URL)
