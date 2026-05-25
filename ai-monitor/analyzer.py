"""
Intelligent Analysis System for Weekly AI Discoveries
Multi-agent architecture to extract meaningful insights and identify biggest changes
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import hashlib

# Ensure shared repo-level modules can be imported when run from `ai-monitor/`.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_core import Agent, AgentContext, AgentRuntime


@dataclass
class Insight:
    """Represents a key insight extracted from updates"""
    type: str  # 'breakthrough', 'new_model', 'major_release', 'trend', 'competitor_move'
    title: str
    description: str
    impact_score: float  # 0-10
    confidence: float  # 0-1
    related_updates: List[str]  # Hashes of related updates
    evidence: List[str]
    timestamp: str


@dataclass
class Change:
    """Represents a significant change detected"""
    category: str  # 'new_company', 'model_release', 'capability_advance', 'market_shift'
    description: str
    magnitude: float  # 0-10
    week_over_week_change: Optional[Dict]
    implications: List[str]


class AnalysisAgent(Agent):
    """Base class for specialized analysis agents"""
    
    def __init__(self, config: Dict, name: str):
        super().__init__(name=name)
        self.config = config
    
    def analyze(self, updates: List[Dict], historical_data: List[Dict]) -> List[Insight]:
        """Analyze updates and return insights"""
        raise NotImplementedError

    def run(self, context: AgentContext):
        """Runtime-compatible entrypoint that preserves existing behavior."""
        return self.analyze(context.updates, context.historical_data)


class PriorityScoringAgent(AnalysisAgent):
    """Agent that scores and ranks updates by importance"""
    
    def analyze(self, updates: List[Dict], historical_data: List[Dict]) -> List[Insight]:
        """Score updates based on multiple factors"""
        insights = []
        
        # Scoring factors
        scoring_rules = {
            'new_model_release': 8.0,
            'major_version_update': 7.0,
            'open_source_announcement': 7.5,
            'research_paper': 6.0,
            'github_release': 5.0,
            'company_announcement': 6.5,
            'capability_breakthrough': 9.0,
            'market_entry': 7.0
        }
        
        for update in updates:
            score = self._calculate_score(update, scoring_rules)
            
            if score >= 6.0:  # High priority threshold
                insight = Insight(
                    type=self._classify_update(update),
                    title=update.get('title', ''),
                    description=update.get('summary', ''),
                    impact_score=score,
                    confidence=0.8,
                    related_updates=[update.get('hash', '')],
                    evidence=[update.get('source', '')],
                    timestamp=update.get('date', '')
                )
                insights.append(insight)
        
        # Sort by impact score
        insights.sort(key=lambda x: x.impact_score, reverse=True)
        return insights[:10]  # Top 10
    
    def _calculate_score(self, update: Dict, rules: Dict) -> float:
        """Calculate impact score for an update"""
        title = update.get('title', '').lower()
        summary = update.get('summary', '').lower()
        source = update.get('source', '').lower()
        keywords = update.get('keywords', [])
        
        score = 5.0  # Base score
        
        # Check for high-impact keywords
        if any(kw in title or kw in summary for kw in ['release', 'announce', 'launch', 'new model']):
            score += 2.0
        
        if any(kw in title or kw in summary for kw in ['open source', 'open-source', 'available']):
            score += 1.5
        
        if 'github' in source and 'release' in title.lower():
            score += 1.0
        
        if 'arxiv' in source:
            score += 0.5  # Research papers are important but less immediate
        
        # Boost for major companies
        major_companies = ['deepseek', 'kimi', 'qwen', 'ernie', 'baichuan', 'zhipu']
        if any(company in title.lower() or company in summary.lower() for company in major_companies):
            score += 1.0
        
        # Recency boost (newer = higher score)
        try:
            update_date = datetime.strptime(update.get('date', ''), '%Y-%m-%d')
            days_old = (datetime.now() - update_date).days
            if days_old <= 7:
                score += 1.0
            elif days_old <= 14:
                score += 0.5
        except:
            pass
        
        return min(score, 10.0)  # Cap at 10
    
    def _classify_update(self, update: Dict) -> str:
        """Classify the type of update"""
        title = update.get('title', '').lower()
        summary = update.get('summary', '').lower()
        
        if 'release' in title or 'release' in summary:
            if 'new' in title or 'v' in title:
                return 'new_model'
            return 'major_release'
        
        if 'open source' in title or 'open-source' in title:
            return 'breakthrough'
        
        if 'github' in update.get('source', '').lower():
            return 'new_model'
        
        if 'arxiv' in update.get('source', '').lower():
            return 'research_paper'
        
        return 'trend'


class ChangeDetectionAgent(AnalysisAgent):
    """Agent that detects significant changes week-over-week"""
    
    def analyze(self, updates: List[Dict], historical_data: List[Dict]) -> List[Change]:
        """Detect significant changes compared to previous weeks"""
        changes = []
        
        if not historical_data:
            return changes
        
        # Get previous week's data
        if len(historical_data) >= 2:
            prev_week = historical_data[-2]
            current_week = historical_data[-1]
            
            # Compare company/model activity
            prev_companies = set()
            curr_companies = set()
            
            for update in prev_week.get('updates', []):
                prev_companies.update(update.get('keywords', []))
            
            for update in current_week.get('updates', []):
                curr_companies.update(update.get('keywords', []))
            
            # New companies/models
            new_entities = curr_companies - prev_companies
            if new_entities:
                changes.append(Change(
                    category='new_company',
                    description=f"New entities detected: {', '.join(new_entities)}",
                    magnitude=7.0,
                    week_over_week_change={'new': list(new_entities)},
                    implications=[f"Monitor {entity} for future developments" for entity in new_entities]
                ))
            
            # Activity spike
            prev_count = len(prev_week.get('updates', []))
            curr_count = len(current_week.get('updates', []))
            
            if curr_count > prev_count * 1.5:  # 50% increase
                if prev_count == 0:
                    description = f"Activity resumed: {prev_count} → {curr_count} updates (prior week had no updates)"
                else:
                    percent_increase = (curr_count / prev_count - 1) * 100
                    description = f"Significant activity increase: {prev_count} → {curr_count} updates (+{percent_increase:.0f}%)"

                changes.append(Change(
                    category='market_shift',
                    description=description,
                    magnitude=6.0,
                    week_over_week_change={'prev': prev_count, 'current': curr_count},
                    implications=["Increased market activity - monitor closely", "Potential major announcements coming"]
                ))
        
        return changes


class SummarizationAgent(AnalysisAgent):
    """Agent that creates executive summaries"""
    
    def analyze(self, updates: List[Dict], historical_data: List[Dict]) -> Dict:
        """Create executive summary of the week"""
        if not updates:
            return {
                'summary': 'No updates this week',
                'key_highlights': [],
                'trends': []
            }
        
        # Group by keyword/company
        by_company = {}
        for update in updates:
            keywords = update.get('keywords', [])
            if not keywords:
                keywords = ['Other']
            
            for keyword in keywords:
                if keyword not in by_company:
                    by_company[keyword] = []
                by_company[keyword].append(update)
        
        # Top companies by activity
        top_companies = sorted(by_company.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        
        # Key highlights
        highlights = []
        for company, company_updates in top_companies[:3]:
            highlights.append(f"{company.upper()}: {len(company_updates)} updates")
        
        # Identify trends
        trends = []
        release_count = sum(1 for u in updates if 'release' in u.get('title', '').lower())
        github_count = sum(1 for u in updates if 'github' in u.get('source', '').lower())
        
        if release_count > len(updates) * 0.3:
            trends.append("High number of releases this week")
        
        if github_count > len(updates) * 0.4:
            trends.append("Strong GitHub activity - many new repositories")
        
        return {
            'summary': f"This week saw {len(updates)} updates across {len(by_company)} companies/models. Top activity: {', '.join([c[0] for c in top_companies[:3]])}",
            'key_highlights': highlights,
            'trends': trends,
            'total_updates': len(updates),
            'unique_companies': len(by_company),
            'top_companies': [{'name': c[0], 'count': len(c[1])} for c in top_companies]
        }


class TrendAnalysisAgent(AnalysisAgent):
    """Agent that identifies long-term trends"""
    
    def analyze(self, updates: List[Dict], historical_data: List[Dict]) -> List[Dict]:
        """Identify trends across multiple weeks"""
        trends = []
        
        if len(historical_data) < 3:
            return trends
        
        # Analyze last 4 weeks
        recent_weeks = historical_data[-4:]
        
        # Trend: Increasing activity
        activity_counts = [len(w.get('updates', [])) for w in recent_weeks]
        if len(activity_counts) >= 3 and activity_counts[-1] > activity_counts[0] * 1.2:
            trends.append({
                'type': 'increasing_activity',
                'description': f"Activity trending up: {activity_counts[0]} → {activity_counts[-1]} updates",
                'confidence': 0.8
            })
        
        # Trend: Emerging companies
        all_companies = {}
        for week in recent_weeks:
            for update in week.get('updates', []):
                for keyword in update.get('keywords', []):
                    if keyword not in all_companies:
                        all_companies[keyword] = []
                    all_companies[keyword].append(week.get('date', ''))
        
        # Companies with increasing presence
        for company, dates in all_companies.items():
            if len(dates) >= 2 and dates[-1] > dates[0]:
                trends.append({
                    'type': 'emerging_company',
                    'description': f"{company} showing increasing activity",
                    'confidence': 0.7
                })
        
        return trends


class IntelligentAnalyzer:
    """Orchestrates multiple analysis agents"""
    
    def __init__(self, results_dir: str = "results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        # Initialize agents through shared runtime to standardize orchestration.
        self.runtime = AgentRuntime()
        self.priority_agent = PriorityScoringAgent({}, "priority_scoring")
        self.change_agent = ChangeDetectionAgent({}, "change_detection")
        self.summary_agent = SummarizationAgent({}, "summarization")
        self.trend_agent = TrendAnalysisAgent({}, "trend_analysis")
        self.runtime.register(self.priority_agent)
        self.runtime.register(self.change_agent)
        self.runtime.register(self.summary_agent)
        self.runtime.register(self.trend_agent)
    
    def analyze_weekly_data(self) -> Dict:
        """Run all analysis agents on weekly data"""
        # Load weekly summary
        summary_file = self.results_dir / "weekly_summary.json"
        if not summary_file.exists():
            return {"error": "No weekly summary found"}
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            summaries = json.load(f)
        
        if not summaries:
            return {"error": "No data to analyze"}
        
        latest = summaries[-1]
        updates = latest.get('updates', [])
        
        # Run all agents through the shared runtime.
        context = AgentContext(
            updates=updates,
            historical_data=summaries,
            metadata={"date": latest.get("date", "")},
        )
        runtime_outputs = self.runtime.run_all(context)
        priority_insights = runtime_outputs.get("priority_scoring") or []
        changes = runtime_outputs.get("change_detection") or []
        summary = runtime_outputs.get("summarization") or {}
        trends = runtime_outputs.get("trend_analysis") or []
        
        # Compile results
        analysis = {
            'date': latest.get('date', ''),
            'executive_summary': summary,
            'top_insights': [asdict(insight) for insight in priority_insights],
            'significant_changes': [asdict(change) for change in changes],
            'trends': trends,
            'recommendations': self._generate_recommendations(priority_insights, changes, trends)
        }
        
        # Save analysis
        self._save_analysis(analysis)
        self._save_runtime_trace(latest.get('date', ''))
        
        return analysis
    
    def _generate_recommendations(self, insights: List[Insight], changes: List[Change], trends: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # High-impact insights
        high_impact = [i for i in insights if i.impact_score >= 8.0]
        if high_impact:
            recommendations.append(f"URGENT: {len(high_impact)} high-impact developments detected - review immediately")
        
        # New entities
        new_entities = [c for c in changes if c.category == 'new_company']
        if new_entities:
            recommendations.append("New companies/models detected - add to monitoring list")
        
        # Activity spikes
        activity_changes = [c for c in changes if c.category == 'market_shift']
        if activity_changes:
            recommendations.append("Market activity spike detected - potential major announcements")
        
        # Trends
        if trends:
            recommendations.append("Long-term trends identified - consider strategic implications")
        
        return recommendations
    
    def _save_analysis(self, analysis: Dict):
        """Save analysis results"""
        timestamp = datetime.now().strftime('%Y%m%d')
        analysis_file = self.results_dir / f"analysis_{timestamp}.json"
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # Also update latest analysis
        latest_file = self.results_dir / "latest_analysis.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

    def _save_runtime_trace(self, analysis_date: str):
        """Save runtime execution trace for observability and eval gates."""
        run_history = self.runtime.run_history
        total_steps = len(run_history)
        success_steps = sum(1 for run in run_history if run.status == "ok")
        failed_steps = total_steps - success_steps
        total_duration_ms = sum(run.duration_ms for run in run_history)
        avg_duration_ms = total_duration_ms / total_steps if total_steps else 0.0

        runtime_trace = {
            "date": analysis_date,
            "recorded_at": datetime.now().isoformat(),
            "summary": {
                "total_steps": total_steps,
                "success_steps": success_steps,
                "failed_steps": failed_steps,
                "success_rate": (success_steps / total_steps) if total_steps else 1.0,
                "average_step_duration_ms": avg_duration_ms,
                "total_duration_ms": total_duration_ms,
                # Placeholder until per-model token accounting is added.
                "estimated_cost_usd": 0.0,
            },
            "runs": [asdict(run) for run in run_history],
        }

        timestamp = datetime.now().strftime('%Y%m%d')
        trace_file = self.results_dir / f"runtime_trace_{timestamp}.json"
        with open(trace_file, 'w', encoding='utf-8') as f:
            json.dump(runtime_trace, f, indent=2, ensure_ascii=False)

        latest_trace_file = self.results_dir / "latest_runtime_trace.json"
        with open(latest_trace_file, 'w', encoding='utf-8') as f:
            json.dump(runtime_trace, f, indent=2, ensure_ascii=False)
    
    def generate_report(self) -> str:
        """Generate human-readable report"""
        analysis_file = self.results_dir / "latest_analysis.json"
        
        if not analysis_file.exists():
            return "No analysis available. Run analysis first."
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        report = f"""
# Weekly AI Market Intelligence Report
## Date: {analysis.get('date', 'N/A')}

## Executive Summary
{analysis.get('executive_summary', {}).get('summary', 'N/A')}

### Key Highlights
"""
        for highlight in analysis.get('executive_summary', {}).get('key_highlights', []):
            report += f"- {highlight}\n"
        
        report += f"""
## Top Insights (Priority Ranked)
"""
        for i, insight in enumerate(analysis.get('top_insights', [])[:5], 1):
            report += f"""
### {i}. {insight.get('title', 'N/A')} [Impact: {insight.get('impact_score', 0):.1f}/10]
- Type: {insight.get('type', 'N/A')}
- Description: {insight.get('description', '')[:200]}...
- Source: {', '.join(insight.get('evidence', []))}
"""
        
        report += f"""
## Significant Changes
"""
        for change in analysis.get('significant_changes', []):
            report += f"""
### {change.get('category', 'N/A').replace('_', ' ').title()}
- {change.get('description', 'N/A')}
- Magnitude: {change.get('magnitude', 0):.1f}/10
- Implications:
"""
            for impl in change.get('implications', []):
                report += f"  - {impl}\n"
        
        report += f"""
## Recommendations
"""
        for rec in analysis.get('recommendations', []):
            report += f"- {rec}\n"
        
        return report


def main():
    """Main entry point"""
    analyzer = IntelligentAnalyzer()
    analysis = analyzer.analyze_weekly_data()
    
    if 'error' in analysis:
        print(f"Error: {analysis['error']}")
        return
    
    # Generate and print report
    report = analyzer.generate_report()
    try:
        print(report)
    except UnicodeEncodeError:
        # Windows console encoding issue - just save to file
        print("Report generated (saved to file due to console encoding)")
    
    # Save report
    report_file = analyzer.results_dir / f"intelligence_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nAnalysis saved to: {report_file}")
    print(f"Latest analysis: {analyzer.results_dir / 'latest_analysis.json'}")


if __name__ == "__main__":
    main()

