# Flask SerpAPI export + tests

Small Flask app that sends a search query to **SerpAPI** (Google organic results), normalizes items to `title` / `url` / `snippet`, and lets the user **download the results as JSON** (structured, machine-readable — not HTML).

## Features

- Single-page **HTML** form (`GET` / `POST` on `/`)
- **SerpAPI** (`engine=google`, `organic_results` only in code)
- **JSON** download via `Content-Disposition: attachment`
- Validation for empty query; basic error handling for API failures
- **pytest** unit tests with **mocked** `requests` (no live API calls in tests)

## Requirements

- **Python 3.9+**
- Dependencies: `flask`, `requests`, `pytest`

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

## Environment

Create a **SerpAPI** key at [serpapi.com](https://serpapi.com), then set:

**Windows (PowerShell)**

```powershell
$env:SERPAPI_KEY="your_serpapi_key"
```

**macOS / Linux**

```bash
export SERPAPI_KEY="your_serpapi_key"
```

Or use a `.env` file (not committed) and `python-dotenv` if you add it — **never** commit real keys.

## Run locally

```bash
python app.py
```

Open `http://127.0.0.1:5000`, enter a query, submit — browser should download a JSON file.

For development you can use `debug=True` in `app.run`; use **`debug=False`** for any public deployment.

## Tests

```bash
python -m pytest tests/ -v
```

Tests patch `app.requests.get` and assert normalized output and error handling.

## Project layout (example)

```
.
├── app.py
├── requirements.txt
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   └── styles.css
└── tests/
    └── test_app.py
```

Adjust paths to match your repo.

## Deploy (optional)

Free tiers (e.g. **Render**) often **sleep** when idle; first request after sleep can be slow. Use **Gunicorn** on Linux, bind to `$PORT`, set `SERPAPI_KEY` in the host’s environment. See your provider’s Flask/Python guide.

## License

## Acknowledgements

- Search results via [SerpAPI](https://serpapi.com) (not the official Google Custom Search API).
