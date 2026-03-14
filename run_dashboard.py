"""
run_dashboard.py — Entry point for the Retail Intelligence Platform (Streamlit)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import subprocess, signal

    port = int(os.environ.get("PORT", 8501))

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "src/ui/dashboard.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.fileWatcherType", "none",
        "--theme.base", "light",
    ]

    print(f"\nRetail Intelligence Platform")
    print(f"-> Running on port {port}\n")

    proc = subprocess.Popen(cmd)
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.send_signal(signal.SIGINT)
        proc.wait()