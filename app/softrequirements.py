# softrequirements.py
from __future__ import annotations

def check() -> dict:
    """Define soft dependencies for the application."""
    return {
        "shinywidgets": "Required for Altair chart rendering",
        "altair": "Required for creating interactive charts",
        "anywidget": "Required for Jupyter widget support"
    }