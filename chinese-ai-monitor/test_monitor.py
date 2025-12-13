"""
Quick test script to verify the monitor is working correctly
"""

from monitor import ChineseAIMonitor
import json
from pathlib import Path

def test_monitor():
    """Test the monitor with a limited search"""
    print("Testing Chinese AI Monitor...")
    print("=" * 60)
    
    # Create monitor instance
    monitor = ChineseAIMonitor()
    
    # Test configuration loading
    print(f"✓ Configuration loaded")
    print(f"  - Search terms: {len(monitor.config.get('search_terms', []))} terms")
    print(f"  - RSS feeds: {len(monitor.config.get('rss_feeds', []))} feeds")
    
    # Test relevance checking
    test_texts = [
        "DeepSeek releases new AI model",
        "Kimi AI gets major update",
        "Random news article about weather",
        "Chinese AI company Zhipu announces breakthrough"
    ]
    
    print(f"\n✓ Testing relevance filter:")
    for text in test_texts:
        is_relevant = monitor._is_relevant(text)
        status = "✓" if is_relevant else "✗"
        print(f"  {status} '{text[:50]}...' -> {is_relevant}")
    
    # Test keyword extraction
    print(f"\n✓ Testing keyword extraction:")
    test_text = "DeepSeek and Kimi AI are leading Chinese AI models"
    keywords = monitor._extract_keywords(test_text)
    print(f"  Keywords found: {keywords}")
    
    # Test a small search (limited to avoid rate limits)
    print(f"\n✓ Running limited search test...")
    print("  (This may take a minute)")
    
    # Temporarily limit search terms for testing
    original_terms = monitor.config['search_terms']
    monitor.config['search_terms'] = ['DeepSeek AI', 'Kimi AI']  # Just 2 terms for testing
    
    try:
        updates = monitor.run_weekly_search()
        print(f"\n✓ Search completed!")
        print(f"  - Found {len(updates)} unique updates")
        
        if updates:
            print(f"\n  Sample results:")
            for i, update in enumerate(updates[:3], 1):
                print(f"    {i}. {update.title[:60]}...")
                print(f"       Source: {update.source}")
                print(f"       Keywords: {', '.join(update.keywords)}")
        
        # Check if results were saved
        results_dir = Path("results")
        if results_dir.exists():
            json_files = list(results_dir.glob("ai_updates_*.json"))
            if json_files:
                print(f"\n✓ Results saved: {len(json_files)} file(s)")
        
    except Exception as e:
        print(f"\n✗ Error during search: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Restore original config
        monitor.config['search_terms'] = original_terms
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("\nTo run the full monitor:")
    print("  python monitor.py")
    print("\nTo schedule weekly runs on Windows:")
    print("  .\\schedule_windows.ps1")


if __name__ == "__main__":
    test_monitor()

