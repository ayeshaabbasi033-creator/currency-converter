# currency-converter-cli

Lightweight command-line currency converter. Live exchange rates, SQLite-cached, full conversion history — zero third-party runtime dependencies (stdlib only: `urllib`, `sqlite3`, `argparse`).

## Install

### Automatic Setup (Recommended for any new computer)

Run the universal installer — it installs the package and automatically configures your `PATH`:

```bash
git clone https://github.com/ayeshaabbasi033-creator/currency-converter-cli
cd currency-converter-cli
python install.py
```

*(On Windows, you can also double-click `install.bat`)*

### Manual Install via pip

```bash
pip install .
```

If your Python scripts directory was not on `PATH`, simply run:
```bash
python -m currency_converter setup-path
```


## Usage

```bash
currency convert 100 USD PKR
currency convert 50 EUR JPY
currency history
currency history --limit 20
```

Example output:

```
100.0 USD = 27774.63 PKR (rate: 277.746349, source: live)
100.0 USD = 27774.63 PKR (rate: 277.746349, source: cache)
```

Typos in currency codes are caught before any network call, with a suggestion:

```
$ currency convert 100 USD USF
Error: unknown to currency 'USF'. Did you mean USD?
```

## How it works

- **Rates**: [open.er-api.com](https://www.exchangerate-api.com/docs/free) — free, no signup, no API key, updated daily, 160+ currencies.
- **Cache**: fetched rates are stored in SQLite (`~/.currency_converter/data.db`) and reused for 60 minutes, cutting repeat API calls. The `source` field in the output shows `live` vs `cache`.
- **History**: every conversion is logged with timestamp, amount, rate, and result.

## Schema

```sql
CREATE TABLE rate_cache (
    base_currency TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    rate REAL NOT NULL,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (base_currency, target_currency)
);

CREATE TABLE conversion_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    amount REAL NOT NULL,
    from_currency TEXT NOT NULL,
    to_currency TEXT NOT NULL,
    rate REAL NOT NULL,
    result REAL NOT NULL
);
```

## Troubleshooting

**`'currency' is not recognized as an internal or external command`**

If the command isn't immediately found after installation:

1. **One-command automatic PATH fix**:
   ```bash
   python -m currency_converter setup-path
   ```
2. **Or run directly via module anytime**:
   ```bash
   python -m currency_converter convert 100 USD PKR
   ```
3. Restart your terminal window for the newly updated environment variables to take effect.


## Stack

Python 3.10+, stdlib only. No `requests`, no ORM, no external services beyond the rate API.

## Tests

```bash
pip install -e ".[dev]"
pytest
```
