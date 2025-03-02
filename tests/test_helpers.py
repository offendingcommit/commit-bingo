"""
Helper module for common test utilities and mocks
"""

import sys
from unittest.mock import MagicMock


def setup_mocks():
    """
    Set up common mocks for testing main.py
    This function needs to be called before importing main.py
    """
    # Create fake modules for nicegui
    nicegui_mock = MagicMock()
    ui_mock = MagicMock()
    nicegui_mock.ui = ui_mock

    # Replace the imports in sys.modules
    sys.modules["nicegui"] = nicegui_mock
    sys.modules["nicegui.ui"] = ui_mock
    sys.modules["fastapi.staticfiles"] = MagicMock()

    return nicegui_mock, ui_mock
