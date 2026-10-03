# currency-converter-cli

Lightweight command-line currency converter. Live exchange rates, SQLite-cached, full conversion history, and zero third-party runtime dependencies (stdlib only: `urllib`, `sqlite3`, `argparse`).

## Install

### Automatic Setup (Recommended)

Run the installer. It installs the package via pip and checks whether the `currency` command is ready to use:

```bash
git clone https://github.com/ayeshaabbasi033-creator/currency-converter
cd currency-converter
python install.py
```

*(On Windows, you can also double-click `install.bat`)*

If the `currency` command isn't on your PATH yet, the installer will print manual instructions for adding it. It does not modify your system PATH or Windows Registry automatically. You can always run the tool via `python -m currency_converter` in the meantime.

### Manual Install via pip

```bash
pip install .
```

## Usage

```bash
currency convert 100 USD PKR
currency convert 50 EUR JPY
currency history
currency history --limit 20
```

Or, without relying on PATH at all:
```bash
python -m currency_converter convert 100 USD PKR
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

- **Rates**: [open.er-api.com](https://www.exchangerate-api.com/docs/free), free, no signup, no API key, updated daily, 160+ currencies.
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

This means your Python Scripts directory isn't on your system PATH. You have two options:

1. **Run via module (no PATH changes needed)**:
   ```bash
   python -m currency_converter convert 100 USD PKR
   ```
2. **Add it to PATH manually**:
   - **Windows**: Settings → System → About → Advanced system settings → Environment Variables → edit your User `Path` → add your Python Scripts folder
   - **macOS/Linux**: add `export PATH="$PATH:<scripts_dir>"` to your shell config file (e.g. `~/.zshrc` or `~/.bashrc`)

   Run `python install.py` to see your exact Scripts directory path printed out.

## Stack

Python 3.10+, stdlib only. No `requests`, no ORM, no external services beyond the rate API.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Design note

An earlier version of this tool automatically modified the user's PATH environment variable (via the Windows Registry on Windows, or shell config files on macOS/Linux) on every single run, without asking. This was removed in favor of an explicit, read-only check with manual instructions, since silently modifying system settings without user consent is poor practice for a CLI tool.