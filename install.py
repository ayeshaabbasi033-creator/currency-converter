"""Universal installer for currency-converter-cli.

Installs the package via pip and automatically adds the scripts directory
to the User's persistent PATH on Windows, macOS, and Linux.
"""

import os
import subprocess
import sys
from pathlib import Path

# Add src to sys.path so we can import path_util before or after install
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from currency_converter.path_util import ensure_path, get_scripts_dir


def main() -> None:
    print("=" * 60)
    print(" Installing currency-converter-cli ...")
    print("=" * 60)

    # 1. Run pip install .
    cmd = [sys.executable, "-m", "pip", "install", str(ROOT_DIR)]
    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\n[Error] pip installation failed. Please check the error above.")
        sys.exit(result.returncode)

    print("\n" + "=" * 60)
    print(" Configuring PATH environment variable ...")
    print("=" * 60 + "\n")

    # 2. Ensure scripts directory is on PATH
    scripts_dir = get_scripts_dir()
    added, msg = ensure_path(silent=False)

    print("\n" + "=" * 60)
    print(" Installation Complete!")
    print("=" * 60)
    print(f"\nExecutable location: {scripts_dir}")
    print("\nYou can now run:")
    print("  currency convert 100 USD PKR")
    print("  currency history")
    print("\nNote: If using an existing terminal window, open a new terminal")
    print("      or run: python -m currency_converter convert 100 USD PKR")
    print("=" * 60)


if __name__ == "__main__":
    main()
