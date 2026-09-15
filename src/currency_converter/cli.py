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


def cmd_history(args: argparse.Namespace) -> None:
    conn = get_connection()
    rows = get_history(conn, args.limit)
    conn.close()

    if not rows:
        print("No conversion history.")
        return

    for ts, amount, base, target, rate, result in rows:
        print(f"{ts}  {amount} {base} -> {result:.2f} {target}  (rate: {rate:.6f})")


def cmd_setup_path(args: argparse.Namespace) -> None:
    ensure_path(silent=False)


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


if __name__ == "__main__":
    main()

