"""
Tests for configuration loader
"""

import pytest
from pathlib import Path
from src.core.config_loader import ConfigLoader

def test_config_loader_missing_file():
    """
    Test that ConfigLoader raises error for missing file
    """
    loader = ConfigLoader("nonexistent.yaml")
    with pytest.raises(FileNotFoundError):
        loader.load()

# Additional tests to be implemented
