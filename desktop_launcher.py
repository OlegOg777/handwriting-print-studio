from __future__ import annotations

import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

from streamlit.web import bootstrap


def bundled_path(name: str) -> Path:
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return root / name


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def open_browser_when_ready(port: int) -> None:
    url = f"http://127.0.0.1:{port}"
    for _ in range(100):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                webbrowser.open_new(url)
                return
        except OSError:
            time.sleep(0.1)


def main() -> None:
    app_path = bundled_path("app.py")
    os.chdir(app_path.parent)
    port = free_port()

    flags = {
        "global.developmentMode": False,
        "server.port": port,
        "server.address": "127.0.0.1",
        "server.headless": True,
        "browser.gatherUsageStats": False,
        "server.fileWatcherType": "none",
    }
    bootstrap.load_config_options(flag_options=flags)
    threading.Thread(
        target=open_browser_when_ready,
        args=(port,),
        daemon=True,
    ).start()
    bootstrap.run(str(app_path), False, [], flags)


if __name__ == "__main__":
    main()
