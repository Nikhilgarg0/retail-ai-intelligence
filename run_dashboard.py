# run_dashboard.py
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import and run streamlit
import streamlit.web.cli as stcli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "src/ui/dashboard.py"]
    sys.exit(stcli.main())