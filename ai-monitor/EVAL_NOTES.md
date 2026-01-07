# Evaluation Notes – AI Monitor

## What is Evaluated

### Coverage of Sources
- **Metric**: Number of unique sources per week (GitHub, Hugging Face, arXiv, Gitee, ModelScope, etc.)
- **Target**: 10+ unique sources per week
- **Current**: Tracking 8+ sources consistently

### Relevance of News
- **Metric**: Percentage of items that match AI keywords (DeepSeek, Kimi, Qwen, etc.)
- **Target**: 80%+ relevance
- **Current**: Using keyword filtering in `_is_relevant()` method

### Redundancy Detection
- **Metric**: Duplicate detection rate using content hashing
- **Target**: <5% duplicates
- **Current**: Using MD5 hashing on title+url+summary

### Agent Performance
- **Priority Scoring Agent**: Impact scores (1-10) for each discovery
- **Change Detection Agent**: Magnitude scores for significant changes
- **Summarization Agent**: Quality of executive summaries
- **Trend Analysis Agent**: Accuracy of trend identification

## Signals

### High-Signal Items
- **Metric**: Number of items with impact score >= 7
- **Target**: 3-5 high-signal items per week
- **Current**: Tracking in `latest_analysis.json`

### Overlap Across Agents
- **Metric**: Consistency of insights across different analysis agents
- **Target**: 70%+ agreement on top insights
- **Current**: Multiple agents analyze same data, compare outputs

### Failure Cases
- **Metric**: API failures, parsing errors, timeout errors
- **Target**: <2% failure rate
- **Current**: Error handling in place, but not systematically tracked

## Future Work

### LLM-Based Scoring
- Add LLM-based quality scoring for news items
- Evaluate relevance using embeddings
- Detect hallucinations in summaries

### Regression Test Suite
- Create test suite to detect drift in agent performance
- Track metrics over time (correctness, latency, coverage)
- Alert on significant changes

### Human-in-the-Loop
- Sample 5-10% of discoveries for human review
- Use expert feedback to improve agent prompts
- Build ground truth dataset for evaluation

### A/B Testing
- Compare different prompt strategies for agents
- Test different LLM models (GPT-4 vs Claude vs open-source)
- Evaluate impact of different tool configurations

## Evaluation Data

- **Weekly summaries**: `results/weekly_summary.json`
- **Analysis reports**: `results/latest_analysis.json`
- **Intelligence reports**: `results/intelligence_report_*.md`

## Related Files

- [Agent Architecture](AGENT_ARCHITECTURE.md)
- [Intelligence System](INTELLIGENCE_SYSTEM.md)
- [Evaluation Framework](../evals/README.md)

