"""
Generate HTML page from weekly summary JSON for GitHub Pages
"""

import json
import html
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from urllib.parse import urlparse


def _safe_external_href(url_raw) -> str:
    """Return an escaped HTTP(S) URL for href attributes, or # for unsafe input."""
    if not url_raw or url_raw == '#':
        return '#'

    url = str(url_raw).strip()
    parsed = urlparse(url)
    if parsed.scheme not in {'http', 'https'} or not parsed.netloc:
        return '#'

    return html.escape(url, quote=True)


def generate_html_page(summary_file: str = "results/weekly_summary.json", 
                       output_file: str = "../docs/ai-monitor.html"):
    """Generate HTML page from weekly summary"""
    
    summary_path = Path(summary_file)
    if not summary_path.exists():
        print(f"Warning: {summary_file} not found. Creating empty page.")
        html = generate_empty_html()
    else:
        with open(summary_path, 'r', encoding='utf-8') as f:
            summaries = json.load(f)
        
        html = generate_html_from_summaries(summaries)
    
    # Write to docs directory
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML page generated: {output_path}")


def generate_html_from_summaries(summaries: List[Dict]) -> str:
    """Generate HTML from summaries data"""
    
    if not summaries:
        return generate_empty_html()
    
    latest = summaries[-1]
    all_updates = latest.get('updates', [])
    
    # Group by keywords
    by_keyword = {}
    for update in all_updates:
        keywords = update.get('keywords', [])
        if not keywords:
            keywords = ['Other']
        for keyword in keywords:
            if keyword not in by_keyword:
                by_keyword[keyword] = []
            by_keyword[keyword].append(update)
    
    # Sort keywords by number of updates
    sorted_keywords = sorted(by_keyword.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Generate HTML
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Market Monitor - E2E AI Engineering</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary: #3b82f6;
            --primary-dark: #2563eb;
            --background: #1a1a1a;
            --card-bg: rgba(40, 40, 40, 0.7);
            --text: #f8fafc;
            --text-light: #cbd5e1;
            --text-muted: #94a3b8;
            --border: rgba(200, 200, 200, 0.1);
            --success: #10b981;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: radial-gradient(circle at 10% 20%, rgba(40, 40, 40, 0.8) 0%, rgba(26, 26, 26, 0.9) 90%);
            color: var(--text);
            line-height: 1.7;
            padding: 2rem 1rem;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem 0;
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, var(--primary), #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .subtitle {{
            color: var(--text-light);
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }}
        
        .meta {{
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 1rem;
        }}
        
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--primary);
            text-decoration: none;
            margin-bottom: 2rem;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            background: rgba(59, 130, 246, 0.1);
            transition: all 0.3s ease;
        }}
        
        .back-link:hover {{
            background: rgba(59, 130, 246, 0.2);
            transform: translateX(-3px);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 3rem;
        }}
        
        .stat-card {{
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            color: var(--text-light);
            font-size: 0.9rem;
        }}
        
        .keyword-section {{
            margin-bottom: 3rem;
        }}
        
        .keyword-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border);
        }}
        
        .keyword-title {{
            font-size: 1.5rem;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--primary);
        }}
        
        .keyword-count {{
            background: var(--primary);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }}
        
        .updates-list {{
            display: grid;
            gap: 1rem;
        }}
        
        .update-card {{
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
        }}
        
        .update-card:hover {{
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        }}
        
        .update-title {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--text);
        }}
        
        .update-title a {{
            color: var(--text);
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .update-title a:hover {{
            color: var(--primary);
        }}
        
        .update-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 0.75rem;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        
        .update-source {{
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }}
        
        .update-date {{
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }}
        
        .update-summary {{
            color: var(--text-light);
            line-height: 1.6;
            margin-top: 0.75rem;
        }}
        
        .update-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--primary);
            text-decoration: none;
            margin-top: 0.75rem;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .update-link:hover {{
            gap: 0.75rem;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-muted);
        }}
        
        .empty-state i {{
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2rem;
            }}
            
            .stats {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">
            <i class="fas fa-arrow-left"></i>
            Back to Portfolio
        </a>
        
        <header>
            <h1><i class="fas fa-robot"></i> AI Market Monitor</h1>
            <p class="subtitle">Weekly tracking of AI developments, models, and innovations</p>
            <div class="meta">
                Last updated: {html.escape(str(latest.get('date', 'N/A')))} | 
                Total updates this week: {len(all_updates)}
            </div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{len(all_updates)}</div>
                <div class="stat-label">Total Updates</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(by_keyword)}</div>
                <div class="stat-label">Companies/Models Tracked</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(set(u['source'] for u in all_updates))}</div>
                <div class="stat-label">Sources</div>
            </div>
        </div>
"""
    
    # Add keyword sections
    for keyword, updates in sorted_keywords:
        # Escape keyword for HTML
        escaped_keyword = html.escape(str(keyword).upper())
        
        html_output += f"""
        <div class="keyword-section">
            <div class="keyword-header">
                <span class="keyword-title">{escaped_keyword}</span>
                <span class="keyword-count">{len(updates)} updates</span>
            </div>
            <div class="updates-list">
"""
        
        for update in updates[:10]:  # Limit to 10 per keyword
            # Get and escape all user-controlled data
            title = html.escape(str(update.get('title', 'No title')))
            url = _safe_external_href(update.get('url', '#'))
            source = html.escape(str(update.get('source', 'Unknown')))
            date = html.escape(str(update.get('date', 'N/A')))
            summary = html.escape(str(update.get('summary', '')))
            
            html_output += f"""
                <div class="update-card">
                    <div class="update-title">
                        <a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>
                    </div>
                    <div class="update-meta">
                        <span class="update-source">
                            <i class="fas fa-newspaper"></i>
                            {source}
                        </span>
                        <span class="update-date">
                            <i class="fas fa-calendar"></i>
                            {date}
                        </span>
                    </div>
                    <div class="update-summary">{summary}</div>
                    <a href="{url}" target="_blank" rel="noopener noreferrer" class="update-link">
                        Read more <i class="fas fa-external-link-alt"></i>
                    </a>
                </div>
"""
        
        html_output += """
            </div>
        </div>
"""
    
    html_output += """
    </div>
</body>
</html>
"""
    
    return html_output


def generate_empty_html() -> str:
    """Generate empty state HTML"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Market Monitor - E2E AI Engineering</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #3b82f6;
            --background: #1a1a1a;
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at 10% 20%, rgba(40, 40, 40, 0.8) 0%, rgba(26, 26, 26, 0.9) 90%);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .container {
            text-align: center;
            max-width: 600px;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: var(--primary);
        }
        .empty-state {
            color: var(--text-muted);
        }
        .empty-state i {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        a {
            color: var(--primary);
            text-decoration: none;
            margin-top: 2rem;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="empty-state">
            <i class="fas fa-search"></i>
            <h1>No Data Yet</h1>
            <p>The weekly monitor hasn't run yet. Check back after the first scheduled run!</p>
            <a href="index.html">← Back to Portfolio</a>
        </div>
    </div>
</body>
</html>
"""


if __name__ == "__main__":
    generate_html_page()

