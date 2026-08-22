"""Live exchange rate lookup via open.er-api.com (free, no API key)."""

import json
import urllib.error
import urllib.request

API_BASE = "https://open.er-api.com/v6/latest"
TIMEOUT_SECONDS = 10


class RateFetchError(Exception):
    """Raised when the exchange rate API request fails or returns bad data."""


def fetch_rate(base: str, target: str) -> float:
    """Fetch the live exchange rate from `base` currency to `target` currency."""
    url = f"{API_BASE}/{base.upper()}"
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise RateFetchError(f"API request failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RateFetchError("API returned invalid JSON") from exc

    if data.get("result") != "success":
        raise RateFetchError(f"API error: {data.get('error-type', 'unknown')}")

    rates = data.get("rates", {})
    target_code = target.upper()
    if target_code not in rates:
        raise RateFetchError(f"Unsupported currency code: {target_code}")

    return float(rates[target_code])
