"""
Regression tests for generated AI monitor HTML safety.
"""

from generate_html import generate_html_from_summaries, safe_href


def test_safe_href_allows_http_urls_and_escapes_attributes():
    assert safe_href('https://example.com/search?q=a&b=1') == 'https://example.com/search?q=a&amp;b=1'
    assert safe_href('HTTP://example.com/path') == 'HTTP://example.com/path'


def test_safe_href_rejects_scriptable_or_relative_urls():
    assert safe_href('javascript:alert(1)') == '#'
    assert safe_href(' data:text/html,<script>alert(1)</script>') == '#'
    assert safe_href('//example.com/path') == '#'
    assert safe_href('/local/path') == '#'


def test_generated_html_replaces_unsafe_update_urls():
    html = generate_html_from_summaries([
        {
            'date': '2026-05-22',
            'updates': [
                {
                    'title': 'Malicious feed item',
                    'source': 'External RSS',
                    'url': 'javascript:alert(1)',
                    'date': '2026-05-22',
                    'summary': 'summary',
                    'keywords': ['AI'],
                }
            ],
        }
    ])

    assert 'javascript:alert(1)' not in html
    assert '<a href="#" target="_blank" rel="noopener noreferrer">Malicious feed item</a>' in html
