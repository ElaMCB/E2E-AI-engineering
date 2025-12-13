# AI Market Intelligence System

## Overview

This system transforms raw weekly discoveries into actionable intelligence using a multi-agent architecture. Instead of reading through hundreds of updates, you get:

- **Executive Summary** - What happened this week in 2-3 sentences
- **Top Insights** - Ranked by impact score (0-10)
- **Significant Changes** - Week-over-week changes detected
- **Actionable Recommendations** - What to do next

## Architecture

### Multi-Agent System

1. **Priority Scoring Agent**
   - Scores each update (0-10) based on:
     - Type (new model, release, research paper)
     - Source credibility
     - Company importance
     - Recency
   - Ranks top 10 insights

2. **Change Detection Agent**
   - Compares current week vs previous weeks
   - Detects:
     - New companies/models entering market
     - Activity spikes (50%+ increase)
     - Emerging trends
   - Calculates change magnitude

3. **Summarization Agent**
   - Creates executive summary
   - Identifies key highlights
   - Detects patterns and trends

4. **Trend Analysis Agent**
   - Analyzes 4+ weeks of data
   - Identifies long-term trends
   - Predicts emerging patterns

### LLM-Powered Analysis (Optional)

For even deeper insights, use `llm_analyzer.py` with:
- DeepSeek API
- OpenAI API
- Any OpenAI-compatible API

The LLM provides:
- Natural language summaries
- Context-aware insights
- Strategic recommendations

## Usage

### Basic Analysis (No API Key Required)

```bash
cd ai-monitor
python analyzer.py
```

This runs all agents and generates:
- `results/latest_analysis.json` - Full analysis data
- `results/analysis_YYYYMMDD.json` - Timestamped analysis
- `results/intelligence_report_YYYYMMDD.md` - Human-readable report

### LLM-Powered Analysis (Requires API Key)

```bash
# Set API key
export DEEPSEEK_API_KEY="your-key-here"
# or
export OPENAI_API_KEY="your-key-here"

# Run LLM analysis
python llm_analyzer.py
```

### View Intelligence Dashboard

The system automatically generates `docs/intelligence.html` which shows:
- Executive summary
- Top insights ranked by impact
- Significant changes
- Recommendations

Access at: `https://elamcb.github.io/E2E-AI-engineering/intelligence.html`

## What Top Performers Do

### 1. **Automated Prioritization**
   - Don't read everything
   - Focus on top 5-10 insights (impact score ≥ 7.0)
   - Review high-impact items first

### 2. **Change Detection**
   - Monitor week-over-week changes
   - Identify new market entrants early
   - Spot activity spikes (potential major announcements)

### 3. **Trend Analysis**
   - Track 4-week trends
   - Identify emerging companies
   - Predict market shifts

### 4. **Actionable Intelligence**
   - Get recommendations, not just data
   - Know what to monitor next
   - Understand implications

### 5. **Strategic Monitoring**
   - Add new entities to watchlist
   - Adjust search terms based on trends
   - Focus resources on high-impact areas

## Integration with Weekly Monitor

The intelligence system runs automatically after the weekly monitor:

1. Monitor collects raw data → `weekly_summary.json`
2. Analyzer processes data → `latest_analysis.json`
3. Intelligence page generated → `intelligence.html`
4. All committed to GitHub automatically

## Example Output

### Executive Summary
"This week saw 14 updates across 3 companies/models. Top activity: KIMI, DEEPSEEK, MOONSHOT"

### Top Insight
"GitHub: kimi-ai-2api - Impact: 8.5/10
Transform Kimi.ai chat experiences into OpenAI API format"

### Significant Change
"Market Shift: Activity increased 50% (8 → 14 updates)
Implications: Increased market activity - monitor closely"

### Recommendation
"URGENT: 3 high-impact developments detected - review immediately"

## Customization

### Adjust Priority Scoring

Edit `analyzer.py` → `PriorityScoringAgent._calculate_score()` to:
- Change scoring weights
- Add custom rules
- Prioritize specific companies

### Add Custom Agents

Create new agent class inheriting from `AnalysisAgent`:

```python
class CustomAgent(AnalysisAgent):
    def analyze(self, updates, historical_data):
        # Your analysis logic
        return insights
```

Then add to `IntelligentAnalyzer.__init__()`.

## Best Practices

1. **Review Top 5 Insights Daily** - Don't get overwhelmed
2. **Monitor Changes Weekly** - Track what's new
3. **Act on Recommendations** - System tells you what to do
4. **Use LLM for Deep Dives** - When you need context
5. **Track Trends Monthly** - Understand long-term patterns

## Performance Tips

- **High-Impact Threshold**: Only review insights with score ≥ 7.0
- **Focus on Changes**: New entities and spikes are most important
- **Use Intelligence Page**: Visual dashboard is faster than reading JSON
- **Set Up Alerts**: Get notified when impact score ≥ 9.0

