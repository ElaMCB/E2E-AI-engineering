# LLM Agent Evaluation

This folder contains examples of:

- **High-throughput evaluation pipelines** for agents
- **A/B tests** across models, prompts, and tools
- **Patterns for human-in-the-loop** / expert-labeled benchmarks
- **Post-deployment style sampling and monitoring**

These examples are inspired by Applied AI roles that lead evaluation of LLM agents in production.

## Structure

```
evals/
  ├── README.md                              # This file
  ├── canvas_style_clinical_eval.md          # JD-aligned description
  ├── eval_config_examples.yaml              # Configuration examples
  ├── run_ab_test_models_prompts.py          # A/B testing framework
  └── metrics/
      ├── correctness.py                     # Correctness metrics
      ├── safety_flags.py                    # Safety evaluation
      └── reliability.py                     # Reliability metrics
      └── runtime_observability.py           # Runtime traces + CI thresholds
```

## Evaluation Lifecycle

1. **Unit Tests**: Fast, deterministic checks on individual components
2. **E2E Tests**: Full workflow validation with realistic inputs
3. **A/B Testing**: Compare models, prompts, and tool configurations
4. **Human-in-the-Loop**: Expert-labeled benchmarks for critical decisions
5. **Post-Deployment Monitoring**: Continuous sampling and drift detection
6. **Runtime Guardrails**: Trace-based thresholds for success rate/latency/step count

## Key Patterns

### High-Throughput Evaluation

Run thousands of test cases across multiple models and prompts to identify regressions and improvements.

### Expert-Determined Ground Truth

For critical applications (healthcare, finance), use domain experts to establish ground truth outcomes.

### Regression Testing

Automated test suites that detect when agent performance degrades after changes.

### Sampling & Governance

Post-deployment monitoring with statistical sampling to ensure agents maintain quality in production.

## Related Projects

- **AI Monitor** (`../ai-monitor/`) - Multi-agent system with evaluation of news quality
- **Excel/CSV Chat** (`../excel-csv-chat-RAG/`) - RAG pipeline with data QA evaluation
- **Healthcare Case Study** (`../docs/canvas_agent_eval_case_study.md`) - Healthcare evaluation example

