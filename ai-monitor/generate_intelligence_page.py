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


def get_personalized_greeting() -> Dict[str, str]:
    """Generate personalized greeting based on time and user info"""
    # Get Eastern Time
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now(eastern)
    hour = now.hour
    
    # Determine time of day
    if 5 <= hour < 12:
        time_greeting = "Good morning"
    elif 12 <= hour < 17:
        time_greeting = "Good afternoon"
    elif 17 <= hour < 21:
        time_greeting = "Good evening"
    else:
        time_greeting = "Good evening"
    
    # User name from GitHub repos
    user_name = "Ela"
    
    # Create personalized message
    greeting = f"{time_greeting}, {user_name}"
    message = "Here are the discoveries for this week. Please skim through them and let me know if you want to engage deeper."
    
    return {
        'greeting': greeting,
        'message': message,
        'time': now.strftime('%I:%M %p ET')
    }


def generate_html_from_analysis(analysis: Dict) -> str:
    """Generate HTML from analysis data"""
    
    exec_summary = analysis.get('executive_summary', {})
    top_insights = analysis.get('top_insights', [])
    changes = analysis.get('significant_changes', [])
    recommendations = analysis.get('recommendations', [])
    
    # Get personalized greeting
    personal = get_personalized_greeting()
    
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
            <button id="engageDeeperBtn" style="margin-top: 1rem; padding: 0.6rem 1.5rem; background: var(--primary); color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-comments"></i> Engage Deeper
            </button>
        </div>
        
        <div id="agentInterface" style="display: none; background: var(--card-bg); border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid var(--border);">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <i class="fas fa-robot" style="font-size: 1.5rem; color: var(--primary);"></i>
                <h3 style="margin: 0; color: var(--text); font-size: 1.1rem;">Your Intelligence Agent</h3>
            </div>
            <div id="agentMessages" style="max-height: 400px; overflow-y: auto; margin-bottom: 1rem; padding: 1rem; background: rgba(0, 0, 0, 0.2); border-radius: 8px;">
                <div class="agent-message" style="margin-bottom: 1rem;">
                    <div style="display: flex; align-items: start; gap: 0.75rem;">
                        <i class="fas fa-robot" style="color: var(--primary); margin-top: 0.25rem;"></i>
                        <div style="flex: 1;">
                            <p style="margin: 0; color: var(--text-light); line-height: 1.6;">
                                Hi Ela! I'm your intelligence agent. I can help you understand the discoveries, answer questions about specific insights, explain changes, or provide recommendations. What would you like to know?
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <input type="text" id="agentInput" placeholder="Ask me anything about this week's discoveries..." style="flex: 1; padding: 0.75rem; background: rgba(0, 0, 0, 0.3); border: 1px solid var(--border); border-radius: 6px; color: var(--text); font-size: 0.9rem;" />
                <button id="agentSendBtn" style="padding: 0.75rem 1.5rem; background: var(--primary); color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
                    <i class="fas fa-paper-plane"></i> Send
                </button>
            </div>
            <div style="margin-top: 1rem; display: flex; flex-wrap: wrap; gap: 0.5rem;">
                <button class="quick-question" data-question="What are the top 3 most important insights?" style="padding: 0.5rem 1rem; background: rgba(59, 130, 246, 0.1); color: var(--primary); border: 1px solid var(--primary); border-radius: 6px; font-size: 0.85rem; cursor: pointer; transition: all 0.3s ease;">
                    Top 3 Insights
                </button>
                <button class="quick-question" data-question="What significant changes happened this week?" style="padding: 0.5rem 1rem; background: rgba(59, 130, 246, 0.1); color: var(--primary); border: 1px solid var(--primary); border-radius: 6px; font-size: 0.85rem; cursor: pointer; transition: all 0.3s ease;">
                    Significant Changes
                </button>
                <button class="quick-question" data-question="What should I focus on?" style="padding: 0.5rem 1rem; background: rgba(59, 130, 246, 0.1); color: var(--primary); border: 1px solid var(--primary); border-radius: 6px; font-size: 0.85rem; cursor: pointer; transition: all 0.3s ease;">
                    What to Focus On
                </button>
                <button class="quick-question" data-question="Tell me about DeepSeek updates" style="padding: 0.5rem 1rem; background: rgba(59, 130, 246, 0.1); color: var(--primary); border: 1px solid var(--primary); border-radius: 6px; font-size: 0.85rem; cursor: pointer; transition: all 0.3s ease;">
                    DeepSeek Updates
                </button>
            </div>
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
    
    <!-- Intelligence Agent Script -->
    <script>
        // Load analysis data for agent
        let analysisData = null;
        fetch('ai-monitor/results/latest_analysis.json')
            .then(response => response.json())
            .then(data => {
                analysisData = data;
            })
            .catch(() => {
                console.log('Analysis data not available');
            });
        
        // Toggle agent interface
        document.getElementById('engageDeeperBtn').addEventListener('click', function() {
            const interface = document.getElementById('agentInterface');
            if (interface.style.display === 'none') {
                interface.style.display = 'block';
                this.innerHTML = '<i class="fas fa-times"></i> Close';
                this.style.background = 'var(--danger)';
            } else {
                interface.style.display = 'none';
                this.innerHTML = '<i class="fas fa-comments"></i> Engage Deeper';
                this.style.background = 'var(--primary)';
            }
        });
        
        // Agent response function
        function getAgentResponse(question) {
            if (!analysisData) {
                return "I'm sorry, I don't have access to the analysis data right now. Please try again later.";
            }
            
            const lowerQuestion = question.toLowerCase();
            const insights = analysisData.top_insights || [];
            const changes = analysisData.significant_changes || [];
            const recommendations = analysisData.recommendations || [];
            const summary = analysisData.executive_summary || {};
            
            // Top insights questions
            if (lowerQuestion.includes('top') && (lowerQuestion.includes('insight') || lowerQuestion.includes('important'))) {
                const top3 = insights.slice(0, 3);
                let response = "Here are the top 3 most important insights this week:\\n\\n";
                top3.forEach((insight, i) => {
                    response += `${i + 1}. ${insight.title} (Impact: ${insight.impact_score}/10)\\n`;
                    response += `   ${insight.description.substring(0, 150)}...\\n\\n`;
                });
                return response;
            }
            
            // Changes questions
            if (lowerQuestion.includes('change') || lowerQuestion.includes('different')) {
                if (changes.length === 0) {
                    return "No significant changes detected this week compared to previous weeks.";
                }
                let response = "Here are the significant changes this week:\\n\\n";
                changes.forEach(change => {
                    response += `• ${change.category.replace('_', ' ').toUpperCase()}: ${change.description}\\n`;
                    response += `  Magnitude: ${change.magnitude}/10\\n\\n`;
                });
                return response;
            }
            
            // Focus/recommendations
            if (lowerQuestion.includes('focus') || lowerQuestion.includes('recommend') || lowerQuestion.includes('should')) {
                if (recommendations.length === 0) {
                    return "Based on the analysis, continue monitoring the top insights regularly.";
                }
                let response = "Here's what you should focus on:\\n\\n";
                recommendations.forEach((rec, i) => {
                    response += `${i + 1}. ${rec}\\n`;
                });
                return response;
            }
            
            // Company-specific questions
            const companies = ['deepseek', 'kimi', 'moonshot', 'qwen', 'ernie'];
            for (const company of companies) {
                if (lowerQuestion.includes(company)) {
                    const companyInsights = insights.filter(insight => 
                        insight.title.toLowerCase().includes(company) || 
                        insight.description.toLowerCase().includes(company)
                    );
                    if (companyInsights.length === 0) {
                        return `I don't see any specific updates about ${company} in the top insights this week.`;
                    }
                    let response = `Here are the ${company} updates this week:\\n\\n`;
                    companyInsights.forEach(insight => {
                        response += `• ${insight.title}\\n`;
                        response += `  ${insight.description.substring(0, 120)}...\\n\\n`;
                    });
                    return response;
                }
            }
            
            // Summary questions
            if (lowerQuestion.includes('summary') || lowerQuestion.includes('overview') || lowerQuestion.includes('what happened')) {
                return summary.summary || "This week saw multiple AI developments across various companies and models.";
            }
            
            // Default response
            return "I can help you with:\\n• Top insights and their impact scores\\n• Significant changes this week\\n• Recommendations on what to focus on\\n• Updates about specific companies (DeepSeek, Kimi, etc.)\\n• Executive summary\\n\\nTry asking: 'What are the top 3 insights?' or 'What changed this week?'";
        }
        
        // Send message function
        function sendMessage() {
            const input = document.getElementById('agentInput');
            const question = input.value.trim();
            if (!question) return;
            
            // Add user message
            const messagesDiv = document.getElementById('agentMessages');
            const userMsg = document.createElement('div');
            userMsg.className = 'agent-message';
            userMsg.style.marginBottom = '1rem';
            userMsg.innerHTML = `
                <div style="display: flex; align-items: start; gap: 0.75rem; flex-direction: row-reverse;">
                    <i class="fas fa-user" style="color: var(--success); margin-top: 0.25rem;"></i>
                    <div style="flex: 1; text-align: right;">
                        <p style="margin: 0; color: var(--text-light); line-height: 1.6; background: rgba(59, 130, 246, 0.2); padding: 0.75rem; border-radius: 8px; display: inline-block;"></p>
                    </div>
                </div>
            `;
            userMsg.querySelector('p').textContent = question;
            messagesDiv.appendChild(userMsg);
            
            // Get agent response
            const response = getAgentResponse(question);
            
            // Add agent response
            setTimeout(() => {
                const agentMsg = document.createElement('div');
                agentMsg.className = 'agent-message';
                agentMsg.style.marginBottom = '1rem';
                agentMsg.innerHTML = `
                    <div style="display: flex; align-items: start; gap: 0.75rem;">
                        <i class="fas fa-robot" style="color: var(--primary); margin-top: 0.25rem;"></i>
                        <div style="flex: 1;">
                            <p style="margin: 0; color: var(--text-light); line-height: 1.6; white-space: pre-line;"></p>
                        </div>
                    </div>
                `;
                agentMsg.querySelector('p').textContent = response;
                messagesDiv.appendChild(agentMsg);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }, 500);
            
            input.value = '';
        }
        
        // Send button
        document.getElementById('agentSendBtn').addEventListener('click', sendMessage);
        
        // Enter key
        document.getElementById('agentInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Quick question buttons
        document.querySelectorAll('.quick-question').forEach(btn => {
            btn.addEventListener('click', function() {
                document.getElementById('agentInput').value = this.dataset.question;
                sendMessage();
            });
        });
    </script>
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

