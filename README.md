# Flask SerpAPI export + testy

Malá Flask aplikace, která odešle vyhledávací dotaz do **SerpAPI** (organické výsledky Google), znormalizuje položky na `title` / `url` / `snippet` a uživateli umožní **stáhnout výsledky jako JSON** (strukturovaný, strojově čitelný formát.

## Funkce

- Jednostránkový **HTML** formulář (`GET` / `POST` na `/`)
- **SerpAPI** (`engine=google`, v kódu jen `organic_results`)
- Stažení **JSON** přes hlavičku `Content-Disposition: attachment`
- Kontrola prázdného dotazu; základní ošetření chyb z API
- Jednotkové testy **pytest** s **namockovaným** `requests` (v testech žádné živé volání API)

## Živá ukázka

**[https://flask-serpapi-export-tests.onrender.com](https://flask-serpapi-export-tests.onrender.com)**

Běží na bezplatné úrovni [Render.com](https://render.com): služba se po době nečinnosti **uspí**. **První požadavek po uspání** může trvat **desítky sekund až zhruba minutu**, než se instance probudí — obnovte stránku nebo počkejte, pak aplikaci používejte jako obvykle.

## Požadavky

- **Python 3.9+**
- Závislosti: `flask`, `requests`, `pytest`

## Nastavení

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

## Prostředí (proměnné)

Vytvořte klíč **SerpAPI** na [serpapi.com](https://serpapi.com) a nastavte:

**Windows (PowerShell)**

```powershell
$env:SERPAPI_KEY="your_serpapi_key"
```

**macOS / Linux**

```bash
export SERPAPI_KEY="your_serpapi_key"
```

Nebo použijte soubor `.env` (nepatří do repozitáře) a případně `python-dotenv` — **nikdy** necommitujte skutečné klíče.

## Lokální spuštění

```bash
python app.py
```

V `app.run(...)` nastavte **`host="127.0.0.1"`** (nebo `"localhost"`), aby Flask naslouchal jen na vašem počítači a sedělo to s URL níže. Pokud použijete **`host="0.0.0.0"`** (např. pro **Render.com**), otevřete URL služby od poskytovatele, ne `127.0.0.1`.

Otevřete `http://127.0.0.1:5000`, zadejte dotaz, odešlete — prohlížeč by měl stáhnout JSON soubor.

Pro vývoj můžete v `app.run` použít `debug=True`; u **veřejného nasazení** použijte **`debug=False`**.

## Testy

```bash
python -m pytest tests/ -v
```

Testy patchují `app.requests.get` a kontrolují normalizovaný výstup a ošetření chyb.

## Rozložení projektu

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
