## గడులు & గృహాలు | Fortresses & Traditional Homes

A community-driven archive to preserve stories of historic fortresses and traditional homes. The app provides a Streamlit front‑end, optional Google Translate powered bilingual UI (English/తెలుగు), user authentication, AI-assisted story writing, and a FastAPI-style backend expected at `http://127.0.0.1:8000`.

### Project Structure
- `app.py` — Main Streamlit app that connects to the backend API and offers bilingual UI, login/signup, AI story assistant, and Google Maps links.
- `1.py` — Standalone prototype/demo Streamlit app that works without a backend using `stories.json` for sample data.
- `stories.json` — Seed/demo data used by `1.py` and may be updated by submissions in the demo.
- `backend/` — Python backend (FastAPI-style) expected to expose endpoints used by `app.py` (see API section). Environment variables are loaded from `backend/.env`.
- `venv/` — Local virtual environment (optional); you may use your own venv/conda instead.

### Key Features
- **Explore Heritage:** Browse contributed places with images, tags, era, region, contributor info, and quick Google Maps link.
- **Submit a Story:** Add heritage entries with name, type, region/area, era, story, tags, and an image URL.
- **AI Story Assistant:** Optionally generate a story draft from bullet points via backend route `/ai/generate-story`.
- **Accounts:** Signup and login from the Streamlit UI (username/password) against the backend.
- **Bilingual UI:** Toggle English/తెలుగు. Static strings and dynamic content can be translated using Google Cloud Translate (optional).
- **Demo Mode:** `1.py` runs without any backend or external services for quick showcasing.

### Prerequisites
- Python 3.9+ (3.10 recommended)
- Recommended: a virtual environment
- Optional (for translation): Google Cloud project and credentials for Translate API

### Installation
1) Create and activate a virtual environment (or reuse `venv/` if present):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

2) Install dependencies:
```bash
pip install streamlit requests pandas python-dotenv google-cloud-translate
# If running/working on the backend too, you may also need (commonly):
# pip install fastapi uvicorn pydantic
```

3) Environment variables:
- The app loads `.env` from `backend/.env`:
  - Configure any backend-related secrets there (e.g., DB URL, model keys).
- For Google Translate (optional), set the Google credentials file path:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/your/service-account.json"
```

### Running the App
There are two ways to run the front‑end:

#### A) Full App (requires backend)
1) Start the backend server (FastAPI-style). Typical command (adjust if your entry module differs):
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
2) In a separate terminal, run the Streamlit app:
```bash
streamlit run app.py
```
3) Open the URL shown by Streamlit (usually `http://localhost:8501`).

#### B) Demo/Prototype (no backend required)
Run the standalone prototype that uses `stories.json`:
```bash
streamlit run 1.py
```

### How It Works (Front‑end Overview)
- `app.py` reads API base URL from `API_URL = http://127.0.0.1:8000`.
- Loads translations and allows toggling English/తెలుగు. If Google Translate is available, dynamic text (names, era, story) can be translated on the fly.
- Pages:
  - **Explore Heritage:** Fetches places from `GET /places/` and renders cards with images, story, contributor, tags, and a Google Maps link.
  - **Submit a Story:** Submits entries to `POST /places/`. Optional AI assistant calls `POST /ai/generate-story` for drafting.
  - **About the Project:** Static project details.
- Authentication:
  - **Signup:** `POST /users/` with `{"username", "password"}`.
  - **Login:** `POST /login` with form data `username`, `password`.

### Expected Backend API (Minimal)
The front‑end expects endpoints similar to:
- `GET /places/` → List places
- `POST /places/` → Create place (expects fields such as: `name`, `type`, `area`, `region`, `era`, `story`, `tags`, `image_url`, `contributor_username`)
- `POST /users/` → Create user
- `POST /login` → Authenticate user
- `POST /ai/generate-story` → Return `{ "story": str }` from bullet points

Your actual backend may implement additional validation, auth, and persistence. Update `API_URL` in `app.py` if your backend runs elsewhere.

### Configuring Google Cloud Translate (Optional)
`app.py` will attempt to initialize `google.cloud.translate_v2.Client()`.
- Ensure the Translate API is enabled on your GCP project.
- Provide a service account with the Translate permissions and set `GOOGLE_APPLICATION_CREDENTIALS` to its JSON key file.
- If translation initialization fails, the app gracefully falls back to showing original text.

### Troubleshooting
- Backend unreachable: Ensure it’s running on `127.0.0.1:8000` and that CORS, firewalls, or proxies are not blocking requests.
- Translate client error: Verify `GOOGLE_APPLICATION_CREDENTIALS` and API enablement. The app will run without translation if unavailable.
- Streamlit not opening: Check the terminal output for the served URL and copy it into your browser.

### License
This project is provided as-is for educational and cultural preservation purposes. Add an explicit license if you plan to distribute.


