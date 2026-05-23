"""
LLM-Powered Intelligent Analysis
Uses LLM to extract insights, summarize, and identify biggest changes
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import os


class LLMAnalyzer:
    """Uses LLM to intelligently analyze weekly discoveries"""
    
    def __init__(self, model: str = "deepseek-chat", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.results_dir = Path("results")
    
    def analyze_with_llm(self, updates: List[Dict], historical_context: List[Dict] = None) -> Dict:
        """Use LLM to analyze and extract insights"""
        try:
            # Try OpenAI API first
            if self.api_key:
                return self._analyze_with_openai(updates, historical_context)
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            return self._fallback_analysis(updates)
        return self._fallback_analysis(updates)
    
    def _analyze_with_openai(self, updates: List[Dict], historical_context: List[Dict]) -> Dict:
        """Analyze using OpenAI-compatible API"""
        try:
            import openai
            
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com" if "deepseek" in self.model.lower() else None
            )
            
            # Prepare context
            context = self._prepare_context(updates, historical_context)
            
            prompt = f"""You are an AI market intelligence analyst. Analyze these weekly AI discoveries and provide:

1. **Executive Summary** (2-3 sentences): What happened this week?
2. **Top 5 Biggest Changes** (ranked by impact):
   - What are the most significant developments?
   - Why do they matter?
3. **Key Insights** (3-5 bullet points):
   - What patterns do you see?
   - What should be monitored?
4. **Action Items** (2-3 items):
   - What should be done based on these findings?

Weekly Updates:
{context}

Format as JSON with keys: summary, top_changes, insights, action_items"""

            response = client.chat.completions.create(
                model=self.model if "deepseek" not in self.model.lower() else "deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are an expert AI market analyst. Provide concise, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content
            
            # Try to parse JSON from response
            try:
                # Extract JSON if wrapped in markdown
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                analysis = json.loads(result_text)
                return analysis
            except:
                # If JSON parsing fails, return structured text
                return {
                    "summary": result_text[:500],
                    "top_changes": [],
                    "insights": [],
                    "action_items": []
                }
        
        except ImportError:
            print("OpenAI library not installed. Install with: pip install openai")
            return self._fallback_analysis(updates)
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            return self._fallback_analysis(updates)
    
    def _prepare_context(self, updates: List[Dict], historical_context: List[Dict]) -> str:
        """Prepare context for LLM"""
        context = f"Total updates: {len(updates)}\n\n"
        
        # Group by company/keyword
        by_keyword = {}
        for update in updates:
            keywords = update.get('keywords', [])
            if not keywords:
                keywords = ['Other']
            for keyword in keywords:
                if keyword not in by_keyword:
                    by_keyword[keyword] = []
                by_keyword[keyword].append(update)
        
        # Top updates per company
        for keyword, keyword_updates in sorted(by_keyword.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            context += f"\n{keyword.upper()} ({len(keyword_updates)} updates):\n"
            for update in keyword_updates[:3]:  # Top 3 per company
                context += f"- {update.get('title', '')}\n"
                context += f"  Source: {update.get('source', '')} | Date: {update.get('date', '')}\n"
                context += f"  {update.get('summary', '')[:150]}...\n"
        
        return context
    
    def _fallback_analysis(self, updates: List[Dict]) -> Dict:
        """Fallback analysis without LLM"""
        return {
            "summary": f"Found {len(updates)} updates this week. Install OpenAI library and set API key for intelligent analysis.",
            "top_changes": [],
            "insights": [],
            "action_items": ["Set up LLM API key for intelligent analysis"]
        }


def main():
    """Main entry point for LLM analysis"""
    # Load weekly data
    results_dir = Path("results")
    summary_file = results_dir / "weekly_summary.json"
    
    if not summary_file.exists():
        print("No weekly summary found. Run monitor.py first.")
        return
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        summaries = json.load(f)
    
    if not summaries:
        print("No data to analyze.")
        return
    
    latest = summaries[-1]
    updates = latest.get('updates', [])
    
    # Run LLM analysis
    analyzer = LLMAnalyzer()
    analysis = analyzer.analyze_with_llm(updates, summaries)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d')
    output_file = results_dir / f"llm_analysis_{timestamp}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    # Print results
    print("\n" + "="*60)
    print("LLM-POWERED INTELLIGENCE REPORT")
    print("="*60)
    print(f"\n{analysis.get('summary', 'N/A')}")
    
    print("\nTOP CHANGES:")
    for i, change in enumerate(analysis.get('top_changes', [])[:5], 1):
        print(f"{i}. {change}")
    
    print("\nKEY INSIGHTS:")
    for insight in analysis.get('insights', []):
        print(f"- {insight}")
    
    print("\nACTION ITEMS:")
    for item in analysis.get('action_items', []):
        print(f"- {item}")
    
    print(f"\n\nFull analysis saved to: {output_file}")


if __name__ == "__main__":
    main()


