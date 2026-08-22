"""Currency code validation and typo suggestions.

VALID_CODES is a snapshot of the codes supported by open.er-api.com
(captured 2026-08-20). Used only for fast, offline typo-checking before
hitting the network — the live API response remains the source of truth
for actual rates.
"""

VALID_CODES: frozenset[str] = frozenset(
    {
        "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
        "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL",
        "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLF", "CLP",
        "CNH", "CNY", "COP", "CRC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP",
        "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP", "GEL",
        "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK",
        "HTG", "HUF", "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP",
        "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KID", "KMF", "KRW", "KWD",
        "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL",
        "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN",
        "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB",
        "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB",
        "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL",
        "SOS", "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND",
        "TOP", "TRY", "TTD", "TVD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU",
        "UZS", "VES", "VND", "VUV", "WST", "XAF", "XCD", "XCG", "XDR", "XOF",
        "XPF", "YER", "ZAR", "ZMW", "ZWG", "ZWL",
    }
)


def is_valid(code: str) -> bool:
    return code.upper() in VALID_CODES


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


def suggest(code: str, max_distance: int = 1) -> str | None:
    """Return the nearest known currency code within `max_distance` edits, else None.

    Ties broken alphabetically for determinism (166 codes, O(1)-scale cost either way).
    """
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
