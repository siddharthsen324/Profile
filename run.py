"""
run.py - Unified launcher script for Siddharth Sen's Developer Profile
Starts the Flask REST backend and automatically opens the application in your browser.
"""

import sys
import threading
import time
import webbrowser
from backend.config import HOST, PORT, DEBUG
from backend.app import create_app

def open_browser():
    """Wait 1.2 seconds for server startup, then open browser."""
    time.sleep(1.2)
    url = f"http://{HOST}:{PORT}"
    print(f"\n[*] Opening application in browser: {url}")
    webbrowser.open_new_tab(url)

if __name__ == "__main__":
    print("=" * 65)
    print("  SIDDHARTH SEN - FULL-STACK DEVELOPER PROFILE & PLATFORM")
    print(f"  Backend & API Server: http://{HOST}:{PORT}/api/profile")
    print(f"  Public Portfolio:     http://{HOST}:{PORT}/")
    print(f"  Admin Dashboard:      http://{HOST}:{PORT}/admin.html")
    print("=" * 65)

    # Launch browser in a background daemon thread
    threading.Thread(target=open_browser, daemon=True).start()

    app = create_app()
    try:
        app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False)
    except KeyboardInterrupt:
        print("\n[*] Server shutdown cleanly.")
        sys.exit(0)
