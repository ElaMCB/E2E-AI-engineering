# Clinical Agent Evaluation

This document describes evaluation patterns for LLM agents in healthcare/clinical settings.

## Evaluation Requirements

### High-Fidelity Unit Tests

Test individual agent components with deterministic inputs:

- **Tool calling accuracy**: Verify agents call correct tools with correct parameters
- **Output format validation**: Ensure structured outputs match expected schemas
- **Error handling**: Test graceful degradation when tools fail

### End-to-End Evaluation

Full workflow validation with realistic clinical scenarios:

- **Patient data extraction**: Test accuracy of extracting structured data from unstructured notes
- **Clinical decision support**: Validate recommendations against clinical guidelines
- **Multi-step workflows**: Test complex agent chains (extract → analyze → recommend)

### Expert-Labeled Benchmarks

Domain experts establish ground truth for critical decisions:

- **Clinical accuracy**: Expert review of agent outputs for medical correctness
- **Safety flags**: Identify potentially harmful recommendations
- **Compliance**: Ensure outputs meet regulatory requirements

## Evaluation Metrics

### Correctness

- **Exact match**: Output matches expected ground truth exactly
- **Semantic similarity**: Use embeddings to measure meaning similarity
- **Clinical accuracy**: Expert-reviewed correctness for medical decisions

### Safety

- **Hallucination detection**: Identify when agents generate unsupported information
- **Contradiction detection**: Flag outputs that contradict established facts
- **Risk scoring**: Assess potential harm from agent recommendations

### Reliability

- **Consistency**: Same input produces similar outputs across runs
- **Latency**: Response time meets clinical workflow requirements
- **Uptime**: System availability for critical workflows

## A/B Testing Framework

Compare different configurations:

- **Models**: GPT-4 vs Claude vs open-source alternatives
- **Prompts**: Different prompt engineering strategies
- **Tools**: Various tool combinations and configurations
- **RAG sources**: Different knowledge bases and retrieval strategies

## Post-Deployment Monitoring

### Statistical Sampling

- Sample 1-5% of production requests for expert review
- Track metrics over time to detect drift
- Alert on significant changes in performance

### Governance

- Maintain audit logs of all agent decisions
- Regular review cycles with clinical experts
- Version control for prompts and model configurations

## Implementation

See `run_ab_test_models_prompts.py` for example A/B testing framework and `metrics/` for evaluation metric implementations.

