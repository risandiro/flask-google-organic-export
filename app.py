import os
import requests
import json

from flask import Flask, render_template, request, Response

# Vytvoření flask aplikace
app = Flask(__name__)

# Automatické znovunačítání šablon bez nutnosti restartovat server
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Nastavení API
SERPAPI_URL = "https://serpapi.com/search"
SERPAPI_KEY = os.environ["SERPAPI_KEY"]

@app.route("/", methods=["GET", "POST"])
def index():
    # Když user odešle form
    if request.method == "POST":
    
        # Získej dotaz z formu a uisti se že pole není prázdný
        query = (request.form.get("query") or "").strip()
        if not query:
            return render_template("index.html", error="Pole nesmí být prázdný."), 400

        # Získej výsledky vyhledávaní a uisti se zda SerpAPI funguje
        try:
            results = fetch_first_page_results(query)
        except Exception as e:
            return render_template("index.html", error=str(e)), 502

        # Převeď do json a následně zakóduj na bajty pro response
        body = json.dumps(results, ensure_ascii=False, indent=2).encode("utf-8")

        return Response(
            body,
            mimetype="application/json; charset=utf-8",
            headers={"Content-Disposition": 'attachment; filename="vysledek_hledani.json"'},
        )

    # Když user otevře stránku
    else:
        return render_template("index.html")


def fetch_first_page_results(query: str, num: int = 10) -> list[dict]:
    # Vyhledaj klíčové slovní spojení v googlu a scrapni prvných 10 výsledkú
    r = requests.get(
        SERPAPI_URL,
        params={
            "engine": "google",
            "api_key": os.environ["SERPAPI_KEY"],
            "q": query,
            "num": min(num, 10)
        },
        timeout=30,
    )

    # Ověř, že HTTP odpověď je úspěšná
    r.raise_for_status()

    # Převeď json odpověď na dict + skontroluj jesli HTTP neprošlo s errorem
    data = r.json()
    if data.get("error"):
        raise RuntimeError(data["error"])

    # Normalizuj data na přehlednejší strukturu
    results = []
    for item in data.get("organic_results") or []:
        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet"),
        })
    return results


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)