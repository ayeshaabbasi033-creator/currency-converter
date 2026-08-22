"""Cross-platform PATH management for currency-converter-cli.

Ensures that the directory containing the `currency` executable is present
in the user's persistent PATH environment variable (Windows Registry, Unix shell profiles).
"""

import os
import sys
import sysconfig
from pathlib import Path


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

    # 3. Executable-adjacent Scripts/bin directory
    exec_dir = os.path.dirname(sys.executable)
    if sys.platform == "win32":
        candidates.append(os.path.join(exec_dir, "Scripts"))
        candidates.append(os.path.join(sys.prefix, "Scripts"))
    else:
        candidates.append(os.path.join(exec_dir, "bin"))
        candidates.append(os.path.join(sys.prefix, "bin"))

    # Priority check: look for actual currency executable
    exe_name = "currency.exe" if sys.platform == "win32" else "currency"
    for candidate in candidates:
        if candidate and os.path.isdir(candidate):
            if os.path.exists(os.path.join(candidate, exe_name)):
                return os.path.abspath(candidate)

    # Fallback to the first existing candidate directory, or default sysconfig scripts
    for candidate in candidates:
        if candidate and os.path.isdir(candidate):
            return os.path.abspath(candidate)

    return os.path.abspath(sysconfig.get_path("scripts"))


def _normalize_path(p: str) -> str:
    """Normalize a path for comparison across casing and separators."""
    return os.path.normcase(os.path.normpath(os.path.abspath(p)))


def is_in_path(target_dir: str) -> bool:
    """Check if target_dir is currently in the active PATH environment variable."""
    norm_target = _normalize_path(target_dir)
    current_paths = [
        _normalize_path(p)
        for p in os.environ.get("PATH", "").split(os.pathsep)
        if p.strip()
    ]
    return norm_target in current_paths


def _broadcast_windows_setting_change() -> None:
    """Notify Windows running applications/Explorer of environment variable update."""
    try:
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_ulong()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            SMTO_ABORTIFHUNG,
            3000,
            ctypes.byref(result),
        )
    except Exception:
        pass


def add_to_windows_user_path(scripts_dir: str) -> tuple[bool, str]:
    """Add scripts_dir to Windows User PATH via winreg (persistent)."""
    if sys.platform != "win32":
        return False, "Not a Windows system."

    import winreg

    norm_target = _normalize_path(scripts_dir)

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE,
        )
    except OSError as exc:
        return False, f"Could not access User Environment registry key: {exc}"

    try:
        try:
            current_val, reg_type = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_val = ""
            reg_type = winreg.REG_EXPAND_SZ

        existing_parts = [p.strip() for p in current_val.split(";") if p.strip()]
        existing_normalized = {_normalize_path(p) for p in existing_parts}

        # Also update the current process PATH
        if not is_in_path(scripts_dir):
            os.environ["PATH"] = f"{os.environ.get('PATH', '')};{scripts_dir}"

        if norm_target in existing_normalized:
            return False, f"'{scripts_dir}' is already in Windows User PATH."

        existing_parts.append(scripts_dir)
        new_val = ";".join(existing_parts)

        winreg.SetValueEx(key, "Path", 0, reg_type, new_val)
        _broadcast_windows_setting_change()
        return True, f"Successfully added '{scripts_dir}' to Windows User PATH."
    finally:
        winreg.CloseKey(key)


def add_to_posix_user_path(scripts_dir: str) -> tuple[bool, str]:
    """Add scripts_dir to user's shell configuration file on macOS / Linux."""
    home = Path.home()
    shell_rc_files = [
        home / ".zshrc",
        home / ".bashrc",
        home / ".bash_profile",
        home / ".profile",
    ]

    target_rc = None
    for rc in shell_rc_files:
        if rc.exists():
            target_rc = rc
            break

    if target_rc is None:
        target_rc = home / ".profile"

    # Also update current process PATH
    if not is_in_path(scripts_dir):
        os.environ["PATH"] = f"{os.environ.get('PATH', '')}:{scripts_dir}"

    export_line = f'export PATH="$PATH:{scripts_dir}"'

    content = ""
    if target_rc.exists():
        try:
            content = target_rc.read_text(encoding="utf-8")
        except Exception:
            content = ""

    if scripts_dir in content or export_line in content:
        return False, f"'{scripts_dir}' is already referenced in {target_rc}."

    try:
        with open(target_rc, "a", encoding="utf-8") as f:
            f.write(f"\n# Added by currency-converter-cli\n{export_line}\n")
        return True, f"Added PATH export for '{scripts_dir}' to {target_rc}."
    except Exception as exc:
        return False, f"Could not write to {target_rc}: {exc}"


def ensure_path(silent: bool = True) -> tuple[bool, str]:
    """Ensure the scripts directory is in the persistent user PATH."""
    scripts_dir = get_scripts_dir()

    if sys.platform == "win32":
        added, msg = add_to_windows_user_path(scripts_dir)
    else:
        added, msg = add_to_posix_user_path(scripts_dir)

    if not silent:
        if added:
            print(f"[PATH Setup] {msg}")
            print(
                "[PATH Setup] Note: Please open a new terminal window for the change to take full effect."
            )
        else:
            print(f"[PATH Setup] {msg}")

    return added, msg
