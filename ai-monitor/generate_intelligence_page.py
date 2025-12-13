"""
Generate HTML page for intelligence/analysis results
Shows top insights, changes, and recommendations
"""

import json
import html
from pathlib import Path
from datetime import datetime
from typing import Dict
import pytz


def generate_intelligence_page(analysis_file: str = "results/latest_analysis.json",
                               output_file: str = "../docs/intelligence.html"):
    """Generate HTML page from analysis results"""
    
    analysis_path = Path(analysis_file)
    if not analysis_path.exists():
        html_output = generate_empty_intelligence_html()
    else:
        with open(analysis_path, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        html_output = generate_html_from_analysis(analysis)
    
    # Write to docs directory
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"Intelligence page generated: {output_path}")


def generate_html_from_analysis(analysis: Dict) -> str:
    """Generate HTML from analysis data"""
    
    exec_summary = analysis.get('executive_summary', {})
    top_insights = analysis.get('top_insights', [])
    changes = analysis.get('significant_changes', [])
    recommendations = analysis.get('recommendations', [])
    
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Market Intelligence - E2E AI Engineering</title>
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
            --warning: #f59e0b;
            --danger: #ef4444;
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
        
        .alert-box {{
            background: var(--card-bg);
            border-left: 4px solid var(--primary);
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
        
        .insight-card {{
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }}
        
        .insight-card:hover {{
            border-color: var(--primary);
            transform: translateY(-2px);
        }}
        
        .impact-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-left: 1rem;
        }}
        
        .impact-high {{
            background: var(--danger);
            color: white;
        }}
        
        .impact-medium {{
            background: var(--warning);
            color: white;
        }}
        
        .impact-low {{
            background: var(--success);
            color: white;
        }}
        
        .recommendation {{
            background: rgba(59, 130, 246, 0.1);
            border-left: 3px solid var(--primary);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link" style="display: inline-flex; align-items: center; gap: 0.5rem; color: var(--primary); text-decoration: none; margin-bottom: 2rem; padding: 0.5rem 1rem; border-radius: 8px; background: rgba(59, 130, 246, 0.1);">
            <i class="fas fa-arrow-left"></i>
            Back to Portfolio
        </a>
        
        <header>
            <h1><i class="fas fa-brain"></i> AI Market Intelligence</h1>
            <p style="color: var(--text-light); font-size: 1.1rem; margin-top: 0.5rem;">
                Intelligent analysis of weekly AI discoveries
            </p>
            <div style="color: var(--text-muted); font-size: 0.9rem; margin-top: 1rem;">
                Analysis Date: {html.escape(str(analysis.get('date', 'N/A')))}
            </div>
        </header>
        
        <div class="alert-box" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.05)); border-left: 4px solid var(--primary); margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                <i class="fas fa-user-circle" style="font-size: 1.5rem; color: var(--primary);"></i>
                <div style="flex: 1;">
                    <h3 style="margin: 0; color: var(--primary); font-size: 1.2rem; font-weight: 600;">
                        {html.escape(personal['greeting'])}
                    </h3>
                    <p style="margin: 0.25rem 0 0 0; color: var(--text-muted); font-size: 0.85rem;">
                        {html.escape(personal['time'])}
                    </p>
                </div>
            </div>
            <p style="color: var(--text-light); line-height: 1.8; margin-top: 0.75rem; font-size: 1rem;">
                {html.escape(personal['message'])}
            </p>
        </div>
        
        <div class="alert-box">
            <h3 style="margin-bottom: 1rem; color: var(--primary);">
                <i class="fas fa-lightbulb"></i> Executive Summary
            </h3>
            <p style="color: var(--text-light); line-height: 1.8;">
                {html.escape(str(exec_summary.get('summary', 'No summary available')))}
            </p>
        </div>
        
        <section style="margin-bottom: 3rem;">
            <h2 style="margin-bottom: 1.5rem; color: var(--text);">
                <i class="fas fa-star"></i> Top Insights (Priority Ranked)
            </h2>
"""
    
    # Add top insights
    for i, insight in enumerate(top_insights[:10], 1):
        impact_score = insight.get('impact_score', 0)
        impact_class = 'impact-high' if impact_score >= 8 else 'impact-medium' if impact_score >= 6 else 'impact-low'
        
        html_output += f"""
            <div class="insight-card">
                <h3 style="margin-bottom: 0.5rem; color: var(--text);">
                    {i}. {html.escape(str(insight.get('title', 'No title')))}
                    <span class="impact-badge {impact_class}">Impact: {impact_score:.1f}/10</span>
                </h3>
                <p style="color: var(--text-light); margin-bottom: 0.5rem;">
                    {html.escape(str(insight.get('description', '')[:300]))}...
                </p>
                <div style="font-size: 0.85rem; color: var(--text-muted);">
                    <span>Type: {html.escape(str(insight.get('type', 'N/A')))}</span> | 
                    <span>Source: {', '.join([html.escape(s) for s in insight.get('evidence', [])])}</span>
                </div>
            </div>
"""
    
    html_output += """
        </section>
        
        <section style="margin-bottom: 3rem;">
            <h2 style="margin-bottom: 1.5rem; color: var(--text);">
                <i class="fas fa-chart-line"></i> Significant Changes
            </h2>
"""
    
    # Add changes
    for change in changes:
        html_output += f"""
            <div class="insight-card">
                <h3 style="margin-bottom: 0.5rem; color: var(--text);">
                    {html.escape(str(change.get('category', 'N/A')).replace('_', ' ').title())}
                    <span class="impact-badge impact-medium">Magnitude: {change.get('magnitude', 0):.1f}/10</span>
                </h3>
                <p style="color: var(--text-light); margin-bottom: 1rem;">
                    {html.escape(str(change.get('description', 'N/A')))}
                </p>
                <div>
                    <strong style="color: var(--text);">Implications:</strong>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; color: var(--text-light);">
"""
        for impl in change.get('implications', []):
            html_output += f"                        <li>{html.escape(str(impl))}</li>\n"
        
        html_output += """
                    </ul>
                </div>
            </div>
"""
    
    html_output += """
        </section>
        
        <section style="margin-bottom: 3rem;">
            <h2 style="margin-bottom: 1.5rem; color: var(--text);">
                <i class="fas fa-tasks"></i> Recommendations
            </h2>
"""
    
    # Add recommendations
    for rec in recommendations:
        html_output += f"""
            <div class="recommendation">
                <i class="fas fa-check-circle" style="color: var(--primary); margin-right: 0.5rem;"></i>
                {html.escape(str(rec))}
            </div>
"""
    
    html_output += """
        </section>
    </div>
    
    <!-- Footer -->
    <footer style="text-align: center; padding: 2rem; margin-top: 4rem; border-top: 1px solid var(--border); color: var(--text-muted); background: var(--card-bg);">
        <p style="margin: 0.5rem 0; color: var(--text-light);">
            © 2025 E2E AI Engineering | 
            <a href="https://github.com/ElaMCB/E2E-AI-engineering" style="color: var(--primary); text-decoration: none;">GitHub</a> | 
            <a href="index.html" style="color: var(--primary); text-decoration: none;">Portfolio</a> | 
            <a href="ai-monitor.html" style="color: var(--primary); text-decoration: none;">Raw Data</a> | 
            Visitors: <span id="footer-visitor-counter" style="color: var(--primary); font-weight: 600;">...</span>
        </p>
    </footer>
    
    <!-- Visitor Tracking -->
    <script src="analytics.js"></script>
</body>
</html>
"""
    
    return html_output


def generate_empty_intelligence_html() -> str:
    """Generate empty state HTML"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Market Intelligence - E2E AI Engineering</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at 10% 20%, rgba(40, 40, 40, 0.8) 0%, rgba(26, 26, 26, 0.9) 90%);
            color: #f8fafc;
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
            color: #3b82f6;
        }
        a {
            color: #3b82f6;
            text-decoration: none;
            margin-top: 2rem;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>No Analysis Available</h1>
        <p style="color: #94a3b8;">Run the analyzer to generate intelligence reports.</p>
        <a href="index.html">← Back to Portfolio</a>
    </div>
</body>
</html>
"""


if __name__ == "__main__":
    generate_intelligence_page()

