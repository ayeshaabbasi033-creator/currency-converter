# currency-converter-cli

Lightweight command-line currency converter you can run straight from the terminal, no browser needed. Live exchange rates, SQLite-cached, full conversion history, and zero third-party runtime dependencies (stdlib only: `urllib`, `sqlite3`, `argparse`).

## Why I built this

This was one of the first projects I ever built, so I kept the idea small on purpose. I wanted to make something other people could actually pick up and use on their own machines, not just something that ran on my laptop. I wanted a quick way to check an exchange rate without opening a browser or a website, so I made a tool that gives you the answer in one line, straight from the terminal. I also wanted it to feel fast, so it remembers each rate for an hour (cached in SQLite) instead of asking the internet every time. The first time it printed a real answer, I remember thinking: wow, it actually works, and I'm the one who made it work.

## Install

### Automatic Setup (Recommended)

Run the installer. It installs the package via pip and checks whether the `currency` command is ready to use:

```bash
git clone https://github.com/ayeshassan/currency-converter
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

      To find your Scripts folder, run `python -c "import sysconfig; print(sysconfig.get_path('scripts'))"`.

## Stack

Python 3.10+, stdlib only. No `requests`, no ORM, no external services beyond the rate API.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## What I learned

- How to design a local caching system using SQLite with a TTL (time-to-live), so the app doesn't call the live API more than necessary, and how to check whether cached data has expired before deciding to trust it.
- How to implement the Damerau-Levenshtein edit-distance algorithm, to catch typos in currency codes and suggest the closest valid match before wasting an API call on an invalid request.
- A real lesson in both software ethics and security: an earlier version of this project automatically modified the Windows Registry and system PATH every time it ran, without telling the user. Fixing it taught me two things at once, first, that silently modifying system settings without consent is poor practice, regardless of intent, and second, as a cybersecurity student, it gave me a concrete, hands-on example of a persistence mechanism (a technique software uses to maintain access or control by modifying system configuration), the same general category of technique used by both legitimate installers and malware. I redesigned the tool to be transparent instead, it now only checks and informs, it never silently changes system settings on its own.
- How to structure a small Python project properly, separating concerns across different files (API calls, database logic, validation, and the command-line interface itself) instead of writing everything in one script.