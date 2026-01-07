"""
Reliability Metrics for LLM Agent Evaluation

This module provides metrics for evaluating the reliability and consistency
of agent outputs across multiple runs.
"""

from typing import List, Dict, Any
import statistics
from collections import Counter

def consistency_score(outputs: List[str]) -> float:
    """
    Measure consistency of agent outputs across multiple runs with same input.
    
    Args:
        outputs: List of outputs from multiple runs
    
    Returns:
        Consistency score between 0.0 and 1.0 (higher is more consistent)
    """
    if len(outputs) <= 1:
        return 1.0
    
    # Exact match rate
    exact_matches = sum(1 for i in range(len(outputs)) 
                       for j in range(i+1, len(outputs)) 
                       if outputs[i] == outputs[j])
    total_pairs = len(outputs) * (len(outputs) - 1) / 2
    exact_match_rate = exact_matches / total_pairs if total_pairs > 0 else 1.0
    
    # Length consistency
    lengths = [len(output) for output in outputs]
    if lengths:
        length_cv = statistics.stdev(lengths) / statistics.mean(lengths) if statistics.mean(lengths) > 0 else 0
        length_score = 1.0 / (1.0 + length_cv)  # Lower coefficient of variation = higher score
    else:
        length_score = 1.0
    
    # Combined score
    return 0.7 * exact_match_rate + 0.3 * length_score

def latency_metrics(latencies_ms: List[float]) -> Dict[str, float]:
    """
    Compute latency statistics.
    
    Args:
        latencies_ms: List of latency measurements in milliseconds
    
    Returns:
        Dictionary with p50, p95, p99, mean, min, max
    """
    if not latencies_ms:
        return {}
    
    sorted_latencies = sorted(latencies_ms)
    n = len(sorted_latencies)
    
    return {
        'p50': sorted_latencies[int(n * 0.50)],
        'p95': sorted_latencies[int(n * 0.95)] if n > 1 else sorted_latencies[0],
        'p99': sorted_latencies[int(n * 0.99)] if n > 1 else sorted_latencies[0],
        'mean': statistics.mean(latencies_ms),
        'min': min(latencies_ms),
        'max': max(latencies_ms),
        'stdev': statistics.stdev(latencies_ms) if len(latencies_ms) > 1 else 0.0
    }

def uptime_percentage(successful_requests: int, total_requests: int) -> float:
    """
    Calculate uptime percentage.
    
    Args:
        successful_requests: Number of successful requests
        total_requests: Total number of requests
    
    Returns:
        Uptime percentage between 0.0 and 1.0
    """
    if total_requests == 0:
        return 1.0
    return successful_requests / total_requests

def error_rate(errors: List[str]) -> Dict[str, float]:
    """
    Analyze error patterns.
    
    Args:
        errors: List of error messages (empty string for successful requests)
    
    Returns:
        Dictionary with error rate and error type distribution
    """
    total = len(errors)
    error_count = sum(1 for e in errors if e)
    error_rate = error_count / total if total > 0 else 0.0
    
    # Count error types
    error_types = Counter([e.split(':')[0] if ':' in e else e for e in errors if e])
    
    return {
        'error_rate': error_rate,
        'success_rate': 1.0 - error_rate,
        'error_types': dict(error_types),
        'total_errors': error_count
    }

def reliability_score(consistency: float, uptime: float, 
                      error_rate: float, latency_p95_ms: float,
                      latency_threshold_ms: float = 5000.0) -> float:
    """
    Compute overall reliability score.
    
    Args:
        consistency: Consistency score (0-1)
        uptime: Uptime percentage (0-1)
        error_rate: Error rate (0-1)
        latency_p95_ms: 95th percentile latency in milliseconds
        latency_threshold_ms: Maximum acceptable latency
    
    Returns:
        Reliability score between 0.0 and 1.0
    """
    # Latency score (lower is better, normalized)
    latency_score = 1.0 if latency_p95_ms <= latency_threshold_ms else max(0.0, 1.0 - (latency_p95_ms - latency_threshold_ms) / latency_threshold_ms)
    
    # Weighted combination
    reliability = (
        0.3 * consistency +
        0.3 * uptime +
        0.2 * (1.0 - error_rate) +
        0.2 * latency_score
    )
    
    return max(0.0, min(1.0, reliability))

def evaluate_reliability(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluate reliability metrics from test results.
    
    Args:
        test_results: List of test result dictionaries with 'output', 'latency_ms', 'error' keys
    
    Returns:
        Dictionary with reliability metrics
    """
    # Group by test case ID to check consistency
    test_case_groups = {}
    for result in test_results:
        test_id = result.get('test_case_id', 'unknown')
        if test_id not in test_case_groups:
            test_case_groups[test_id] = []
        test_case_groups[test_id].append(result)
    
    # Compute consistency for each test case
    consistency_scores = []
    for test_id, results in test_case_groups.items():
        if len(results) > 1:
            outputs = [r.get('output', '') for r in results]
            consistency_scores.append(consistency_score(outputs))
    
    avg_consistency = statistics.mean(consistency_scores) if consistency_scores else 1.0
    
    # Compute latency metrics
    latencies = [r.get('latency_ms', 0) for r in test_results if 'latency_ms' in r]
    latency_stats = latency_metrics(latencies) if latencies else {}
    
    # Compute uptime
    errors = [r.get('error', '') for r in test_results]
    error_stats = error_rate(errors)
    uptime = error_stats.get('success_rate', 1.0)
    
    # Overall reliability score
    latency_p95 = latency_stats.get('p95', 0.0)
    overall_reliability = reliability_score(
        consistency=avg_consistency,
        uptime=uptime,
        error_rate=error_stats.get('error_rate', 0.0),
        latency_p95_ms=latency_p95
    )
    
    return {
        'overall_reliability': overall_reliability,
        'consistency': avg_consistency,
        'uptime': uptime,
        'error_rate': error_stats.get('error_rate', 0.0),
        'latency_metrics': latency_stats,
        'error_analysis': error_stats
    }

