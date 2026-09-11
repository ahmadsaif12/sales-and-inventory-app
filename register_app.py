#!/usr/bin/env python3

"""Create and register Django apps automatically.

Usage:

    make register APP=accounts
    make register APP="accounts users products"

    python register_app.py accounts
    python register_app.py accounts users products
"""

import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

SETTINGS_PATH = BASE_DIR / "InventoryMS" / "settings.py"
URLS_PATH = BASE_DIR / "InventoryMS" / "urls.py"


APP_URLS_TEMPLATE = """from django.urls import path
from . import views

app_name = "{app_name}"

urlpatterns = [
    # path("", views.home, name="home"),
]
"""


def add_to_installed_apps(app_name: str) -> None:
    """Add app to INSTALLED_APPS if it is not already registered."""

    content = SETTINGS_PATH.read_text()

    installed_apps_start = content.find("INSTALLED_APPS")

    if installed_apps_start == -1:
        raise RuntimeError("INSTALLED_APPS not found in settings.py")

    installed_apps_end = content.find("]", installed_apps_start)

    if installed_apps_end == -1:
        raise RuntimeError("Could not find end of INSTALLED_APPS")

    block = content[installed_apps_start:installed_apps_end]

    if f"'{app_name}'" in block or f'"{app_name}"' in block:
        print(f"[*] '{app_name}' already in INSTALLED_APPS")
        return

    entry = f"    '{app_name}',\n"

    content = (
        content[:installed_apps_end]
        + entry
        + content[installed_apps_end:]
    )

    SETTINGS_PATH.write_text(content)

    print(f"[+] '{app_name}' added to INSTALLED_APPS")


def ensure_include_import() -> None:
    """Make sure project urls.py imports include."""

    content = URLS_PATH.read_text()

    if "from django.urls import include, path" in content:
        return

    if "from django.urls import path" in content:
        content = content.replace(
            "from django.urls import path",
            "from django.urls import include, path",
            1,
        )
    else:
        content = "from django.urls import include, path\n" + content

    URLS_PATH.write_text(content)

    print("[+] Added 'include' import to project urls.py")


def wire_url(app_name: str) -> None:
    """Add app URL to project urls.py."""

    content = URLS_PATH.read_text()

    entry = f"    path('{app_name}/', include('{app_name}.urls')),\n"

    if entry.strip() in content:
        print(f"[*] '{app_name}' URL already wired")
        return

    urlpatterns_start = content.find("urlpatterns")

    if urlpatterns_start == -1:
        raise RuntimeError("urlpatterns not found in project urls.py")

    open_bracket = content.find("[", urlpatterns_start)

    if open_bracket == -1:
        raise RuntimeError("Could not find urlpatterns list")

    content = (
        content[:open_bracket + 1]
        + "\n"
        + entry
        + content[open_bracket + 1:]
    )

    URLS_PATH.write_text(content)

    print(f"[+] '{app_name}' URL wired to project urls.py")


def ensure_app_urls(app_name: str) -> None:
    """Create app urls.py if it does not exist."""

    app_urls_path = BASE_DIR / app_name / "urls.py"

    if app_urls_path.exists():
        print(f"[*] '{app_name}/urls.py' already exists")
        return

    app_urls_path.write_text(
        APP_URLS_TEMPLATE.format(app_name=app_name)
    )

    print(f"[+] '{app_name}/urls.py' created")


def create_app(app_name: str) -> None:
    """Create Django app if it does not already exist."""

    app_dir = BASE_DIR / app_name

    if app_dir.is_dir():
        print(f"[*] App '{app_name}' already exists")
        return

    subprocess.run(
        [
            sys.executable,
            "manage.py",
            "startapp",
            app_name,
        ],
        cwd=BASE_DIR,
        check=True,
    )

    print(f"[+] App '{app_name}' created")


def register_app(app_name: str) -> None:
    """Create and completely register one Django app."""

    print(f"\n=== Registering app: {app_name} ===")

    create_app(app_name)
    add_to_installed_apps(app_name)
    ensure_include_import()
    ensure_app_urls(app_name)
    wire_url(app_name)

    print(f"\nDone! App '{app_name}' is ready.\n")


def main() -> None:
    apps = [app.strip() for app in sys.argv[1:] if app.strip()]

    if not apps:
        print(__doc__)
        sys.exit(1)

    for app_name in apps:
        register_app(app_name)


if __name__ == "__main__":
    main()