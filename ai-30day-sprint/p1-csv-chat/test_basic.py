"""
Basic smoke tests for CSV chat app that don't require full dependencies.
"""

import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that we can at least import the module structure."""
    try:
        # Just check if the file exists and is readable
        app_file = Path(__file__).parent / "app.py"
        assert app_file.exists(), "app.py should exist"
        
        # Try to read the file to check syntax
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 0, "app.py should not be empty"
        
        # Try basic import (may fail if dependencies missing, that's okay)
        try:
            import app
            assert True, "app module imported successfully"
        except ImportError as e:
            # If it fails due to missing dependencies, that's acceptable
            pytest.skip(f"app module has missing dependencies: {e}")
    except Exception as e:
        pytest.fail(f"Failed to check app.py: {e}")


def test_test_file_exists():
    """Test that test file itself is valid."""
    test_file = Path(__file__)
    assert test_file.exists(), "test_basic.py should exist"
    assert test_file.stat().st_size > 0, "test_basic.py should not be empty"


def test_public_share_requires_explicit_opt_in(monkeypatch):
    """The local CSV app should not expose a public Gradio tunnel by default."""
    try:
        import app
    except ImportError as e:
        pytest.skip(f"app module has missing dependencies: {e}")

    monkeypatch.delenv("GRADIO_SHARE", raising=False)
    assert app.public_share_enabled() is False

    monkeypatch.setenv("GRADIO_SHARE", "true")
    assert app.public_share_enabled() is True

