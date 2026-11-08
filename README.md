# House Plants Fullstack App

A full-stack web application for browsing house plants: a React frontend that talks to a FastAPI backend, which in turn fetches data from the external House Plants API (RapidAPI).

## Features

- Browse a list of house plants (Latin name, family, categories)
- Search and filter the list
- View full details for a single plant
- Clear error handling with meaningful HTTP status codes
- Backend unit tests with mocked external API calls

## Tech Stack

**Frontend:** React 18 (Hooks), React Router, Axios, custom responsive CSS

**Backend:** Python, FastAPI, Requests, Pytest

**External API:** [House Plants API](https://rapidapi.com) on RapidAPI

## Project Structure

```
house-plant-app/
├── plant-backend/
│   ├── main.py            # FastAPI app: /plants/ and /plants/{plant_id}
│   ├── test_main.py       # Pytest unit tests (external API is mocked)
│   └── .env.example       # Required environment variables
├── src/
│   ├── App.js             # Routing
│   └── plant-frontend/
│       ├── plantTable.jsx # Plant list with search and filter
│       └── plantDetail.jsx# Single plant details
├── public/
└── package.json
```

## API Endpoints

| Method | Path                 | Description                          |
|--------|----------------------|--------------------------------------|
| GET    | `/plants/`           | Simplified data for all plants       |
| GET    | `/plants/{plant_id}` | Full data for a single plant         |

Status codes: `200` success, `204` no content, `400` bad request, `404` not found, `500` / `503` server or connection errors.

## Getting Started

### 1. Backend

```bash
cd plant-backend
pip install fastapi uvicorn requests pytest httpx
cp .env.example .env      # then put your RapidAPI key in .env
py main.py                # runs on http://localhost:8001
```

### 2. Frontend

From the project root:

```bash
npm install
npm start                 # runs on http://localhost:3000
```

### 3. Tests

```bash
cd plant-backend
py -m pytest test_main.py -v
```

## Notes

- The RapidAPI key is read from an environment variable (`RAPIDAPI_KEY`) and is never committed.
- Development time: about 9–10 hours.
- Tools used during development: ChatGPT (GPT-4), Amazon Q.
