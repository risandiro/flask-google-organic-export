import os
import pytest
from unittest.mock import MagicMock, patch

# Pokud v prostředí chybí SERPAPI_KEY, nastav testovací placeholdr.
os.environ.setdefault("SERPAPI_KEY", "test-key")

@patch("app.requests.get")
def test_fetch_vystup_normalizovany(mock_get):
    """Ověř normalizaci organic_results na title, url, snippet (link -> url)."""

    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = { # prototyp očekávaných dat
        "organic_results": [
            {"title": "Titulek", "link": "https://example.com", "snippet": "Úryvek"},
        ],
    }
    mock_get.return_value = mock_resp

    from app import fetch_first_page_results
    out = fetch_first_page_results("query")
    assert out == [
        {"title": "Titulek", "url": "https://example.com", "snippet": "Úryvek"},
    ]
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["params"]["q"] == "query"


@patch("app.requests.get")
def test_fetch_prazdne_vysledky(mock_get):
    """Ověř zda při prázdné JSON odpovědi jse vrátí prázdný seznam výsledků."""

    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {} # žádný organic_results
    mock_get.return_value = mock_resp

    from app import fetch_first_page_results
    assert fetch_first_page_results("cokolvek") == []


@patch("app.requests.get")
def test_fetch_serpapi_error_v_json(mock_get):
    """Ověř zda při poli error v JSON odpovědi zachytíme RuntimeError se zprávou z API."""

    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {"error": "quota exceeded"}
    mock_get.return_value = mock_resp

    from app import fetch_first_page_results
    with pytest.raises(RuntimeError, match="quota exceeded"):
        fetch_first_page_results("x")