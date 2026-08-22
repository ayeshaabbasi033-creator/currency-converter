# Comprehensive Beginner's Guide to the Currency Converter CLI

Welcome! This document is designed for someone who has **zero prior programming experience**. It breaks down the entire Currency Converter project into plain English, using real-world analogies, straightforward definitions, and an in-depth line-by-line breakdown.

---

## Table of Contents
1. [High-Level Overview](#1-high-level-overview)
2. [Setup & Execution](#2-setup--execution)
3. [Concept Glossary](#3-concept-glossary)
4. [Line-by-Line Code Breakdown](#4-line-by-line-code-breakdown)
   - [File 1: `src/currency_converter/currencies.py`](#file-1-srccurrency_convertercurrenciespy)
   - [File 2: `src/currency_converter/api.py`](#file-2-srccurrency_converterapipy)
   - [File 3: `src/currency_converter/db.py`](#file-3-srccurrency_converterdbpy)
   - [File 4: `src/currency_converter/path_util.py`](#file-4-srccurrency_converterpath_utilpy)
   - [File 5: `src/currency_converter/cli.py`](#file-5-srccurrency_converterclipy)
   - [File 6: `src/currency_converter/__main__.py`](#file-6-srccurrency_converter__main__py)
   - [File 7: `install.py`](#file-7-installpy)
5. [Execution Flow (Walkthrough)](#5-execution-flow-walkthrough)

---

## 1. High-Level Overview

### What Does This Program Do?
The **Currency Converter CLI** is a command-line tool that converts money from one currency to another (e.g., converting 100 US Dollars to Pakistani Rupees or Euros) using live, up-to-the-minute global exchange rates.

### The Airport Currency Exchange Booth Analogy
To understand how the program works behind the scenes, imagine an **Exchange Booth at an International Airport**:

```
[ You (User) ]
      │
      │ 1. Ask: "Convert 100 USD to PKR"
      ▼
[ The Booth Teller (cli.py) ]
      │
      ├─► 2. Spell-Check: "Are USD and PKR real currencies?" (currencies.py)
      │
      ├─► 3. Quick Ledger Check: "Did we check USD to PKR in the last 60 mins?" (db.py)
      │         │
      │         ├─► YES: Use the notebook rate immediately! (Fast & saves internet)
      │         │
      │         └─► NO: Call International Headquarters via telephone (api.py)
      │                   └─► Write the new rate into the notebook (db.py)
      │
      ├─► 4. Math: 100 × 278.50 = 27,850 PKR
      │
      ├─► 5. History Log: Record transaction into permanent filing cabinet (db.py)
      │
      └─► 6. Receipt: Hand the result back to your screen:
              "100.0 USD = 27850.00 PKR (rate: 278.500000, source: live)"
```

### Why Is It Built This Way?
1. **Speed & Reliability**: If you convert money multiple times, checking a local database on your hard drive (the cache) is 1,000 times faster than connecting to an internet server every single time.
2. **Zero Third-Party Clutter**: It runs purely on Python's built-in tools (the standard library). You do not need to install complicated third-party packages.
3. **Automatic System Setup**: It includes built-in automation to ensure your operating system (Windows, Mac, or Linux) knows where the `currency` command lives so you can run it from any terminal.

---

## 2. Setup & Execution

### Prerequisites
- Any modern computer running Windows, macOS, or Linux.
- **Python 3.10** or newer installed.

---

### Step-by-Step Installation

#### Option A: Universal 1-Click Installer (Recommended)
1. Open your **Command Prompt** (CMD) or **Terminal**.
2. Navigate to the project directory:
   ```bash
   cd "C:\Users\mateen\Desktop\New folder\currency-converter-cli"
   ```
3. Run the installer script:
   ```bash
   python install.py
   ```
   *(On Windows, you can also simply double-click `install.bat`)*

This single command:
- Installs the program.
- Automatically adds the program to your computer's `PATH` so you can use the word `currency` anywhere.

---

#### Option B: Standard Python Installation
If you prefer running manual standard commands:
```bash
pip install .
```
If your terminal gives a warning that the Scripts folder is not on PATH, run:
```bash
python -m currency_converter setup-path
```

---

### How to Run the Program

#### 1. Convert Currency
To convert an amount between two currencies:
```bash
currency convert 100 USD PKR
```
*Output:*
```text
100.0 USD = 27774.63 PKR (rate: 277.746349, source: live)
```

If you run the exact same conversion immediately again:
```bash
currency convert 100 USD PKR
```
*Output:*
```text
100.0 USD = 27774.63 PKR (rate: 277.746349, source: cache)
```
*(Notice how the second one says `source: cache` because it read the rate from your local computer instead of fetching it over the web).*

#### 2. Typo Detection & Suggestions
If you make a typo, the program will catch it before making any internet calls:
```bash
currency convert 100 USD USF
```
*Output:*
```text
Error: unknown to currency 'USF'. Did you mean USD?
```

#### 3. View Conversion History
To see your previous conversions:
```bash
currency history
```
*Output:*
```text
2026-08-20T12:08:48.123456  100.0 USD -> 27774.63 PKR  (rate: 277.746349)
2026-08-20T12:05:10.987654  50.0 EUR -> 8125.50 JPY  (rate: 162.510000)
```

To limit the history to the last 5 records:
```bash
currency history --limit 5
```

---

## 3. Concept Glossary

| Term | Simple Definition | Everyday Analogy |
| :--- | :--- | :--- |
| **Python** | A programming language that allows humans to write readable instructions that a computer executes. | A universal recipe book for your computer. |
| **CLI (Command-Line Interface)** | A text-based screen where you type commands instead of clicking graphical buttons. | Ordering food by text message rather than pointing at a visual menu. |
| **Variable** | A named storage container in computer memory that holds a piece of data. | A labeled cardboard box with an item inside (e.g., a box labeled `amount` containing `100`). |
| **Data Types** | | |
| ↳ **String (`str`)** | Text enclosed in quotes, such as `"USD"` or `"Hello"`. | Words written on a piece of paper. |
| ↳ **Float (`float`)** | A number that has decimal places, like `278.50` or `1.25`. | Money measurements with cents/pennies. |
| ↳ **Integer (`int`)** | A whole counting number without decimals, like `10` or `-5`. | Counting physical coins in your hand. |
| ↳ **Boolean (`bool`)** | A value that is strictly either `True` or `False`. | A simple light switch (On or Off). |
| ↳ **`None`** | A special Python value representing the total absence of a value. | An empty box with nothing in it. |
| **Data Structures** | | |
| ↳ **List (`list`)** | An ordered collection of items enclosed in square brackets `[1, 2, 3]`. | A grocery shopping list. |
| ↳ **Tuple (`tuple`)** | A locked, unchangeable group of items in parentheses `(100, "USD", 278.5)`. | A sealed envelope with fixed documents inside. |
| ↳ **Dictionary (`dict`)** | A collection of paired data (keys and values) like `{"USD": 1.0, "EUR": 0.85}`. | An actual language dictionary where you look up a word (key) to get its definition (value). |
| ↳ **Frozenset (`frozenset`)** | A locked collection of unique items optimized for lightning-fast lookup. | A master checklist of VIP guest names at a doorway. |
| **Function (`def`)** | A named block of instructions that takes inputs, performs work, and gives back a result (`return`). | A microwave oven: you put food in (input), press start, and it gives cooked food out (output). |
| **Parameters & Arguments** | *Parameters* are the placeholders defined in a function; *Arguments* are the actual values passed in when calling it. | A blender has a slot for "fruit" (parameter); you drop in an "apple" (argument). |
| **Type Hints** | Optional annotations like `def convert(amount: float) -> str:` showing expected data types. | Labeling a box "Fragile Glass Only" so people know what belongs inside. |
| **Conditionals (`if` / `else`)** | Logic branches where the computer chooses what to do based on whether a condition is true. | "If it is raining, take an umbrella; else, wear sunglasses." |
| **Loops (`for` / `while`)** | Repeating an action multiple times for every item in a collection. | Stamping 100 envelopes one by one until the pile is finished. |
| **Exceptions (`try` / `except`)** | Python's emergency response system for handling errors gracefully without crashing. | An airbag in a car that deploys safely when a crash occurs. |
| **API (Application Programming Interface)** | A web service that allows two software programs to communicate and exchange data over the internet. | A waiter who takes your food order to the kitchen and brings back the meal. |
| **JSON (JavaScript Object Notation)** | A universal plain-text format used to transmit structured data over the web. | A standardized cargo shipping container that fits on any ship or truck. |
| **SQLite Database** | A self-contained, serverless database that stores tables inside a single local file (`.db`). | A physical filing cabinet saved directly inside your computer's user folder. |
| **Cache (TTL)** | Storing temporary data locally so you don't have to re-fetch it; TTL (Time-To-Live) is its expiration time. | Keeping today's newspaper on your coffee table for an hour rather than walking back to the newsstand every 5 minutes. |
| **`PATH` Environment Variable** | A master list of folders where your operating system searches when you type a command in the terminal. | The list of standard phone numbers saved in your phone's speed-dial. |

---

## 4. Line-by-Line Code Breakdown

Below is the complete, meticulous inspection of every file in the project.

---

### File 1: `src/currency_converter/currencies.py`
**Purpose**: Holds the master list of 160+ world currency codes and provides a smart "did you mean?" suggestion engine when the user makes a typo.

```python
"""Currency code validation and typo suggestions.

VALID_CODES is a snapshot of the codes supported by open.er-api.com
(captured 2026-08-20). Used only for fast, offline typo-checking before
hitting the network — the live API response remains the source of truth
for actual rates.
"""
```
- **Lines 1–7**: A **Docstring** (documentation string). In Python, text wrapped in triple quotes `"""` is used to explain what the file does. Python ignores this during execution, but developers read it.

```python
VALID_CODES: frozenset[str] = frozenset(
    {
        "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
        "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL",
        "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLF", "CLP",
        # ... (166 currency codes in total)
        "XPF", "YER", "ZAR", "ZMW", "ZWG", "ZWL",
    }
)
```
- **`VALID_CODES`**: A variable name written in all-caps, which by convention indicates a **constant** (a value that does not change).
- **`frozenset(...)`**: Converts the set of currency strings into an immutable (unmodifiable) set. In computer science, checking if an item exists inside a set takes \(O(1)\) constant time (instantaneous), regardless of whether there are 10 items or 10,000 items.

```python
def is_valid(code: str) -> bool:
    return code.upper() in VALID_CODES
```
- **`def is_valid(code: str) -> bool:`**:
  - `def` tells Python we are defining a new function named `is_valid`.
  - `code: str` means this function expects one input named `code`, which should be a string of text.
  - `-> bool` means this function will return either `True` or `False`.
- **`code.upper()`**: Automatically converts lowercase inputs like `"usd"` to uppercase `"USD"`.
- **`in VALID_CODES`**: Checks if that uppercase code is in our master list. If yes, it gives back `True`; otherwise `False`.

```python
def _edit_distance(a: str, b: str) -> int:
    """Damerau-Levenshtein distance (adjacent transpositions count as 1 edit, not 2)."""
    la, lb = len(a), len(b)
    d = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        d[i][0] = i
    for j in range(lb + 1):
        d[0][j] = j
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,  # deletion
                d[i][j - 1] + 1,  # insertion
                d[i - 1][j - 1] + cost,  # substitution
            )
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)  # transposition
    return d[la][lb]
```
- **`_edit_distance`**: The leading underscore `_` signifies that this is a private helper function intended for internal use inside this file.
- **The Algorithm**: This implements the famous **Damerau-Levenshtein Distance** algorithm. It calculates how many single-character edits (insertions, deletions, substitutions, or swapping two neighboring letters) are required to transform word `a` into word `b`.
  - Example: Changing `"USF"` into `"USD"` requires 1 substitution (edit distance = 1).
  - Example: Changing `"UDS"` into `"USD"` requires swapping `D` and `S` (transposition edit distance = 1).

```python
def suggest(code: str, max_distance: int = 1) -> str | None:
    """Return the nearest known currency code within `max_distance` edits, else None."""
    code = code.upper()
    best_code: str | None = None
    best_dist: int | None = None
    for candidate in sorted(VALID_CODES):
        dist = _edit_distance(code, candidate)
        if best_dist is None or dist < best_dist:
            best_dist, best_code = dist, candidate
    if best_dist is not None and best_dist <= max_distance:
        return best_code
    return None
```
- **`suggest(...)`**:
  - Takes the mistyped code (e.g., `"USF"`).
  - Loops (`for candidate in sorted(VALID_CODES)`) through all 166 real currencies.
  - Measures the distance between the typo and every real currency.
  - If the closest valid currency is within 1 typo (`max_distance = 1`), it returns that code (e.g. `"USD"`).
  - If the typo is completely unrecognizable (e.g., `"12345"`), it returns `None`.

---

### File 2: `src/currency_converter/api.py`
**Purpose**: Reaches out over the internet to fetch live exchange rate data and handles network problems gracefully.

```python
"""Live exchange rate lookup via open.er-api.com (free, no API key)."""

import json
import urllib.error
import urllib.request

API_BASE = "https://open.er-api.com/v6/latest"
TIMEOUT_SECONDS = 10
```
- **`import json`**: Imports Python's built-in tool for reading web data formats.
- **`import urllib.error` & `urllib.request`**: Imports Python's built-in web browser-like tools for making HTTP requests without needing external libraries.
- **`API_BASE`**: The public URL where live exchange data is hosted.
- **`TIMEOUT_SECONDS = 10`**: Tells Python: "If the server does not respond within 10 seconds, stop waiting and report a timeout error instead of freezing forever."

```python
class RateFetchError(Exception):
    """Raised when the exchange rate API request fails or returns bad data."""
```
- **`class RateFetchError(Exception):`**: Creates a custom error type. If something goes wrong while contacting the API, our program can raise this specific error so we can show a user-friendly message rather than a scary computer crash dump.

```python
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
```
- **`url = f"{API_BASE}/{base.upper()}"`**: An **f-string** (formatted string literal). If `base` is `"USD"`, this creates `"https://open.er-api.com/v6/latest/USD"`.
- **`try:`**: Starts a protective block. If any error happens inside this block, Python will jump to the `except` blocks below.
- **`with urllib.request.urlopen(...) as response:`**: Opens an internet connection to the URL and automatically closes it when finished.
- **`response.read().decode()`**: Reads the raw incoming bytes of data over the internet cable and converts them into readable text.
- **`json.loads(...)`**: Parses that text into a Python dictionary.
- **`except ... as exc:`**: If your internet is disconnected or the server is down, this catches the failure and raises our clean `RateFetchError`.

```python
    if data.get("result") != "success":
        raise RateFetchError(f"API error: {data.get('error-type', 'unknown')}")

    rates = data.get("rates", {})
    target_code = target.upper()
    if target_code not in rates:
        raise RateFetchError(f"Unsupported currency code: {target_code}")

    return float(rates[target_code])
```
- **`data.get("result") != "success"`**: Checks if the API returned an official confirmation of success.
- **`rates = data.get("rates", {})`**: Extracts the sub-dictionary containing all 160+ currency rates (e.g. `{"EUR": 0.92, "PKR": 277.7, ...}`).
- **`return float(rates[target_code])`**: Finds the target currency's rate, converts it to a floating-point decimal number, and hands it back.

---

### File 3: `src/currency_converter/db.py`
**Purpose**: Manages the SQLite database stored on your hard drive for caching exchange rates and recording conversion history.

```python
"""SQLite persistence: rate cache (TTL-based) and conversion history."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path.home() / ".currency_converter" / "data.db"
CACHE_TTL_MINUTES = 60
```
- **`import sqlite3`**: Imports Python's built-in SQL database engine.
- **`Path.home() / ".currency_converter" / "data.db"`**:
  - `Path.home()` dynamically finds your user directory (e.g. `C:\Users\mateen` on Windows or `/home/mateen` on Linux).
  - This sets the database file path to `~/.currency_converter/data.db`.
- **`CACHE_TTL_MINUTES = 60`**: Sets the Time-To-Live expiration window to 60 minutes.

```python
SCHEMA = """
CREATE TABLE IF NOT EXISTS rate_cache (
    base_currency TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    rate REAL NOT NULL,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (base_currency, target_currency)
);

CREATE TABLE IF NOT EXISTS conversion_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    amount REAL NOT NULL,
    from_currency TEXT NOT NULL,
    to_currency TEXT NOT NULL,
    rate REAL NOT NULL,
    result REAL NOT NULL
);
"""
```
- **`SCHEMA`**: SQL database instructions to create two tables if they do not already exist:
  1. `rate_cache`: Stores previously fetched rates with timestamps.
  2. `conversion_history`: Stores a log of every conversion you make.

```python
def get_connection() -> sqlite3.Connection:
    """Open the DB connection, creating the data dir/schema on first run."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    return conn
```
- **`DB_PATH.parent.mkdir(parents=True, exist_ok=True)`**: Automatically creates the `.currency_converter` folder on your computer if it doesn't already exist.
- **`sqlite3.connect(DB_PATH)`**: Connects to the database file.
- **`conn.executescript(SCHEMA)`**: Runs the table setup script.

```python
def get_cached_rate(conn: sqlite3.Connection, base: str, target: str) -> float | None:
    """Return a cached rate if present and younger than CACHE_TTL_MINUTES, else None."""
    row = conn.execute(
        "SELECT rate, fetched_at FROM rate_cache WHERE base_currency = ? AND target_currency = ?",
        (base.upper(), target.upper()),
    ).fetchone()
    if row is None:
        return None

    rate, fetched_at = row
    fetched_dt = datetime.fromisoformat(fetched_at)
    if datetime.now() - fetched_dt > timedelta(minutes=CACHE_TTL_MINUTES):
        return None
    return rate
```
- **`get_cached_rate`**:
  - Searches the `rate_cache` table for this currency pair.
  - If nothing is found, it returns `None`.
  - If found, it compares the current time (`datetime.now()`) with when the rate was recorded (`fetched_dt`).
  - If more than 60 minutes have passed, the cached rate is considered expired and it returns `None`.
  - Otherwise, it returns the fresh cached rate.

```python
def cache_rate(conn: sqlite3.Connection, base: str, target: str, rate: float) -> None:
    """Insert or refresh a cached rate for a currency pair."""
    conn.execute(
        "INSERT OR REPLACE INTO rate_cache (base_currency, target_currency, rate, fetched_at) "
        "VALUES (?, ?, ?, ?)",
        (base.upper(), target.upper(), rate, datetime.now().isoformat()),
    )
    conn.commit()
```
- **`cache_rate`**: Saves a freshly fetched rate along with the current timestamp. `INSERT OR REPLACE` ensures old entries for the same currency pair get updated smoothly.

```python
def log_conversion(
    conn: sqlite3.Connection, amount: float, base: str, target: str, rate: float, result: float
) -> None:
    """Append a completed conversion to history."""
    conn.execute(
        "INSERT INTO conversion_history (timestamp, amount, from_currency, to_currency, rate, result) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), amount, base.upper(), target.upper(), rate, result),
    )
    conn.commit()


def get_history(
    conn: sqlite3.Connection, limit: int = 10
) -> list[tuple[str, float, str, str, float, float]]:
    """Return the most recent conversions, newest first."""
    return conn.execute(
        "SELECT timestamp, amount, from_currency, to_currency, rate, result "
        "FROM conversion_history ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
```
- **`log_conversion`**: Adds a new record to the history log.
- **`get_history`**: Retrieves the newest conversions from the database up to the requested limit (defaults to 10).

---

### File 4: `src/currency_converter/path_util.py`
**Purpose**: Automatically detects and registers the Python `Scripts` directory into your operating system's permanent `PATH` environment variable.

```python
def get_scripts_dir() -> str:
    """Find the directory where `currency` executable is installed."""
    candidates = []
    # 1. Standard sysconfig scripts path
    try:
        candidates.append(sysconfig.get_path("scripts"))
    except Exception:
        pass
    # 2. User scheme scripts path
    try:
        user_scheme = sysconfig.get_preferred_scheme("user")
        user_scripts = sysconfig.get_path("scripts", user_scheme)
        if user_scripts:
            candidates.append(user_scripts)
    except Exception:
        pass
    # ...
```
- **`get_scripts_dir()`**: Inspects Python's configuration to find the exact folder where `currency.exe` (Windows) or `currency` (Mac/Linux) was saved during `pip install`.

```python
def add_to_windows_user_path(scripts_dir: str) -> tuple[bool, str]:
    """Add scripts_dir to Windows User PATH via winreg (persistent)."""
    if sys.platform != "win32":
        return False, "Not a Windows system."

    import winreg
    # Opens HKEY_CURRENT_USER\Environment in the Windows Registry
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Environment",
        0,
        winreg.KEY_READ | winreg.KEY_WRITE,
    )
    # Reads the existing PATH, appends our Scripts folder, and saves it back!
    # ...
```
- **`add_to_windows_user_path`**:
  - Uses Python's built-in `winreg` module to open the Windows Registry.
  - Appends the Scripts directory to the User `Path` key permanently.
  - Broadcasts a Windows message (`WM_SETTINGCHANGE`) so open programs and new terminals recognize the change immediately.

```python
def add_to_posix_user_path(scripts_dir: str) -> tuple[bool, str]:
    """Add scripts_dir to user's shell configuration file on macOS / Linux."""
    home = Path.home()
    # Looks for .zshrc, .bashrc, or .profile and adds export PATH="$PATH:<dir>"
    # ...
```
- **`add_to_posix_user_path`**: On macOS and Linux, it finds your shell configuration file (`~/.bashrc` or `~/.zshrc`) and appends the path export line automatically.

```python
def ensure_path(silent: bool = True) -> tuple[bool, str]:
    """Ensure the scripts directory is in the persistent user PATH."""
    scripts_dir = get_scripts_dir()
    if sys.platform == "win32":
        added, msg = add_to_windows_user_path(scripts_dir)
    else:
        added, msg = add_to_posix_user_path(scripts_dir)
    # ...
```
- **`ensure_path`**: A single unified function that runs the right PATH configuration logic for your specific operating system.

---

### File 5: `src/currency_converter/cli.py`
**Purpose**: The main control center of the program. It parses user commands and coordinates validation, caching, API calls, and displaying outputs.

```python
"""Entry point for the `currency` command."""

import argparse
import sys

from currency_converter.api import RateFetchError, fetch_rate
from currency_converter.currencies import is_valid, suggest
from currency_converter.db import (
    cache_rate,
    get_cached_rate,
    get_connection,
    get_history,
    log_conversion,
)
from currency_converter.path_util import ensure_path
```
- **`import argparse`**: Imports Python's built-in command-line argument parser. This handles reading subcommands like `convert` and `history`, and options like `--limit`.

```python
def _validate_currency(code: str, label: str) -> bool:
    """Print a did-you-mean error and return False if `code` isn't a known currency."""
    if is_valid(code):
        return True

    match = suggest(code)
    if match:
        print(f"Error: unknown {label} currency '{code.upper()}'. Did you mean {match}?", file=sys.stderr)
    else:
        print(f"Error: unknown {label} currency '{code.upper()}'.", file=sys.stderr)
    return False
```
- **`_validate_currency`**:
  - Checks if the currency code given by the user exists.
  - If valid, returns `True`.
  - If invalid, prints a helpful suggestion (e.g. `Did you mean USD?`) to `sys.stderr` (the standard error output stream) and returns `False`.

```python
def cmd_convert(args: argparse.Namespace) -> None:
    if not _validate_currency(args.from_currency, "from"):
        sys.exit(1)
    if not _validate_currency(args.to_currency, "to"):
        sys.exit(1)

    conn = get_connection()
    rate = get_cached_rate(conn, args.from_currency, args.to_currency)
    source = "cache"

    if rate is None:
        try:
            rate = fetch_rate(args.from_currency, args.to_currency)
        except RateFetchError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            conn.close()
            sys.exit(1)
        cache_rate(conn, args.from_currency, args.to_currency, rate)
        source = "live"

    result = args.amount * rate
    log_conversion(conn, args.amount, args.from_currency, args.to_currency, rate, result)
    conn.close()

    print(
        f"{args.amount} {args.from_currency.upper()} = {result:.2f} {args.to_currency.upper()} "
        f"(rate: {rate:.6f}, source: {source})"
    )
```
- **`cmd_convert`**:
  1. Validates both input currencies. If either is invalid, terminates early with `sys.exit(1)`.
  2. Opens the SQLite database connection (`get_connection()`).
  3. Checks for a cached rate (`get_cached_rate(...)`).
  4. If no cached rate exists (`rate is None`), calls the live API (`fetch_rate(...)`) and saves the fresh rate into the cache (`cache_rate(...)`).
  5. Multiplies the input amount by the rate (`result = args.amount * rate`).
  6. Saves the conversion in history (`log_conversion(...)`).
  7. Prints the clean result formatted to 2 decimal places (`result:.2f`) and rate to 6 decimal places (`rate:.6f`).

```python
def cmd_history(args: argparse.Namespace) -> None:
    conn = get_connection()
    rows = get_history(conn, args.limit)
    conn.close()

    if not rows:
        print("No conversion history.")
        return

    for ts, amount, base, target, rate, result in rows:
        print(f"{ts}  {amount} {base} -> {result:.2f} {target}  (rate: {rate:.6f})")
```
- **`cmd_history`**: Reads past conversions from SQLite and displays them neatly.

```python
def cmd_setup_path(args: argparse.Namespace) -> None:
    ensure_path(silent=False)
```
- **`cmd_setup_path`**: Manually triggers the PATH configuration tool and prints verbose feedback.

```python
def main() -> None:
    # Silently ensure the scripts directory is in PATH on any machine
    ensure_path(silent=True)

    parser = argparse.ArgumentParser(prog="currency", description="Lightweight live currency converter")
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparsers.add_parser("convert", help="Convert an amount between currencies")
    convert_parser.add_argument("amount", type=float)
    convert_parser.add_argument("from_currency", type=str)
    convert_parser.add_argument("to_currency", type=str)
    convert_parser.set_defaults(func=cmd_convert)

    history_parser = subparsers.add_parser("history", help="Show past conversions")
    history_parser.add_argument("--limit", type=int, default=10)
    history_parser.set_defaults(func=cmd_history)

    setup_path_parser = subparsers.add_parser(
        "setup-path", help="Add the currency command to your user PATH permanently"
    )
    setup_path_parser.set_defaults(func=cmd_setup_path)

    args = parser.parse_args()
    args.func(args)
```
- **`main()`**:
  - Automatically runs `ensure_path(silent=True)` in the background on every launch.
  - Builds the command structure (`convert`, `history`, `setup-path`).
  - Reads the arguments you typed in the terminal and calls the matching function (`args.func(args)`).

---

### File 6: `src/currency_converter/__main__.py`
**Purpose**: Allows you to run the package directly via Python (`python -m currency_converter`).

```python
from currency_converter.cli import main

if __name__ == "__main__":
    main()
```
- **`if __name__ == "__main__":`**: A standard Python idiom. It means: "If this file is being executed directly by the user (rather than being imported as a helper inside another file), run the `main()` function."

---

### File 7: `install.py`
**Purpose**: The universal installer for any new computer.

```python
def main() -> None:
    # 1. Run pip install .
    cmd = [sys.executable, "-m", "pip", "install", str(ROOT_DIR)]
    result = subprocess.run(cmd)

    # 2. Ensure scripts directory is on PATH
    scripts_dir = get_scripts_dir()
    added, msg = ensure_path(silent=False)
```
- Uses Python's `subprocess` module to execute `pip install .` in the background and then immediately configures `PATH`.

---

## 5. Execution Flow (Walkthrough)

Let’s trace step-by-step what happens when you type the following command and press Enter:

```bash
currency convert 100 USD EUR
```

```
========================================================================================
 STEP 1: Terminal Execution
   - Your operating system checks its PATH, finds `currency.exe`, and starts Python.
========================================================================================
                                     │
                                     ▼
========================================================================================
 STEP 2: `main()` in `cli.py` Starts
   - `ensure_path(silent=True)` runs in the background to ensure PATH integrity.
   - `argparse` reads your inputs:
       • command: 'convert'
       • amount: 100.0 (float)
       • from_currency: 'USD' (string)
       • to_currency: 'EUR' (string)
========================================================================================
                                     │
                                     ▼
========================================================================================
 STEP 3: Validation in `currencies.py`
   - Checks: Is "USD" in VALID_CODES? -> Yes (True).
   - Checks: Is "EUR" in VALID_CODES? -> Yes (True).
========================================================================================
                                     │
                                     ▼
========================================================================================
 STEP 4: Local Database Cache Check (`db.py`)
   - Connects to SQLite database at `~/.currency_converter/data.db`.
   - Runs query: "SELECT rate, fetched_at FROM rate_cache WHERE USD and EUR".
   - Scenario A (Cached & < 60 mins old):
       -> Found rate 0.925000 in database.
       -> Source set to "cache".
   - Scenario B (Not in database or > 60 mins old):
       -> Calls `api.py` -> `fetch_rate("USD", "EUR")`.
       -> Contacts `https://open.er-api.com/v6/latest/USD`.
       -> Receives rate: 0.925000.
       -> Writes 0.925000 to SQLite `rate_cache`.
       -> Source set to "live".
========================================================================================
                                     │
                                     ▼
========================================================================================
 STEP 5: Calculation
   - Multiplies: 100.0 * 0.925000 = 92.50
========================================================================================
                                     │
                                     ▼
========================================================================================
 STEP 6: History Logging (`db.py`)
   - Appends row to `conversion_history`:
     [Timestamp, 100.0, "USD", "EUR", 0.925000, 92.50]
   - Closes database connection.
========================================================================================
                                     │
                                     ▼
========================================================================================
 STEP 7: Output to Terminal
   - Prints formatted text to your console:
     100.0 USD = 92.50 EUR (rate: 0.925000, source: live)
========================================================================================
```

---

## Summary Cheat Sheet

- **To Convert**: `currency convert <amount> <FROM> <TO>`
- **To View History**: `currency history`
- **To Fix PATH on a new computer**: `python install.py` or `python -m currency_converter setup-path`
- **Data Location**: `~/.currency_converter/data.db`
