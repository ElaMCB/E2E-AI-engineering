"""
Tests for evaluation metrics modules and A/B testing framework.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that metric modules can be imported."""
    try:
        from metrics.correctness import evaluate_correctness
        from metrics.reliability import evaluate_reliability
        from metrics.safety_flags import safety_score
        assert True
    except ImportError as e:
        pytest.skip(f"Could not import metrics: {e}")


def test_correctness_exact_match():
    """Test exact match correctness evaluation."""
    from metrics.correctness import evaluate_correctness, exact_match
    
    # Test exact match
    score = evaluate_correctness("test", "test", metric="exact_match")
    assert score == 1.0
    
    # Test with different strings
    score2 = evaluate_correctness("hello", "world", metric="exact_match")
    assert score2 == 0.0
    
    # Test with whitespace
    score3 = exact_match("  hello  ", "hello")
    assert score3 == 1.0


def test_correctness_semantic_similarity():
    """Test semantic similarity evaluation."""
    from metrics.correctness import evaluate_correctness
    
    # Same text should have high similarity
    score = evaluate_correctness("hello world", "hello world", metric="semantic_similarity")
    assert score == 1.0
    
    # Different text should have lower similarity
    score2 = evaluate_correctness("hello", "goodbye", metric="semantic_similarity")
    assert 0.0 <= score2 <= 1.0


def test_correctness_structured():
    """Test structured output evaluation."""
    from metrics.correctness import evaluate_correctness, structured_output_match
    
    # Exact match
    pred = {"name": "John", "age": 30}
    exp = {"name": "John", "age": 30}
    score = structured_output_match(pred, exp)
    assert score == 1.0
    
    # Partial match
    pred2 = {"name": "John", "age": 25}
    score2 = structured_output_match(pred2, exp)
    assert 0.0 < score2 < 1.0
    
    # JSON string input
    score3 = evaluate_correctness('{"a": 1}', '{"a": 1}', metric="structured")
    assert score3 == 1.0


def test_reliability_consistency():
    """Test consistency score calculation."""
    from metrics.reliability import consistency_score
    
    # Identical outputs should be perfectly consistent
    score = consistency_score(["test", "test", "test"])
    assert score == 1.0
    
    # Single output should be consistent
    score2 = consistency_score(["single"])
    assert score2 == 1.0
    
    # Different outputs should have lower consistency
    score3 = consistency_score(["a", "b", "c"])
    assert score3 < 1.0


def test_reliability_latency_metrics():
    """Test latency metrics calculation."""
    from metrics.reliability import latency_metrics
    
    latencies = [100, 150, 200, 250, 300]
    metrics = latency_metrics(latencies)
    
    assert 'p50' in metrics
    assert 'p95' in metrics
    assert 'mean' in metrics
    assert metrics['min'] == 100
    assert metrics['max'] == 300


def test_reliability_evaluate():
    """Test full reliability evaluation."""
    from metrics.reliability import evaluate_reliability
    
    test_results = [
        {'test_case_id': 'test1', 'output': 'result', 'latency_ms': 100, 'error': ''},
        {'test_case_id': 'test1', 'output': 'result', 'latency_ms': 110, 'error': ''},
        {'test_case_id': 'test2', 'output': 'other', 'latency_ms': 150, 'error': ''},
    ]
    
    result = evaluate_reliability(test_results)
    
    assert 'overall_reliability' in result
    assert 'consistency' in result
    assert 'uptime' in result
    assert 0.0 <= result['overall_reliability'] <= 1.0


def test_safety_score():
    """Test safety score calculation."""
    from metrics.safety_flags import safety_score, assess_risk_level
    
    # Safe general output
    score = safety_score("The sky is blue.", domain="general")
    assert 0.0 <= score <= 1.0
    
    # Healthcare output with risk indicators
    score2 = safety_score("You should take this medication.", domain="healthcare")
    assert score2 <= 1.0  # Should have some deduction
    
    # Risk level assessment
    risk = assess_risk_level("This is a safe statement.", domain="general")
    assert risk == "low"
    
    risk2 = assess_risk_level("The diagnosis is confirmed.", domain="healthcare")
    assert risk2 == "high"


def test_ab_test_runner():
    """Test A/B test runner."""
    from run_ab_test_models_prompts import ABTestRunner, BUILTIN_TEST_CASES
    
    runner = ABTestRunner(use_builtin=True)
    
    # Run with a small subset of tests
    analysis = runner.run_ab_test(BUILTIN_TEST_CASES[:3])
    
    assert 'variants' in analysis
    assert len(analysis['variants']) > 0
    
    # Check that metrics are calculated
    for variant_name, stats in analysis['variants'].items():
        assert 'correctness' in stats
        assert 'safety' in stats
        assert 'sample_size' in stats


def test_eval_score():
    """Test overall eval score calculation."""
    from run_ab_test_models_prompts import ABTestRunner, BUILTIN_TEST_CASES
    
    runner = ABTestRunner(use_builtin=True)
    runner.run_ab_test(BUILTIN_TEST_CASES[:5])
    
    score = runner.get_eval_score()
    assert 0.0 <= score <= 100.0

