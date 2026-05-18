# 🎵 Resonance

A Spotify-connected music analytics and recommendation platform focused on ingesting listening-history data, generating personalized recommendation playlists, and visualizing user listening behavior through a backend-first architecture.

This project was intentionally designed to emphasize:

- OAuth authentication flows
- backend service architecture
- PostgreSQL data modeling
- recommendation system logic
- API integration workflows
- frontend/backend coordination

---

## Current Status

**Portfolio MVP/Local Development Complete**

Core functionality currently works locally:

- Spotify OAuth authentication
- Token refresh + encrypted token persistence
- Top tracks + top artists ingestion
- PostgreSQL persistence layer
- Recommendation generation pipeline
- Recommendation dashboard frontend
- Playlist export workflow (partial)

Spotify Playlist creation succeeds, but Spotify currently returns intermittent `403 Forbidden` responses during playlist track insertion for some developer applications despite valid OAuth scopes and playlist ownership.


---

## Demo Media

**Dashboard Overview**

![Dashboard Overview](assets/dashboard-overview.gif)

**Spotify Login Flow**

![Spotify Login Flow](assets/spotify-oauth-flow.gif)

**Recommendation Playlist Output**

![Recommendation Playlist](assets/recommendation-playlist.gif)

**API Documentation**

![Swagger Docs](assets/swagger-docs-v2.gif)

---

## Features

- **Spotify OAuth Authentication**
  - Spotify login integration
  - Access + refresh token handling
  - Automatic token refresh window
  - Secure token persistence

- **Listening History Ingestion**
  - User top tracks ingestion
  - User top artists ingestion
  - Historical ranking persistence
  - Artist metadata + genres storage

- **Recommendation Engine**
  - Personalized recommendation generation
  - Artist similarity scoring
  - Listening-history ranking logic
  - Recommendation explainability output
  - Deterministic recommendation ordering

- **Frontend Dashboard**
  - Top-track dashboard visualization
  - Generated recommendation playlist
  - Album artwork rendering
  - Recommendation score + reasoning display

- **Spotify Playlist Export Workflow**
  - Playlist creation support
  - Spotify URI conversion pipeline
  - Export endpoint implementation
  - Playlist modification flow partially blocked by Spotify API restrictions

---

## Architecture Overview
```txt
Spotify OAuth + Web API
            ↓
FastAPI Backend Services
            ↓
Recommendation + Ingestion Layer
            ↓
PostgreSQL Database
            ↓
Next.js Frontend Dashboard
```
---

## Recommendation Strategy

The current MVP recommendation engine intentionally avoids relying on Spotify recommendation endpoints due to Spotify API access restrictions affecting newer developer applications.

Instead, recommendation are generated internally using the following strategy:

- Spotify tracks ranked `1-10` become the user's strongest taste-profile signals
- Tracks ranked `11-50` become recommendation candidates
- Candidate tracks are scored based on:
    - artist overlap
    - listening-history ranking proximity
    - stored listening metadata

This approach keeps recommendation generation fully backend-controlled and deterministic.
## Developer Contributions

This project was independently designed and implemented with a strong emphasis on backend engineering and API integration workflows:

- Designed a PostgreSQL relational schema to model:
    - users
    - Spotify tokens
    - tracks
    - artists
    - historical listening rankings
    - recommendation outputs
- Built a FastAPI backend supporting:
    - OAuth authentication flows
    - token refresh handling
    - ingestion workflows
    - recommendation endpoints
    - playlist export workflows
- Implemented Spotify ingestion services that:
    - normalize Spotify API responses
    - persist relational listening-history data
    - maintain historical ranking snapshots
- Built a recommendation engine that:
    - separates user taste-profile tracks from recommendation candidates
    - generates weighted recommendation scores
    - produces explainable recommendation reasoning
- Implemented frontend/backend integration through:
    - typed API requests
    - frontend loading/error handling
    - dashboard rendering of recommendation outputs
- Structured the project around:
    - service-layer separation
    - reusable API communication patterns
    - environment-based configuration
    - deployment-oriented architecture conventions


---

## Technologies and Tools Used

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Spotify Web API**
- **OAuth 2.0**
- **Next.js / React**
- **TypeScript**
- **Axios**
- **JWT-style token workflows**
- **Git/GitHub**

---

## Assumptions & Limitations

Spotify has significantly restricted access to several recommendation--related API endpoints for newer developer applications, including:
- audio features
- recommendation endpoints
- some playlist modification workflows

Because of these platform limitations:
- recommendation logic is generated internally rather than through Spotify recommendations
- audio-feature-based recommendation scoring is currently disabled
- playlist creation succeeds, but playlist track insertion may return intermittent `403 Forbidden` responses depending on Spotify developer application permissions

The project therefore focuses primarily on:
- backend architecture
- ingestion workflows
- recommendation system design
- OAuth/API integration patterns

rather than production-scale Spotify deployment.

---
## Project Structure
```
.
├── backend/
│   ├── app/
│   │   ├── db/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── services/
│   │   └── components/
│   │
│   ├── package.json
│   └── next.config.ts
│
└── README.md
```
---

## How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/hjlinto/resonance-music-engine

```
2. Set up the backend
```bash
cd backend
python -m venv venv
source .venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. Configure environment variables
```bash
DATABASE_URL=your_database_url
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/auth/spotify/callback
```
4. Run database setup and start the API
```bash
uvicorn app.main:app --reload
```
5. Start the frontend
```bash
cd ../frontend
npm install
npm run dev
```
6. Open:
- Frontend: http://localhost:3000
- Swagger Docs: http://127.0.0.1:8000/docs
---
## Reflections

- Spotify API restrictions significantly influenced recommendation-system architecture decisions during development.
- Building an internally controlled recommendation pipeline became more maintainable than depending on deprecated or restricted Spotify recommendation endpoints.
- If continuing development beyond the MVP stage, I would likely:
    - integrate third-party listening-history providers
    - support user-uploaded Spotify export data
    - build a fully custom recommendation engine independent of Spotify recommendation APIs
    - expand recommendation scoring with clustering and vector-based similarity approaches
    - add asynchronous ingestion/background jobs for large listening-history imports
---
## Author

Created by **Hunter J. Linton**
