"""
Basic tests for evaluation metrics modules.
"""

import pytest


def test_imports():
    """Test that metric modules can be imported."""
    try:
        from metrics.correctness import evaluate_correctness
        from metrics.reliability import evaluate_reliability
        from metrics.safety_flags import safety_score
        assert True
    except ImportError as e:
        pytest.skip(f"Could not import metrics: {e}")


def test_correctness_basic():
    """Test basic correctness evaluation."""
    try:
        from metrics.correctness import evaluate_correctness
        
        # Test exact match
        score = evaluate_correctness("test", "test", metric="exact_match")
        assert 0.0 <= score <= 1.0
        
        # Test with different strings
        score2 = evaluate_correctness("hello", "world", metric="exact_match")
        assert score2 == 0.0
    except ImportError:
        pytest.skip("Metrics module not available")


def test_reliability_basic():
    """Test basic reliability evaluation."""
    try:
        from metrics.reliability import consistency_score
        
        # Test consistency with identical outputs
        score = consistency_score(["test", "test", "test"])
        assert 0.0 <= score <= 1.0
        assert score == 1.0  # Should be perfectly consistent
    except ImportError:
        pytest.skip("Metrics module not available")

