"""Installer for currency-converter-cli.

Installs the package via pip. If the `currency` command isn't recognized
afterward, the user's Scripts/bin directory may need to be added to PATH
manually (instructions are printed below if needed).
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


def main() -> None:
    print("=" * 60)
    print(" Installing currency-converter-cli ...")
    print("=" * 60)

    # Run pip install .
    cmd = [sys.executable, "-m", "pip", "install", str(ROOT_DIR)]
    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\n[Error] pip installation failed. Please check the error above.")
        sys.exit(result.returncode)

    print("\n" + "=" * 60)
    print(" Installation Complete!")
    print("=" * 60)

    # Check if the 'currency' command is actually reachable, without
    # modifying any system settings ourselves.
    if shutil.which("currency") is None:
        print(
            "\n[Note] The 'currency' command isn't on your PATH yet.\n"
            "You can still run it with:\n"
            "  python -m currency_converter convert 100 USD PKR\n"
            "\nOr, to use the short 'currency' command directly, add your\n"
            "Python Scripts directory to your system PATH manually:\n"
            "  Windows: Settings > System > About > Advanced system settings\n"
            "           > Environment Variables > edit your User 'Path'\n"
            "  macOS/Linux: add 'export PATH=\"$PATH:<scripts_dir>\"' to your\n"
            "           shell config file (e.g. ~/.zshrc or ~/.bashrc)"
        )
    else:
        print("\nYou can now run:")
        print("  currency convert 100 USD PKR")
        print("  currency history")

    print("=" * 60)


if __name__ == "__main__":
    main()