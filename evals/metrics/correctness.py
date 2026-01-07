"""
Correctness Metrics for LLM Agent Evaluation

This module provides metrics for evaluating the correctness of agent outputs.
"""

from typing import Any, Dict, List
import json

def exact_match(predicted: str, expected: str) -> float:
    """
    Exact match metric: returns 1.0 if strings match exactly, 0.0 otherwise.
    
    Args:
        predicted: The agent's output
        expected: The ground truth output
    
    Returns:
        Score between 0.0 and 1.0
    """
    return 1.0 if predicted.strip() == expected.strip() else 0.0

def semantic_similarity(predicted: str, expected: str, embedding_model=None) -> float:
    """
    Semantic similarity metric using embeddings.
    
    In a real implementation, this would:
    1. Generate embeddings for both strings
    2. Compute cosine similarity
    3. Return similarity score
    
    Args:
        predicted: The agent's output
        expected: The ground truth output
        embedding_model: Optional embedding model (e.g., sentence-transformers)
    
    Returns:
        Similarity score between 0.0 and 1.0
    """
    # Placeholder: In real implementation, use sentence-transformers or similar
    # from sentence_transformers import SentenceTransformer
    # model = embedding_model or SentenceTransformer('all-MiniLM-L6-v2')
    # embeddings = model.encode([predicted, expected])
    # similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    # return float(similarity)
    
    # Mock implementation
    if predicted.lower() == expected.lower():
        return 1.0
    return 0.7  # Placeholder

def structured_output_match(predicted: Dict[str, Any], expected: Dict[str, Any]) -> float:
    """
    Evaluate correctness of structured outputs (JSON, dicts).
    
    Args:
        predicted: Agent's structured output
        expected: Ground truth structured output
    
    Returns:
        Score between 0.0 and 1.0
    """
    if predicted == expected:
        return 1.0
    
    # Partial credit for matching keys
    predicted_keys = set(predicted.keys())
    expected_keys = set(expected.keys())
    
    key_overlap = len(predicted_keys & expected_keys) / len(expected_keys) if expected_keys else 0.0
    
    # Check value matches for overlapping keys
    value_matches = 0
    for key in predicted_keys & expected_keys:
        if predicted[key] == expected[key]:
            value_matches += 1
    
    value_score = value_matches / len(expected_keys) if expected_keys else 0.0
    
    # Weighted combination
    return 0.3 * key_overlap + 0.7 * value_score

def clinical_accuracy(predicted: str, expected: str, expert_review: bool = False) -> float:
    """
    Clinical accuracy metric for healthcare applications.
    
    Requires expert review for critical decisions.
    
    Args:
        predicted: Agent's output
        expected: Ground truth (expert-determined)
        expert_review: Whether this has been reviewed by domain expert
    
    Returns:
        Score between 0.0 and 1.0
    """
    if not expert_review:
        # Fallback to semantic similarity if no expert review
        return semantic_similarity(predicted, expected)
    
    # In real implementation, this would use expert-labeled scores
    return exact_match(predicted, expected)

def evaluate_correctness(predicted: Any, expected: Any, metric: str = "exact_match") -> float:
    """
    Main function to evaluate correctness using specified metric.
    
    Args:
        predicted: Agent's output (string or dict)
        expected: Ground truth (string or dict)
        metric: Metric to use ("exact_match", "semantic_similarity", "structured", "clinical")
    
    Returns:
        Score between 0.0 and 1.0
    """
    if metric == "exact_match":
        return exact_match(str(predicted), str(expected))
    elif metric == "semantic_similarity":
        return semantic_similarity(str(predicted), str(expected))
    elif metric == "structured":
        if isinstance(predicted, dict) and isinstance(expected, dict):
            return structured_output_match(predicted, expected)
        else:
            # Try to parse as JSON
            try:
                pred_dict = json.loads(predicted) if isinstance(predicted, str) else predicted
                exp_dict = json.loads(expected) if isinstance(expected, str) else expected
                return structured_output_match(pred_dict, exp_dict)
            except:
                return exact_match(str(predicted), str(expected))
    elif metric == "clinical":
        return clinical_accuracy(str(predicted), str(expected))
    else:
        raise ValueError(f"Unknown metric: {metric}")

