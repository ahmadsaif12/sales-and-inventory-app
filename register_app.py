#!/usr/bin/env python3
"""Register one or more Django apps in INSTALLED_APPS and the project urls.py.

If the app directory does not exist yet it is created with `startapp`.
Already-registered apps are skipped (idempotent), so the script is safe to
re-run for any number of apps.

Usage:
  make register APP=accounts
  make register APP="accounts users products"
  python register_app.py accounts users products
"""
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
SETTINGS_PATH = BASE_DIR / "InventoryMS" / "settings.py"
URLS_PATH = BASE_DIR / "InventoryMS" / "urls.py"

APP_URLS_TEMPLATE = """from django.urls import path
from . import views

app_name = '{app_name}'

urlpatterns = [
    # path('', views.home, name='home'),
]
"""


def _append_in_block(content: str, block_marker: str, entry: str) -> str:
    """Insert `entry` just before the closing `]` of the block after marker."""
    start = content.index(block_marker)
    open_idx = content.index("[", start)
    close_idx = content.index("]", open_idx)
    block = content[open_idx:close_idx]

    if entry.strip() in block:
        return content

    indent = "    "
    for line in block.splitlines():
        stripped = line.strip()
        leading = line[: len(line) - len(line.lstrip())]
        if stripped and leading:
            indent = leading
            break

    return content[:close_idx] + indent + entry + "\n" + content[close_idx:]


def add_to_installed_apps(app_name: str) -> str:
    content = SETTINGS_PATH.read_text()
    entry = f"'{app_name}',"
    if entry in content.split("INSTALLED_APPS")[1].split("]")[0]:
        print(f"[*] '{app_name}' already in INSTALLED_APPS")
        return content
    updated = _append_in_block(content, "INSTALLED_APPS", entry)
    if updated != content:
        SETTINGS_PATH.write_text(updated)
        print(f"[+] '{app_name}' added to INSTALLED_APPS")
    return updated


def wire_url(app_name: str) -> str:
    content = URLS_PATH.read_text()
    entry = f"path('{app_name}/', include('{app_name}.urls')),"
    if entry.strip() in content.split("urlpatterns = [")[1].split("]")[0]:
        print(f"[*] '{app_name}' URL already wired in urls.py")
        return content
    updated = _append_in_block(content, "urlpatterns = [", entry)
    if updated != content:
        URLS_PATH.write_text(updated)
        print(f"[+] '{app_name}' URL wired to project urls.py")
    return updated


def ensure_app_urls(app_name: str) -> None:
    app_urls_path = BASE_DIR / app_name / "urls.py"
    if app_urls_path.exists():
        print(f"[*] '{app_name}/urls.py' already exists")
        return
    app_urls_path.write_text(APP_URLS_TEMPLATE.format(app_name=app_name))
    print(f"[+] '{app_name}/urls.py' created")


def register_app(app_name: str) -> None:
    app_dir = BASE_DIR / app_name
    if not app_dir.is_dir():
        subprocess.run(
            [sys.executable, "manage.py", "startapp", app_name], check=True
        )
        print(f"[+] App '{app_name}' created")

    add_to_installed_apps(app_name)
    wire_url(app_name)
    ensure_app_urls(app_name)
    print(f"\nDone! App '{app_name}' is registered.\n")


def main() -> None:
    apps = [a for a in sys.argv[1:] if a]
    if not apps:
        print(__doc__)
        sys.exit(1)

    for app in apps:
        register_app(app)


if __name__ == "__main__":
    main()