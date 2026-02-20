"""
run_dashboard.py — Entry point for the Retail Intelligence Platform (Streamlit)
"""
import os
import sys

# ── Make sure the project root is on the Python path ─────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import subprocess, signal

    port = int(os.environ.get("PORT", 8501))

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "src/ui/dashboard.py",
        "--server.port",           str(port),
        "--server.headless",       "false",
        "--server.runOnSave",      "true",
        "--server.fileWatcherType","poll",
        "--theme.base",            "light",
    ]

    print(f"\n  Retail Intelligence Platform")
    print(f"  ->  Local:  http://localhost:{port}")
    print(f"  Press Ctrl+C to quit\n")

    proc = subprocess.Popen(cmd)
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.send_signal(signal.SIGINT)
        proc.wait()