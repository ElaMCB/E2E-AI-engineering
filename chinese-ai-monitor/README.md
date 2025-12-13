# AI Market Weekly Monitor

Automated weekly monitoring system to track AI market advances, new models, and innovations. Get early alerts about developments from companies like DeepSeek, Kimi, Zhipu AI, Baichuan, and others.

## Purpose

Stay ahead of AI developments by automatically searching and tracking:
- New AI models and releases (DeepSeek, Kimi, Qwen, etc.)
- AI company announcements
- AI innovations and breakthroughs
- Market trends and competitive intelligence

## Features

- **Multi-source Search**: Combines Gitee, ModelScope, GitHub, Hugging Face, arXiv, DuckDuckGo, RSS feeds, and NewsAPI
- **Gitee Integration**: Monitors China's primary code hosting platform (10M+ repos) - often first to see releases
- **ModelScope Integration**: Tracks Alibaba's AI platform (70K+ models, 16M developers) - major AI hub
- **GitHub Integration**: Monitors repositories, releases, and code updates
- **Hugging Face Integration**: Tracks new model releases and updates
- **arXiv Integration**: Discovers research papers and publications
- **Deduplication**: Automatically filters duplicate articles
- **Keyword Tracking**: Monitors specific AI companies and models
- **Weekly Reports**: Generates markdown reports with summaries
- **Historical Tracking**: Maintains 12 weeks of history
- **No API Keys Required**: Works with GitHub, Hugging Face, arXiv, DuckDuckGo and RSS feeds out of the box

## 2025 Publication Trends

Based on analysis of AI company publication patterns throughout 2025:

### Key Platforms (Priority Order)
1. **Gitee** - China's primary code hosting (10M+ repos, 5M+ users) - Often first to see releases
2. **ModelScope** - Alibaba's platform (70K+ models, 16M developers) - Major AI hub
3. **GitHub** - International releases, open-source code
4. **Hugging Face** - Model distribution and weights
5. **arXiv** - Research papers and technical documentation
6. **Company Blogs** - Official announcements

### 2025 Trends
- **Open-Source Strategy**: Models account for ~40% of global AI models (Sept 2025)
- **Cost Advantage**: LLMs cost ~1/5 of foreign counterparts
- **Multi-Platform Publishing**: Companies publish simultaneously on Gitee, GitHub, Hugging Face
- **Rapid Iteration**: Multiple versions released throughout the year
- **Timing Patterns**: Major releases in Q1 (DeepSeek-R1), Q2 (open-source push), Q3 (Alibaba Qwen-3), Q4 (year-end updates)

See [PUBLICATION_TRENDS.md](PUBLICATION_TRENDS.md) for detailed analysis.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure (Optional)

Edit `config.json` to customize:
- Search terms (add more AI companies/models)
- RSS feeds (add more news sources)
- GitHub token (optional, for higher rate limits)
- NewsAPI key (optional, for more results)
- Enable/disable specific sources (GitHub, Hugging Face, arXiv, etc.)

### 3. Run Manually

```bash
python monitor.py
```

This will:
- Search all configured sources
- Save results to `results/` directory
- Generate a weekly report
- Track seen articles to avoid duplicates

## Schedule Weekly Runs

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Weekly" (choose your day/time)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\chinese-ai-monitor\monitor.py`
7. Start in: `C:\path\to\chinese-ai-monitor`

Or use PowerShell:

```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\path\to\chinese-ai-monitor\monitor.py" -WorkingDirectory "C:\path\to\chinese-ai-monitor"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9AM
Register-ScheduledTask -TaskName "AIMonitor" -Action $action -Trigger $trigger
```

### Linux/Mac (Cron)

```bash
# Edit crontab
crontab -e

# Add this line to run every Monday at 9 AM
0 9 * * 1 cd /path/to/chinese-ai-monitor && /usr/bin/python3 monitor.py >> logs/monitor.log 2>&1
```

### GitHub Actions (Cloud-based)

Create `.github/workflows/weekly-ai-monitor.yml`:

```yaml
name: Weekly AI Monitor

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  workflow_dispatch:  # Allow manual runs

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r chinese-ai-monitor/requirements.txt
      - name: Run monitor
        run: python chinese-ai-monitor/monitor.py
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: ai-monitor-results
          path: chinese-ai-monitor/results/
```

## Output Files

Results are saved in the `results/` directory:

- `ai_updates_YYYYMMDD_HHMMSS.json` - Individual run results
- `weekly_summary.json` - Last 12 weeks of summaries
- `report_YYYYMMDD.md` - Human-readable markdown report
- `seen_hashes.json` - Tracks seen articles (for deduplication)

## Configuration

### Search Terms

Add more AI companies/models to track in `config.json`:

```json
{
  "search_terms": [
    "Your New AI Model",
    "Another AI Company"
  ]
}
```

### RSS Feeds

Add more news sources:

```json
{
  "rss_feeds": [
    "https://your-news-source.com/feed"
  ]
}
```

### GitHub Token (Optional)

Get a GitHub personal access token from [GitHub Settings](https://github.com/settings/tokens) for higher rate limits:

```json
{
  "github_token": "ghp_your_token_here"
}
```

### Gitee Token (Optional)

Get a Gitee personal access token from [Gitee Settings](https://gitee.com/profile/personal_access_tokens) for higher rate limits:

```json
{
  "gitee_token": "your_gitee_token_here"
}
```

### NewsAPI (Optional)

Get a free API key from [newsapi.org](https://newsapi.org) and add to `config.json`:

```json
{
  "news_api_key": "your-api-key-here"
}
```

### Enable/Disable Sources

Control which sources to search (prioritized in order):

```json
{
  "gitee_enabled": true,
  "modelscope_enabled": true,
  "github_enabled": true,
  "huggingface_enabled": true,
  "arxiv_enabled": true,
  "duckduckgo_enabled": true
}
```

**Note**: Gitee and ModelScope are searched first as they're often the earliest sources for AI releases.

## Example Report

```
# AI Market Weekly Report
## Date: 2025-01-13
## Total Updates: 15

### DEEPSEEK (3 updates)

- **DeepSeek Releases New Model**
  - Source: TechCrunch
  - URL: https://...
  - Summary: DeepSeek announced...

### KIMI (2 updates)

- **Kimi AI Expands Features**
  - Source: The Verge
  - URL: https://...
  - Summary: Moonshot AI's Kimi...
```

## Tracked Companies/Models

Currently monitoring:
- **DeepSeek** - Deep learning research company
- **Kimi** - Moonshot AI's conversational AI
- **Zhipu AI (智谱AI)** - GLM model series
- **Baichuan (百川智能)** - Open-source LLM
- **01.AI (零一万物)** - Yi model series
- **Moonshot AI (月之暗面)** - Kimi creator
- **MiniMax** - Multimodal AI
- **Ernie Bot (文心一言)** - Baidu's AI
- **Qwen (通义千问)** - Alibaba's model
- **Doubao (豆包)** - ByteDance's AI

## 🔍 How It Works

1. **Search Phase**: Queries multiple sources using configured search terms
2. **Filtering**: Keeps only articles relevant to AI
3. **Deduplication**: Removes articles seen in previous runs
4. **Keyword Extraction**: Identifies which models/companies are mentioned
5. **Storage**: Saves results in JSON and generates markdown reports

## Tips

- Run manually first to test configuration
- Check `results/` directory after first run
- Review `weekly_summary.json` to see historical trends
- Add more RSS feeds for better coverage
- Consider adding NewsAPI key for more comprehensive results

## Troubleshooting

**No results found?**
- Check internet connection
- Verify RSS feeds are accessible
- Try running with fewer search terms

**Duplicate results?**
- Check that `seen_hashes.json` is being saved
- Clear `seen_hashes.json` to reset deduplication

**Import errors?**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

## License

Part of the E2E-AI-engineering portfolio project.

