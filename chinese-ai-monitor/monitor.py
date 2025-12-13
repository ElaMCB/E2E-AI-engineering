"""
Weekly Chinese AI Market Monitor
Automatically searches and tracks Chinese AI developments, models, and innovations.
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import feedparser
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class AIUpdate:
    """Represents a single AI development update"""
    title: str
    source: str
    url: str
    date: str
    summary: str
    keywords: List[str]
    hash: str  # For deduplication
    
    def __post_init__(self):
        if not self.hash:
            # Create hash from title + url for deduplication
            content = f"{self.title}{self.url}".encode('utf-8')
            self.hash = hashlib.md5(content).hexdigest()


class ChineseAIMonitor:
    """Monitors Chinese AI market developments"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
        self.seen_hashes = self._load_seen_hashes()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "search_terms": [
                "DeepSeek AI",
                "Kimi AI",
                "Chinese AI model",
                "中国AI模型",
                "智谱AI",
                "Zhipu AI",
                "百川智能",
                "Baichuan AI",
                "零一万物",
                "01.AI",
                "月之暗面",
                "Moonshot AI",
                "MiniMax",
                "文心一言",
                "Ernie Bot",
                "通义千问",
                "Qwen",
                "豆包",
                "Doubao",
                "Chinese LLM",
                "中国大模型",
                "AI innovation China"
            ],
            "rss_feeds": [
                "https://techcrunch.com/feed/",
                "https://www.theverge.com/rss/index.xml",
                "https://rss.cnn.com/rss/edition.rss",
                "https://feeds.feedburner.com/venturebeat/SGAE"
            ],
            "news_api_key": None,  # Optional: Add your NewsAPI key
            "duckduckgo_enabled": True,
            "output_format": "json",
            "max_results_per_source": 20
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _load_seen_hashes(self) -> set:
        """Load previously seen article hashes to avoid duplicates"""
        seen_file = self.results_dir / "seen_hashes.json"
        if seen_file.exists():
            with open(seen_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def _save_seen_hashes(self):
        """Save seen hashes to file"""
        seen_file = self.results_dir / "seen_hashes.json"
        with open(seen_file, 'w') as f:
            json.dump(list(self.seen_hashes), f, indent=2)
    
    def search_duckduckgo(self, query: str, max_results: int = 10) -> List[AIUpdate]:
        """Search using DuckDuckGo (no API key required)"""
        updates = []
        try:
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query,
                    max_results=max_results,
                    region='us-en',
                    safesearch='moderate'
                ))
                
                for result in results:
                    # Filter for Chinese AI relevance
                    if self._is_relevant(result.get('title', '') + ' ' + result.get('body', '')):
                        update = AIUpdate(
                            title=result.get('title', 'No title'),
                            source=result.get('href', 'Unknown'),
                            url=result.get('href', ''),
                            date=datetime.now().strftime('%Y-%m-%d'),
                            summary=result.get('body', '')[:200] + '...',
                            keywords=self._extract_keywords(result.get('title', '') + ' ' + result.get('body', '')),
                            hash=''
                        )
                        
                        if update.hash not in self.seen_hashes:
                            updates.append(update)
                            self.seen_hashes.add(update.hash)
        
        except ImportError:
            print("Warning: duckduckgo_search not installed. Install with: pip install duckduckgo-search")
        except Exception as e:
            print(f"Error searching DuckDuckGo: {e}")
        
        return updates
    
    def search_rss_feeds(self) -> List[AIUpdate]:
        """Search RSS feeds for Chinese AI news"""
        updates = []
        
        for feed_url in self.config.get('rss_feeds', []):
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:self.config.get('max_results_per_source', 20)]:
                    # Check if entry is relevant to Chinese AI
                    content = entry.get('title', '') + ' ' + entry.get('summary', '')
                    
                    if self._is_relevant(content):
                        # Parse date
                        date_str = datetime.now().strftime('%Y-%m-%d')
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            try:
                                date_str = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                            except:
                                pass
                        
                        update = AIUpdate(
                            title=entry.get('title', 'No title'),
                            source=feed.feed.get('title', feed_url),
                            url=entry.get('link', ''),
                            date=date_str,
                            summary=entry.get('summary', '')[:200] + '...',
                            keywords=self._extract_keywords(content),
                            hash=''
                        )
                        
                        if update.hash not in self.seen_hashes:
                            updates.append(update)
                            self.seen_hashes.add(update.hash)
            
            except Exception as e:
                print(f"Error parsing RSS feed {feed_url}: {e}")
        
        return updates
    
    def search_news_api(self) -> List[AIUpdate]:
        """Search using NewsAPI (requires API key)"""
        updates = []
        api_key = self.config.get('news_api_key')
        
        if not api_key:
            return updates
        
        try:
            for term in self.config.get('search_terms', [])[:5]:  # Limit to avoid rate limits
                url = f"https://newsapi.org/v2/everything"
                params = {
                    'q': term,
                    'apiKey': api_key,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 10
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    for article in data.get('articles', []):
                        content = article.get('title', '') + ' ' + article.get('description', '')
                        
                        if self._is_relevant(content):
                            update = AIUpdate(
                                title=article.get('title', 'No title'),
                                source=article.get('source', {}).get('name', 'Unknown'),
                                url=article.get('url', ''),
                                date=article.get('publishedAt', datetime.now().isoformat())[:10],
                                summary=article.get('description', '')[:200] + '...',
                                keywords=self._extract_keywords(content),
                                hash=''
                            )
                            
                            if update.hash not in self.seen_hashes:
                                updates.append(update)
                                self.seen_hashes.add(update.hash)
        
        except Exception as e:
            print(f"Error using NewsAPI: {e}")
        
        return updates
    
    def _is_relevant(self, text: str) -> bool:
        """Check if text is relevant to Chinese AI developments"""
        text_lower = text.lower()
        
        # Chinese AI companies and models
        chinese_ai_keywords = [
            'deepseek', 'kimi', 'zhipu', '智谱', 'baichuan', '百川',
            '01.ai', '零一万物', 'moonshot', '月之暗面', 'minimax',
            'ernie', '文心', 'qwen', '通义', 'doubao', '豆包',
            'chinese ai', 'china ai', '中国ai', '中国大模型',
            'chinese llm', 'chinese model'
        ]
        
        return any(keyword in text_lower for keyword in chinese_ai_keywords)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        keywords = []
        text_lower = text.lower()
        
        known_models = [
            'deepseek', 'kimi', 'zhipu', 'baichuan', 'moonshot', 'minimax',
            'ernie', 'qwen', 'doubao', '01.ai'
        ]
        
        for model in known_models:
            if model in text_lower:
                keywords.append(model)
        
        return list(set(keywords))
    
    def run_weekly_search(self) -> List[AIUpdate]:
        """Run all search methods and collect updates"""
        print(f"Starting weekly Chinese AI market search at {datetime.now()}")
        all_updates = []
        
        # Search DuckDuckGo
        if self.config.get('duckduckgo_enabled', True):
            print("Searching DuckDuckGo...")
            for term in self.config.get('search_terms', [])[:10]:  # Limit to avoid rate limits
                updates = self.search_duckduckgo(term, max_results=5)
                all_updates.extend(updates)
                print(f"  Found {len(updates)} results for '{term}'")
        
        # Search RSS feeds
        print("Searching RSS feeds...")
        rss_updates = self.search_rss_feeds()
        all_updates.extend(rss_updates)
        print(f"  Found {len(rss_updates)} results from RSS feeds")
        
        # Search NewsAPI if configured
        if self.config.get('news_api_key'):
            print("Searching NewsAPI...")
            news_updates = self.search_news_api()
            all_updates.extend(news_updates)
            print(f"  Found {len(news_updates)} results from NewsAPI")
        
        # Remove duplicates based on hash
        unique_updates = {}
        for update in all_updates:
            if update.hash not in unique_updates:
                unique_updates[update.hash] = update
        
        final_updates = list(unique_updates.values())
        
        # Sort by date (newest first)
        final_updates.sort(key=lambda x: x.date, reverse=True)
        
        print(f"\nTotal unique updates found: {len(final_updates)}")
        
        # Save results
        self._save_results(final_updates)
        self._save_seen_hashes()
        
        return final_updates
    
    def _save_results(self, updates: List[AIUpdate]):
        """Save results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if self.config.get('output_format') == 'json':
            filename = self.results_dir / f"ai_updates_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([asdict(update) for update in updates], f, indent=2, ensure_ascii=False)
        
        # Also save to weekly summary
        summary_file = self.results_dir / "weekly_summary.json"
        weekly_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'updates': [asdict(update) for update in updates]
        }
        
        # Load existing summaries
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                summaries = json.load(f)
        else:
            summaries = []
        
        summaries.append(weekly_data)
        
        # Keep only last 12 weeks
        summaries = summaries[-12:]
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {filename}")
        print(f"Weekly summary updated: {summary_file}")
    
    def generate_report(self) -> str:
        """Generate a human-readable report"""
        summary_file = self.results_dir / "weekly_summary.json"
        
        if not summary_file.exists():
            return "No reports available yet. Run the monitor first."
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            summaries = json.load(f)
        
        if not summaries:
            return "No reports available."
        
        latest = summaries[-1]
        report = f"""
# Chinese AI Market Weekly Report
## Date: {latest['date']}
## Total Updates: {len(latest['updates'])}

"""
        
        # Group by keywords
        by_keyword = {}
        for update in latest['updates']:
            for keyword in update.get('keywords', []):
                if keyword not in by_keyword:
                    by_keyword[keyword] = []
                by_keyword[keyword].append(update)
        
        for keyword, updates in sorted(by_keyword.items()):
            report += f"\n### {keyword.upper()} ({len(updates)} updates)\n\n"
            for update in updates[:5]:  # Top 5 per keyword
                report += f"- **{update['title']}**\n"
                report += f"  - Source: {update['source']}\n"
                report += f"  - URL: {update['url']}\n"
                report += f"  - Summary: {update['summary']}\n\n"
        
        return report


def main():
    """Main entry point"""
    monitor = ChineseAIMonitor()
    updates = monitor.run_weekly_search()
    
    # Generate and print report
    report = monitor.generate_report()
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    # Save report to file
    report_file = monitor.results_dir / f"report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()

