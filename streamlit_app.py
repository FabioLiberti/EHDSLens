"""
EHDSLens Streamlit Cloud Entry Point

This file is the entry point for Streamlit Cloud deployment.
It simply imports and runs the dashboard from the installed package.
"""

# For Streamlit Cloud, we need to ensure the package is in the path
import sys
from pathlib import Path

# Add src to path for local development
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

# Import and run the dashboard
from ehdslens.dashboard import create_dashboard

if __name__ == "__main__":
    create_dashboard()
else:
    # When run by Streamlit
    create_dashboard()
